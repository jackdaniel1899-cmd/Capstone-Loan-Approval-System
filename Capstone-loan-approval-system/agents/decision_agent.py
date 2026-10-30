import json
from anthropic import Anthropic

client = Anthropic()


def run_decision_agent(
    application_data: dict, profile_analysis: dict, risk_analysis: dict
) -> dict:
    """
    Loan Decision Agent - synthesizes final decision.
    Calls synthesize_decision tool directly.
    """

    from mcp_servers.decision_synthesis_server import synthesize_decision

    decision_result = {
        "classification": "MANUAL_REVIEW",
        "risk_score": 50,
        "confidence_level": "MEDIUM",
        "key_decision_factors": [],
        "explanation": "",
        "llm_assessment": "",
    }

    try:
        result = synthesize_decision(
            profile_json=json.dumps(profile_analysis),
            risk_json=json.dumps(risk_analysis),
            application_id=application_data.get("application_id", "APP-001"),
        )

        decision_result.update(result)

        llm_prompt = f"""You are the Loan Decision Agent. Based on the profile, risk analysis, and decision synthesis, confirm or refine the classification:

Classification: {result.get('classification')}
Risk Score: {result.get('risk_score')}/100
Confidence: {result.get('confidence_level')}
Key Factors: {result.get('key_decision_factors')}

Confirm if this decision is sound in 2-3 sentences."""

        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=300,
            messages=[{"role": "user", "content": llm_prompt}],
        )

        decision_result["llm_assessment"] = response.content[0].text

    except Exception as e:
        decision_result["llm_assessment"] = f"Error during decision synthesis: {str(e)}"

    return decision_result
