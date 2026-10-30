# Agentic AI Intelligent Loan Approval System

A multi-agent AI system for intelligent loan application processing using LangGraph, FastAPI, Streamlit, and Anthropic Claude.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Chatbot UI                     │
│           (Application submission & result display)          │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP
┌──────────────────────────▼──────────────────────────────────┐
│               FastAPI Microservice (8000)                   │
│             (REST endpoint: /api/v1/loan/apply)             │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│            LangGraph Orchestration Engine                    │
│  Workflow: Validate → Profile → Risk → Decision → Compliance│
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼────────┐ ┌───────▼─────────┐ ┌────▼───────────┐
│ Profile Agent  │ │  Risk Agent     │ │ Decision Agent │
│   (Haiku-4.5)  │ │  (Haiku-4.5)    │ │ (Haiku-4.5)    │
└───────┬────────┘ └────┬────────────┘ └────┬───────────┘
        │                │                   │
┌───────▼────────┐ ┌────▼────────────┐ ┌────▼───────────┐
│ ApplicantDB    │ │ RiskRulesDB     │ │ DecisionSynthesis
│ MCP Server     │ │ MCP Server      │ │ MCP Server
└────────────────┘ └─────────────────┘ └────┬───────────┘
                                             │
                                    ┌────────▼──────────┐
                                    │ Compliance Agent  │
                                    │  (Haiku-4.5)      │
                                    └────────┬──────────┘
                                             │
                                    ┌────────▼──────────┐
                                    │ NotificationSystem
                                    │ MCP Server
                                    └───────────────────┘
```

## 📋 Key Components

### 1. **MCP Servers** (Model Context Protocol)
- `applicant_db_server.py` - Profile analysis with income/employment/credit metrics
- `risk_rules_server.py` - Financial risk calculation (DTI, credit risk, anomalies)
- `decision_synthesis_server.py` - Rule-based loan decision synthesis
- `notification_server.py` - Compliance action logging and case ID generation

### 2. **Agents** (Claude Haiku 4.5)
- `profile_agent.py` - Analyzes applicant profile
- `risk_agent.py` - Evaluates financial risk
- `decision_agent.py` - Synthesizes final decision
- `compliance_agent.py` - Logs actions and sends notifications

### 3. **Orchestration** (LangGraph)
- Sequential workflow: Validation → Profile → Risk → Decision → Compliance
- State management via `LoanApplicationState` TypedDict
- Error handling and state propagation

### 4. **API** (FastAPI)
- `POST /api/v1/loan/apply` - Process loan application
- `GET /health` - Health check
- CORS enabled for Streamlit integration

### 5. **UI** (Streamlit)
- Chat-style application submission form
- Real-time color-coded decision display
- Application history tracking
- Expandable analysis details

## 🚀 Installation & Setup

### 1. Clone & Install Dependencies
```bash
cd /home/ubuntu/Desktop/Capstone
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
export ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Run the System

**Terminal 1 - Start FastAPI Microservice:**
```bash
cd /home/ubuntu/Desktop/Capstone
python -m uvicorn microservice.api:app --reload --port 8000
```

**Terminal 2 - Start Streamlit UI:**
```bash
cd /home/ubuntu/Desktop/Capstone
streamlit run ui/app.py
```

The UI will open at `http://localhost:8501`

## 📊 Workflow

1. **User submits application** via Streamlit form
2. **Validation node** checks required fields
3. **Profile Agent** analyzes applicant via ApplicantDB MCP server
4. **Risk Agent** calculates risk metrics via RiskRulesDB MCP server
5. **Decision Agent** synthesizes decision via DecisionSynthesis MCP server
6. **Compliance Agent** logs action via NotificationSystem MCP server
7. **Result displayed** with color-coded classification (Approved/Rejected/Review)

## 📝 Sample Test Input

```
Applicant Name: John Doe
Age: 35
Income: $75,000
Employment Type: SALARIED
Credit Score: 720
Loan Amount: $200,000
Tenure: 20 years
Monthly Liabilities: $500
Location: NYC
```

**Expected Result:** APPROVED with medium risk score (~40-50)

## 🔧 Decision Logic

### Profile Agent
- **Income Stability Score:** 0-100 based on employment type + income range
- **Employment Risk:** LOW/MEDIUM/HIGH
- **Credit Summary:** Text based on credit score ranges
- **Completeness Flags:** Data validation warnings

### Risk Agent
- **Debt-to-Income Ratio:** (Monthly Debt) / (Monthly Income)
- **Credit Risk Level:** LOW (<750), MEDIUM (650-749), HIGH (550-649), CRITICAL (<550)
- **Loan Amount Risk:** Compare to 5× annual income threshold
- **Anomalies:** Flags unusual patterns (loan > 10× income, etc.)

### Decision Agent
- Composite risk scoring (0-100)
- Classification: APPROVED / REJECTED / MANUAL_REVIEW
- Confidence levels: HIGH / MEDIUM / LOW
- Key decision factors extracted

### Compliance Agent
- Generates unique case ID
- Logs timestamp and action
- Returns notification summary

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Chatbot UI | Streamlit |
| Microservice | FastAPI + Uvicorn |
| Orchestration | LangGraph |
| Agent Communication | MCP (stdio) |
| LLM | Anthropic Claude Haiku 4.5 |
| Language | Python 3.x |
| Data Format | JSON/Pydantic |

## 📦 Project Structure

```
Capstone/
├── requirements.txt
├── .env.example
├── README.md
├── mcp_servers/
│   ├── applicant_db_server.py
│   ├── risk_rules_server.py
│   ├── decision_synthesis_server.py
│   └── notification_server.py
├── agents/
│   ├── profile_agent.py
│   ├── risk_agent.py
│   ├── decision_agent.py
│   └── compliance_agent.py
├── orchestrator/
│   ├── state.py
│   └── orchestrator.py
├── microservice/
│   └── api.py
└── ui/
    └── app.py
```

## 📊 Response Format

```json
{
  "application_id": "APP-1730205600",
  "applicant_name": "John Doe",
  "classification": "APPROVED",
  "risk_score": 45,
  "confidence_level": "MEDIUM",
  "case_id": "A1B2C3D4",
  "key_decision_factors": [
    "Strong credit score",
    "Stable employment",
    "Conservative debt-to-income ratio"
  ],
  "explanation": "Application APP-1730205600: Loan approved. Risk score: 45/100...",
  "profile_summary": {
    "income_stability_score": 85,
    "employment_risk": "LOW",
    "completeness_flags": []
  },
  "risk_summary": {
    "debt_to_income_ratio": 0.35,
    "credit_score_risk_level": "LOW",
    "loan_amount_risk": "LOW"
  }
}
```

## 🎯 Features

✅ Multi-agent orchestration with LangGraph  
✅ MCP-based agent communication  
✅ Real-time Streamlit UI with chat history  
✅ FastAPI REST microservice  
✅ Claude Haiku 4.5 for intelligent analysis  
✅ Comprehensive audit trail with case IDs  
✅ Configurable decision logic  
✅ Error handling and validation  
✅ Color-coded decision display  
✅ Application history tracking  

## 🔐 Security Notes

- API runs on localhost only (modify CORS for production)
- All decisions are auditable with case IDs
- No sensitive data is logged
- MCP servers run in subprocess isolation

## 📚 Further Enhancements

- [ ] Integrate real external databases
- [ ] Add WebSocket support for real-time updates
- [ ] Implement decision explainability scores
- [ ] Add batch processing API
- [ ] Create admin dashboard
- [ ] Add role-based access control
- [ ] Implement appeal workflow
- [ ] Add ML-based decision refinement

## 📄 License

Educational use - Capstone Project

## 🤝 Support

For issues or questions, refer to the orchestrator state flow and agent outputs in the Streamlit UI.
