

def calculate_debt_to_income(
    income: int, loan_amount: int, tenure: int, existing_liabilities: int
) -> float:
    monthly_income = income / 12
    if monthly_income <= 0:
        return 999.0

    monthly_payment = loan_amount / (tenure * 12)
    total_monthly_debt = monthly_payment + (existing_liabilities / 12)

    return round(total_monthly_debt / monthly_income, 2)


def get_credit_risk_level(credit_score: int) -> str:
    if credit_score >= 750:
        return "LOW"
    elif credit_score >= 650:
        return "MEDIUM"
    elif credit_score >= 550:
        return "HIGH"
    else:
        return "CRITICAL"


def get_loan_amount_risk(income: int, loan_amount: int) -> str:
    threshold = income * 5

    if loan_amount <= threshold:
        return "LOW"
    elif loan_amount <= threshold * 1.5:
        return "MEDIUM"
    elif loan_amount <= threshold * 2:
        return "HIGH"
    else:
        return "CRITICAL"


def detect_anomalies(
    income: int, loan_amount: int, tenure: int, credit_score: int
) -> list:
    anomalies = []

    if loan_amount > income * 10:
        anomalies.append("Loan exceeds 10x annual income")

    if tenure < 1 or tenure > 40:
        anomalies.append("Unusual loan tenure (must be 1-40 years)")

    if credit_score < 550 and loan_amount > income * 3:
        anomalies.append("Poor credit with large loan amount")

    if income < 15000 and loan_amount > 50000:
        anomalies.append("Low income with disproportionately large loan")

    return anomalies


def calculate_risk_metrics(
    income: int,
    loan_amount: int,
    tenure: int,
    credit_score: int,
    existing_liabilities: int,
) -> dict:
    """Calculate financial risk metrics for the loan application."""

    dti_ratio = calculate_debt_to_income(income, loan_amount, tenure, existing_liabilities)
    credit_risk = get_credit_risk_level(credit_score)
    loan_risk = get_loan_amount_risk(income, loan_amount)
    anomalies = detect_anomalies(income, loan_amount, tenure, credit_score)

    risk_reasoning = f"Debt-to-Income Ratio: {dti_ratio:.2f}. "
    if dti_ratio > 0.5:
        risk_reasoning += "High DTI indicates significant debt burden. "
    if credit_risk in ["HIGH", "CRITICAL"]:
        risk_reasoning += f"Credit risk level is {credit_risk}. "
    if loan_risk in ["HIGH", "CRITICAL"]:
        risk_reasoning += f"Loan amount risk is {loan_risk}. "

    return {
        "debt_to_income_ratio": dti_ratio,
        "credit_score_risk_level": credit_risk,
        "loan_amount_risk": loan_risk,
        "anomaly_detection": anomalies,
        "reasoning": risk_reasoning,
        "income": income,
        "loan_amount": loan_amount,
        "credit_score": credit_score,
    }
