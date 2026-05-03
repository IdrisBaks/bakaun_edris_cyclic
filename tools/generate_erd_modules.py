#!/usr/bin/env python3
"""Generate corrected PostgreSQL ERD PNGs for modules 2-6.

The diagrams are rendered directly from the audited schema metadata below so
field lists and FK targets remain deterministic and easy to review.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


OUT_DIR = Path("docs/erd")
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
FONT_REG = FONT_DIR / "DejaVuSans.ttf"
FONT_BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"
FONT_MONO = FONT_DIR / "DejaVuSansMono.ttf"
FONT_MONO_BOLD = FONT_DIR / "DejaVuSansMono-Bold.ttf"
FONT_MONO_ITALIC = FONT_DIR / "DejaVuSansMono-Oblique.ttf"

BG = (255, 255, 255, 255)
TEXT = (29, 39, 52, 255)
MUTED = (88, 100, 118, 255)
ROW_ALT = (247, 249, 252, 255)
ROW_WHITE = (255, 255, 255, 255)
GRID = (210, 218, 229, 255)
FK_BLUE = (32, 99, 185, 255)
PK_GOLD = (191, 137, 26, 255)
EXTERNAL_FILL = (245, 247, 250, 255)
EXTERNAL_BORDER = (148, 163, 184, 255)


@dataclass(frozen=True)
class Field:
    name: str
    dtype: str
    pk: bool = False
    fk: str | None = None
    unique: bool = False


def f(name: str, dtype: str, *, pk: bool = False, fk: str | None = None, unique: bool = False) -> Field:
    return Field(name, dtype, pk, fk, unique)


SCHEMA: dict[str, list[Field]] = {
    "accounts_profile": [
        f("profileID", "int8", pk=True),
        f("profileImg", "varchar"),
        f("firstName", "varchar"),
        f("lastName", "varchar"),
        f("middleName", "varchar"),
        f("contactNum", "varchar"),
        f("birthDate", "date"),
        f("profileType", "varchar"),
        f("latitude", "numeric"),
        f("longitude", "numeric"),
        f("location_sharing_enabled", "bool"),
        f("location_updated_at", "timestamptz"),
        f("accountFK_id", "int8", fk="accounts_accounts"),
    ],
    "accounts_workerprofile": [
        f("id", "int8", pk=True),
        f("description", "varchar"),
        f("workerRating", "int4"),
        f("totalEarningGross", "numeric"),
        f("availability_status", "varchar"),
        f("bio", "varchar"),
        f("hourly_rate", "numeric"),
        f("daily_rate", "numeric"),
        f("profile_completion_percentage", "int4"),
        f("soft_skills", "text"),
        f("is_available_daily_jobs", "bool"),
        f("profileID_id", "int8", fk="accounts_profile", unique=True),
    ],
    "accounts_clientprofile": [
        f("id", "int8", pk=True),
        f("description", "varchar"),
        f("totalJobsPosted", "int4"),
        f("clientRating", "int4"),
        f("activeJobsCount", "int4"),
        f("profileID_id", "int8", fk="accounts_profile", unique=True),
    ],
    "accounts_agency": [
        f("agencyId", "int8", pk=True),
        f("businessName", "varchar"),
        f("businessDesc", "varchar"),
        f("contactNumber", "varchar"),
        f("city", "varchar"),
        f("country", "varchar"),
        f("postal_code", "varchar"),
        f("province", "varchar"),
        f("street_address", "varchar"),
        f("barangay", "varchar"),
        f("createdAt", "timestamptz"),
        f("accountFK_id", "int8", fk="accounts_accounts"),
    ],
    "accounts_barangay": [
        f("barangayID", "int4", pk=True),
        f("name", "varchar"),
        f("zipCode", "varchar"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("city_id", "int4", fk="accounts_city"),
    ],
    "accounts_city": [
        f("cityID", "int4", pk=True),
        f("name", "varchar", unique=True),
        f("province", "varchar"),
        f("region", "varchar"),
        f("zipCode", "varchar"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
    ],
    "specializations": [
        f("specializationID", "int8", pk=True),
        f("specializationName", "varchar"),
        f("averageProjectCostMax", "numeric"),
        f("averageProjectCostMin", "numeric"),
        f("description", "text"),
        f("minimumRate", "numeric"),
        f("rateType", "varchar"),
        f("skillLevel", "varchar"),
        f("is_custom", "bool"),
        f("created_by_agency_id", "int8", fk="accounts_agency"),
        f("created_by_worker_id", "int8", fk="accounts_accounts"),
    ],
    "accounts_workerspecialization": [
        f("id", "int8", pk=True),
        f("experienceYears", "int4"),
        f("certification", "varchar"),
        f("skillType", "varchar"),
        f("displayOrder", "int4"),
        f("workerID_id", "int8", fk="accounts_workerprofile"),
        f("specializationID_id", "int8", fk="specializations"),
    ],
    "accounts_interestedjobs": [
        f("id", "int8", pk=True),
        f("clientID_id", "int8", fk="accounts_clientprofile"),
        f("specializationID_id", "int8", fk="specializations"),
    ],
    "accounts_wallet": [
        f("walletID", "int8", pk=True),
        f("balance", "numeric"),
        f("reservedBalance", "numeric"),
        f("pendingEarnings", "numeric"),
        f("autoWithdrawEnabled", "bool"),
        f("lastAutoWithdrawAt", "timestamptz"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("accountFK_id", "int8", fk="accounts_accounts", unique=True),
        f("preferredPaymentMethodID_id", "int8 nullable", fk="accounts_userpaymentmethod"),
    ],
    "accounts_userpaymentmethod": [
        f("id", "int8", pk=True),
        f("methodType", "varchar"),
        f("accountName", "varchar"),
        f("accountNumber", "varchar"),
        f("bankName", "varchar"),
        f("bankCode", "varchar"),
        f("isPrimary", "bool"),
        f("isVerified", "bool"),
        f("paymongoRecipientId", "varchar"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("accountFK_id", "int8", fk="accounts_accounts"),
    ],
    "accounts_pushtoken": [
        f("tokenID", "int8", pk=True),
        f("pushToken", "varchar", unique=True),
        f("deviceType", "varchar"),
        f("isActive", "bool"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("lastUsed", "timestamptz"),
        f("accountFK_id", "int8", fk="accounts_accounts"),
    ],
    "accounts_notificationsettings": [
        f("settingsID", "int8", pk=True),
        f("pushEnabled", "bool"),
        f("soundEnabled", "bool"),
        f("jobUpdates", "bool"),
        f("messages", "bool"),
        f("payments", "bool"),
        f("reviews", "bool"),
        f("kycUpdates", "bool"),
        f("doNotDisturbStart", "time"),
        f("doNotDisturbEnd", "time"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("accountFK_id", "int8", fk="accounts_accounts", unique=True),
    ],
    "jobs": [
        f("jobID", "int8", pk=True),
        f("title", "varchar"),
        f("description", "text"),
        f("budget", "numeric"),
        f("location", "varchar"),
        f("expectedDuration", "varchar"),
        f("urgency", "varchar"),
        f("preferredStartDate", "date"),
        f("materialsNeeded", "jsonb"),
        f("status", "varchar"),
        f("completedAt", "timestamptz"),
        f("cancellationReason", "text"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("assignedWorkerID_id", "int8", fk="accounts_workerprofile"),
        f("categoryID_id", "int8", fk="specializations"),
        f("clientID_id", "int8", fk="accounts_clientprofile"),
        f("clientMarkedComplete", "bool"),
        f("clientMarkedCompleteAt", "timestamptz"),
        f("workerMarkedComplete", "bool"),
        f("workerMarkedCompleteAt", "timestamptz"),
        f("escrowAmount", "numeric"),
        f("escrowPaid", "bool"),
        f("escrowPaidAt", "timestamptz"),
        f("remainingPayment", "numeric"),
        f("remainingPaymentPaid", "bool"),
        f("remainingPaymentPaidAt", "timestamptz"),
        f("finalPaymentMethod", "varchar"),
        f("cashPaymentProofUrl", "varchar"),
        f("paymentMethodSelectedAt", "timestamptz"),
        f("cashProofUploadedAt", "timestamptz"),
        f("cashPaymentApproved", "bool"),
        f("cashPaymentApprovedAt", "timestamptz"),
        f("cashPaymentApprovedBy_id", "int8", fk="accounts_accounts"),
        f("assignedAgencyFK_id", "int8", fk="accounts_agency"),
        f("jobType", "varchar"),
        f("inviteRejectionReason", "text"),
        f("inviteRespondedAt", "timestamptz"),
        f("inviteStatus", "varchar"),
        f("clientConfirmedWorkStarted", "bool"),
        f("clientConfirmedWorkStartedAt", "timestamptz"),
        f("assignedEmployeeID_id", "int8", fk="agency_employees"),
        f("assignmentNotes", "text"),
        f("employeeAssignedAt", "timestamptz"),
        f("is_team_job", "bool"),
        f("budget_allocation_type", "varchar"),
        f("team_job_start_threshold", "numeric"),
        f("paymentReleaseDate", "timestamptz"),
        f("paymentReleasedToWorker", "bool"),
        f("paymentReleasedAt", "timestamptz"),
        f("paymentHeldReason", "varchar"),
        f("job_scope", "varchar"),
        f("skill_level_required", "varchar"),
        f("work_environment", "varchar"),
        f("payment_model", "varchar"),
        f("duration_days", "int4"),
        f("daily_rate_agreed", "numeric"),
        f("actual_start_date", "date"),
        f("total_days_worked", "int4"),
        f("daily_escrow_total", "numeric"),
        f("materialsCost", "numeric"),
        f("materials_status", "varchar"),
        f("scheduled_end_date", "date"),
        f("qa_day_offset", "int4"),
        f("workerMarkedOnTheWay", "bool"),
        f("workerMarkedOnTheWayAt", "timestamptz"),
        f("workerMarkedJobStarted", "bool"),
        f("workerMarkedJobStartedAt", "timestamptz"),
        f("is_early_completed", "bool"),
        f("early_completed_at", "timestamptz"),
        f("early_completion_payout", "numeric"),
        f("shift_type", "varchar"),
        f("cancelledAt", "timestamptz"),
        f("cancelledByRole", "varchar"),
        f("cancelledByAccountID_id", "int8", fk="accounts_accounts"),
        f("cancellationStage", "varchar"),
        f("clientRefundAmount", "numeric"),
        f("workerCompensationAmount", "numeric"),
        f("agency_flow_mode", "varchar"),
    ],
    "job_skill_slots": [
        f("skillSlotID", "int8", pk=True),
        f("workers_needed", "int4"),
        f("budget_allocated", "numeric"),
        f("skill_level_required", "varchar"),
        f("status", "varchar"),
        f("notes", "text"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("jobID_id", "int8", fk="jobs"),
        f("specializationID_id", "int8", fk="specializations"),
        f("invited_agency_id", "int8", fk="accounts_agency"),
        f("agency_invite_status", "varchar"),
        f("agency_invite_responded_at", "timestamptz"),
        f("last_rejected_agency_id", "int8"),
        f("last_rejected_agency_name", "varchar"),
        f("last_rejected_at", "timestamptz"),
        f("last_rejection_reason", "text"),
    ],
    "job_applications": [
        f("applicationID", "int8", pk=True),
        f("proposalMessage", "text"),
        f("proposedBudget", "numeric"),
        f("estimatedDuration", "varchar"),
        f("budgetOption", "varchar"),
        f("status", "varchar"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("jobID_id", "int8", fk="jobs"),
        f("workerID_id", "int8", fk="accounts_workerprofile"),
        f("applied_skill_slot_id", "int8", fk="job_skill_slots"),
        f("selected_materials", "jsonb"),
        f("proposed_daily_rate", "numeric"),
        f("proposed_days", "int4"),
        f("negotiation_count", "int2"),
        f("applied_shift", "varchar"),
        f("clientRejectionReason", "text"),
    ],
    "price_negotiations": [
        f("negotiationID", "int8", pk=True),
        f("application_id", "int8", fk="job_applications"),
        f("actor", "varchar"),
        f("round_number", "int2"),
        f("proposed_budget", "numeric"),
        f("proposed_daily_rate", "numeric"),
        f("proposed_days", "int4"),
        f("message", "text"),
        f("status", "varchar"),
        f("createdAt", "timestamptz"),
    ],
    "job_worker_assignments": [
        f("assignmentID", "int8", pk=True),
        f("slot_position", "int4"),
        f("assignment_status", "varchar"),
        f("worker_marked_complete", "bool"),
        f("worker_marked_complete_at", "timestamptz"),
        f("completion_notes", "text"),
        f("individual_rating", "numeric"),
        f("assignedAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("jobID_id", "int8", fk="jobs"),
        f("skillSlotID_id", "int8", fk="job_skill_slots"),
        f("workerID_id", "int8", fk="accounts_workerprofile"),
        f("client_confirmed_arrival", "bool"),
        f("client_confirmed_arrival_at", "timestamptz"),
        f("daily_rate_at_assignment", "numeric"),
        f("days_worked", "int4"),
        f("total_earned", "numeric"),
        f("early_completed", "bool"),
        f("early_completed_at", "timestamptz"),
        f("early_completion_payout", "numeric"),
        f("assigned_shift", "varchar"),
    ],
    "job_employee_assignments": [
        f("assignmentID", "int8", pk=True),
        f("assignedAt", "timestamptz"),
        f("notes", "text"),
        f("isPrimaryContact", "bool"),
        f("status", "varchar"),
        f("employeeMarkedComplete", "bool"),
        f("employeeMarkedCompleteAt", "timestamptz"),
        f("completionNotes", "text"),
        f("assignedBy_id", "int8", fk="accounts_accounts"),
        f("employee_id", "int8", fk="agency_employees"),
        f("job_id", "int8", fk="jobs"),
        f("skill_slot_id", "int8", fk="job_skill_slots"),
        f("dispatched", "bool"),
        f("dispatchedAt", "timestamptz"),
        f("clientConfirmedArrival", "bool"),
        f("clientConfirmedArrivalAt", "timestamptz"),
        f("agencyMarkedComplete", "bool"),
        f("agencyMarkedCompleteAt", "timestamptz"),
        f("paymentAmount", "numeric"),
        f("clientApproved", "bool"),
        f("clientApprovedAt", "timestamptz"),
        f("early_completed", "bool"),
        f("early_completed_at", "timestamptz"),
        f("early_completion_payout", "numeric"),
    ],
    "job_logs": [
        f("logID", "int8", pk=True),
        f("oldStatus", "varchar"),
        f("newStatus", "varchar"),
        f("notes", "text"),
        f("createdAt", "timestamptz"),
        f("changedBy_id", "int8", fk="accounts_accounts"),
        f("jobID_id", "int8", fk="jobs"),
        f("actionType", "varchar"),
        f("metadata", "jsonb"),
    ],
    "saved_jobs": [
        f("savedJobID", "int8", pk=True),
        f("savedAt", "timestamptz"),
        f("jobID_id", "int8", fk="jobs"),
        f("workerID_id", "int8", fk="accounts_workerprofile"),
    ],
    "job_disputes": [
        f("disputeID", "int8", pk=True),
        f("disputedBy", "varchar"),
        f("reason", "varchar"),
        f("description", "text"),
        f("status", "varchar"),
        f("priority", "varchar"),
        f("jobAmount", "numeric"),
        f("disputedAmount", "numeric"),
        f("resolution", "text"),
        f("resolvedDate", "timestamptz"),
        f("assignedTo", "varchar"),
        f("openedDate", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("jobID_id", "int8", fk="jobs"),
        f("backjobStarted", "bool"),
        f("backjobStartedAt", "timestamptz"),
        f("clientConfirmedBackjob", "bool"),
        f("clientConfirmedBackjobAt", "timestamptz"),
        f("workerMarkedBackjobComplete", "bool"),
        f("workerMarkedBackjobCompleteAt", "timestamptz"),
        f("termsAccepted", "bool"),
        f("termsVersion", "varchar"),
        f("termsAcceptedAt", "timestamptz"),
        f("adminRejectedAt", "timestamptz"),
        f("adminRejectionReason", "text"),
        f("in_negotiation_at", "timestamptz"),
        f("scheduled_date", "date"),
        f("workerScheduleConfirmed", "bool"),
        f("workerScheduleConfirmedAt", "timestamptz"),
    ],
    "dispute_evidence": [
        f("evidenceID", "int8", pk=True),
        f("imageURL", "varchar"),
        f("description", "text"),
        f("createdAt", "timestamptz"),
        f("disputeID_id", "int8", fk="job_disputes"),
        f("uploadedBy_id", "int8", fk="accounts_accounts"),
    ],
    "backjob_schedule_confirmations": [
        f("confirmationID", "int8", pk=True),
        f("confirmed", "bool"),
        f("confirmedAt", "timestamptz"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("assignmentID_id", "int8", fk="job_worker_assignments"),
        f("confirmedBy_id", "int8", fk="accounts_accounts"),
        f("disputeID_id", "int8", fk="job_disputes"),
    ],
    "job_reviews": [
        f("reviewID", "int8", pk=True),
        f("reviewerType", "varchar"),
        f("rating", "numeric"),
        f("comment", "text"),
        f("status", "varchar"),
        f("isFlagged", "bool"),
        f("flagReason", "text"),
        f("flaggedAt", "timestamptz"),
        f("helpfulCount", "int4"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("flaggedBy_id", "int8", fk="accounts_accounts"),
        f("jobID_id", "int8", fk="jobs"),
        f("revieweeID_id", "int8", fk="accounts_accounts"),
        f("reviewerID_id", "int8", fk="accounts_accounts"),
        f("revieweeAgencyID_id", "int8", fk="accounts_agency"),
        f("revieweeEmployeeID_id", "int8", fk="agency_employees"),
        f("revieweeProfileID_id", "int8", fk="accounts_profile"),
        f("rating_communication", "numeric"),
        f("rating_professionalism", "numeric"),
        f("rating_punctuality", "numeric"),
        f("rating_quality", "numeric"),
        f("agency_response", "text"),
        f("agency_response_at", "timestamptz"),
        f("backjob_edit_deadline", "timestamptz"),
    ],
    "review_skill_tags": [
        f("tagID", "int8", pk=True),
        f("createdAt", "timestamptz"),
        f("reviewID_id", "int8", fk="job_reviews"),
        f("workerSpecializationID_id", "int8", fk="accounts_workerspecialization"),
    ],
    "job_materials": [
        f("jobMaterialID", "int8", pk=True),
        f("name", "varchar"),
        f("description", "text"),
        f("quantity", "int4"),
        f("unit", "varchar"),
        f("source", "varchar"),
        f("purchase_price", "numeric"),
        f("receipt_image_url", "varchar"),
        f("client_approved", "bool"),
        f("client_approved_at", "timestamptz"),
        f("client_rejected", "bool"),
        f("rejection_reason", "text"),
        f("added_by", "varchar"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("jobID_id", "int8", fk="jobs"),
        f("workerMaterialID_id", "int8", fk="worker_materials"),
    ],
    "job_photos": [
        f("photoID", "int8", pk=True),
        f("photoURL", "varchar"),
        f("fileName", "varchar"),
        f("uploadedAt", "timestamptz"),
        f("jobID_id", "int8", fk="jobs"),
    ],
    "daily_attendance": [
        f("attendanceID", "int8", pk=True),
        f("date", "date"),
        f("time_in", "timestamptz"),
        f("time_out", "timestamptz"),
        f("status", "varchar"),
        f("worker_confirmed", "bool"),
        f("worker_confirmed_at", "timestamptz"),
        f("client_confirmed", "bool"),
        f("client_confirmed_at", "timestamptz"),
        f("amount_earned", "numeric"),
        f("payment_processed", "bool"),
        f("payment_processed_at", "timestamptz"),
        f("notes", "text"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("jobID_id", "int8", fk="jobs"),
        f("workerID_id", "int8", fk="accounts_workerprofile"),
        f("assignmentID_id", "int8", fk="job_worker_assignments"),
        f("employeeID_id", "int8", fk="agency_employees"),
        f("absent_penalty_amount", "numeric"),
        f("absent_penalty_applied", "bool"),
        f("absent_penalty_applied_at", "timestamptz"),
        f("absent_penalty_percent", "numeric"),
        f("cash_payment_proof_url", "varchar"),
        f("cash_payment_verified", "bool"),
        f("cash_payment_verified_at", "timestamptz"),
        f("cash_proof_uploaded_at", "timestamptz"),
        f("payment_method", "varchar"),
    ],
    "daily_job_extensions": [
        f("extensionID", "int8", pk=True),
        f("additional_days", "int4"),
        f("additional_escrow", "numeric"),
        f("reason", "text"),
        f("status", "varchar"),
        f("requested_by", "varchar"),
        f("client_approved", "bool"),
        f("client_approved_at", "timestamptz"),
        f("worker_approved", "bool"),
        f("worker_approved_at", "timestamptz"),
        f("escrow_collected", "bool"),
        f("escrow_collected_at", "timestamptz"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("jobID_id", "int8", fk="jobs"),
        f("requestedByUser_id", "int8", fk="accounts_accounts"),
    ],
    "daily_rate_changes": [
        f("changeID", "int8", pk=True),
        f("old_rate", "numeric"),
        f("new_rate", "numeric"),
        f("reason", "text"),
        f("effective_date", "date"),
        f("status", "varchar"),
        f("requested_by", "varchar"),
        f("client_approved", "bool"),
        f("client_approved_at", "timestamptz"),
        f("worker_approved", "bool"),
        f("worker_approved_at", "timestamptz"),
        f("escrow_adjusted", "bool"),
        f("escrow_adjustment_amount", "numeric"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("jobID_id", "int8", fk="jobs"),
        f("requestedByUser_id", "int8", fk="accounts_accounts"),
    ],
    "daily_skip_day_requests": [
        f("skipRequestID", "int8", pk=True),
        f("request_date", "date"),
        f("status", "varchar"),
        f("requested_by", "varchar"),
        f("requested_account_ids", "jsonb"),
        f("requested_count", "int4"),
        f("total_required", "int4"),
        f("requires_all_team_workers", "bool"),
        f("all_workers_requested", "bool"),
        f("reviewedAt", "timestamptz"),
        f("client_rejection_reason", "text"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("jobID_id", "int8", fk="jobs"),
        f("requestedByUser_id", "int8", fk="accounts_accounts"),
        f("reviewedByUser_id", "int8", fk="accounts_accounts"),
        f("target_employee_id", "int8", fk="agency_employees"),
        f("target_type", "varchar"),
        f("target_worker_account_id", "int8", fk="accounts_accounts"),
    ],
    "accounts_kyc": [
        f("kycID", "int8", pk=True),
        f("kyc_status", "varchar"),
        f("reviewedAt", "timestamptz"),
        f("notes", "text"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("accountFK_id", "int8", fk="accounts_accounts"),
        f("reviewedBy_id", "int8", fk="accounts_accounts"),
        f("rejectionCategory", "varchar"),
        f("rejectionReason", "text"),
        f("resubmissionCount", "int4"),
        f("maxResubmissions", "int4"),
    ],
    "accounts_kycfiles": [
        f("kycFileID", "int8", pk=True),
        f("idType", "varchar"),
        f("fileURL", "varchar"),
        f("fileName", "varchar"),
        f("fileSize", "int4"),
        f("uploadedAt", "timestamptz"),
        f("kycID_id", "int8", fk="accounts_kyc"),
        f("ai_verification_status", "varchar"),
        f("face_detected", "bool"),
        f("face_count", "int4"),
        f("face_confidence", "float8"),
        f("ocr_text", "text"),
        f("ocr_confidence", "float8"),
        f("quality_score", "float8"),
        f("ai_confidence_score", "float8"),
        f("ai_rejection_reason", "varchar"),
        f("ai_rejection_message", "varchar"),
        f("ai_warnings", "jsonb"),
        f("ai_details", "jsonb"),
        f("verified_at", "timestamptz"),
    ],
    "kyc_extracted_data": [
        f("extractedDataID", "int8", pk=True),
        f("extracted_full_name", "varchar"),
        f("extracted_first_name", "varchar"),
        f("extracted_middle_name", "varchar"),
        f("extracted_last_name", "varchar"),
        f("extracted_birth_date", "date"),
        f("extracted_address", "text"),
        f("extracted_id_number", "varchar"),
        f("extracted_id_type", "varchar"),
        f("extracted_expiry_date", "date"),
        f("extracted_nationality", "varchar"),
        f("extracted_sex", "varchar"),
        f("confidence_full_name", "float8"),
        f("confidence_birth_date", "float8"),
        f("confidence_address", "float8"),
        f("confidence_id_number", "float8"),
        f("overall_confidence", "float8"),
        f("confirmed_full_name", "varchar"),
        f("confirmed_first_name", "varchar"),
        f("confirmed_middle_name", "varchar"),
        f("confirmed_last_name", "varchar"),
        f("confirmed_birth_date", "date"),
        f("confirmed_address", "text"),
        f("confirmed_id_number", "varchar"),
        f("extraction_status", "varchar"),
        f("extraction_source", "varchar"),
        f("user_edited_fields", "jsonb"),
        f("confirmed_at", "timestamptz"),
        f("extracted_at", "timestamptz"),
        f("raw_extraction_data", "jsonb"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("kycID_id", "int8", fk="accounts_kyc", unique=True),
        f("extracted_place_of_birth", "varchar"),
        f("extracted_clearance_number", "varchar"),
        f("extracted_clearance_type", "varchar"),
        f("extracted_clearance_issue_date", "date"),
        f("extracted_clearance_validity_date", "date"),
        f("confidence_place_of_birth", "float8"),
        f("confidence_clearance_number", "float8"),
        f("confirmed_nationality", "varchar"),
        f("confirmed_sex", "varchar"),
        f("confirmed_place_of_birth", "varchar"),
        f("confirmed_clearance_number", "varchar"),
        f("confirmed_clearance_type", "varchar"),
        f("confirmed_clearance_issue_date", "date"),
        f("confirmed_clearance_validity_date", "date"),
        f("face_match_completed", "bool"),
        f("face_match_score", "float8"),
    ],
    "agency_agencykyc": [
        f("agencyKycID", "int8", pk=True),
        f("status", "varchar"),
        f("reviewedAt", "timestamptz"),
        f("notes", "varchar"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("accountFK_id", "int8", fk="accounts_accounts"),
        f("reviewedBy_id", "int8", fk="accounts_accounts"),
        f("rejectionCategory", "varchar"),
        f("rejectionReason", "text"),
        f("resubmissionCount", "int4"),
        f("maxResubmissions", "int4"),
        f("face_similarity_score", "float8"),
    ],
    "agency_agencykycfile": [
        f("fileID", "int8", pk=True),
        f("fileType", "varchar"),
        f("fileURL", "varchar"),
        f("fileName", "varchar"),
        f("fileSize", "int4"),
        f("uploadedAt", "timestamptz"),
        f("agencyKyc_id", "int8", fk="agency_agencykyc"),
        f("ai_verification_status", "varchar"),
        f("face_detected", "bool"),
        f("face_count", "int4"),
        f("face_confidence", "float8"),
        f("ocr_text", "text"),
        f("ocr_confidence", "float8"),
        f("quality_score", "float8"),
        f("ai_confidence_score", "float8"),
        f("ai_rejection_reason", "varchar"),
        f("ai_rejection_message", "varchar"),
        f("ai_warnings", "jsonb"),
        f("ai_details", "jsonb"),
        f("verified_at", "timestamptz"),
    ],
    "agency_kyc_extracted_data": [
        f("extractedDataID", "int8", pk=True),
        f("extracted_business_name", "varchar"),
        f("extracted_business_type", "varchar"),
        f("extracted_business_address", "text"),
        f("extracted_permit_number", "varchar"),
        f("extracted_permit_issue_date", "date"),
        f("extracted_permit_expiry_date", "date"),
        f("extracted_dti_number", "varchar"),
        f("extracted_sec_number", "varchar"),
        f("extracted_tin", "varchar"),
        f("extracted_rep_full_name", "varchar"),
        f("extracted_rep_id_number", "varchar"),
        f("extracted_rep_id_type", "varchar"),
        f("extracted_rep_birth_date", "date"),
        f("extracted_rep_address", "text"),
        f("confirmed_business_name", "varchar"),
        f("confirmed_business_type", "varchar"),
        f("confirmed_business_address", "text"),
        f("confirmed_permit_number", "varchar"),
        f("confirmed_permit_issue_date", "date"),
        f("confirmed_permit_expiry_date", "date"),
        f("confirmed_dti_number", "varchar"),
        f("confirmed_sec_number", "varchar"),
        f("confirmed_tin", "varchar"),
        f("confirmed_rep_full_name", "varchar"),
        f("confirmed_rep_id_number", "varchar"),
        f("confirmed_rep_birth_date", "date"),
        f("confirmed_rep_address", "text"),
        f("confidence_business_name", "float8"),
        f("confidence_business_address", "float8"),
        f("confidence_permit_number", "float8"),
        f("confidence_rep_name", "float8"),
        f("overall_confidence", "float8"),
        f("extraction_status", "varchar"),
        f("extraction_source", "varchar"),
        f("extracted_at", "timestamptz"),
        f("confirmed_at", "timestamptz"),
        f("user_edited_fields", "jsonb"),
        f("raw_extraction_data", "jsonb"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("agencyKyc_id", "int8", fk="agency_agencykyc", unique=True),
    ],
    "adminpanel_kyclogs": [
        f("kycLogID", "int8", pk=True),
        f("action", "varchar"),
        f("reviewedAt", "timestamptz"),
        f("reason", "text"),
        f("userEmail", "varchar"),
        f("userAccountID", "int8"),
        f("createdAt", "timestamptz"),
        f("accountFK_id", "int8", fk="accounts_accounts"),
        f("kycID", "int8"),
        f("reviewedBy_id", "int8", fk="accounts_accounts"),
        f("kycType", "varchar"),
    ],
    "adminpanel_adminaccount": [
        f("adminID", "int8", pk=True),
        f("role", "varchar"),
        f("permissions", "jsonb"),
        f("isActive", "bool"),
        f("lastLogin", "timestamptz"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("accountFK_id", "int8", fk="accounts_accounts", unique=True),
    ],
    "adminpanel_auditlog": [
        f("auditLogID", "int8", pk=True),
        f("adminEmail", "varchar"),
        f("action", "varchar"),
        f("entityType", "varchar"),
        f("entityID", "varchar"),
        f("details", "jsonb"),
        f("beforeValue", "jsonb"),
        f("afterValue", "jsonb"),
        f("ipAddress", "inet"),
        f("userAgent", "text"),
        f("createdAt", "timestamptz"),
        f("adminFK_id", "int8", fk="accounts_accounts"),
    ],
    "adminpanel_supportticket": [
        f("ticketID", "int8", pk=True),
        f("subject", "varchar"),
        f("category", "varchar"),
        f("priority", "varchar"),
        f("status", "varchar"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("lastReplyAt", "timestamptz"),
        f("resolvedAt", "timestamptz"),
        f("assignedTo_id", "int8", fk="accounts_accounts"),
        f("userFK_id", "int8", fk="accounts_accounts"),
        f("agencyFK_id", "int8", fk="accounts_agency"),
        f("ticketType", "varchar"),
        f("platform", "varchar"),
        f("deviceInfo", "text"),
        f("appVersion", "varchar"),
    ],
    "adminpanel_supportticketreply": [
        f("replyID", "int8", pk=True),
        f("content", "text"),
        f("isSystemMessage", "bool"),
        f("attachmentURL", "varchar"),
        f("createdAt", "timestamptz"),
        f("senderFK_id", "int8", fk="accounts_accounts"),
        f("ticketFK_id", "int8", fk="adminpanel_supportticket"),
    ],
    "adminpanel_userreport": [
        f("reportID", "int8", pk=True),
        f("reportType", "varchar"),
        f("reason", "varchar"),
        f("description", "text"),
        f("relatedContentID", "int8"),
        f("status", "varchar"),
        f("adminNotes", "text"),
        f("actionTaken", "varchar"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("resolvedAt", "timestamptz"),
        f("reportedUserFK_id", "int8", fk="accounts_accounts"),
        f("reporterFK_id", "int8", fk="accounts_accounts"),
        f("reviewedBy_id", "int8", fk="accounts_accounts"),
    ],
    "adminpanel_platformsettings": [
        f("settingsID", "int8", pk=True),
        f("platformFeePercentage", "numeric"),
        f("escrowHoldingDays", "int4"),
        f("maxJobBudget", "numeric"),
        f("minJobBudget", "numeric"),
        f("workerVerificationRequired", "bool"),
        f("autoApproveKYC", "bool"),
        f("kycDocumentExpiryDays", "int4"),
        f("maintenanceMode", "bool"),
        f("sessionTimeoutMinutes", "int4"),
        f("maxUploadSizeMB", "int4"),
        f("lastUpdated", "timestamptz"),
        f("updatedBy_id", "int8", fk="accounts_accounts"),
        f("kycAutoApproveMinConfidence", "numeric"),
        f("kycFaceMatchMinSimilarity", "numeric"),
        f("kycRequireUserConfirmation", "bool"),
    ],
    "adminpanel_cannedresponse": [
        f("responseID", "int8", pk=True),
        f("title", "varchar"),
        f("content", "text"),
        f("category", "varchar"),
        f("shortcuts", "jsonb"),
        f("usageCount", "int4"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("createdBy_id", "int8", fk="accounts_accounts"),
    ],
    "adminpanel_contentmoderationterm": [
        f("termID", "int8", pk=True),
        f("term", "varchar"),
        f("normalizedTerm", "varchar", unique=True),
        f("isActive", "bool"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("createdBy_id", "int8", fk="accounts_accounts"),
        f("updatedBy_id", "int8", fk="accounts_accounts"),
    ],
    "adminpanel_faq": [
        f("faqID", "int8", pk=True),
        f("question", "varchar"),
        f("answer", "text"),
        f("category", "varchar"),
        f("sortOrder", "int4"),
        f("viewCount", "int4"),
        f("isPublished", "bool"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
    ],
    "adminpanel_systemroles": [
        f("systemRoleID", "int8", pk=True),
        f("systemRole", "varchar"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("accountID_id", "int8", fk="accounts_accounts"),
    ],
    "accounts_notification": [
        f("notificationID", "int8", pk=True),
        f("notificationType", "varchar"),
        f("title", "varchar"),
        f("message", "text"),
        f("isRead", "bool"),
        f("relatedKYCLogID", "int8"),
        f("createdAt", "timestamptz"),
        f("readAt", "timestamptz"),
        f("accountFK_id", "int8", fk="accounts_accounts"),
        f("relatedJobID", "int8"),
        f("relatedApplicationID", "int8"),
        f("profile_type", "varchar"),
    ],
    "conversation": [
        f("conversationID", "int8", pk=True),
        f("lastMessageText", "text"),
        f("lastMessageTime", "timestamptz"),
        f("unreadCountClient", "int4"),
        f("unreadCountWorker", "int4"),
        f("status", "varchar"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("client_id", "int8", fk="accounts_profile"),
        f("lastMessageSender_id", "int8", fk="accounts_profile"),
        f("relatedJobPosting_id", "int8", fk="jobs", unique=True),
        f("worker_id", "int8", fk="accounts_profile"),
        f("archivedByClient", "bool"),
        f("archivedByWorker", "bool"),
        f("agency_id", "int8", fk="accounts_agency"),
        f("conversation_type", "varchar"),
    ],
    "conversation_participants": [
        f("participantID", "int8", pk=True),
        f("participant_type", "varchar"),
        f("unread_count", "int4"),
        f("is_archived", "bool"),
        f("joined_at", "timestamptz"),
        f("last_read_at", "timestamptz"),
        f("conversation_id", "int8", fk="conversation"),
        f("profile_id", "int8", fk="accounts_profile"),
        f("skill_slot_id", "int8", fk="job_skill_slots"),
        f("admin_account_id", "int8", fk="accounts_accounts"),
    ],
    "message": [
        f("messageID", "int8", pk=True),
        f("messageText", "text"),
        f("messageType", "varchar"),
        f("locationAddress", "varchar"),
        f("locationLandmark", "varchar"),
        f("locationLatitude", "numeric"),
        f("locationLongitude", "numeric"),
        f("isRead", "bool"),
        f("readAt", "timestamptz"),
        f("createdAt", "timestamptz"),
        f("conversationID_id", "int8", fk="conversation"),
        f("sender_id", "int8", fk="accounts_profile"),
        f("senderAgency_id", "int8", fk="accounts_agency"),
        f("sender_admin_id", "int8", fk="accounts_accounts"),
    ],
    "message_attachment": [
        f("attachmentID", "int8", pk=True),
        f("fileURL", "varchar"),
        f("fileName", "varchar"),
        f("fileSize", "int4"),
        f("fileType", "varchar"),
        f("uploadedAt", "timestamptz"),
        f("messageID_id", "int8", fk="message"),
    ],
    "accounts_transaction": [
        f("transactionID", "int8", pk=True),
        f("transactionType", "varchar"),
        f("amount", "numeric"),
        f("balanceAfter", "numeric"),
        f("status", "varchar"),
        f("description", "varchar"),
        f("referenceNumber", "varchar"),
        f("paymentMethod", "varchar"),
        f("createdAt", "timestamptz"),
        f("completedAt", "timestamptz"),
        f("relatedJobPosting_id", "int8", fk="jobs"),
        f("walletID_id", "int8", fk="accounts_wallet"),
        f("invoiceURL", "varchar"),
        f("xenditExternalID", "varchar"),
        f("xenditInvoiceID", "varchar", unique=True),
        f("xenditPaymentChannel", "varchar"),
        f("xenditPaymentID", "varchar"),
        f("xenditPaymentMethod", "varchar"),
        f("adminReferenceNumber", "varchar"),
        f("processedAt", "timestamptz"),
        f("processedByAdmin_id", "int8", fk="accounts_accounts"),
        f("paymongoPaymentId", "varchar"),
        f("paymongoTransferId", "varchar"),
        f("paymongoTransferStatus", "varchar"),
    ],
    "agency_employees": [
        f("employeeID", "int8", pk=True),
        f("name", "varchar"),
        f("email", "varchar"),
        f("role", "varchar"),
        f("avatar", "varchar"),
        f("rating", "numeric"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("agency_id", "int8", fk="accounts_accounts"),
        f("employeeOfTheMonth", "bool"),
        f("employeeOfTheMonthDate", "timestamptz"),
        f("employeeOfTheMonthReason", "text"),
        f("isActive", "bool"),
        f("lastRatingUpdate", "timestamptz"),
        f("totalEarnings", "numeric"),
        f("totalJobsCompleted", "int4"),
        f("firstName", "varchar"),
        f("middleName", "varchar"),
        f("lastName", "varchar"),
        f("specializations", "text"),
        f("daily_rate", "numeric"),
        f("hourly_rate", "numeric"),
        f("is_available_daily_jobs", "bool"),
        f("mobile", "varchar"),
    ],
    "worker_certifications": [
        f("certificationID", "int8", pk=True),
        f("name", "varchar"),
        f("issuing_organization", "varchar"),
        f("issue_date", "date"),
        f("expiry_date", "date"),
        f("certificate_url", "varchar"),
        f("is_verified", "bool"),
        f("verified_at", "timestamptz"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("verified_by_id", "int8", fk="accounts_accounts"),
        f("workerID_id", "int8", fk="accounts_workerprofile"),
        f("specializationID_id", "int8", fk="accounts_workerspecialization"),
    ],
    "certification_logs": [
        f("certLogID", "int8", pk=True),
        f("certificationID", "int8"),
        f("action", "varchar"),
        f("reviewedAt", "timestamptz"),
        f("reason", "text"),
        f("workerEmail", "varchar"),
        f("workerAccountID", "int8"),
        f("certificationName", "varchar"),
        f("reviewedBy_id", "int8", fk="accounts_accounts"),
        f("workerID_id", "int8", fk="accounts_workerprofile"),
    ],
    "worker_materials": [
        f("materialID", "int8", pk=True),
        f("name", "varchar"),
        f("description", "text"),
        f("price", "numeric"),
        f("unit", "varchar"),
        f("image_url", "varchar"),
        f("is_available", "bool"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("workerID_id", "int8", fk="accounts_workerprofile"),
        f("quantity", "numeric"),
        f("categoryID_id", "int8", fk="specializations"),
        f("agencyID_id", "int8", fk="accounts_agency"),
    ],
    "worker_portfolio": [
        f("portfolioID", "int8", pk=True),
        f("image_url", "varchar"),
        f("caption", "text"),
        f("display_order", "int4"),
        f("file_name", "varchar"),
        f("file_size", "int4"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("workerID_id", "int8", fk="accounts_workerprofile"),
    ],
    "profiles_workerproduct": [
        f("productID", "int8", pk=True),
        f("productName", "varchar"),
        f("description", "text"),
        f("price", "numeric"),
        f("priceUnit", "varchar"),
        f("inStock", "bool"),
        f("stockQuantity", "int4"),
        f("productImage", "varchar"),
        f("isActive", "bool"),
        f("createdAt", "timestamptz"),
        f("updatedAt", "timestamptz"),
        f("categoryID_id", "int8", fk="specializations"),
        f("workerID_id", "int8", fk="accounts_workerprofile"),
    ],
}


@dataclass(frozen=True)
class Module:
    title: str
    note: str
    filename: str
    accent: tuple[int, int, int, int]
    columns: list[list[str]]


MODULES = [
    Module(
        "Module 2 - Profiles, Location, Wallet & Specializations",
        "13 tables | corrected FK targets from PostgreSQL schema",
        "erd_v2_module2_profiles.png",
        (31, 126, 99, 255),
        [
            ["accounts_profile", "accounts_workerprofile", "accounts_clientprofile"],
            ["accounts_agency", "specializations", "accounts_workerspecialization", "accounts_interestedjobs"],
            ["accounts_city", "accounts_barangay"],
            ["accounts_wallet", "accounts_userpaymentmethod", "accounts_pushtoken", "accounts_notificationsettings"],
        ],
    ),
    Module(
        "Module 3 - Jobs, Applications & Assignments",
        "8 tables | jobs includes every workflow/payment/cancellation field",
        "erd_v2_module3_jobs.png",
        (198, 136, 21, 255),
        [
            ["jobs"],
            ["job_skill_slots", "job_applications", "price_negotiations"],
            ["job_worker_assignments", "job_employee_assignments", "job_logs", "saved_jobs"],
        ],
    ),
    Module(
        "Module 4 - Disputes, Reviews, Daily Operations & Attendance",
        "11 tables | corrected review, attendance, and daily operation FKs",
        "erd_v2_module4_disputes.png",
        (192, 87, 42, 255),
        [
            ["job_disputes", "dispute_evidence", "backjob_schedule_confirmations"],
            ["job_reviews", "review_skill_tags"],
            ["job_materials", "job_photos"],
            ["daily_attendance", "daily_job_extensions", "daily_rate_changes", "daily_skip_day_requests"],
        ],
    ),
    Module(
        "Module 5 - KYC Verification (Individual & Agency)",
        "7 tables | extracted data tables shown as 1-to-1 unique FK records",
        "erd_v2_module5_kyc.png",
        (161, 91, 176, 255),
        [
            ["accounts_kyc", "accounts_kycfiles"],
            ["kyc_extracted_data", "adminpanel_kyclogs"],
            ["agency_agencykyc", "agency_agencykycfile"],
            ["agency_kyc_extracted_data"],
        ],
    ),
    Module(
        "Module 6 - Admin Panel, Messaging, Notifications & Worker Assets",
        "22 tables | corrected messaging, agency employee, and certification FKs",
        "erd_v2_module6_admin.png",
        (58, 91, 134, 255),
        [
            ["adminpanel_adminaccount", "adminpanel_auditlog", "adminpanel_systemroles", "accounts_notification"],
            ["adminpanel_supportticket", "adminpanel_supportticketreply", "adminpanel_userreport"],
            ["adminpanel_platformsettings", "adminpanel_cannedresponse", "adminpanel_contentmoderationterm", "adminpanel_faq"],
            ["conversation", "conversation_participants", "message", "message_attachment"],
            ["accounts_transaction", "agency_employees", "worker_certifications", "certification_logs"],
            ["worker_materials", "worker_portfolio", "profiles_workerproduct"],
        ],
    ),
]


EXPECTED_AUDIT_FKS = {
    ("accounts_interestedjobs", "clientID_id"): "accounts_clientprofile",
    ("accounts_wallet", "preferredPaymentMethodID_id"): "accounts_userpaymentmethod",
    ("certification_logs", "workerID_id"): "accounts_workerprofile",
    ("review_skill_tags", "workerSpecializationID_id"): "accounts_workerspecialization",
    ("job_reviews", "revieweeAgencyID_id"): "accounts_agency",
    ("job_reviews", "revieweeEmployeeID_id"): "agency_employees",
    ("job_reviews", "revieweeProfileID_id"): "accounts_profile",
    ("job_reviews", "flaggedBy_id"): "accounts_accounts",
    ("adminpanel_supportticket", "agencyFK_id"): "accounts_agency",
    ("accounts_transaction", "processedByAdmin_id"): "accounts_accounts",
    ("conversation", "client_id"): "accounts_profile",
    ("conversation", "worker_id"): "accounts_profile",
    ("conversation", "lastMessageSender_id"): "accounts_profile",
    ("message", "sender_id"): "accounts_profile",
    ("message", "senderAgency_id"): "accounts_agency",
    ("message", "sender_admin_id"): "accounts_accounts",
    ("agency_employees", "agency_id"): "accounts_accounts",
    ("worker_certifications", "specializationID_id"): "accounts_workerspecialization",
}


def load_fonts(scale: float) -> dict[str, ImageFont.FreeTypeFont]:
    def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(str(path), max(8, int(size * scale)))

    return {
        "title": font(FONT_BOLD, 32),
        "note": font(FONT_REG, 18),
        "header": font(FONT_BOLD, 18),
        "field": font(FONT_MONO, 14),
        "field_bold": font(FONT_MONO_BOLD, 14),
        "field_italic": font(FONT_MONO_ITALIC, 14),
        "small": font(FONT_REG, 12),
        "small_bold": font(FONT_BOLD, 12),
    }


def table_size(fields: list[Field], *, row_h: int, header_h: int, width: int) -> tuple[int, int]:
    return width, header_h + row_h * len(fields)


def all_module_tables(module: Module) -> list[str]:
    return [table for column in module.columns for table in column]


def lighten(color: tuple[int, int, int, int], amount: int = 235) -> tuple[int, int, int, int]:
    r, g, b, a = color
    return (
        min(255, int((r + amount) / 2)),
        min(255, int((g + amount) / 2)),
        min(255, int((b + amount) / 2)),
        a,
    )


def draw_key(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    draw.ellipse((x, y + 5, x + 11, y + 16), outline=PK_GOLD, width=2)
    draw.line((x + 11, y + 10, x + 24, y + 10), fill=PK_GOLD, width=2)
    draw.line((x + 19, y + 10, x + 19, y + 15), fill=PK_GOLD, width=2)
    draw.line((x + 23, y + 10, x + 23, y + 14), fill=PK_GOLD, width=2)


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> int:
    left, _, right, _ = draw.textbbox((0, 0), text, font=font)
    return right - left


def fit_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_w: int) -> str:
    if text_width(draw, text, font) <= max_w:
        return text
    suffix = "..."
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi) // 2
        if text_width(draw, text[:mid] + suffix, font) <= max_w:
            lo = mid + 1
        else:
            hi = mid
    return text[: max(0, lo - 1)] + suffix


def draw_crow_foot(draw: ImageDraw.ImageDraw, x: int, y: int, direction: int, color: tuple[int, int, int, int]) -> None:
    stem = 14 * direction
    draw.line((x, y, x + stem, y), fill=color, width=2)
    draw.line((x, y, x + stem, y - 9), fill=color, width=2)
    draw.line((x, y, x + stem, y + 9), fill=color, width=2)


def draw_one_bar(draw: ImageDraw.ImageDraw, x: int, y: int, direction: int, color: tuple[int, int, int, int]) -> None:
    draw.line((x, y - 10, x, y + 10), fill=color, width=2)
    draw.line((x, y, x + 12 * direction, y), fill=color, width=2)


def draw_relation(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    target_box: tuple[int, int, int, int],
    color: tuple[int, int, int, int],
) -> None:
    sx, sy = start
    tx1, ty1, tx2, ty2 = target_box
    # Connect to the nearest horizontal side of the parent table/reference.
    if sx < tx1:
        ex, ey, side = tx1, (ty1 + ty2) // 2, -1
    elif sx > tx2:
        ex, ey, side = tx2, (ty1 + ty2) // 2, 1
    else:
        ex, ey, side = (tx1 + tx2) // 2, ty1, -1

    mid_x = sx + (ex - sx) // 2
    points = [(sx, sy), (mid_x, sy), (mid_x, ey), (ex, ey)]
    draw.line(points, fill=color, width=2, joint="curve")
    draw_crow_foot(draw, sx, sy, -1 if ex < sx else 1, color)
    draw_one_bar(draw, ex, ey, side, color)


def render_module(module: Module) -> Path:
    fonts = load_fonts(1.0)
    margin = 56
    gap_x = 42
    gap_y = 30
    table_w = 640
    row_h = 27
    header_h = 42
    title_h = 112
    external_h = 80

    column_heights = []
    for column in module.columns:
        height = sum(table_size(SCHEMA[t], row_h=row_h, header_h=header_h, width=table_w)[1] for t in column)
        height += gap_y * max(0, len(column) - 1)
        column_heights.append(height)

    ext_targets = sorted({
        field.fk
        for table in all_module_tables(module)
        for field in SCHEMA[table]
        if field.fk and field.fk not in all_module_tables(module)
    })
    ext_rows = 0 if not ext_targets else (len(ext_targets) + 4) // 5
    ext_area_h = external_h * ext_rows

    width = margin * 2 + len(module.columns) * table_w + (len(module.columns) - 1) * gap_x
    height = title_h + ext_area_h + max(column_heights) + margin
    image = Image.new("RGBA", (width, height), BG)
    draw = ImageDraw.Draw(image)

    draw.text((margin, 24), module.title, fill=TEXT, font=fonts["title"])
    draw.text((margin, 66), module.note, fill=MUTED, font=fonts["note"])
    draw.line((margin, 96, width - margin, 96), fill=lighten(module.accent, 225), width=3)

    positions: dict[str, tuple[int, int, int, int]] = {}
    row_positions: dict[tuple[str, str], tuple[int, int]] = {}
    ref_positions: dict[str, tuple[int, int, int, int]] = {}

    if ext_targets:
        draw.text((margin, title_h - 8), "External referenced tables", fill=MUTED, font=fonts["small_bold"])
        ref_w = (width - margin * 2 - gap_x * 4) // 5
        for idx, target in enumerate(ext_targets):
            r, c = divmod(idx, 5)
            x = margin + c * (ref_w + gap_x)
            y = title_h + r * external_h + 14
            box = (x, y, x + ref_w, y + 46)
            ref_positions[target] = box
            draw.rounded_rectangle(box, radius=10, fill=EXTERNAL_FILL, outline=EXTERNAL_BORDER, width=2)
            label = fit_text(draw, target, fonts["small_bold"], ref_w - 24)
            draw.text((x + 12, y + 13), label, fill=MUTED, font=fonts["small_bold"])

    top = title_h + ext_area_h + 16
    for col_idx, column in enumerate(module.columns):
        x = margin + col_idx * (table_w + gap_x)
        y = top
        for table in column:
            _, h = table_size(SCHEMA[table], row_h=row_h, header_h=header_h, width=table_w)
            positions[table] = (x, y, x + table_w, y + h)
            for row_idx, field in enumerate(SCHEMA[table]):
                row_positions[(table, field.name)] = (x + table_w - 4, y + header_h + row_idx * row_h + row_h // 2)
            y += h + gap_y

    rel_color = (*module.accent[:3], 92)
    for table in all_module_tables(module):
        for field in SCHEMA[table]:
            if not field.fk:
                continue
            target = positions.get(field.fk) or ref_positions.get(field.fk)
            if not target:
                continue
            draw_relation(draw, row_positions[(table, field.name)], target, rel_color)

    for table in all_module_tables(module):
        x1, y1, x2, y2 = positions[table]
        draw.rounded_rectangle((x1, y1, x2, y2), radius=10, fill=(255, 255, 255, 255), outline=module.accent, width=2)
        draw.rounded_rectangle((x1, y1, x2, y1 + header_h), radius=10, fill=module.accent, outline=module.accent, width=2)
        draw.rectangle((x1, y1 + header_h - 10, x2, y1 + header_h), fill=module.accent)
        draw.text((x1 + 16, y1 + 10), table, fill=(255, 255, 255, 255), font=fonts["header"])

        for idx, field in enumerate(SCHEMA[table]):
            row_y = y1 + header_h + idx * row_h
            draw.rectangle((x1 + 1, row_y, x2 - 1, row_y + row_h), fill=ROW_ALT if idx % 2 else ROW_WHITE)
            draw.line((x1 + 1, row_y, x2 - 1, row_y), fill=GRID, width=1)

            font = fonts["field_bold"] if field.pk else fonts["field_italic"] if field.fk else fonts["field"]
            color = FK_BLUE if field.fk else TEXT
            label_x = x1 + 16
            if field.pk:
                draw_key(draw, x1 + 12, row_y + 3)
                draw.text((x1 + 42, row_y + 5), "PK", fill=PK_GOLD, font=fonts["small_bold"])
                label_x = x1 + 76

            detail = f"{field.name} | {field.dtype}"
            if field.unique:
                detail += " UNIQUE"
            if field.fk:
                detail += f" \u2192 {field.fk}"
            detail = fit_text(draw, detail, font, x2 - label_x - 14)
            draw.text((label_x, row_y + 5), detail, fill=color, font=font)

    legend_y = height - margin + 16
    if legend_y < height - 22:
        draw.text((margin, legend_y), "Crow's foot = many/FK side; single bar = referenced PK/unique side.", fill=MUTED, font=fonts["small"])

    path = OUT_DIR / module.filename
    image.convert("RGB").save(path, "PNG", optimize=True, dpi=(300, 300))
    return path


def validate() -> None:
    for module in MODULES:
        tables = all_module_tables(module)
        assert len(tables) == len(set(tables)), module.title
        for table in tables:
            assert table in SCHEMA, table
            assert any(field.pk for field in SCHEMA[table]), f"{table} has no PK"
    for (table, field_name), target in EXPECTED_AUDIT_FKS.items():
        matches = [field for field in SCHEMA[table] if field.name == field_name]
        assert matches, f"Missing audited FK {table}.{field_name}"
        assert matches[0].fk == target, f"{table}.{field_name} -> {matches[0].fk}, expected {target}"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    validate()
    for module in MODULES:
        path = render_module(module)
        print(path)


if __name__ == "__main__":
    main()
