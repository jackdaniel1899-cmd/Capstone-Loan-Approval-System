import json
import uuid
from datetime import datetime

notifications_log = []


def send_notification(
    application_id: str,
    classification: str,
    applicant_name: str,
    reasoning: str,
    risk_score: float,
) -> dict:
    """Send notification and log compliance action for loan decision."""

    case_id = str(uuid.uuid4())[:8].upper()
    timestamp = datetime.utcnow().isoformat() + "Z"

    action_map = {
        "APPROVED": "Loan approved - notify applicant",
        "REJECTED": "Loan rejected - notify applicant with details",
        "MANUAL_REVIEW": "Escalated to manual review - notify stakeholders",
    }

    action_taken = action_map.get(classification, "Unknown action")

    notification_entry = {
        "case_id": case_id,
        "application_id": application_id,
        "applicant_name": applicant_name,
        "classification": classification,
        "risk_score": risk_score,
        "action_taken": action_taken,
        "timestamp": timestamp,
        "reasoning_summary": reasoning[:100] + "..." if len(reasoning) > 100 else reasoning,
    }

    notifications_log.append(notification_entry)

    summary = f"Notification sent for application {application_id}. "
    summary += f"Decision: {classification}. "
    summary += f"Case ID: {case_id}. "
    summary += f"Risk Score: {risk_score}/100."

    return {
        "action_taken": action_taken,
        "notification_sent": True,
        "case_id": case_id,
        "timestamp": timestamp,
        "summary": summary,
        "applicant_name": applicant_name,
        "classification": classification,
    }
