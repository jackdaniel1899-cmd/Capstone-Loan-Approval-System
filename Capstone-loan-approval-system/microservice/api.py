from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from orchestrator.orchestrator import run_loan_application

app = FastAPI(
    title="Agentic AI Loan Approval System",
    description="Multi-agent system for intelligent loan application processing",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoanApplication(BaseModel):
    """Loan application request model."""

    application_id: str = Field(..., description="Unique application identifier")
    applicant_name: str = Field(..., description="Name of the applicant")
    age: int = Field(..., ge=18, le=100, description="Age of applicant")
    income: int = Field(..., ge=0, description="Annual income in USD")
    employment_type: str = Field(
        ...,
        description="Type of employment (SALARIED, SELF_EMPLOYED, BUSINESS_OWNER, FREELANCER, STUDENT, RETIRED)",
    )
    credit_score: int = Field(..., ge=300, le=850, description="Credit score (300-850)")
    loan_amount: int = Field(..., ge=1000, description="Requested loan amount in USD")
    tenure: int = Field(..., ge=1, le=40, description="Loan tenure in years")
    existing_liabilities: int = Field(..., ge=0, description="Existing monthly liabilities in USD")
    location: str = Field(..., description="Applicant location")


class LoanDecisionResponse(BaseModel):
    """Loan decision response model."""

    application_id: str
    applicant_name: str
    classification: str
    risk_score: float
    confidence_level: str
    case_id: str
    key_decision_factors: list
    explanation: str
    profile_summary: dict
    risk_summary: dict
    error: Optional[str] = None


@app.get("/health", tags=["Health"])
def health_check():
    """Check API health status."""
    return {"status": "ok", "service": "Loan Approval System"}


@app.post("/api/v1/loan/apply", response_model=LoanDecisionResponse, tags=["Loan Processing"])
def process_loan_application(application: LoanApplication):
    """Process a loan application through the multi-agent system."""
    try:
        application_dict = application.model_dump()

        result = run_loan_application(application_dict)

        if result.get("error"):
            raise HTTPException(status_code=400, detail=result["error"])

        decision = result.get("decision", {})
        profile = result.get("profile_analysis", {})
        risk = result.get("risk_analysis", {})
        compliance = result.get("compliance_result", {})

        return LoanDecisionResponse(
            application_id=result.get("application_id", ""),
            applicant_name=result.get("applicant_name", ""),
            classification=decision.get("classification", "MANUAL_REVIEW"),
            risk_score=decision.get("risk_score", 50),
            confidence_level=decision.get("confidence_level", "MEDIUM"),
            case_id=compliance.get("case_id", "N/A"),
            key_decision_factors=decision.get("key_decision_factors", []),
            explanation=decision.get("explanation", ""),
            profile_summary={
                "income_stability_score": profile.get("income_stability_score", 0),
                "employment_risk": profile.get("employment_risk", "MEDIUM"),
                "completeness_flags": profile.get("completeness_flags", []),
            },
            risk_summary={
                "debt_to_income_ratio": risk.get("debt_to_income_ratio", 0),
                "credit_score_risk_level": risk.get("credit_score_risk_level", "MEDIUM"),
                "loan_amount_risk": risk.get("loan_amount_risk", "MEDIUM"),
            },
            error=None,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("FASTAPI_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
