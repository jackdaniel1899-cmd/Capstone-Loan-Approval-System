# 🏦 Agentic AI Intelligent Loan Approval System

## ✅ Project Status: COMPLETE & READY TO RUN

Welcome! This is a complete implementation of a multi-agent AI system for intelligent loan approval processing.

---

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies
```bash
cd /home/ubuntu/Desktop/Capstone
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
```

### 2. Start the API Server (Terminal 1)
```bash
python -m uvicorn microservice.api:app --reload --port 8000
```

### 3. Start the UI (Terminal 2)
```bash
streamlit run ui/app.py
```

**Open browser:** http://localhost:8501

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[QUICK_START.md](QUICK_START.md)** | 3-step setup with test scenarios |
| **[README.md](README.md)** | Full architecture and features |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | Technical deep dive with diagrams |
| **[PROJECT_SUMMARY.txt](PROJECT_SUMMARY.txt)** | Complete project overview |

---

## 🎯 What This System Does

```
User submits loan application
         ↓
    [FastAPI Server]
         ↓
[LangGraph Orchestrator]
         ↓
[4 Intelligent Agents]
  ├─ Profile Agent (analyzes applicant)
  ├─ Risk Agent (calculates financial risk)
  ├─ Decision Agent (makes final decision)
  └─ Compliance Agent (logs and audits)
         ↓
[Real-time UI Display]
  ✅ APPROVED / ❌ REJECTED / ⚠️ MANUAL REVIEW
```

---

## 🏗️ 5-Layer Architecture

| Layer | Component | Technology |
|-------|-----------|-----------|
| **1. Presentation** | Streamlit Chatbot | UI/8501 |
| **2. Microservice** | FastAPI REST | API/8000 |
| **3. Orchestration** | LangGraph | State Machine |
| **4. Agents** | 4 Domain Agents | Claude Haiku 4.5 |
| **5. Communication** | MCP Servers | Stdio Protocol |

---

## 📊 Test the System

### Sample Loan Application
```
Name: John Doe
Age: 35
Income: $75,000
Employment: SALARIED
Credit Score: 720
Loan Amount: $200,000
Tenure: 20 years
Monthly Liabilities: $500
Location: NYC
```

**Expected Result:** ✅ APPROVED, Risk Score: 40-50/100

### Different Scenarios to Try
- **High Risk:** Low income + high loan amount + poor credit
- **Manual Review:** Borderline cases with moderate risk
- **Rejected:** Critical risk factors

---

## 🔧 Project Structure

```
Capstone/
├── START_HERE.md                ← You are here
├── QUICK_START.md               ← Fast setup
├── README.md                    ← Full guide
├── ARCHITECTURE.md              ← Technical details
├── requirements.txt             ← Dependencies
├── .env.example                 ← Config template
│
├── mcp_servers/                 ← 4 MCP servers
│   ├── applicant_db_server.py
│   ├── risk_rules_server.py
│   ├── decision_synthesis_server.py
│   └── notification_server.py
│
├── agents/                      ← 4 Intelligent agents
│   ├── profile_agent.py
│   ├── risk_agent.py
│   ├── decision_agent.py
│   └── compliance_agent.py
│
├── orchestrator/                ← LangGraph orchestration
│   ├── orchestrator.py
│   └── state.py
│
├── microservice/                ← FastAPI server
│   └── api.py
│
└── ui/                          ← Streamlit UI
    └── app.py
```

---

## 🎓 Learning Path

1. **Understand the architecture:**
   - Read [README.md](README.md) for high-level overview
   - Review [ARCHITECTURE.md](ARCHITECTURE.md) for technical details

2. **Run the system:**
   - Follow [QUICK_START.md](QUICK_START.md)
   - Test with provided sample data

3. **Explore the code:**
   - Check out MCP servers for decision logic
   - Review agents for Claude integration
   - Study LangGraph orchestrator

4. **Customize for your needs:**
   - Modify decision logic in MCP servers
   - Add new agents or workflows
   - Integrate real databases

---

## ⚙️ API Endpoints

### Health Check
```bash
GET http://localhost:8000/health
```
Response: `{"status": "ok", "service": "Loan Approval System"}`

### Process Loan Application
```bash
POST http://localhost:8000/api/v1/loan/apply
```
Request body:
```json
{
  "application_id": "APP-001",
  "applicant_name": "John Doe",
  "age": 35,
  "income": 75000,
  "employment_type": "SALARIED",
  "credit_score": 720,
  "loan_amount": 200000,
  "tenure": 20,
  "existing_liabilities": 500,
  "location": "NYC"
}
```

### Swagger Documentation
```
http://localhost:8000/docs
```

---

## 🚨 Troubleshooting

**"Cannot connect to API"**
- Ensure API is running on port 8000
- Check: `curl http://localhost:8000/health`

**"Module not found"**
- Run from `/home/ubuntu/Desktop/Capstone`
- Verify dependencies: `pip install -r requirements.txt`

**"Claude API Error"**
- Check `ANTHROPIC_API_KEY` is set
- Verify API key is valid

**More help?**
- See Troubleshooting section in [QUICK_START.md](QUICK_START.md)

---

## ✨ Key Features

✅ **Multi-agent orchestration** with LangGraph  
✅ **4 domain-specific agents** with Claude Haiku 4.5  
✅ **MCP servers** for standardized communication  
✅ **Real-time Streamlit UI** with chat history  
✅ **FastAPI microservice** with auto-docs  
✅ **Audit trail** with unique case IDs  
✅ **Color-coded decisions** (green/red/yellow)  
✅ **Type-safe** Python with Pydantic  
✅ **Full error handling** and validation  
✅ **Comprehensive documentation**  

---

## 🎯 Decision Logic

### Risk Score (0-100)
- Lower score = Lower risk = More likely to approve
- Higher score = Higher risk = More likely to reject

### Classification
- **Risk < 35:** ✅ APPROVED (HIGH confidence)
- **Risk < 60:** ✅ APPROVED (MEDIUM confidence)
- **Risk < 75:** ⚠️ MANUAL_REVIEW (MEDIUM confidence)
- **Risk ≥ 75:** ❌ REJECTED (HIGH confidence)

### Factors Considered
- Credit score and history
- Income stability and employment type
- Debt-to-income ratio
- Loan amount relative to income
- Anomaly detection (unusual patterns)

---

## 📈 Performance

**End-to-End Response:** ~5-10 seconds (LLM latency dominated)

**Per-Agent Processing:**
- Profile Analysis: ~1-2 seconds
- Risk Calculation: ~1-2 seconds
- Decision Synthesis: ~1-2 seconds
- Compliance Logging: ~1-2 seconds

---

## 🔐 Security

✅ All inputs validated  
✅ Error handling without exposing internals  
✅ Unique audit trail per decision  
✅ No sensitive data in logs  
✅ Localhost-only access (dev mode)  

For production:
- Add authentication layer
- Use HTTPS
- Implement rate limiting
- Store audit logs in database

---

## 🚀 Next Steps

1. **Run the system:** Follow [QUICK_START.md](QUICK_START.md)
2. **Test scenarios:** Try different applicant profiles
3. **Review decisions:** Understand why each decision was made
4. **Customize logic:** Modify MCP servers for your rules
5. **Extend system:** Add new agents or data sources
6. **Deploy:** Prepare for production use

---

## 📞 Support

For detailed information, refer to:
- [README.md](README.md) - Complete architecture guide
- [QUICK_START.md](QUICK_START.md) - Setup and testing
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical specifications
- [PROJECT_SUMMARY.txt](PROJECT_SUMMARY.txt) - Project overview

---

## 🎓 Technology Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| UI | Streamlit | Chat interface, real-time updates |
| API | FastAPI | High performance, auto Swagger docs |
| Orchestration | LangGraph | State machine, type-safe |
| Agents | Claude Haiku 4.5 | Fast, cost-effective, intelligent |
| Communication | MCP | Standardized protocol, isolation |
| Data | Pydantic | Type safety, validation |

---

## ✅ Implementation Checklist

- ✅ 5-layer architecture implemented
- ✅ 4 MCP servers with mock data
- ✅ 4 intelligent agents with Claude
- ✅ LangGraph orchestrator
- ✅ FastAPI microservice
- ✅ Streamlit chatbot UI
- ✅ Comprehensive documentation
- ✅ Git repository initialized
- ✅ Ready for testing and deployment

---

## 🎉 Ready to Start?

**Quick Start (Copy & Paste):**

```bash
# 1. Setup
cd /home/ubuntu/Desktop/Capstone
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-YOUR_KEY

# 2. Start API (Terminal 1)
python -m uvicorn microservice.api:app --reload --port 8000

# 3. Start UI (Terminal 2)
streamlit run ui/app.py

# 4. Open browser
# http://localhost:8501
```

**Questions?** See [QUICK_START.md](QUICK_START.md) for detailed steps.

---

**🚀 Welcome to the Agentic AI Intelligent Loan Approval System!**

*Built with Claude Haiku 4.5, LangGraph, FastAPI, and Streamlit*
