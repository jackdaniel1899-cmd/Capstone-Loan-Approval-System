from typing import TypedDict, Optional, List, Dict, Any


class LoanApplicationState(TypedDict):
    """State schema for loan application workflow."""

    application: dict
    applicant_name: str
    profile_analysis: dict
    risk_analysis: dict
    decision: dict
    compliance_result: dict
    error: Optional[str]
