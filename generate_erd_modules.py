from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont


OUT = Path(".")
BG = "#ffffff"
TITLE = "#1f2937"
NOTE = "#64748b"
HEADER = "#1e3a5f"
HEADER_ALT = "#294b73"
ROW = "#ffffff"
ROW_ALT = "#f7f9fc"
GRID = "#cbd5e1"
TEXT = "#111827"
FK_BLUE = "#1d4ed8"
KEY_GOLD = "#c59b20"
LINE = "#64748b"


@dataclass(frozen=True)
class Field:
    name: str
    dtype: str


@dataclass(frozen=True)
class FK:
    table: str
    field: str
    target: str


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    base = Path("/usr/share/fonts/truetype/dejavu")
    return ImageFont.truetype(str(base / name), size=size)


FONT_TITLE = font("DejaVuSans-Bold.ttf", 38)
FONT_NOTE = font("DejaVuSans.ttf", 18)
FONT_HEADER = font("DejaVuSans-Bold.ttf", 17)
FONT_CELL = font("DejaVuSans.ttf", 14)
FONT_CELL_BOLD = font("DejaVuSans-Bold.ttf", 14)
FONT_CELL_ITALIC = font("DejaVuSansMono-Oblique.ttf", 14)
FONT_LABEL = font("DejaVuSans.ttf", 12)


FIELDS: Dict[str, List[Field]] = {
    "accounts_profile": [
        Field("profileID", "int8"),
        Field("profileImg", "varchar"),
        Field("firstName", "varchar"),
        Field("lastName", "varchar"),
        Field("middleName", "varchar"),
        Field("contactNum", "varchar"),
        Field("birthDate", "date"),
        Field("profileType", "varchar"),
        Field("latitude", "numeric"),
        Field("longitude", "numeric"),
        Field("location_sharing_enabled", "bool"),
        Field("location_updated_at", "timestamptz"),
        Field("accountFK_id", "int8"),
    ],
    "accounts_workerprofile": [
        Field("id", "int8"),
        Field("description", "varchar"),
        Field("workerRating", "int4"),
        Field("totalEarningGross", "numeric"),
        Field("availability_status", "varchar"),
        Field("bio", "varchar"),
        Field("hourly_rate", "numeric"),
        Field("daily_rate", "numeric"),
        Field("profile_completion_percentage", "int4"),
        Field("soft_skills", "text"),
        Field("is_available_daily_jobs", "bool"),
        Field("profileID_id", "int8"),
    ],
    "accounts_clientprofile": [
        Field("id", "int8"),
        Field("description", "varchar"),
        Field("totalJobsPosted", "int4"),
        Field("clientRating", "int4"),
        Field("activeJobsCount", "int4"),
        Field("profileID_id", "int8"),
    ],
    "accounts_agency": [
        Field("agencyId", "int8"),
        Field("businessName", "varchar"),
        Field("businessDesc", "varchar"),
        Field("contactNumber", "varchar"),
        Field("city", "varchar"),
        Field("country", "varchar"),
        Field("postal_code", "varchar"),
        Field("province", "varchar"),
        Field("street_address", "varchar"),
        Field("barangay", "varchar"),
        Field("createdAt", "timestamptz"),
        Field("accountFK_id", "int8"),
    ],
    "accounts_barangay": [
        Field("barangayID", "int4"),
        Field("name", "varchar"),
        Field("zipCode", "varchar"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("city_id", "int4"),
    ],
    "accounts_city": [
        Field("cityID", "int4"),
        Field("name", "varchar"),
        Field("province", "varchar"),
        Field("region", "varchar"),
        Field("zipCode", "varchar"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
    ],
    "specializations": [
        Field("specializationID", "int8"),
        Field("specializationName", "varchar"),
        Field("averageProjectCostMax", "numeric"),
        Field("averageProjectCostMin", "numeric"),
        Field("description", "text"),
        Field("minimumRate", "numeric"),
        Field("rateType", "varchar"),
        Field("skillLevel", "varchar"),
        Field("is_custom", "bool"),
        Field("created_by_agency_id", "int8"),
        Field("created_by_worker_id", "int8"),
    ],
    "accounts_workerspecialization": [
        Field("id", "int8"),
        Field("experienceYears", "int4"),
        Field("certification", "varchar"),
        Field("skillType", "varchar"),
        Field("displayOrder", "int4"),
        Field("workerID_id", "int8"),
        Field("specializationID_id", "int8"),
    ],
    "accounts_interestedjobs": [
        Field("id", "int8"),
        Field("clientID_id", "int8"),
        Field("specializationID_id", "int8"),
    ],
    "accounts_wallet": [
        Field("walletID", "int8"),
        Field("balance", "numeric"),
        Field("reservedBalance", "numeric"),
        Field("pendingEarnings", "numeric"),
        Field("autoWithdrawEnabled", "bool"),
        Field("lastAutoWithdrawAt", "timestamptz"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("accountFK_id", "int8"),
        Field("preferredPaymentMethodID_id", "int8 nullable"),
    ],
    "accounts_userpaymentmethod": [
        Field("id", "int8"),
        Field("methodType", "varchar"),
        Field("accountName", "varchar"),
        Field("accountNumber", "varchar"),
        Field("bankName", "varchar"),
        Field("bankCode", "varchar"),
        Field("isPrimary", "bool"),
        Field("isVerified", "bool"),
        Field("paymongoRecipientId", "varchar"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("accountFK_id", "int8"),
    ],
    "accounts_pushtoken": [
        Field("tokenID", "int8"),
        Field("pushToken", "varchar UNIQUE"),
        Field("deviceType", "varchar"),
        Field("isActive", "bool"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("lastUsed", "timestamptz"),
        Field("accountFK_id", "int8"),
    ],
    "accounts_notificationsettings": [
        Field("settingsID", "int8"),
        Field("pushEnabled", "bool"),
        Field("soundEnabled", "bool"),
        Field("jobUpdates", "bool"),
        Field("messages", "bool"),
        Field("payments", "bool"),
        Field("reviews", "bool"),
        Field("kycUpdates", "bool"),
        Field("doNotDisturbStart", "time"),
        Field("doNotDisturbEnd", "time"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("accountFK_id", "int8 UNIQUE"),
    ],
    "jobs": [
        Field("jobID", "int8"),
        Field("title", "varchar"),
        Field("description", "text"),
        Field("budget", "numeric"),
        Field("location", "varchar"),
        Field("expectedDuration", "varchar"),
        Field("urgency", "varchar"),
        Field("preferredStartDate", "date"),
        Field("materialsNeeded", "jsonb"),
        Field("status", "varchar"),
        Field("completedAt", "timestamptz"),
        Field("cancellationReason", "text"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("assignedWorkerID_id", "int8"),
        Field("categoryID_id", "int8"),
        Field("clientID_id", "int8"),
        Field("clientMarkedComplete", "bool"),
        Field("clientMarkedCompleteAt", "timestamptz"),
        Field("workerMarkedComplete", "bool"),
        Field("workerMarkedCompleteAt", "timestamptz"),
        Field("escrowAmount", "numeric"),
        Field("escrowPaid", "bool"),
        Field("escrowPaidAt", "timestamptz"),
        Field("remainingPayment", "numeric"),
        Field("remainingPaymentPaid", "bool"),
        Field("remainingPaymentPaidAt", "timestamptz"),
        Field("finalPaymentMethod", "varchar"),
        Field("cashPaymentProofUrl", "varchar"),
        Field("paymentMethodSelectedAt", "timestamptz"),
        Field("cashProofUploadedAt", "timestamptz"),
        Field("cashPaymentApproved", "bool"),
        Field("cashPaymentApprovedAt", "timestamptz"),
        Field("cashPaymentApprovedBy_id", "int8"),
        Field("assignedAgencyFK_id", "int8"),
        Field("jobType", "varchar"),
        Field("inviteRejectionReason", "text"),
        Field("inviteRespondedAt", "timestamptz"),
        Field("inviteStatus", "varchar"),
        Field("clientConfirmedWorkStarted", "bool"),
        Field("clientConfirmedWorkStartedAt", "timestamptz"),
        Field("assignedEmployeeID_id", "int8"),
        Field("assignmentNotes", "text"),
        Field("employeeAssignedAt", "timestamptz"),
        Field("is_team_job", "bool"),
        Field("budget_allocation_type", "varchar"),
        Field("team_job_start_threshold", "numeric"),
        Field("paymentReleaseDate", "timestamptz"),
        Field("paymentReleasedToWorker", "bool"),
        Field("paymentReleasedAt", "timestamptz"),
        Field("paymentHeldReason", "varchar"),
        Field("job_scope", "varchar"),
        Field("skill_level_required", "varchar"),
        Field("work_environment", "varchar"),
        Field("payment_model", "varchar"),
        Field("duration_days", "int4"),
        Field("daily_rate_agreed", "numeric"),
        Field("actual_start_date", "date"),
        Field("total_days_worked", "int4"),
        Field("daily_escrow_total", "numeric"),
        Field("materialsCost", "numeric"),
        Field("materials_status", "varchar"),
        Field("scheduled_end_date", "date"),
        Field("qa_day_offset", "int4"),
        Field("workerMarkedOnTheWay", "bool"),
        Field("workerMarkedOnTheWayAt", "timestamptz"),
        Field("workerMarkedJobStarted", "bool"),
        Field("workerMarkedJobStartedAt", "timestamptz"),
        Field("is_early_completed", "bool"),
        Field("early_completed_at", "timestamptz"),
        Field("early_completion_payout", "numeric"),
        Field("shift_type", "varchar"),
        Field("cancelledAt", "timestamptz"),
        Field("cancelledByRole", "varchar"),
        Field("cancelledByAccountID_id", "int8"),
        Field("cancellationStage", "varchar"),
        Field("clientRefundAmount", "numeric"),
        Field("workerCompensationAmount", "numeric"),
        Field("agency_flow_mode", "varchar"),
    ],
    "job_skill_slots": [
        Field("skillSlotID", "int8"),
        Field("workers_needed", "int4"),
        Field("budget_allocated", "numeric"),
        Field("skill_level_required", "varchar"),
        Field("status", "varchar"),
        Field("notes", "text"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("jobID_id", "int8"),
        Field("specializationID_id", "int8"),
        Field("invited_agency_id", "int8"),
        Field("agency_invite_status", "varchar"),
        Field("agency_invite_responded_at", "timestamptz"),
        Field("last_rejected_agency_id", "int8"),
        Field("last_rejected_agency_name", "varchar"),
        Field("last_rejected_at", "timestamptz"),
        Field("last_rejection_reason", "text"),
    ],
    "job_applications": [
        Field("applicationID", "int8"),
        Field("proposalMessage", "text"),
        Field("proposedBudget", "numeric"),
        Field("estimatedDuration", "varchar"),
        Field("budgetOption", "varchar"),
        Field("status", "varchar"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("jobID_id", "int8"),
        Field("workerID_id", "int8"),
        Field("applied_skill_slot_id", "int8"),
        Field("selected_materials", "jsonb"),
        Field("proposed_daily_rate", "numeric"),
        Field("proposed_days", "int4"),
        Field("negotiation_count", "int2"),
        Field("applied_shift", "varchar"),
        Field("clientRejectionReason", "text"),
    ],
    "price_negotiations": [
        Field("negotiationID", "int8"),
        Field("application_id", "int8"),
        Field("actor", "varchar"),
        Field("round_number", "int2"),
        Field("proposed_budget", "numeric"),
        Field("proposed_daily_rate", "numeric"),
        Field("proposed_days", "int4"),
        Field("message", "text"),
        Field("status", "varchar"),
        Field("createdAt", "timestamptz"),
    ],
    "job_worker_assignments": [
        Field("assignmentID", "int8"),
        Field("slot_position", "int4"),
        Field("assignment_status", "varchar"),
        Field("worker_marked_complete", "bool"),
        Field("worker_marked_complete_at", "timestamptz"),
        Field("completion_notes", "text"),
        Field("individual_rating", "numeric"),
        Field("assignedAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("jobID_id", "int8"),
        Field("skillSlotID_id", "int8"),
        Field("workerID_id", "int8"),
        Field("client_confirmed_arrival", "bool"),
        Field("client_confirmed_arrival_at", "timestamptz"),
        Field("daily_rate_at_assignment", "numeric"),
        Field("days_worked", "int4"),
        Field("total_earned", "numeric"),
        Field("early_completed", "bool"),
        Field("early_completed_at", "timestamptz"),
        Field("early_completion_payout", "numeric"),
        Field("assigned_shift", "varchar"),
    ],
    "job_employee_assignments": [
        Field("assignmentID", "int8"),
        Field("assignedAt", "timestamptz"),
        Field("notes", "text"),
        Field("isPrimaryContact", "bool"),
        Field("status", "varchar"),
        Field("employeeMarkedComplete", "bool"),
        Field("employeeMarkedCompleteAt", "timestamptz"),
        Field("completionNotes", "text"),
        Field("assignedBy_id", "int8"),
        Field("employee_id", "int8"),
        Field("job_id", "int8"),
        Field("skill_slot_id", "int8"),
        Field("dispatched", "bool"),
        Field("dispatchedAt", "timestamptz"),
        Field("clientConfirmedArrival", "bool"),
        Field("clientConfirmedArrivalAt", "timestamptz"),
        Field("agencyMarkedComplete", "bool"),
        Field("agencyMarkedCompleteAt", "timestamptz"),
        Field("paymentAmount", "numeric"),
        Field("clientApproved", "bool"),
        Field("clientApprovedAt", "timestamptz"),
        Field("early_completed", "bool"),
        Field("early_completed_at", "timestamptz"),
        Field("early_completion_payout", "numeric"),
    ],
    "job_logs": [
        Field("logID", "int8"),
        Field("oldStatus", "varchar"),
        Field("newStatus", "varchar"),
        Field("notes", "text"),
        Field("createdAt", "timestamptz"),
        Field("changedBy_id", "int8"),
        Field("jobID_id", "int8"),
        Field("actionType", "varchar"),
        Field("metadata", "jsonb"),
    ],
    "saved_jobs": [
        Field("savedJobID", "int8"),
        Field("savedAt", "timestamptz"),
        Field("jobID_id", "int8"),
        Field("workerID_id", "int8"),
    ],
    "job_disputes": [
        Field("disputeID", "int8"),
        Field("disputedBy", "varchar"),
        Field("reason", "varchar"),
        Field("description", "text"),
        Field("status", "varchar"),
        Field("priority", "varchar"),
        Field("jobAmount", "numeric"),
        Field("disputedAmount", "numeric"),
        Field("resolution", "text"),
        Field("resolvedDate", "timestamptz"),
        Field("assignedTo", "varchar"),
        Field("openedDate", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("jobID_id", "int8"),
        Field("backjobStarted", "bool"),
        Field("backjobStartedAt", "timestamptz"),
        Field("clientConfirmedBackjob", "bool"),
        Field("clientConfirmedBackjobAt", "timestamptz"),
        Field("workerMarkedBackjobComplete", "bool"),
        Field("workerMarkedBackjobCompleteAt", "timestamptz"),
        Field("termsAccepted", "bool"),
        Field("termsVersion", "varchar"),
        Field("termsAcceptedAt", "timestamptz"),
        Field("adminRejectedAt", "timestamptz"),
        Field("adminRejectionReason", "text"),
        Field("in_negotiation_at", "timestamptz"),
        Field("scheduled_date", "date"),
        Field("workerScheduleConfirmed", "bool"),
        Field("workerScheduleConfirmedAt", "timestamptz"),
    ],
    "dispute_evidence": [
        Field("evidenceID", "int8"),
        Field("imageURL", "varchar"),
        Field("description", "text"),
        Field("createdAt", "timestamptz"),
        Field("disputeID_id", "int8"),
        Field("uploadedBy_id", "int8"),
    ],
    "backjob_schedule_confirmations": [
        Field("confirmationID", "int8"),
        Field("confirmed", "bool"),
        Field("confirmedAt", "timestamptz"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("assignmentID_id", "int8"),
        Field("confirmedBy_id", "int8"),
        Field("disputeID_id", "int8"),
    ],
    "job_reviews": [
        Field("reviewID", "int8"),
        Field("reviewerType", "varchar"),
        Field("rating", "numeric"),
        Field("comment", "text"),
        Field("status", "varchar"),
        Field("isFlagged", "bool"),
        Field("flagReason", "text"),
        Field("flaggedAt", "timestamptz"),
        Field("helpfulCount", "int4"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("flaggedBy_id", "int8"),
        Field("jobID_id", "int8"),
        Field("revieweeID_id", "int8"),
        Field("reviewerID_id", "int8"),
        Field("revieweeAgencyID_id", "int8"),
        Field("revieweeEmployeeID_id", "int8"),
        Field("revieweeProfileID_id", "int8"),
        Field("rating_communication", "numeric"),
        Field("rating_professionalism", "numeric"),
        Field("rating_punctuality", "numeric"),
        Field("rating_quality", "numeric"),
        Field("agency_response", "text"),
        Field("agency_response_at", "timestamptz"),
        Field("backjob_edit_deadline", "timestamptz"),
    ],
    "review_skill_tags": [
        Field("tagID", "int8"),
        Field("createdAt", "timestamptz"),
        Field("reviewID_id", "int8"),
        Field("workerSpecializationID_id", "int8"),
    ],
    "job_materials": [
        Field("jobMaterialID", "int8"),
        Field("name", "varchar"),
        Field("description", "text"),
        Field("quantity", "int4"),
        Field("unit", "varchar"),
        Field("source", "varchar"),
        Field("purchase_price", "numeric"),
        Field("receipt_image_url", "varchar"),
        Field("client_approved", "bool"),
        Field("client_approved_at", "timestamptz"),
        Field("client_rejected", "bool"),
        Field("rejection_reason", "text"),
        Field("added_by", "varchar"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("jobID_id", "int8"),
        Field("workerMaterialID_id", "int8"),
    ],
    "job_photos": [
        Field("photoID", "int8"),
        Field("photoURL", "varchar"),
        Field("fileName", "varchar"),
        Field("uploadedAt", "timestamptz"),
        Field("jobID_id", "int8"),
    ],
    "daily_attendance": [
        Field("attendanceID", "int8"),
        Field("date", "date"),
        Field("time_in", "timestamptz"),
        Field("time_out", "timestamptz"),
        Field("status", "varchar"),
        Field("worker_confirmed", "bool"),
        Field("worker_confirmed_at", "timestamptz"),
        Field("client_confirmed", "bool"),
        Field("client_confirmed_at", "timestamptz"),
        Field("amount_earned", "numeric"),
        Field("payment_processed", "bool"),
        Field("payment_processed_at", "timestamptz"),
        Field("notes", "text"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("jobID_id", "int8"),
        Field("workerID_id", "int8"),
        Field("assignmentID_id", "int8"),
        Field("employeeID_id", "int8"),
        Field("absent_penalty_amount", "numeric"),
        Field("absent_penalty_applied", "bool"),
        Field("absent_penalty_applied_at", "timestamptz"),
        Field("absent_penalty_percent", "numeric"),
        Field("cash_payment_proof_url", "varchar"),
        Field("cash_payment_verified", "bool"),
        Field("cash_payment_verified_at", "timestamptz"),
        Field("cash_proof_uploaded_at", "timestamptz"),
        Field("payment_method", "varchar"),
    ],
    "daily_job_extensions": [
        Field("extensionID", "int8"),
        Field("additional_days", "int4"),
        Field("additional_escrow", "numeric"),
        Field("reason", "text"),
        Field("status", "varchar"),
        Field("requested_by", "varchar"),
        Field("client_approved", "bool"),
        Field("client_approved_at", "timestamptz"),
        Field("worker_approved", "bool"),
        Field("worker_approved_at", "timestamptz"),
        Field("escrow_collected", "bool"),
        Field("escrow_collected_at", "timestamptz"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("jobID_id", "int8"),
        Field("requestedByUser_id", "int8"),
    ],
    "daily_rate_changes": [
        Field("changeID", "int8"),
        Field("old_rate", "numeric"),
        Field("new_rate", "numeric"),
        Field("reason", "text"),
        Field("effective_date", "date"),
        Field("status", "varchar"),
        Field("requested_by", "varchar"),
        Field("client_approved", "bool"),
        Field("client_approved_at", "timestamptz"),
        Field("worker_approved", "bool"),
        Field("worker_approved_at", "timestamptz"),
        Field("escrow_adjusted", "bool"),
        Field("escrow_adjustment_amount", "numeric"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("jobID_id", "int8"),
        Field("requestedByUser_id", "int8"),
    ],
    "daily_skip_day_requests": [
        Field("skipRequestID", "int8"),
        Field("request_date", "date"),
        Field("status", "varchar"),
        Field("requested_by", "varchar"),
        Field("requested_account_ids", "jsonb"),
        Field("requested_count", "int4"),
        Field("total_required", "int4"),
        Field("requires_all_team_workers", "bool"),
        Field("all_workers_requested", "bool"),
        Field("reviewedAt", "timestamptz"),
        Field("client_rejection_reason", "text"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("jobID_id", "int8"),
        Field("requestedByUser_id", "int8"),
        Field("reviewedByUser_id", "int8"),
        Field("target_employee_id", "int8"),
        Field("target_type", "varchar"),
        Field("target_worker_account_id", "int8"),
    ],
    "accounts_kyc": [
        Field("kycID", "int8"),
        Field("kyc_status", "varchar"),
        Field("reviewedAt", "timestamptz"),
        Field("notes", "text"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("accountFK_id", "int8"),
        Field("reviewedBy_id", "int8"),
        Field("rejectionCategory", "varchar"),
        Field("rejectionReason", "text"),
        Field("resubmissionCount", "int4"),
        Field("maxResubmissions", "int4"),
    ],
    "accounts_kycfiles": [
        Field("kycFileID", "int8"),
        Field("idType", "varchar"),
        Field("fileURL", "varchar"),
        Field("fileName", "varchar"),
        Field("fileSize", "int4"),
        Field("uploadedAt", "timestamptz"),
        Field("kycID_id", "int8"),
        Field("ai_verification_status", "varchar"),
        Field("face_detected", "bool"),
        Field("face_count", "int4"),
        Field("face_confidence", "float8"),
        Field("ocr_text", "text"),
        Field("ocr_confidence", "float8"),
        Field("quality_score", "float8"),
        Field("ai_confidence_score", "float8"),
        Field("ai_rejection_reason", "varchar"),
        Field("ai_rejection_message", "varchar"),
        Field("ai_warnings", "jsonb"),
        Field("ai_details", "jsonb"),
        Field("verified_at", "timestamptz"),
    ],
    "kyc_extracted_data": [
        Field("extractedDataID", "int8"),
        Field("extracted_full_name", "varchar"),
        Field("extracted_first_name", "varchar"),
        Field("extracted_middle_name", "varchar"),
        Field("extracted_last_name", "varchar"),
        Field("extracted_birth_date", "date"),
        Field("extracted_address", "text"),
        Field("extracted_id_number", "varchar"),
        Field("extracted_id_type", "varchar"),
        Field("extracted_expiry_date", "date"),
        Field("extracted_nationality", "varchar"),
        Field("extracted_sex", "varchar"),
        Field("confidence_full_name", "float8"),
        Field("confidence_birth_date", "float8"),
        Field("confidence_address", "float8"),
        Field("confidence_id_number", "float8"),
        Field("overall_confidence", "float8"),
        Field("confirmed_full_name", "varchar"),
        Field("confirmed_first_name", "varchar"),
        Field("confirmed_middle_name", "varchar"),
        Field("confirmed_last_name", "varchar"),
        Field("confirmed_birth_date", "date"),
        Field("confirmed_address", "text"),
        Field("confirmed_id_number", "varchar"),
        Field("extraction_status", "varchar"),
        Field("extraction_source", "varchar"),
        Field("user_edited_fields", "jsonb"),
        Field("confirmed_at", "timestamptz"),
        Field("extracted_at", "timestamptz"),
        Field("raw_extraction_data", "jsonb"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("kycID_id", "int8 UNIQUE"),
        Field("extracted_place_of_birth", "varchar"),
        Field("extracted_clearance_number", "varchar"),
        Field("extracted_clearance_type", "varchar"),
        Field("extracted_clearance_issue_date", "date"),
        Field("extracted_clearance_validity_date", "date"),
        Field("confidence_place_of_birth", "float8"),
        Field("confidence_clearance_number", "float8"),
        Field("confirmed_nationality", "varchar"),
        Field("confirmed_sex", "varchar"),
        Field("confirmed_place_of_birth", "varchar"),
        Field("confirmed_clearance_number", "varchar"),
        Field("confirmed_clearance_type", "varchar"),
        Field("confirmed_clearance_issue_date", "date"),
        Field("confirmed_clearance_validity_date", "date"),
        Field("face_match_completed", "bool"),
        Field("face_match_score", "float8"),
    ],
    "agency_agencykyc": [
        Field("agencyKycID", "int8"),
        Field("status", "varchar"),
        Field("reviewedAt", "timestamptz"),
        Field("notes", "varchar"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("accountFK_id", "int8"),
        Field("reviewedBy_id", "int8"),
        Field("rejectionCategory", "varchar"),
        Field("rejectionReason", "text"),
        Field("resubmissionCount", "int4"),
        Field("maxResubmissions", "int4"),
        Field("face_similarity_score", "float8"),
    ],
    "agency_agencykycfile": [
        Field("fileID", "int8"),
        Field("fileType", "varchar"),
        Field("fileURL", "varchar"),
        Field("fileName", "varchar"),
        Field("fileSize", "int4"),
        Field("uploadedAt", "timestamptz"),
        Field("agencyKyc_id", "int8"),
        Field("ai_verification_status", "varchar"),
        Field("face_detected", "bool"),
        Field("face_count", "int4"),
        Field("face_confidence", "float8"),
        Field("ocr_text", "text"),
        Field("ocr_confidence", "float8"),
        Field("quality_score", "float8"),
        Field("ai_confidence_score", "float8"),
        Field("ai_rejection_reason", "varchar"),
        Field("ai_rejection_message", "varchar"),
        Field("ai_warnings", "jsonb"),
        Field("ai_details", "jsonb"),
        Field("verified_at", "timestamptz"),
    ],
    "agency_kyc_extracted_data": [
        Field("extractedDataID", "int8"),
        Field("extracted_business_name", "varchar"),
        Field("extracted_business_type", "varchar"),
        Field("extracted_business_address", "text"),
        Field("extracted_permit_number", "varchar"),
        Field("extracted_permit_issue_date", "date"),
        Field("extracted_permit_expiry_date", "date"),
        Field("extracted_dti_number", "varchar"),
        Field("extracted_sec_number", "varchar"),
        Field("extracted_tin", "varchar"),
        Field("extracted_rep_full_name", "varchar"),
        Field("extracted_rep_id_number", "varchar"),
        Field("extracted_rep_id_type", "varchar"),
        Field("extracted_rep_birth_date", "date"),
        Field("extracted_rep_address", "text"),
        Field("confirmed_business_name", "varchar"),
        Field("confirmed_business_type", "varchar"),
        Field("confirmed_business_address", "text"),
        Field("confirmed_permit_number", "varchar"),
        Field("confirmed_permit_issue_date", "date"),
        Field("confirmed_permit_expiry_date", "date"),
        Field("confirmed_dti_number", "varchar"),
        Field("confirmed_sec_number", "varchar"),
        Field("confirmed_tin", "varchar"),
        Field("confirmed_rep_full_name", "varchar"),
        Field("confirmed_rep_id_number", "varchar"),
        Field("confirmed_rep_birth_date", "date"),
        Field("confirmed_rep_address", "text"),
        Field("confidence_business_name", "float8"),
        Field("confidence_business_address", "float8"),
        Field("confidence_permit_number", "float8"),
        Field("confidence_rep_name", "float8"),
        Field("overall_confidence", "float8"),
        Field("extraction_status", "varchar"),
        Field("extraction_source", "varchar"),
        Field("extracted_at", "timestamptz"),
        Field("confirmed_at", "timestamptz"),
        Field("user_edited_fields", "jsonb"),
        Field("raw_extraction_data", "jsonb"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("agencyKyc_id", "int8 UNIQUE"),
    ],
    "adminpanel_kyclogs": [
        Field("kycLogID", "int8"),
        Field("action", "varchar"),
        Field("reviewedAt", "timestamptz"),
        Field("reason", "text"),
        Field("userEmail", "varchar"),
        Field("userAccountID", "int8"),
        Field("createdAt", "timestamptz"),
        Field("accountFK_id", "int8"),
        Field("kycID", "int8"),
        Field("reviewedBy_id", "int8"),
        Field("kycType", "varchar"),
    ],
    "adminpanel_adminaccount": [
        Field("adminID", "int8"),
        Field("role", "varchar"),
        Field("permissions", "jsonb"),
        Field("isActive", "bool"),
        Field("lastLogin", "timestamptz"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("accountFK_id", "int8 UNIQUE"),
    ],
    "adminpanel_auditlog": [
        Field("auditLogID", "int8"),
        Field("adminEmail", "varchar"),
        Field("action", "varchar"),
        Field("entityType", "varchar"),
        Field("entityID", "varchar"),
        Field("details", "jsonb"),
        Field("beforeValue", "jsonb"),
        Field("afterValue", "jsonb"),
        Field("ipAddress", "inet"),
        Field("userAgent", "text"),
        Field("createdAt", "timestamptz"),
        Field("adminFK_id", "int8"),
    ],
    "adminpanel_supportticket": [
        Field("ticketID", "int8"),
        Field("subject", "varchar"),
        Field("category", "varchar"),
        Field("priority", "varchar"),
        Field("status", "varchar"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("lastReplyAt", "timestamptz"),
        Field("resolvedAt", "timestamptz"),
        Field("assignedTo_id", "int8"),
        Field("userFK_id", "int8"),
        Field("agencyFK_id", "int8"),
        Field("ticketType", "varchar"),
        Field("platform", "varchar"),
        Field("deviceInfo", "text"),
        Field("appVersion", "varchar"),
    ],
    "adminpanel_supportticketreply": [
        Field("replyID", "int8"),
        Field("content", "text"),
        Field("isSystemMessage", "bool"),
        Field("attachmentURL", "varchar"),
        Field("createdAt", "timestamptz"),
        Field("senderFK_id", "int8"),
        Field("ticketFK_id", "int8"),
    ],
    "adminpanel_userreport": [
        Field("reportID", "int8"),
        Field("reportType", "varchar"),
        Field("reason", "varchar"),
        Field("description", "text"),
        Field("relatedContentID", "int8"),
        Field("status", "varchar"),
        Field("adminNotes", "text"),
        Field("actionTaken", "varchar"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("resolvedAt", "timestamptz"),
        Field("reportedUserFK_id", "int8"),
        Field("reporterFK_id", "int8"),
        Field("reviewedBy_id", "int8"),
    ],
    "adminpanel_platformsettings": [
        Field("settingsID", "int8"),
        Field("platformFeePercentage", "numeric"),
        Field("escrowHoldingDays", "int4"),
        Field("maxJobBudget", "numeric"),
        Field("minJobBudget", "numeric"),
        Field("workerVerificationRequired", "bool"),
        Field("autoApproveKYC", "bool"),
        Field("kycDocumentExpiryDays", "int4"),
        Field("maintenanceMode", "bool"),
        Field("sessionTimeoutMinutes", "int4"),
        Field("maxUploadSizeMB", "int4"),
        Field("lastUpdated", "timestamptz"),
        Field("updatedBy_id", "int8"),
        Field("kycAutoApproveMinConfidence", "numeric"),
        Field("kycFaceMatchMinSimilarity", "numeric"),
        Field("kycRequireUserConfirmation", "bool"),
    ],
    "adminpanel_cannedresponse": [
        Field("responseID", "int8"),
        Field("title", "varchar"),
        Field("content", "text"),
        Field("category", "varchar"),
        Field("shortcuts", "jsonb"),
        Field("usageCount", "int4"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("createdBy_id", "int8"),
    ],
    "adminpanel_contentmoderationterm": [
        Field("termID", "int8"),
        Field("term", "varchar"),
        Field("normalizedTerm", "varchar UNIQUE"),
        Field("isActive", "bool"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("createdBy_id", "int8"),
        Field("updatedBy_id", "int8"),
    ],
    "adminpanel_faq": [
        Field("faqID", "int8"),
        Field("question", "varchar"),
        Field("answer", "text"),
        Field("category", "varchar"),
        Field("sortOrder", "int4"),
        Field("viewCount", "int4"),
        Field("isPublished", "bool"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
    ],
    "adminpanel_systemroles": [
        Field("systemRoleID", "int8"),
        Field("systemRole", "varchar"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("accountID_id", "int8"),
    ],
    "accounts_notification": [
        Field("notificationID", "int8"),
        Field("notificationType", "varchar"),
        Field("title", "varchar"),
        Field("message", "text"),
        Field("isRead", "bool"),
        Field("relatedKYCLogID", "int8"),
        Field("createdAt", "timestamptz"),
        Field("readAt", "timestamptz"),
        Field("accountFK_id", "int8"),
        Field("relatedJobID", "int8"),
        Field("relatedApplicationID", "int8"),
        Field("profile_type", "varchar"),
    ],
    "conversation": [
        Field("conversationID", "int8"),
        Field("lastMessageText", "text"),
        Field("lastMessageTime", "timestamptz"),
        Field("unreadCountClient", "int4"),
        Field("unreadCountWorker", "int4"),
        Field("status", "varchar"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("client_id", "int8"),
        Field("lastMessageSender_id", "int8"),
        Field("relatedJobPosting_id", "int8"),
        Field("worker_id", "int8"),
        Field("archivedByClient", "bool"),
        Field("archivedByWorker", "bool"),
        Field("agency_id", "int8"),
        Field("conversation_type", "varchar"),
    ],
    "conversation_participants": [
        Field("participantID", "int8"),
        Field("participant_type", "varchar"),
        Field("unread_count", "int4"),
        Field("is_archived", "bool"),
        Field("joined_at", "timestamptz"),
        Field("last_read_at", "timestamptz"),
        Field("conversation_id", "int8"),
        Field("profile_id", "int8"),
        Field("skill_slot_id", "int8"),
        Field("admin_account_id", "int8"),
    ],
    "message": [
        Field("messageID", "int8"),
        Field("messageText", "text"),
        Field("messageType", "varchar"),
        Field("locationAddress", "varchar"),
        Field("locationLandmark", "varchar"),
        Field("locationLatitude", "numeric"),
        Field("locationLongitude", "numeric"),
        Field("isRead", "bool"),
        Field("readAt", "timestamptz"),
        Field("createdAt", "timestamptz"),
        Field("conversationID_id", "int8"),
        Field("sender_id", "int8"),
        Field("senderAgency_id", "int8"),
        Field("sender_admin_id", "int8"),
    ],
    "message_attachment": [
        Field("attachmentID", "int8"),
        Field("fileURL", "varchar"),
        Field("fileName", "varchar"),
        Field("fileSize", "int4"),
        Field("fileType", "varchar"),
        Field("uploadedAt", "timestamptz"),
        Field("messageID_id", "int8"),
    ],
    "accounts_transaction": [
        Field("transactionID", "int8"),
        Field("transactionType", "varchar"),
        Field("amount", "numeric"),
        Field("balanceAfter", "numeric"),
        Field("status", "varchar"),
        Field("description", "varchar"),
        Field("referenceNumber", "varchar"),
        Field("paymentMethod", "varchar"),
        Field("createdAt", "timestamptz"),
        Field("completedAt", "timestamptz"),
        Field("relatedJobPosting_id", "int8"),
        Field("walletID_id", "int8"),
        Field("invoiceURL", "varchar"),
        Field("xenditExternalID", "varchar"),
        Field("xenditInvoiceID", "varchar UNIQUE"),
        Field("xenditPaymentChannel", "varchar"),
        Field("xenditPaymentID", "varchar"),
        Field("xenditPaymentMethod", "varchar"),
        Field("adminReferenceNumber", "varchar"),
        Field("processedAt", "timestamptz"),
        Field("processedByAdmin_id", "int8"),
        Field("paymongoPaymentId", "varchar"),
        Field("paymongoTransferId", "varchar"),
        Field("paymongoTransferStatus", "varchar"),
    ],
    "agency_employees": [
        Field("employeeID", "int8"),
        Field("name", "varchar"),
        Field("email", "varchar"),
        Field("role", "varchar"),
        Field("avatar", "varchar"),
        Field("rating", "numeric"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("agency_id", "int8"),
        Field("employeeOfTheMonth", "bool"),
        Field("employeeOfTheMonthDate", "timestamptz"),
        Field("employeeOfTheMonthReason", "text"),
        Field("isActive", "bool"),
        Field("lastRatingUpdate", "timestamptz"),
        Field("totalEarnings", "numeric"),
        Field("totalJobsCompleted", "int4"),
        Field("firstName", "varchar"),
        Field("middleName", "varchar"),
        Field("lastName", "varchar"),
        Field("specializations", "text"),
        Field("daily_rate", "numeric"),
        Field("hourly_rate", "numeric"),
        Field("is_available_daily_jobs", "bool"),
        Field("mobile", "varchar"),
    ],
    "worker_certifications": [
        Field("certificationID", "int8"),
        Field("name", "varchar"),
        Field("issuing_organization", "varchar"),
        Field("issue_date", "date"),
        Field("expiry_date", "date"),
        Field("certificate_url", "varchar"),
        Field("is_verified", "bool"),
        Field("verified_at", "timestamptz"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("verified_by_id", "int8"),
        Field("workerID_id", "int8"),
        Field("specializationID_id", "int8"),
    ],
    "certification_logs": [
        Field("certLogID", "int8"),
        Field("certificationID", "int8"),
        Field("action", "varchar"),
        Field("reviewedAt", "timestamptz"),
        Field("reason", "text"),
        Field("workerEmail", "varchar"),
        Field("workerAccountID", "int8"),
        Field("certificationName", "varchar"),
        Field("reviewedBy_id", "int8"),
        Field("workerID_id", "int8"),
    ],
    "worker_materials": [
        Field("materialID", "int8"),
        Field("name", "varchar"),
        Field("description", "text"),
        Field("price", "numeric"),
        Field("unit", "varchar"),
        Field("image_url", "varchar"),
        Field("is_available", "bool"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("workerID_id", "int8"),
        Field("quantity", "numeric"),
        Field("categoryID_id", "int8"),
        Field("agencyID_id", "int8"),
    ],
    "worker_portfolio": [
        Field("portfolioID", "int8"),
        Field("image_url", "varchar"),
        Field("caption", "text"),
        Field("display_order", "int4"),
        Field("file_name", "varchar"),
        Field("file_size", "int4"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("workerID_id", "int8"),
    ],
    "profiles_workerproduct": [
        Field("productID", "int8"),
        Field("productName", "varchar"),
        Field("description", "text"),
        Field("price", "numeric"),
        Field("priceUnit", "varchar"),
        Field("inStock", "bool"),
        Field("stockQuantity", "int4"),
        Field("productImage", "varchar"),
        Field("isActive", "bool"),
        Field("createdAt", "timestamptz"),
        Field("updatedAt", "timestamptz"),
        Field("categoryID_id", "int8"),
        Field("workerID_id", "int8"),
    ],
}


PKS = {
    table: fields[0].name
    for table, fields in FIELDS.items()
}


ALL_FKS: List[FK] = [
    FK("accounts_profile", "accountFK_id", "accounts_accounts"),
    FK("accounts_workerprofile", "profileID_id", "accounts_profile"),
    FK("accounts_clientprofile", "profileID_id", "accounts_profile"),
    FK("accounts_agency", "accountFK_id", "accounts_accounts"),
    FK("accounts_barangay", "city_id", "accounts_city"),
    FK("accounts_workerspecialization", "workerID_id", "accounts_workerprofile"),
    FK("accounts_workerspecialization", "specializationID_id", "specializations"),
    FK("accounts_interestedjobs", "clientID_id", "accounts_clientprofile"),
    FK("accounts_interestedjobs", "specializationID_id", "specializations"),
    FK("accounts_wallet", "accountFK_id", "accounts_accounts"),
    FK("accounts_wallet", "preferredPaymentMethodID_id", "accounts_userpaymentmethod"),
    FK("accounts_userpaymentmethod", "accountFK_id", "accounts_accounts"),
    FK("accounts_pushtoken", "accountFK_id", "accounts_accounts"),
    FK("accounts_notificationsettings", "accountFK_id", "accounts_accounts"),
    FK("specializations", "created_by_agency_id", "accounts_agency"),
    FK("specializations", "created_by_worker_id", "accounts_accounts"),
    FK("jobs", "clientID_id", "accounts_clientprofile"),
    FK("jobs", "assignedWorkerID_id", "accounts_workerprofile"),
    FK("jobs", "assignedAgencyFK_id", "accounts_agency"),
    FK("jobs", "assignedEmployeeID_id", "agency_employees"),
    FK("jobs", "categoryID_id", "specializations"),
    FK("jobs", "cancelledByAccountID_id", "accounts_accounts"),
    FK("jobs", "cashPaymentApprovedBy_id", "accounts_accounts"),
    FK("job_skill_slots", "jobID_id", "jobs"),
    FK("job_skill_slots", "specializationID_id", "specializations"),
    FK("job_skill_slots", "invited_agency_id", "accounts_agency"),
    FK("job_applications", "jobID_id", "jobs"),
    FK("job_applications", "workerID_id", "accounts_workerprofile"),
    FK("job_applications", "applied_skill_slot_id", "job_skill_slots"),
    FK("price_negotiations", "application_id", "job_applications"),
    FK("job_worker_assignments", "jobID_id", "jobs"),
    FK("job_worker_assignments", "skillSlotID_id", "job_skill_slots"),
    FK("job_worker_assignments", "workerID_id", "accounts_workerprofile"),
    FK("job_employee_assignments", "job_id", "jobs"),
    FK("job_employee_assignments", "employee_id", "agency_employees"),
    FK("job_employee_assignments", "skill_slot_id", "job_skill_slots"),
    FK("job_employee_assignments", "assignedBy_id", "accounts_accounts"),
    FK("job_logs", "jobID_id", "jobs"),
    FK("job_logs", "changedBy_id", "accounts_accounts"),
    FK("saved_jobs", "jobID_id", "jobs"),
    FK("saved_jobs", "workerID_id", "accounts_workerprofile"),
    FK("job_disputes", "jobID_id", "jobs"),
    FK("dispute_evidence", "disputeID_id", "job_disputes"),
    FK("dispute_evidence", "uploadedBy_id", "accounts_accounts"),
    FK("backjob_schedule_confirmations", "disputeID_id", "job_disputes"),
    FK("backjob_schedule_confirmations", "assignmentID_id", "job_worker_assignments"),
    FK("backjob_schedule_confirmations", "confirmedBy_id", "accounts_accounts"),
    FK("job_reviews", "jobID_id", "jobs"),
    FK("job_reviews", "reviewerID_id", "accounts_accounts"),
    FK("job_reviews", "revieweeID_id", "accounts_accounts"),
    FK("job_reviews", "revieweeProfileID_id", "accounts_profile"),
    FK("job_reviews", "revieweeAgencyID_id", "accounts_agency"),
    FK("job_reviews", "revieweeEmployeeID_id", "agency_employees"),
    FK("job_reviews", "flaggedBy_id", "accounts_accounts"),
    FK("review_skill_tags", "reviewID_id", "job_reviews"),
    FK("review_skill_tags", "workerSpecializationID_id", "accounts_workerspecialization"),
    FK("job_materials", "jobID_id", "jobs"),
    FK("job_materials", "workerMaterialID_id", "worker_materials"),
    FK("job_photos", "jobID_id", "jobs"),
    FK("daily_attendance", "jobID_id", "jobs"),
    FK("daily_attendance", "workerID_id", "accounts_workerprofile"),
    FK("daily_attendance", "assignmentID_id", "job_worker_assignments"),
    FK("daily_attendance", "employeeID_id", "agency_employees"),
    FK("daily_job_extensions", "jobID_id", "jobs"),
    FK("daily_job_extensions", "requestedByUser_id", "accounts_accounts"),
    FK("daily_rate_changes", "jobID_id", "jobs"),
    FK("daily_rate_changes", "requestedByUser_id", "accounts_accounts"),
    FK("daily_skip_day_requests", "jobID_id", "jobs"),
    FK("daily_skip_day_requests", "requestedByUser_id", "accounts_accounts"),
    FK("daily_skip_day_requests", "reviewedByUser_id", "accounts_accounts"),
    FK("daily_skip_day_requests", "target_employee_id", "agency_employees"),
    FK("daily_skip_day_requests", "target_worker_account_id", "accounts_accounts"),
    FK("accounts_kyc", "accountFK_id", "accounts_accounts"),
    FK("accounts_kyc", "reviewedBy_id", "accounts_accounts"),
    FK("accounts_kycfiles", "kycID_id", "accounts_kyc"),
    FK("kyc_extracted_data", "kycID_id", "accounts_kyc"),
    FK("agency_agencykyc", "accountFK_id", "accounts_accounts"),
    FK("agency_agencykyc", "reviewedBy_id", "accounts_accounts"),
    FK("agency_agencykycfile", "agencyKyc_id", "agency_agencykyc"),
    FK("agency_kyc_extracted_data", "agencyKyc_id", "agency_agencykyc"),
    FK("adminpanel_kyclogs", "accountFK_id", "accounts_accounts"),
    FK("adminpanel_kyclogs", "reviewedBy_id", "accounts_accounts"),
    FK("adminpanel_adminaccount", "accountFK_id", "accounts_accounts"),
    FK("adminpanel_auditlog", "adminFK_id", "accounts_accounts"),
    FK("adminpanel_supportticket", "userFK_id", "accounts_accounts"),
    FK("adminpanel_supportticket", "assignedTo_id", "accounts_accounts"),
    FK("adminpanel_supportticket", "agencyFK_id", "accounts_agency"),
    FK("adminpanel_supportticketreply", "ticketFK_id", "adminpanel_supportticket"),
    FK("adminpanel_supportticketreply", "senderFK_id", "accounts_accounts"),
    FK("adminpanel_userreport", "reporterFK_id", "accounts_accounts"),
    FK("adminpanel_userreport", "reportedUserFK_id", "accounts_accounts"),
    FK("adminpanel_userreport", "reviewedBy_id", "accounts_accounts"),
    FK("adminpanel_platformsettings", "updatedBy_id", "accounts_accounts"),
    FK("adminpanel_cannedresponse", "createdBy_id", "accounts_accounts"),
    FK("adminpanel_contentmoderationterm", "createdBy_id", "accounts_accounts"),
    FK("adminpanel_contentmoderationterm", "updatedBy_id", "accounts_accounts"),
    FK("adminpanel_systemroles", "accountID_id", "accounts_accounts"),
    FK("accounts_notification", "accountFK_id", "accounts_accounts"),
    FK("conversation", "client_id", "accounts_profile"),
    FK("conversation", "worker_id", "accounts_profile"),
    FK("conversation", "agency_id", "accounts_agency"),
    FK("conversation", "relatedJobPosting_id", "jobs"),
    FK("conversation", "lastMessageSender_id", "accounts_profile"),
    FK("conversation_participants", "conversation_id", "conversation"),
    FK("conversation_participants", "profile_id", "accounts_profile"),
    FK("conversation_participants", "skill_slot_id", "job_skill_slots"),
    FK("conversation_participants", "admin_account_id", "accounts_accounts"),
    FK("message", "conversationID_id", "conversation"),
    FK("message", "sender_id", "accounts_profile"),
    FK("message", "senderAgency_id", "accounts_agency"),
    FK("message", "sender_admin_id", "accounts_accounts"),
    FK("message_attachment", "messageID_id", "message"),
    FK("accounts_transaction", "walletID_id", "accounts_wallet"),
    FK("accounts_transaction", "relatedJobPosting_id", "jobs"),
    FK("accounts_transaction", "processedByAdmin_id", "accounts_accounts"),
    FK("agency_employees", "agency_id", "accounts_accounts"),
    FK("worker_certifications", "workerID_id", "accounts_workerprofile"),
    FK("worker_certifications", "specializationID_id", "accounts_workerspecialization"),
    FK("worker_certifications", "verified_by_id", "accounts_accounts"),
    FK("certification_logs", "workerID_id", "accounts_workerprofile"),
    FK("certification_logs", "reviewedBy_id", "accounts_accounts"),
    FK("worker_materials", "workerID_id", "accounts_workerprofile"),
    FK("worker_materials", "agencyID_id", "accounts_agency"),
    FK("worker_materials", "categoryID_id", "specializations"),
    FK("worker_portfolio", "workerID_id", "accounts_workerprofile"),
    FK("profiles_workerproduct", "workerID_id", "accounts_workerprofile"),
    FK("profiles_workerproduct", "categoryID_id", "specializations"),
]


MODULES = {
    "module2": {
        "title": "Module 2 - Profiles, Location, Wallet & Specializations",
        "filename": "erd_v2_module2_profiles.png",
        "tables": [
            "accounts_profile",
            "accounts_workerprofile",
            "accounts_clientprofile",
            "accounts_agency",
            "accounts_barangay",
            "accounts_city",
            "specializations",
            "accounts_workerspecialization",
            "accounts_interestedjobs",
            "accounts_wallet",
            "accounts_userpaymentmethod",
            "accounts_pushtoken",
            "accounts_notificationsettings",
        ],
        "cols": 4,
    },
    "module3": {
        "title": "Module 3 - Jobs, Applications & Assignments",
        "filename": "erd_v2_module3_jobs.png",
        "tables": [
            "jobs",
            "job_skill_slots",
            "job_applications",
            "price_negotiations",
            "job_worker_assignments",
            "job_employee_assignments",
            "job_logs",
            "saved_jobs",
        ],
        "cols": 3,
    },
    "module4": {
        "title": "Module 4 - Disputes, Reviews, Daily Operations & Attendance",
        "filename": "erd_v2_module4_disputes.png",
        "tables": [
            "job_disputes",
            "dispute_evidence",
            "backjob_schedule_confirmations",
            "job_reviews",
            "review_skill_tags",
            "job_materials",
            "job_photos",
            "daily_attendance",
            "daily_job_extensions",
            "daily_rate_changes",
            "daily_skip_day_requests",
        ],
        "cols": 4,
    },
    "module5": {
        "title": "Module 5 - KYC Verification (Individual & Agency)",
        "filename": "erd_v2_module5_kyc.png",
        "tables": [
            "accounts_kyc",
            "accounts_kycfiles",
            "kyc_extracted_data",
            "agency_agencykyc",
            "agency_agencykycfile",
            "agency_kyc_extracted_data",
            "adminpanel_kyclogs",
        ],
        "cols": 3,
    },
    "module6": {
        "title": "Module 6 - Admin Panel, Messaging, Notifications & Worker Assets",
        "filename": "erd_v2_module6_admin.png",
        "tables": [
            "adminpanel_adminaccount",
            "adminpanel_auditlog",
            "adminpanel_supportticket",
            "adminpanel_supportticketreply",
            "adminpanel_userreport",
            "adminpanel_platformsettings",
            "adminpanel_cannedresponse",
            "adminpanel_contentmoderationterm",
            "adminpanel_faq",
            "adminpanel_systemroles",
            "accounts_notification",
            "conversation",
            "conversation_participants",
            "message",
            "message_attachment",
            "accounts_transaction",
            "agency_employees",
            "worker_certifications",
            "certification_logs",
            "worker_materials",
            "worker_portfolio",
            "profiles_workerproduct",
        ],
        "cols": 5,
    },
}


def table_size(table: str, width: int = 470) -> Tuple[int, int]:
    return width, 36 + 24 * len(FIELDS[table])


def layout_tables(tables: List[str], cols: int) -> Tuple[Dict[str, Tuple[int, int, int, int]], int, int]:
    margin_x, margin_y = 70, 130
    gap_x, gap_y = 95, 80
    width = 470
    col_heights = [margin_y] * cols
    positions: Dict[str, Tuple[int, int, int, int]] = {}
    for i, table in enumerate(tables):
        col = i % cols
        x = margin_x + col * (width + gap_x)
        y = col_heights[col]
        w, h = table_size(table, width)
        positions[table] = (x, y, x + w, y + h)
        col_heights[col] = y + h + gap_y
    canvas_w = margin_x * 2 + cols * width + (cols - 1) * gap_x
    canvas_h = max(col_heights) + 50
    return positions, canvas_w, canvas_h


def fks_for(tables: Iterable[str]) -> List[FK]:
    table_set = set(tables)
    return [fk for fk in ALL_FKS if fk.table in table_set]


def fk_target(table: str, field: str) -> Optional[str]:
    for fk in ALL_FKS:
        if fk.table == table and fk.field == field:
            return fk.target
    return None


def draw_key(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    draw.ellipse((x, y + 3, x + 10, y + 13), outline=KEY_GOLD, width=2)
    draw.line((x + 10, y + 8, x + 23, y + 8), fill=KEY_GOLD, width=2)
    draw.line((x + 18, y + 8, x + 18, y + 13), fill=KEY_GOLD, width=2)
    draw.line((x + 22, y + 8, x + 22, y + 12), fill=KEY_GOLD, width=2)


def draw_crow_foot(draw: ImageDraw.ImageDraw, x: int, y: int, side: str) -> None:
    size = 13
    if side == "left":
        draw.line((x, y, x - size, y - size), fill=LINE, width=2)
        draw.line((x, y, x - size, y), fill=LINE, width=2)
        draw.line((x, y, x - size, y + size), fill=LINE, width=2)
    elif side == "right":
        draw.line((x, y, x + size, y - size), fill=LINE, width=2)
        draw.line((x, y, x + size, y), fill=LINE, width=2)
        draw.line((x, y, x + size, y + size), fill=LINE, width=2)
    elif side == "top":
        draw.line((x, y, x - size, y - size), fill=LINE, width=2)
        draw.line((x, y, x, y - size), fill=LINE, width=2)
        draw.line((x, y, x + size, y - size), fill=LINE, width=2)
    else:
        draw.line((x, y, x - size, y + size), fill=LINE, width=2)
        draw.line((x, y, x, y + size), fill=LINE, width=2)
        draw.line((x, y, x + size, y + size), fill=LINE, width=2)


def side_point(box: Tuple[int, int, int, int], target: Tuple[int, int, int, int]) -> Tuple[int, int, str]:
    x1, y1, x2, y2 = box
    tx1, ty1, tx2, ty2 = target
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    tcx, tcy = (tx1 + tx2) // 2, (ty1 + ty2) // 2
    dx, dy = tcx - cx, tcy - cy
    if abs(dx) >= abs(dy):
        return (x2, cy, "right") if dx > 0 else (x1, cy, "left")
    return (cx, y2, "bottom") if dy > 0 else (cx, y1, "top")


def draw_relationships(draw: ImageDraw.ImageDraw, positions: Dict[str, Tuple[int, int, int, int]], tables: List[str]) -> None:
    for idx, fk in enumerate(fks_for(tables)):
        if fk.target not in positions:
            continue
        child = positions[fk.table]
        parent = positions[fk.target]
        sx, sy, sside = side_point(child, parent)
        ex, ey, eside = side_point(parent, child)
        color = LINE
        offset = (idx % 7 - 3) * 4
        if sside in ("left", "right"):
            sy += offset
            ey += offset
        else:
            sx += offset
            ex += offset
        midx = (sx + ex) // 2
        midy = (sy + ey) // 2
        draw.line((sx, sy, midx, sy, midx, ey, ex, ey), fill=color, width=2)
        draw_crow_foot(draw, sx, sy, sside)
        if eside in ("left", "right"):
            draw.line((ex, ey - 11, ex, ey + 11), fill=color, width=2)
        else:
            draw.line((ex - 11, ey, ex + 11, ey), fill=color, width=2)
        label = f"{fk.field} \u2192 {fk.target}"
        bbox = draw.textbbox((0, 0), label, font=FONT_LABEL)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        lx, ly = midx + 4, midy - th - 4
        draw.rectangle((lx - 3, ly - 2, lx + tw + 3, ly + th + 3), fill=BG, outline="#e2e8f0")
        draw.text((lx, ly), label, fill="#475569", font=FONT_LABEL)


def draw_table(draw: ImageDraw.ImageDraw, table: str, box: Tuple[int, int, int, int], header_color: str) -> None:
    x1, y1, x2, y2 = box
    width = x2 - x1
    draw.rectangle(box, fill=ROW, outline=GRID, width=2)
    draw.rectangle((x1, y1, x2, y1 + 36), fill=header_color, outline=header_color)
    draw.text((x1 + 12, y1 + 8), table, fill="white", font=FONT_HEADER)
    y = y1 + 36
    pk = PKS[table]
    for idx, field in enumerate(FIELDS[table]):
        fill = ROW_ALT if idx % 2 else ROW
        draw.rectangle((x1, y, x2, y + 24), fill=fill, outline=GRID)
        target = fk_target(table, field.name)
        is_pk = field.name == pk
        name_x = x1 + 12
        if is_pk:
            draw_key(draw, name_x, y + 4)
            draw.text((name_x + 30, y + 4), "PK", fill=KEY_GOLD, font=FONT_CELL_BOLD)
            name_x += 58
        row_font = FONT_CELL_ITALIC if target else FONT_CELL_BOLD if is_pk else FONT_CELL
        row_color = FK_BLUE if target else TEXT
        text = f"{field.name} | {field.dtype}"
        if target:
            text += f"  \u2192 {target}"
        draw.text((name_x, y + 4), text, fill=row_color, font=row_font)
        y += 24
    draw.line((x1 + width // 2, y1 + 36, x1 + width // 2, y2), fill="#e5e7eb", width=1)


def render_module(module_key: str) -> None:
    module = MODULES[module_key]
    tables: List[str] = module["tables"]
    positions, canvas_w, canvas_h = layout_tables(tables, module["cols"])
    img = Image.new("RGB", (canvas_w, canvas_h), BG)
    draw = ImageDraw.Draw(img)
    draw.text((70, 35), module["title"], fill=TITLE, font=FONT_TITLE)
    note = f"Table count: {len(tables)} | PK = gold key, FK = blue italic with target table"
    draw.text((72, 84), note, fill=NOTE, font=FONT_NOTE)
    draw_relationships(draw, positions, tables)
    for idx, table in enumerate(tables):
        draw_table(draw, table, positions[table], HEADER if idx % 2 == 0 else HEADER_ALT)
    out = OUT / module["filename"]
    img.save(out, optimize=True)
    print(f"Wrote {out} ({canvas_w}x{canvas_h})")


def validate() -> None:
    for key, module in MODULES.items():
        tables = module["tables"]
        missing_tables = [t for t in tables if t not in FIELDS]
        if missing_tables:
            raise ValueError(f"{key} missing field definitions: {missing_tables}")
        for fk in fks_for(tables):
            names = {field.name for field in FIELDS[fk.table]}
            if fk.field not in names:
                raise ValueError(f"{key}: missing FK field {fk.table}.{fk.field}")


def main() -> None:
    validate()
    for module_key in ["module2", "module3", "module4", "module5", "module6"]:
        render_module(module_key)


if __name__ == "__main__":
    main()
