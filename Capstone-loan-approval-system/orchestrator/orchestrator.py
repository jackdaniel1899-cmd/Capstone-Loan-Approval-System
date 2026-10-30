from langgraph.graph import StateGraph, END
from orchestrator.state import LoanApplicationState
from agents.profile_agent import run_profile_agent
from agents.risk_agent import run_risk_agent
from agents.decision_agent import run_decision_agent
from agents.compliance_agent import run_compliance_agent


def validate_node(state: LoanApplicationState) -> LoanApplicationState:
    """Validate application data."""
    application = state.get("application", {})

    required_fields = [
        "application_id",
        "age",
        "income",
        "employment_type",
        "credit_score",
        "loan_amount",
        "tenure",
        "existing_liabilities",
        "location",
        "applicant_name",
    ]

    missing_fields = [f for f in required_fields if f not in application or application.get(f) is None]

    if missing_fields:
        return {
            **state,
            "error": f"Missing required fields: {', '.join(missing_fields)}",
        }

    state["applicant_name"] = application.get("applicant_name", "Unknown")
    return state


def profile_node(state: LoanApplicationState) -> LoanApplicationState:
    """Profile analysis node - calls Application Profile Agent."""
    if state.get("error"):
        return state

    try:
        profile_result = run_profile_agent(state["application"])
        return {**state, "profile_analysis": profile_result}
    except Exception as e:
        return {**state, "error": f"Profile analysis failed: {str(e)}"}


def risk_node(state: LoanApplicationState) -> LoanApplicationState:
    """Risk analysis node - calls Financial Risk Analysis Agent."""
    if state.get("error"):
        return state

    try:
        risk_result = run_risk_agent(state["application"])
        return {**state, "risk_analysis": risk_result}
    except Exception as e:
        return {**state, "error": f"Risk analysis failed: {str(e)}"}


def decision_node(state: LoanApplicationState) -> LoanApplicationState:
    """Decision synthesis node - calls Loan Decision Agent."""
    if state.get("error"):
        return state

    try:
        decision_result = run_decision_agent(
            state["application"],
            state.get("profile_analysis", {}),
            state.get("risk_analysis", {}),
        )
        return {**state, "decision": decision_result}
    except Exception as e:
        return {**state, "error": f"Decision synthesis failed: {str(e)}"}


def compliance_node(state: LoanApplicationState) -> LoanApplicationState:
    """Compliance action node - calls Compliance & Action Orchestration Agent."""
    if state.get("error"):
        return state

    try:
        compliance_result = run_compliance_agent(
            state["application"],
            state.get("decision", {}),
            state.get("applicant_name", "Unknown"),
        )
        return {**state, "compliance_result": compliance_result}
    except Exception as e:
        return {**state, "error": f"Compliance action failed: {str(e)}"}


def create_orchestrator():
    """Create and compile the LangGraph orchestrator."""
    workflow = StateGraph(LoanApplicationState)

    workflow.add_node("validate", validate_node)
    workflow.add_node("profile", profile_node)
    workflow.add_node("risk", risk_node)
    workflow.add_node("decision", decision_node)
    workflow.add_node("compliance", compliance_node)

    workflow.set_entry_point("validate")

    workflow.add_edge("validate", "profile")
    workflow.add_edge("profile", "risk")
    workflow.add_edge("risk", "decision")
    workflow.add_edge("decision", "compliance")
    workflow.add_edge("compliance", END)

    return workflow.compile()


def run_loan_application(application_data: dict) -> dict:
    """Run the complete loan application workflow."""
    graph = create_orchestrator()

    initial_state = {
        "application": application_data,
        "applicant_name": application_data.get("applicant_name", "Unknown"),
        "profile_analysis": {},
        "risk_analysis": {},
        "decision": {},
        "compliance_result": {},
        "error": None,
    }

    final_state = graph.invoke(initial_state)

    return {
        "application_id": application_data.get("application_id", ""),
        "applicant_name": final_state.get("applicant_name", "Unknown"),
        "profile_analysis": final_state.get("profile_analysis", {}),
        "risk_analysis": final_state.get("risk_analysis", {}),
        "decision": final_state.get("decision", {}),
        "compliance_result": final_state.get("compliance_result", {}),
        "error": final_state.get("error"),
    }
