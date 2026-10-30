

import json


def synthesize_classification(profile: dict, risk: dict) -> tuple:
    """
    Synthesize decision based on profile and risk analysis.
    Returns: (classification, risk_score, confidence_level, key_factors)
    """
    completeness_flags = profile.get("completeness_flags", [])

    income_stability = profile.get("income_stability_score", 50)
    employment_risk = profile.get("employment_risk", "MEDIUM")
    employment_type = profile.get("employment_type", "SALARIED")
    credit_score = profile.get("credit_score", 600)

    dti_ratio = risk.get("debt_to_income_ratio", 0.5)
    credit_risk = risk.get("credit_score_risk_level", "MEDIUM")
    loan_risk = risk.get("loan_amount_risk", "MEDIUM")
    anomalies = risk.get("anomaly_detection", [])

    # REJECTION criteria (HIGH RISK)
    rejection_flags = []

    if credit_risk == "CRITICAL":
        rejection_flags.append("Critical credit score")

    if loan_risk == "CRITICAL":
        rejection_flags.append("Loan amount far exceeds safe limits")

    if dti_ratio > 0.65:
        rejection_flags.append("Debt burden exceeds 65% of income")

    if employment_type == "STUDENT" and loan_risk in ["HIGH", "CRITICAL"]:
        rejection_flags.append("Student with high loan amount")

    if len(anomalies) >= 2:
        rejection_flags.append("Multiple risk anomalies detected")

    # If multiple rejection flags or critical credit/loan, REJECT
    if len(rejection_flags) >= 2 or credit_risk == "CRITICAL" or loan_risk == "CRITICAL":
        risk_score = min(100, 50 + 15 + 15 + 10)  # At least 90
        if credit_risk == "CRITICAL":
            risk_score = min(100, risk_score + 10)
        if loan_risk == "CRITICAL":
            risk_score = min(100, risk_score + 10)
        return ("REJECTED", risk_score, "HIGH", rejection_flags)

    # APPROVED criteria (LOW RISK)
    approval_flags = []

    if credit_score >= 750:
        approval_flags.append("Excellent credit score")
    elif credit_score >= 700:
        approval_flags.append("Good credit score")

    if loan_risk == "LOW":
        approval_flags.append("Conservative loan amount")

    if dti_ratio < 0.30:
        approval_flags.append("Low debt-to-income ratio")

    if employment_risk == "LOW":
        approval_flags.append("Stable employment")

    if income_stability >= 80:
        approval_flags.append("High income stability")

    # APPROVED: Credit >= 700 AND Loan <= 3x AND DTI <= 0.5 AND Stable employment
    if (credit_score >= 700 and
        loan_risk in ["LOW", "MEDIUM"] and
        dti_ratio <= 0.5 and
        employment_risk != "HIGH"):

        risk_score = 50
        if credit_score >= 750:
            risk_score -= 20
        elif credit_score >= 700:
            risk_score -= 10

        if loan_risk == "LOW":
            risk_score -= 15
        elif loan_risk == "MEDIUM":
            risk_score -= 5

        if dti_ratio < 0.30:
            risk_score -= 10
        elif dti_ratio <= 0.5:
            risk_score -= 5

        if income_stability >= 80:
            risk_score -= 10

        risk_score = max(0, min(50, risk_score))

        if not approval_flags:
            approval_flags = ["Meets approval criteria"]

        return ("APPROVED", risk_score, "HIGH", approval_flags[:3])

    # MANUAL_REVIEW (MODERATE RISK - Everything else)
    manual_review_flags = []

    if credit_score >= 650:
        manual_review_flags.append("Fair to good credit")
    else:
        manual_review_flags.append("Below average credit")

    if loan_risk == "HIGH":
        manual_review_flags.append("Moderately high loan amount")

    if dti_ratio > 0.45:
        manual_review_flags.append("Elevated debt-to-income")

    if employment_type in ["FREELANCER", "SELF_EMPLOYED"]:
        manual_review_flags.append("Variable income employment")

    if completeness_flags:
        manual_review_flags.extend(completeness_flags)

    if not manual_review_flags:
        manual_review_flags = ["Requires manual review for final approval"]

    # Calculate risk score for MANUAL_REVIEW
    risk_score = 60

    if credit_risk == "LOW":
        risk_score -= 5
    elif credit_risk == "HIGH":
        risk_score += 5

    if loan_risk == "LOW":
        risk_score -= 5
    elif loan_risk == "HIGH":
        risk_score += 5

    if dti_ratio > 0.5:
        risk_score += 10

    if income_stability < 50:
        risk_score += 5

    risk_score = max(60, min(75, risk_score))

    return ("MANUAL_REVIEW", risk_score, "MEDIUM", manual_review_flags[:3])


def synthesize_decision(
    profile_json, risk_json, application_id: str
) -> dict:
    """Synthesize loan decision based on profile and risk analysis."""

    profile = json.loads(profile_json) if isinstance(profile_json, str) else profile_json
    risk = json.loads(risk_json) if isinstance(risk_json, str) else risk_json

    classification, risk_score, confidence, key_factors = synthesize_classification(
        profile, risk
    )

    explanation = f"Application {application_id}: "
    if classification == "APPROVED":
        explanation += f"Loan approved. Risk score: {risk_score}/100 ({confidence} confidence). "
    elif classification == "REJECTED":
        explanation += f"Loan rejected due to high risk. Risk score: {risk_score}/100. "
    else:
        explanation += f"Application requires manual review. Risk score: {risk_score}/100. "

    explanation += f"Key factors: {', '.join(key_factors)}."

    return {
        "classification": classification,
        "risk_score": risk_score,
        "confidence_level": confidence,
        "key_decision_factors": key_factors,
        "explanation": explanation,
        "application_id": application_id,
    }
