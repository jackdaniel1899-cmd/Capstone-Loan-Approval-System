import json
from anthropic import Anthropic

client = Anthropic()


def run_profile_agent(application_data: dict) -> dict:
    """
    Application Profile Agent - analyzes applicant details.
    Calls analyze_applicant_profile tool directly.
    """

    from mcp_servers.applicant_db_server import analyze_applicant_profile

    profile_analysis_result = {
        "age": application_data.get("age", 0),
        "income": application_data.get("income", 0),
        "employment_type": application_data.get("employment_type", "SALARIED"),
        "credit_score": application_data.get("credit_score", 600),
        "income_stability_score": 0,
        "employment_risk": "MEDIUM",
        "credit_history_summary": "",
        "completeness_flags": [],
        "llm_assessment": "",
    }

    try:
        result = analyze_applicant_profile(
            age=application_data.get("age", 0),
            income=application_data.get("income", 0),
            employment_type=application_data.get("employment_type", "SALARIED"),
            credit_score=application_data.get("credit_score", 600),
            existing_liabilities=application_data.get("existing_liabilities", 0),
            loan_amount=application_data.get("loan_amount", 0),
            tenure=application_data.get("tenure", 0),
        )

        profile_analysis_result.update(result)

        llm_prompt = f"""You are the Application Profile Agent. Based on this profile analysis, provide a concise assessment:

Profile Analysis: {json.dumps(result, indent=2)}

Provide your assessment in 1-2 sentences."""

        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=200,
            messages=[{"role": "user", "content": llm_prompt}],
        )

        profile_analysis_result["llm_assessment"] = response.content[0].text

    except Exception as e:
        profile_analysis_result["llm_assessment"] = f"Error during profile analysis: {str(e)}"

    return profile_analysis_result
