# System Architecture Documentation

## 🏛️ Five-Layer Architecture

### Layer 1: Presentation Layer
**Component:** Streamlit UI (`ui/app.py`)
- Chat-style interface for loan application submission
- Real-time decision display with color coding
- Application history tracking
- Expandable analysis panels
- System status indicator

### Layer 2: Microservice Layer
**Component:** FastAPI (`microservice/api.py`)
- REST API endpoint: `POST /api/v1/loan/apply`
- Request validation via Pydantic models
- CORS enabled for cross-origin requests
- Health check endpoint: `GET /health`
- Connects UI to orchestration layer

### Layer 3: Orchestration Layer
**Component:** LangGraph (`orchestrator/orchestrator.py`)
- Sequential state machine workflow
- Nodes: validate → profile → risk → decision → compliance
- Type-safe state management via `LoanApplicationState`
- Error propagation through workflow
- Graph compilation for efficient execution

### Layer 4: Agent Layer
**Components:** 4 Domain-Specific Agents (all using Claude Haiku 4.5)

#### 4.1 Application Profile Agent (`agents/profile_agent.py`)
- **MCP Server:** ApplicantDB
- **Inputs:** Age, Income, Employment Type, Credit Score, Liabilities, Loan Amount, Tenure
- **Tools Called:** `analyze_applicant_profile()`
- **Outputs:**
  - Income Stability Score (0-100)
  - Employment Risk (LOW/MEDIUM/HIGH)
  - Credit History Summary (text)
  - Completeness Flags (data validation)
  - LLM Assessment (Claude enrichment)

#### 4.2 Financial Risk Analysis Agent (`agents/risk_agent.py`)
- **MCP Server:** RiskRulesDB
- **Inputs:** Income, Loan Amount, Tenure, Credit Score, Existing Liabilities
- **Tools Called:** `calculate_risk_metrics()`
- **Outputs:**
  - Debt-to-Income Ratio (0-2.0+)
  - Credit Score Risk Level (LOW/MEDIUM/HIGH/CRITICAL)
  - Loan Amount Risk (LOW/MEDIUM/HIGH/CRITICAL)
  - Anomaly Detection (list of flags)
  - Risk Reasoning (text explanation)
  - LLM Assessment (Claude analysis)

#### 4.3 Loan Decision Agent (`agents/decision_agent.py`)
- **MCP Server:** DecisionSynthesis
- **Inputs:** Profile Analysis + Risk Analysis + Application ID
- **Tools Called:** `synthesize_decision()`
- **Outputs:**
  - Classification (APPROVED/REJECTED/MANUAL_REVIEW)
  - Risk Score (0-100 composite)
  - Confidence Level (HIGH/MEDIUM/LOW)
  - Key Decision Factors (top 3)
  - Explanation (narrative)
  - LLM Assessment (Claude confirmation)

#### 4.4 Compliance & Action Orchestration Agent (`agents/compliance_agent.py`)
- **MCP Server:** NotificationSystem
- **Inputs:** Application Data + Decision + Applicant Name
- **Tools Called:** `send_notification()`
- **Outputs:**
  - Action Taken (classification-specific action)
  - Notification Sent (boolean)
  - Case ID (UUID truncated)
  - Timestamp (ISO 8601)
  - Summary (text)
  - LLM Assessment (Claude confirmation)

### Layer 5: Communication Layer (MCP Servers)
**Protocol:** Model Context Protocol (stdio-based)

#### 5.1 ApplicantDB Server (`mcp_servers/applicant_db_server.py`)
**FastMCP Server** with mock in-memory data
- **Tool:** `analyze_applicant_profile()`
- **Logic:** Rules-based profile analysis
- **Data Source:** Employment risk matrix + income bands
- **Processing:** Instant (no I/O)

#### 5.2 RiskRulesDB Server (`mcp_servers/risk_rules_server.py`)
**FastMCP Server** with mock in-memory data
- **Tool:** `calculate_risk_metrics()`
- **Logic:** Financial ratios + credit score mapping
- **Data Source:** Hardcoded thresholds and rules
- **Processing:** Mathematical calculations

#### 5.3 DecisionSynthesis Server (`mcp_servers/decision_synthesis_server.py`)
**FastMCP Server** with mock in-memory data
- **Tool:** `synthesize_decision()`
- **Logic:** Weighted composite scoring
- **Data Source:** Profile + Risk JSON merging
- **Processing:** Decision tree evaluation

#### 5.4 NotificationSystem Server (`mcp_servers/notification_server.py`)
**FastMCP Server** with in-memory logging
- **Tool:** `send_notification()`
- **Logic:** Action mapping + case ID generation
- **Data Source:** In-memory notifications log
- **Processing:** UUID generation + timestamp

---

## 📊 Data Flow Diagram

```
┌──────────────────────────────────────────────────────────┐
│         User Submits Loan Application (Streamlit)       │
└────────────────────────┬─────────────────────────────────┘
                         │
                         │ HTTP POST JSON
                         │
┌────────────────────────▼─────────────────────────────────┐
│              FastAPI Microservice                        │
│          POST /api/v1/loan/apply (8000)                 │
└────────────────────────┬─────────────────────────────────┘
                         │
                         │ Python function call
                         │
┌────────────────────────▼─────────────────────────────────┐
│          LangGraph Orchestrator                          │
│                                                          │
│  Initial State: { application, profile_analysis: {},    │
│                   risk_analysis: {}, ... }             │
└────────────────────────┬─────────────────────────────────┘
                         │
          ┌──────────────┴──────────────┐
          │                             │
┌─────────▼──────────┐      ┌──────────▼────────────┐
│ Validate Node      │      │ Profile Agent        │
│ - Check fields     │      │ - Extract profile    │
│ - Return error     │      │ - Score income stab. │
│ - Propagate state  │      │ - LLM assessment    │
└─────────┬──────────┘      └──────────┬────────────┘
          │                            │
          └────────────┬───────────────┘
                       │
                       │ Pass state with profile_analysis
                       │
              ┌────────▼──────────┐
              │ Risk Agent        │
              │ - Calculate DTI   │
              │ - Map credit risk │
              │ - Detect anomaly  │
              │ - LLM analysis    │
              └────────┬──────────┘
                       │
                       │ Pass state with risk_analysis
                       │
              ┌────────▼──────────┐
              │ Decision Agent    │
              │ - Weight scores   │
              │ - Rule-based      │
              │ - Synthesize      │
              │ - LLM confirmation│
              └────────┬──────────┘
                       │
                       │ Pass state with decision
                       │
              ┌────────▼──────────┐
              │ Compliance Agent  │
              │ - Generate CaseID │
              │ - Log action      │
              │ - Send notif      │
              │ - LLM verify      │
              └────────┬──────────┘
                       │
                       │ Final state
                       │
┌──────────────────────▼──────────────────────────────────┐
│         Return JSON with all agent outputs             │
│  {classification, risk_score, case_id, factors, ...}  │
└──────────────────────┬─────────────────────────────────┘
                       │
                       │ HTTP Response JSON
                       │
┌──────────────────────▼──────────────────────────────────┐
│   Display Decision in Streamlit UI                     │
│   - Color-coded banner (green/red/yellow)             │
│   - Risk score gauge                                  │
│   - Key factors list                                  │
│   - Expandable detailed analysis                      │
│   - Add to chat history                               │
└──────────────────────────────────────────────────────────┘
```

---

## 🔄 State Machine (LangGraph)

```
START
  │
  └──► [validate] ──(error: end)──► [error handling]
         │
         └──► [profile] ──► profile_analysis state
         │
         └──► [risk] ──► risk_analysis state
         │
         └──► [decision] ──► decision state
         │
         └──► [compliance] ──► compliance_result state
         │
         └──► END ──► Return final state
```

**State Transitions:**
- `validate` → `profile` (on success)
- `profile` → `risk` (always)
- `risk` → `decision` (always)
- `decision` → `compliance` (always, includes REJECTED)
- `compliance` → END (always)
- Any node → END (if error in any previous node)

---

## 🧠 Decision Logic

### Risk Score Calculation (0-100)

```
base_score = 50

# Credit score factor
if credit_risk == "LOW":
    base_score -= 15
elif credit_risk == "MEDIUM":
    base_score -= 5
elif credit_risk == "HIGH":
    base_score += 15
elif credit_risk == "CRITICAL":
    base_score += 30

# Loan amount factor
if loan_risk == "LOW":
    base_score -= 10
elif loan_risk == "MEDIUM":
    base_score += 5
elif loan_risk == "HIGH":
    base_score += 15
elif loan_risk == "CRITICAL":
    base_score += 25

# Debt-to-Income factor
if dti > 0.5:
    base_score += (dti - 0.5) * 20

# Income stability factor
if income_stability >= 80:
    base_score -= 10
elif income_stability >= 60:
    base_score -= 5
elif income_stability < 40:
    base_score += 15

# Clamp to 0-100
risk_score = max(0, min(100, base_score))
```

### Classification Rules

```
if risk_score < 35:
    classification = "APPROVED"
    confidence = "HIGH"
elif risk_score < 60:
    classification = "APPROVED"
    confidence = "MEDIUM"
elif risk_score < 75:
    classification = "MANUAL_REVIEW"
    confidence = "MEDIUM"
else:
    classification = "REJECTED"
    confidence = "HIGH"
```

---

## 📦 Technology Stack Rationale

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **UI Framework** | Streamlit | Rapid development, chat-like interface, real-time updates |
| **Microservice** | FastAPI | High performance, async support, auto Swagger docs |
| **Orchestration** | LangGraph | State machine pattern, type safety, agent coordination |
| **Agent Framework** | Anthropic SDK | Latest Claude models, tool use, structured output |
| **LLM Model** | Claude Haiku 4.5 | Cost-effective, fast inference, suitable for agents |
| **Communication** | MCP (stdio) | Standardized protocol, subprocess isolation, simplicity |
| **Data Validation** | Pydantic | Type safety, JSON schema generation, error clarity |
| **Language** | Python 3.x | Ecosystem, simplicity, ML integration |

---

## 🔐 Security Considerations

1. **Isolation:** MCP servers run in subprocess isolation
2. **No Secrets in Logs:** Application data never logged directly
3. **API Validation:** Pydantic ensures input sanitization
4. **Auditability:** Every decision has a unique case ID + timestamp
5. **Error Handling:** Graceful degradation with error propagation
6. **CORS:** Localhost-only for development (changeable for production)

---

## 📈 Performance Characteristics

- **Profile Agent:** ~1-2 seconds (rule evaluation + LLM call)
- **Risk Agent:** ~1-2 seconds (calculation + LLM call)
- **Decision Agent:** ~1-2 seconds (scoring + LLM call)
- **Compliance Agent:** ~1-2 seconds (logging + LLM call)
- **Total End-to-End:** ~5-10 seconds (dominated by LLM latency)

**Bottleneck:** LLM API calls (each agent calls Claude)

**Optimization Opportunities:**
- Cache LLM responses for similar profiles
- Batch multiple applications
- Use faster/smaller models for preprocessing
- Implement request timeout and retry logic

---

## 🔧 Extension Points

### Add New Agent
1. Create `agents/new_agent.py`
2. Implement `run_new_agent(state: dict) -> dict`
3. Add node to LangGraph in `orchestrator/orchestrator.py`
4. Add edge connections

### Add New MCP Server
1. Create `mcp_servers/new_server.py` with FastMCP
2. Define tools with `@app.tool()` decorator
3. Import and call in corresponding agent

### Modify Decision Logic
- Edit `mcp_servers/decision_synthesis_server.py`
- Update risk score calculation formula
- Adjust classification thresholds

### Add External Data Source
- Replace in-memory logic with database calls
- Examples: PostgreSQL, MongoDB, REST API calls
- Update MCP servers to connect to external services

---

## 📝 Testing Strategy

### Unit Tests (per agent/MCP server)
```python
# Test profile agent with known inputs
profile = run_profile_agent({age: 35, income: 75000, ...})
assert profile['income_stability_score'] == 85
```

### Integration Tests (full workflow)
```python
# Test full orchestrator
result = run_loan_application({...})
assert result['decision']['classification'] in ['APPROVED', 'REJECTED', 'MANUAL_REVIEW']
```

### End-to-End Tests (API + UI)
```
1. Submit via Streamlit UI
2. Verify API response
3. Check case ID generation
4. Validate state transitions
```

---

## 📊 API Contract

### Request Schema (POST /api/v1/loan/apply)
```json
{
  "application_id": "string (unique)",
  "applicant_name": "string",
  "age": "integer (18-100)",
  "income": "integer (>0)",
  "employment_type": "string (enum)",
  "credit_score": "integer (300-850)",
  "loan_amount": "integer (>1000)",
  "tenure": "integer (1-40)",
  "existing_liabilities": "integer (>=0)",
  "location": "string"
}
```

### Response Schema
```json
{
  "application_id": "string",
  "applicant_name": "string",
  "classification": "string (APPROVED|REJECTED|MANUAL_REVIEW)",
  "risk_score": "float (0-100)",
  "confidence_level": "string (HIGH|MEDIUM|LOW)",
  "case_id": "string (8 chars)",
  "key_decision_factors": "array[string]",
  "explanation": "string",
  "profile_summary": {...},
  "risk_summary": {...},
  "error": "null or string"
}
```

---

## 🎯 Success Metrics

- ✅ All 4 agents produce output
- ✅ LangGraph state flows correctly  
- ✅ Decisions are explainable
- ✅ Case IDs are unique and auditable
- ✅ Response time < 15 seconds
- ✅ No data loss in workflow
- ✅ Graceful error handling
- ✅ Reproducible results for same inputs
