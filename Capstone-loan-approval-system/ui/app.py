import streamlit as st
import requests
import json
from datetime import datetime
import time

st.set_page_config(
    page_title="Intelligent Loan Approval System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "http://localhost:8000/api/v1/loan/apply"
HEALTH_URL = "http://localhost:8000/health"

st.title("🏦 Intelligent Loan Approval System")

with st.sidebar:
    st.header("System Status")

    try:
        health = requests.get(HEALTH_URL, timeout=2)
        if health.status_code == 200:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Error")
    except requests.exceptions.RequestException:
        st.error("❌ API Offline")

    st.markdown("---")
    st.header("Architecture Overview")
    st.info(
        """
    **5-Layer Architecture:**

    1. **Presentation** → Streamlit UI
    2. **Microservice** → FastAPI REST
    3. **Orchestration** → LangGraph
    4. **Agents** → 4 Domain Agents
    5. **Communication** → MCP Servers
    """
    )

    st.markdown("---")
    st.header("How It Works")
    st.markdown(
        """
    1. Submit loan application
    2. Profile Agent analyzes applicant
    3. Risk Agent calculates financial risk
    4. Decision Agent synthesizes outcome
    5. Compliance Agent sends notification
    """
    )

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

col1, col2 = st.columns([2, 1])

with col1:
    st.header("New Loan Application")

    with st.form("loan_application_form", clear_on_submit=True):
        st.subheader("Applicant Information")

        col_a, col_b = st.columns(2)
        with col_a:
            applicant_name = st.text_input("Applicant Name", value="John Doe")
            age = st.number_input("Age", min_value=18, max_value=100, value=35)
            employment_type = st.selectbox(
                "Employment Type",
                ["SALARIED", "SELF_EMPLOYED", "BUSINESS_OWNER", "FREELANCER", "STUDENT", "RETIRED"],
            )
            location = st.text_input("Location", value="NYC")

        with col_b:
            annual_income = st.number_input("Annual Income ($)", min_value=0, value=75000)
            credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=720)
            existing_liabilities = st.number_input("Monthly Liabilities ($)", min_value=0, value=500)
            application_id = f"APP-{int(time.time())}"

        st.subheader("Loan Details")

        col_c, col_d = st.columns(2)
        with col_c:
            loan_amount = st.number_input("Loan Amount ($)", min_value=1000, value=200000)

        with col_d:
            tenure = st.number_input("Loan Tenure (Years)", min_value=1, max_value=40, value=20)

        submitted = st.form_submit_button("📊 Process Application", use_container_width=True)

        if submitted:
            with st.spinner("Processing loan application..."):
                application_data = {
                    "application_id": application_id,
                    "applicant_name": applicant_name,
                    "age": age,
                    "income": annual_income,
                    "employment_type": employment_type,
                    "credit_score": credit_score,
                    "loan_amount": loan_amount,
                    "tenure": tenure,
                    "existing_liabilities": existing_liabilities,
                    "location": location,
                }

                try:
                    response = requests.post(API_URL, json=application_data, timeout=30)

                    if response.status_code == 200:
                        result = response.json()

                        st.session_state.chat_history.append(
                            {
                                "timestamp": datetime.now(),
                                "applicant": applicant_name,
                                "result": result,
                            }
                        )

                        st.success("✅ Application processed successfully!")

                        classification = result.get("classification", "UNKNOWN")
                        risk_score = result.get("risk_score", 0)
                        case_id = result.get("case_id", "N/A")

                        if classification == "APPROVED":
                            st.markdown(
                                f"""
                            <div style="background-color: #d4edda; padding: 20px; border-radius: 10px; margin: 10px 0;">
                            <h2 style="color: #155724; margin: 0;">✅ LOAN APPROVED</h2>
                            <p style="color: #155724; margin: 10px 0;">Case ID: <strong>{case_id}</strong></p>
                            <p style="color: #155724; margin: 10px 0;">Risk Score: <strong>{risk_score}/100</strong></p>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )
                        elif classification == "REJECTED":
                            st.markdown(
                                f"""
                            <div style="background-color: #f8d7da; padding: 20px; border-radius: 10px; margin: 10px 0;">
                            <h2 style="color: #721c24; margin: 0;">❌ LOAN REJECTED</h2>
                            <p style="color: #721c24; margin: 10px 0;">Case ID: <strong>{case_id}</strong></p>
                            <p style="color: #721c24; margin: 10px 0;">Risk Score: <strong>{risk_score}/100</strong></p>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                f"""
                            <div style="background-color: #fff3cd; padding: 20px; border-radius: 10px; margin: 10px 0;">
                            <h2 style="color: #856404; margin: 0;">⚠️ MANUAL REVIEW REQUIRED</h2>
                            <p style="color: #856404; margin: 10px 0;">Case ID: <strong>{case_id}</strong></p>
                            <p style="color: #856404; margin: 10px 0;">Risk Score: <strong>{risk_score}/100</strong></p>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )

                        st.markdown("---")

                        with st.expander("📋 Detailed Analysis", expanded=True):
                            st.subheader("Key Decision Factors")
                            factors = result.get("key_decision_factors", [])
                            for factor in factors:
                                st.write(f"• {factor}")

                            st.subheader("Decision Explanation")
                            st.info(result.get("explanation", "No explanation available"))

                            st.subheader("Profile Analysis")
                            profile = result.get("profile_summary", {})
                            st.json(profile)

                            st.subheader("Risk Analysis")
                            risk = result.get("risk_summary", {})
                            st.json(risk)

                            st.subheader("Full Response")
                            st.json(result)

                    else:
                        st.error(f"API Error: {response.status_code}")
                        st.error(response.text)

                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to API. Is it running on localhost:8000?")
                except requests.exceptions.Timeout:
                    st.error("❌ API request timed out")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

with col2:
    st.header("📜 Application History")

    if st.session_state.chat_history:
        for idx, entry in enumerate(reversed(st.session_state.chat_history)):
            with st.container():
                result = entry["result"]
                classification = result.get("classification", "UNKNOWN")
                applicant = entry["applicant"]
                timestamp = entry["timestamp"].strftime("%H:%M:%S")

                if classification == "APPROVED":
                    emoji = "✅"
                    color = "green"
                elif classification == "REJECTED":
                    emoji = "❌"
                    color = "red"
                else:
                    emoji = "⚠️"
                    color = "orange"

                st.markdown(
                    f"<div style='border-left: 4px solid {color}; padding: 10px; margin: 5px 0;'>"
                    f"<b>{emoji} {applicant}</b><br>"
                    f"<small>{timestamp}</small><br>"
                    f"<small>Risk: {result.get('risk_score', 0)}/100</small>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

                if st.button("View", key=f"view_{idx}"):
                    st.session_state.selected_result = entry["result"]

    else:
        st.info("No applications processed yet")

    st.markdown("---")

    if "selected_result" in st.session_state:
        result = st.session_state.selected_result
        classification = result.get("classification", "UNKNOWN")
        risk_score = result.get("risk_score", 0)
        case_id = result.get("case_id", "N/A")
        applicant_name = result.get("applicant_name", "Unknown")

        st.subheader(f"📋 Selected Application - {applicant_name}")

        if classification == "APPROVED":
            st.markdown(
                f"""
            <div style="background-color: #d4edda; padding: 20px; border-radius: 10px; margin: 10px 0;">
            <h3 style="color: #155724; margin: 0;">✅ LOAN APPROVED</h3>
            <p style="color: #155724; margin: 10px 0;">Case ID: <strong>{case_id}</strong></p>
            <p style="color: #155724; margin: 10px 0;">Risk Score: <strong>{risk_score}/100</strong></p>
            </div>
            """,
                unsafe_allow_html=True,
            )
        elif classification == "REJECTED":
            st.markdown(
                f"""
            <div style="background-color: #f8d7da; padding: 20px; border-radius: 10px; margin: 10px 0;">
            <h3 style="color: #721c24; margin: 0;">❌ LOAN REJECTED</h3>
            <p style="color: #721c24; margin: 10px 0;">Case ID: <strong>{case_id}</strong></p>
            <p style="color: #721c24; margin: 10px 0;">Risk Score: <strong>{risk_score}/100</strong></p>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
            <div style="background-color: #fff3cd; padding: 20px; border-radius: 10px; margin: 10px 0;">
            <h3 style="color: #856404; margin: 0;">⚠️ MANUAL REVIEW REQUIRED</h3>
            <p style="color: #856404; margin: 10px 0;">Case ID: <strong>{case_id}</strong></p>
            <p style="color: #856404; margin: 10px 0;">Risk Score: <strong>{risk_score}/100</strong></p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with st.expander("📋 Detailed Analysis", expanded=True):
            st.subheader("Key Decision Factors")
            factors = result.get("key_decision_factors", [])
            for factor in factors:
                st.write(f"• {factor}")

            st.subheader("Decision Explanation")
            st.info(result.get("explanation", "No explanation available"))

            st.subheader("Profile Analysis")
            profile = result.get("profile_summary", {})
            if profile:
                st.json(profile)
            else:
                st.write("No profile summary available")

            st.subheader("Risk Analysis")
            risk = result.get("risk_summary", {})
            if risk:
                st.json(risk)
            else:
                st.write("No risk summary available")

            st.subheader("Full Response")
            st.json(result)

st.markdown("---")
st.markdown(
    "<center><small>🤖 Powered by Anthropic Claude | Multi-Agent AI Architecture</small></center>",
    unsafe_allow_html=True,
)
