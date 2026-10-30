# Quick Start Guide

## 1️⃣ One-Time Setup

```bash
# Navigate to project
cd /home/ubuntu/Desktop/Capstone

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE" > .env
```

## 2️⃣ Run in Two Terminals

### Terminal 1 - Start API Server
```bash
cd /home/ubuntu/Desktop/Capstone
python -m uvicorn microservice.api:app --reload --port 8000
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
Press CTRL+C to quit
```

### Terminal 2 - Start Streamlit UI
```bash
cd /home/ubuntu/Desktop/Capstone
streamlit run ui/app.py
```

You should see:
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

## 3️⃣ Test the System

**Open browser:** http://localhost:8501

**Fill in the form with sample data:**
- Applicant Name: John Doe
- Age: 35
- Income: $75,000
- Employment Type: SALARIED
- Credit Score: 720
- Loan Amount: $200,000
- Tenure: 20 years
- Monthly Liabilities: $500
- Location: NYC

**Click: "📊 Process Application"**

## ✅ Expected Results

You should see:
1. **Green banner** with "✅ LOAN APPROVED"
2. **Risk Score:** ~40-50/100
3. **Case ID:** Generated unique ID
4. **Key Factors:** Listed (e.g., "Strong credit score", "Stable employment")
5. **Full Analysis:** Profile, Risk, and Decision details

## 🔧 Test Different Scenarios

TEST 1: ✅ APPROVED (Green Banner - Risk 20-35)
 
Name: Michael Thompson | Age: 42 | Income: 95000
Employment: SALARIED | Credit: 750 | Loan: 180000
Tenure: 15 | Liabilities: 300 | Location: Chicago
Why APPROVED:
 
✅ Credit 750 ≥ 700
✅ Loan 1.9× income ≤ 3×
✅ DTI 16% ≤ 50%
✅ SALARIED employment
TEST 2: ⚠️ MANUAL_REVIEW (Yellow Banner - Risk 65-72)
 
Name: Jennifer Chen | Age: 31 | Income: 68000
Employment: FREELANCER | Credit: 680 | Loan: 220000
Tenure: 20 | Liabilities: 800 | Location: Austin
Why MANUAL_REVIEW:
 
⚠️ Credit 680 (just under 700)
⚠️ Loan 3.2× income (moderate-high)
⚠️ DTI 30% (moderate)
⚠️ FREELANCER (variable income)
TEST 3: ❌ REJECTED (Red Banner - Risk 92-100)
 
Name: David Martinez | Age: 58 | Income: 32000
Employment: STUDENT | Credit: 480 | Loan: 280000
Tenure: 25 | Liabilities: 1800 | Location: Miami
Why REJECTED:
 
❌ Credit 480 < 550 (CRITICAL)
❌ Loan 8.75× income > 5× (CRITICAL)
❌ DTI 103% > 65% (CRITICAL)
❌ STUDENT employment (high risk)

## 🐛 Troubleshooting

**"Cannot connect to API"**
- Make sure Terminal 1 is running FastAPI
- Check http://localhost:8000/health returns `{"status": "ok"}`

**"ImportError: No module named 'mcp_servers'"**
- Make sure you're running from `/home/ubuntu/Desktop/Capstone` directory
- Python should be able to find relative imports

**"Claude API Error"**
- Verify `ANTHROPIC_API_KEY` is set in `.env`
- Check API key is valid at https://console.anthropic.com

**"MCP Server Error"**
- MCP servers run in-process via direct imports
- Check FastMCP is installed: `pip install fastmcp`

## 📊 View API Documentation

Open: http://localhost:8000/docs

You'll see the interactive Swagger API documentation with:
- `/health` endpoint
- `/api/v1/loan/apply` endpoint
- Request/response schemas
- Try-it-out forms

## 🎯 Next Steps

Once the system is running:
1. Test with multiple applications
2. Review decision explanations
3. Check application history in the sidebar
4. Observe how risk scores change with different inputs
5. Review the README.md for architecture details

## 💡 Tips

- **Faster Testing:** Use Test Cases in sidebar history to re-submit similar apps
- **Debug Mode:** Add prints to agents for detailed tracing
- **Custom Rules:** Edit MCP servers to adjust decision logic
- **Extend System:** Add new agents or MCP servers as needed
