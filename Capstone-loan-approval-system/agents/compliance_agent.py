import json
from anthropic import Anthropic

client = Anthropic()


def run_compliance_agent(
    application_data: dict, decision: dict, applicant_name: str
) -> dict:
    """
    Compliance and Action Orchestration Agent - sends notifications and logs.
    Calls send_notification tool directly.
    """

    from mcp_servers.notification_server import send_notification

    compliance_result = {
        "action_taken": "",
        "notification_sent": False,
        "case_id": "",
        "timestamp": "",
        "summary": "",
        "llm_assessment": "",
    }

    try:
        result = send_notification(
            application_id=application_data.get("application_id", "APP-001"),
            classification=decision.get("classification", "MANUAL_REVIEW"),
            applicant_name=applicant_name,
            reasoning=decision.get("explanation", ""),
            risk_score=decision.get("risk_score", 50),
        )

        compliance_result.update(result)

        llm_prompt = f"""You are the Compliance and Action Orchestration Agent. Confirm the compliance action taken:

Classification: {decision.get('classification')}
Case ID: {result.get('case_id')}
Action: {result.get('action_taken')}
Timestamp: {result.get('timestamp')}

Confirm this action is compliant and summarize in 2 sentences."""

        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=300,
            messages=[{"role": "user", "content": llm_prompt}],
        )

        compliance_result["llm_assessment"] = response.content[0].text

    except Exception as e:
        compliance_result["llm_assessment"] = f"Error during compliance action: {str(e)}"

    return compliance_result
