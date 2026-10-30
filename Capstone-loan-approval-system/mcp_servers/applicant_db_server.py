EMPLOYMENT_RISK = {
    "SALARIED": ("LOW", 85),
    "SELF_EMPLOYED": ("HIGH", 45),
    "BUSINESS_OWNER": ("HIGH", 50),
    "FREELANCER": ("MEDIUM", 60),
    "STUDENT": ("HIGH", 30),
    "RETIRED": ("MEDIUM", 70),
}


def get_income_stability_score(income: int, employment_type: str) -> int:
    if employment_type not in EMPLOYMENT_RISK:
        employment_type = "SALARIED"

    base_score = EMPLOYMENT_RISK[employment_type][1]

    if income < 20000:
        return max(base_score - 30, 10)
    elif income < 40000:
        return max(base_score - 15, 20)
    elif income < 60000:
        return base_score
    elif income < 100000:
        return min(base_score + 10, 95)
    else:
        return min(base_score + 20, 100)


def get_credit_summary(credit_score: int) -> str:
    if credit_score >= 750:
        return "Excellent credit history with strong payment discipline"
    elif credit_score >= 700:
        return "Good credit history with mostly on-time payments"
    elif credit_score >= 650:
        return "Fair credit history with some late payments"
    elif credit_score >= 550:
        return "Poor credit history with multiple missed payments"
    else:
        return "Critical credit issues - very limited credit history or serious delinquencies"


def analyze_applicant_profile(
    age: int,
    income: int,
    employment_type: str,
    credit_score: int,
    existing_liabilities: int,
    loan_amount: int,
    tenure: int,
) -> dict:
    """Analyze applicant profile and return assessment metrics."""

    income_stability_score = get_income_stability_score(income, employment_type)
    employment_risk, _ = EMPLOYMENT_RISK.get(employment_type, ("MEDIUM", 60))
    credit_summary = get_credit_summary(credit_score)

    completeness_flags = []
    if age < 18 or age > 75:
        completeness_flags.append("Age outside standard lending range")
    if income <= 0:
        completeness_flags.append("Income not properly documented")
    if credit_score < 300:
        completeness_flags.append("Credit score below minimum threshold")
    if tenure <= 0 or tenure > 40:
        completeness_flags.append("Unusual loan tenure")

    return {
        "income_stability_score": income_stability_score,
        "employment_risk": employment_risk,
        "credit_history_summary": credit_summary,
        "completeness_flags": completeness_flags,
        "age": age,
        "employment_type": employment_type,
        "credit_score": credit_score,
    }
