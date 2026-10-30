import json
from anthropic import Anthropic

client = Anthropic()


def run_risk_agent(application_data: dict) -> dict:
    """
    Financial Risk Analysis Agent - analyzes financial risk metrics.
    Calls calculate_risk_metrics tool directly.
    """

    from mcp_servers.risk_rules_server import calculate_risk_metrics

    risk_analysis_result = {
        "debt_to_income_ratio": 0.0,
        "credit_score_risk_level": "MEDIUM",
        "loan_amount_risk": "MEDIUM",
        "anomaly_detection": [],
        "reasoning": "",
        "llm_assessment": "",
    }

    try:
        result = calculate_risk_metrics(
            income=application_data.get("income", 0),
            loan_amount=application_data.get("loan_amount", 0),
            tenure=application_data.get("tenure", 0),
            credit_score=application_data.get("credit_score", 600),
            existing_liabilities=application_data.get("existing_liabilities", 0),
        )

        risk_analysis_result.update(result)

        llm_prompt = f"""You are the Financial Risk Analysis Agent. Based on these risk metrics, provide your analysis:

Risk Metrics: {json.dumps(result, indent=2)}

Provide your analysis in 2-3 sentences."""

        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=300,
            messages=[{"role": "user", "content": llm_prompt}],
        )

        risk_analysis_result["llm_assessment"] = response.content[0].text

    except Exception as e:
        risk_analysis_result["llm_assessment"] = f"Error during risk analysis: {str(e)}"

    return risk_analysis_result
