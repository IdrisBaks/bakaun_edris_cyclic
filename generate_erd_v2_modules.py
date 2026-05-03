#!/usr/bin/env python3
"""Generate corrected ERD diagram images for schema modules 2-6."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple

from PIL import Image, ImageDraw, ImageFont


@dataclass
class FieldSpec:
    name: str
    dtype: str


@dataclass
class TableSpec:
    name: str
    pk: str
    fields: List[FieldSpec]
    fks: Dict[str, str] = field(default_factory=dict)
    unique_fks: Set[str] = field(default_factory=set)


@dataclass
class ModuleSpec:
    title: str
    filename: str
    table_names: List[str]
    n_cols: int


def fs(name: str, dtype: str) -> FieldSpec:
    return FieldSpec(name=name, dtype=dtype)


def build_table_specs() -> Dict[str, TableSpec]:
    return {
        # MODULE 2
        "accounts_profile": TableSpec(
            name="accounts_profile",
            pk="profileID",
            fields=[
                fs("profileID", "int8"),
                fs("profileImg", "varchar"),
                fs("firstName", "varchar"),
                fs("lastName", "varchar"),
                fs("contactNum", "varchar"),
                fs("birthDate", "date"),
                fs("profileType", "varchar"),
                fs("accountFK_id", "int8"),
                fs("middleName", "varchar"),
                fs("latitude", "numeric"),
                fs("location_sharing_enabled", "bool"),
                fs("location_updated_at", "timestamptz"),
                fs("longitude", "numeric"),
            ],
            fks={"accountFK_id": "accounts_accounts"},
        ),
        "accounts_workerprofile": TableSpec(
            name="accounts_workerprofile",
            pk="id",
            fields=[
                fs("id", "int8"),
                fs("description", "varchar"),
                fs("workerRating", "int4"),
                fs("totalEarningGross", "numeric"),
                fs("availability_status", "varchar"),
                fs("profileID_id", "int8"),
                fs("bio", "varchar"),
                fs("hourly_rate", "numeric"),
                fs("profile_completion_percentage", "int4"),
                fs("soft_skills", "text"),
                fs("daily_rate", "numeric"),
                fs("is_available_daily_jobs", "bool"),
            ],
            fks={"profileID_id": "accounts_profile"},
            unique_fks={"profileID_id"},
        ),
        "accounts_clientprofile": TableSpec(
            name="accounts_clientprofile",
            pk="id",
            fields=[
                fs("id", "int8"),
                fs("description", "varchar"),
                fs("totalJobsPosted", "int4"),
                fs("clientRating", "int4"),
                fs("profileID_id", "int8"),
                fs("activeJobsCount", "int4"),
            ],
            fks={"profileID_id": "accounts_profile"},
            unique_fks={"profileID_id"},
        ),
        "accounts_agency": TableSpec(
            name="accounts_agency",
            pk="agencyId",
            fields=[
                fs("agencyId", "int8"),
                fs("businessName", "varchar"),
                fs("businessDesc", "varchar"),
                fs("createdAt", "timestamptz"),
                fs("accountFK_id", "int8"),
                fs("city", "varchar"),
                fs("country", "varchar"),
                fs("postal_code", "varchar"),
                fs("province", "varchar"),
                fs("street_address", "varchar"),
                fs("contactNumber", "varchar"),
                fs("barangay", "varchar"),
            ],
            fks={"accountFK_id": "accounts_accounts"},
        ),
        "accounts_barangay": TableSpec(
            name="accounts_barangay",
            pk="barangayID",
            fields=[
                fs("barangayID", "int4"),
                fs("name", "varchar"),
                fs("zipCode", "varchar"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("city_id", "int4"),
            ],
            fks={"city_id": "accounts_city"},
        ),
        "accounts_city": TableSpec(
            name="accounts_city",
            pk="cityID",
            fields=[
                fs("cityID", "int4"),
                fs("name", "varchar"),
                fs("province", "varchar"),
                fs("region", "varchar"),
                fs("zipCode", "varchar"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
            ],
        ),
        "specializations": TableSpec(
            name="specializations",
            pk="specializationID",
            fields=[
                fs("specializationID", "int8"),
                fs("specializationName", "varchar"),
                fs("averageProjectCostMax", "numeric"),
                fs("averageProjectCostMin", "numeric"),
                fs("description", "text"),
                fs("minimumRate", "numeric"),
                fs("rateType", "varchar"),
                fs("skillLevel", "varchar"),
                fs("is_custom", "bool"),
                fs("created_by_agency_id", "int8"),
                fs("created_by_worker_id", "int8"),
            ],
            fks={
                "created_by_agency_id": "accounts_agency",
                "created_by_worker_id": "accounts_accounts",
            },
        ),
        "accounts_workerspecialization": TableSpec(
            name="accounts_workerspecialization",
            pk="id",
            fields=[
                fs("id", "int8"),
                fs("experienceYears", "int4"),
                fs("certification", "varchar"),
                fs("specializationID_id", "int8"),
                fs("workerID_id", "int8"),
                fs("skillType", "varchar"),
                fs("displayOrder", "int4"),
            ],
            fks={
                "specializationID_id": "specializations",
                "workerID_id": "accounts_workerprofile",
            },
        ),
        "accounts_interestedjobs": TableSpec(
            name="accounts_interestedjobs",
            pk="id",
            fields=[
                fs("id", "int8"),
                fs("clientID_id", "int8"),
                fs("specializationID_id", "int8"),
            ],
            fks={
                "clientID_id": "accounts_clientprofile",
                "specializationID_id": "specializations",
            },
        ),
        "accounts_wallet": TableSpec(
            name="accounts_wallet",
            pk="walletID",
            fields=[
                fs("walletID", "int8"),
                fs("balance", "numeric"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("accountFK_id", "int8"),
                fs("reservedBalance", "numeric"),
                fs("pendingEarnings", "numeric"),
                fs("autoWithdrawEnabled", "bool"),
                fs("preferredPaymentMethodID_id", "int8"),
                fs("lastAutoWithdrawAt", "timestamptz"),
            ],
            fks={
                "accountFK_id": "accounts_accounts",
                "preferredPaymentMethodID_id": "accounts_userpaymentmethod",
            },
            unique_fks={"accountFK_id"},
        ),
        "accounts_userpaymentmethod": TableSpec(
            name="accounts_userpaymentmethod",
            pk="id",
            fields=[
                fs("id", "int8"),
                fs("methodType", "varchar"),
                fs("accountName", "varchar"),
                fs("accountNumber", "varchar"),
                fs("bankName", "varchar"),
                fs("isPrimary", "bool"),
                fs("isVerified", "bool"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("accountFK_id", "int8"),
                fs("bankCode", "varchar"),
                fs("paymongoRecipientId", "varchar"),
            ],
            fks={"accountFK_id": "accounts_accounts"},
        ),
        "accounts_pushtoken": TableSpec(
            name="accounts_pushtoken",
            pk="tokenID",
            fields=[
                fs("tokenID", "int8"),
                fs("pushToken", "varchar"),
                fs("deviceType", "varchar"),
                fs("isActive", "bool"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("lastUsed", "timestamptz"),
                fs("accountFK_id", "int8"),
            ],
            fks={"accountFK_id": "accounts_accounts"},
        ),
        "accounts_notificationsettings": TableSpec(
            name="accounts_notificationsettings",
            pk="settingsID",
            fields=[
                fs("settingsID", "int8"),
                fs("pushEnabled", "bool"),
                fs("soundEnabled", "bool"),
                fs("jobUpdates", "bool"),
                fs("messages", "bool"),
                fs("payments", "bool"),
                fs("reviews", "bool"),
                fs("kycUpdates", "bool"),
                fs("doNotDisturbStart", "time"),
                fs("doNotDisturbEnd", "time"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("accountFK_id", "int8"),
            ],
            fks={"accountFK_id": "accounts_accounts"},
            unique_fks={"accountFK_id"},
        ),
        # MODULE 3
        "jobs": TableSpec(
            name="jobs",
            pk="jobID",
            fields=[
                fs("jobID", "int8"),
                fs("title", "varchar"),
                fs("description", "text"),
                fs("budget", "numeric"),
                fs("location", "varchar"),
                fs("expectedDuration", "varchar"),
                fs("urgency", "varchar"),
                fs("preferredStartDate", "date"),
                fs("materialsNeeded", "jsonb"),
                fs("status", "varchar"),
                fs("completedAt", "timestamptz"),
                fs("cancellationReason", "text"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("assignedWorkerID_id", "int8"),
                fs("categoryID_id", "int8"),
                fs("clientID_id", "int8"),
                fs("clientMarkedComplete", "bool"),
                fs("clientMarkedCompleteAt", "timestamptz"),
                fs("workerMarkedComplete", "bool"),
                fs("workerMarkedCompleteAt", "timestamptz"),
                fs("escrowAmount", "numeric"),
                fs("escrowPaid", "bool"),
                fs("escrowPaidAt", "timestamptz"),
                fs("remainingPayment", "numeric"),
                fs("remainingPaymentPaid", "bool"),
                fs("remainingPaymentPaidAt", "timestamptz"),
                fs("finalPaymentMethod", "varchar"),
                fs("cashPaymentProofUrl", "varchar"),
                fs("paymentMethodSelectedAt", "timestamptz"),
                fs("cashProofUploadedAt", "timestamptz"),
                fs("cashPaymentApproved", "bool"),
                fs("cashPaymentApprovedAt", "timestamptz"),
                fs("cashPaymentApprovedBy_id", "int8"),
                fs("assignedAgencyFK_id", "int8"),
                fs("jobType", "varchar"),
                fs("inviteRejectionReason", "text"),
                fs("inviteRespondedAt", "timestamptz"),
                fs("inviteStatus", "varchar"),
                fs("clientConfirmedWorkStarted", "bool"),
                fs("clientConfirmedWorkStartedAt", "timestamptz"),
                fs("assignedEmployeeID_id", "int8"),
                fs("assignmentNotes", "text"),
                fs("employeeAssignedAt", "timestamptz"),
                fs("is_team_job", "bool"),
                fs("budget_allocation_type", "varchar"),
                fs("team_job_start_threshold", "numeric"),
                fs("paymentReleaseDate", "timestamptz"),
                fs("paymentReleasedToWorker", "bool"),
                fs("paymentReleasedAt", "timestamptz"),
                fs("paymentHeldReason", "varchar"),
                fs("job_scope", "varchar"),
                fs("skill_level_required", "varchar"),
                fs("work_environment", "varchar"),
                fs("payment_model", "varchar"),
                fs("duration_days", "int4"),
                fs("daily_rate_agreed", "numeric"),
                fs("actual_start_date", "date"),
                fs("total_days_worked", "int4"),
                fs("daily_escrow_total", "numeric"),
                fs("materialsCost", "numeric"),
                fs("materials_status", "varchar"),
                fs("scheduled_end_date", "date"),
                fs("qa_day_offset", "int4"),
                fs("workerMarkedOnTheWay", "bool"),
                fs("workerMarkedOnTheWayAt", "timestamptz"),
                fs("workerMarkedJobStarted", "bool"),
                fs("workerMarkedJobStartedAt", "timestamptz"),
                fs("is_early_completed", "bool"),
                fs("early_completed_at", "timestamptz"),
                fs("early_completion_payout", "numeric"),
                fs("shift_type", "varchar"),
                fs("cancelledAt", "timestamptz"),
                fs("cancelledByRole", "varchar"),
                fs("cancelledByAccountID_id", "int8"),
                fs("cancellationStage", "varchar"),
                fs("clientRefundAmount", "numeric"),
                fs("workerCompensationAmount", "numeric"),
                fs("agency_flow_mode", "varchar"),
            ],
            fks={
                "assignedWorkerID_id": "accounts_workerprofile",
                "categoryID_id": "specializations",
                "clientID_id": "accounts_clientprofile",
                "cashPaymentApprovedBy_id": "accounts_accounts",
                "assignedAgencyFK_id": "accounts_agency",
                "assignedEmployeeID_id": "agency_employees",
                "cancelledByAccountID_id": "accounts_accounts",
            },
        ),
        "job_skill_slots": TableSpec(
            name="job_skill_slots",
            pk="skillSlotID",
            fields=[
                fs("skillSlotID", "int8"),
                fs("workers_needed", "int4"),
                fs("budget_allocated", "numeric"),
                fs("skill_level_required", "varchar"),
                fs("status", "varchar"),
                fs("notes", "text"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("jobID_id", "int8"),
                fs("specializationID_id", "int8"),
                fs("invited_agency_id", "int8"),
                fs("agency_invite_status", "varchar"),
                fs("agency_invite_responded_at", "timestamptz"),
                fs("last_rejected_agency_id", "int8"),
                fs("last_rejected_agency_name", "varchar"),
                fs("last_rejected_at", "timestamptz"),
                fs("last_rejection_reason", "text"),
            ],
            fks={
                "jobID_id": "jobs",
                "specializationID_id": "specializations",
                "invited_agency_id": "accounts_agency",
            },
        ),
        "job_applications": TableSpec(
            name="job_applications",
            pk="applicationID",
            fields=[
                fs("applicationID", "int8"),
                fs("proposalMessage", "text"),
                fs("proposedBudget", "numeric"),
                fs("estimatedDuration", "varchar"),
                fs("budgetOption", "varchar"),
                fs("status", "varchar"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("jobID_id", "int8"),
                fs("workerID_id", "int8"),
                fs("applied_skill_slot_id", "int8"),
                fs("selected_materials", "jsonb"),
                fs("proposed_daily_rate", "numeric"),
                fs("proposed_days", "int4"),
                fs("negotiation_count", "int2"),
                fs("applied_shift", "varchar"),
                fs("clientRejectionReason", "text"),
            ],
            fks={
                "jobID_id": "jobs",
                "workerID_id": "accounts_workerprofile",
                "applied_skill_slot_id": "job_skill_slots",
            },
        ),
        "price_negotiations": TableSpec(
            name="price_negotiations",
            pk="negotiationID",
            fields=[
                fs("negotiationID", "int8"),
                fs("application_id", "int8"),
                fs("actor", "varchar"),
                fs("round_number", "int2"),
                fs("proposed_budget", "numeric"),
                fs("proposed_daily_rate", "numeric"),
                fs("proposed_days", "int4"),
                fs("message", "text"),
                fs("status", "varchar"),
                fs("createdAt", "timestamptz"),
            ],
            fks={"application_id": "job_applications"},
        ),
        "job_worker_assignments": TableSpec(
            name="job_worker_assignments",
            pk="assignmentID",
            fields=[
                fs("assignmentID", "int8"),
                fs("slot_position", "int4"),
                fs("assignment_status", "varchar"),
                fs("worker_marked_complete", "bool"),
                fs("worker_marked_complete_at", "timestamptz"),
                fs("completion_notes", "text"),
                fs("individual_rating", "numeric"),
                fs("assignedAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("jobID_id", "int8"),
                fs("skillSlotID_id", "int8"),
                fs("workerID_id", "int8"),
                fs("client_confirmed_arrival", "bool"),
                fs("client_confirmed_arrival_at", "timestamptz"),
                fs("daily_rate_at_assignment", "numeric"),
                fs("days_worked", "int4"),
                fs("total_earned", "numeric"),
                fs("early_completed", "bool"),
                fs("early_completed_at", "timestamptz"),
                fs("early_completion_payout", "numeric"),
                fs("assigned_shift", "varchar"),
            ],
            fks={
                "jobID_id": "jobs",
                "skillSlotID_id": "job_skill_slots",
                "workerID_id": "accounts_workerprofile",
            },
        ),
        "job_employee_assignments": TableSpec(
            name="job_employee_assignments",
            pk="assignmentID",
            fields=[
                fs("assignmentID", "int8"),
                fs("assignedAt", "timestamptz"),
                fs("notes", "text"),
                fs("isPrimaryContact", "bool"),
                fs("status", "varchar"),
                fs("employeeMarkedComplete", "bool"),
                fs("employeeMarkedCompleteAt", "timestamptz"),
                fs("completionNotes", "text"),
                fs("assignedBy_id", "int8"),
                fs("employee_id", "int8"),
                fs("job_id", "int8"),
                fs("skill_slot_id", "int8"),
                fs("dispatched", "bool"),
                fs("dispatchedAt", "timestamptz"),
                fs("clientConfirmedArrival", "bool"),
                fs("clientConfirmedArrivalAt", "timestamptz"),
                fs("agencyMarkedComplete", "bool"),
                fs("agencyMarkedCompleteAt", "timestamptz"),
                fs("paymentAmount", "numeric"),
                fs("clientApproved", "bool"),
                fs("clientApprovedAt", "timestamptz"),
                fs("early_completed", "bool"),
                fs("early_completed_at", "timestamptz"),
                fs("early_completion_payout", "numeric"),
            ],
            fks={
                "assignedBy_id": "accounts_accounts",
                "employee_id": "agency_employees",
                "job_id": "jobs",
                "skill_slot_id": "job_skill_slots",
            },
        ),
        "job_logs": TableSpec(
            name="job_logs",
            pk="logID",
            fields=[
                fs("logID", "int8"),
                fs("oldStatus", "varchar"),
                fs("newStatus", "varchar"),
                fs("notes", "text"),
                fs("createdAt", "timestamptz"),
                fs("changedBy_id", "int8"),
                fs("jobID_id", "int8"),
                fs("actionType", "varchar"),
                fs("metadata", "jsonb"),
            ],
            fks={"changedBy_id": "accounts_accounts", "jobID_id": "jobs"},
        ),
        "saved_jobs": TableSpec(
            name="saved_jobs",
            pk="savedJobID",
            fields=[
                fs("savedJobID", "int8"),
                fs("savedAt", "timestamptz"),
                fs("jobID_id", "int8"),
                fs("workerID_id", "int8"),
            ],
            fks={"jobID_id": "jobs", "workerID_id": "accounts_workerprofile"},
        ),
        # MODULE 4
        "job_disputes": TableSpec(
            name="job_disputes",
            pk="disputeID",
            fields=[
                fs("disputeID", "int8"),
                fs("disputedBy", "varchar"),
                fs("reason", "varchar"),
                fs("description", "text"),
                fs("status", "varchar"),
                fs("priority", "varchar"),
                fs("jobAmount", "numeric"),
                fs("disputedAmount", "numeric"),
                fs("resolution", "text"),
                fs("resolvedDate", "timestamptz"),
                fs("assignedTo", "varchar"),
                fs("openedDate", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("jobID_id", "int8"),
                fs("backjobStarted", "bool"),
                fs("backjobStartedAt", "timestamptz"),
                fs("clientConfirmedBackjob", "bool"),
                fs("clientConfirmedBackjobAt", "timestamptz"),
                fs("workerMarkedBackjobComplete", "bool"),
                fs("workerMarkedBackjobCompleteAt", "timestamptz"),
                fs("termsAccepted", "bool"),
                fs("termsVersion", "varchar"),
                fs("termsAcceptedAt", "timestamptz"),
                fs("adminRejectedAt", "timestamptz"),
                fs("adminRejectionReason", "text"),
                fs("in_negotiation_at", "timestamptz"),
                fs("scheduled_date", "date"),
                fs("workerScheduleConfirmed", "bool"),
                fs("workerScheduleConfirmedAt", "timestamptz"),
            ],
            fks={"jobID_id": "jobs"},
        ),
        "dispute_evidence": TableSpec(
            name="dispute_evidence",
            pk="evidenceID",
            fields=[
                fs("evidenceID", "int8"),
                fs("imageURL", "varchar"),
                fs("description", "text"),
                fs("createdAt", "timestamptz"),
                fs("disputeID_id", "int8"),
                fs("uploadedBy_id", "int8"),
            ],
            fks={"disputeID_id": "job_disputes", "uploadedBy_id": "accounts_accounts"},
        ),
        "backjob_schedule_confirmations": TableSpec(
            name="backjob_schedule_confirmations",
            pk="confirmationID",
            fields=[
                fs("confirmationID", "int8"),
                fs("confirmed", "bool"),
                fs("confirmedAt", "timestamptz"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("assignmentID_id", "int8"),
                fs("confirmedBy_id", "int8"),
                fs("disputeID_id", "int8"),
            ],
            fks={
                "assignmentID_id": "job_worker_assignments",
                "confirmedBy_id": "accounts_accounts",
                "disputeID_id": "job_disputes",
            },
        ),
        "job_reviews": TableSpec(
            name="job_reviews",
            pk="reviewID",
            fields=[
                fs("reviewID", "int8"),
                fs("reviewerType", "varchar"),
                fs("rating", "numeric"),
                fs("comment", "text"),
                fs("status", "varchar"),
                fs("isFlagged", "bool"),
                fs("flagReason", "text"),
                fs("flaggedAt", "timestamptz"),
                fs("helpfulCount", "int4"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("flaggedBy_id", "int8"),
                fs("jobID_id", "int8"),
                fs("revieweeID_id", "int8"),
                fs("reviewerID_id", "int8"),
                fs("revieweeAgencyID_id", "int8"),
                fs("revieweeEmployeeID_id", "int8"),
                fs("revieweeProfileID_id", "int8"),
                fs("rating_communication", "numeric"),
                fs("rating_professionalism", "numeric"),
                fs("rating_punctuality", "numeric"),
                fs("rating_quality", "numeric"),
                fs("agency_response", "text"),
                fs("agency_response_at", "timestamptz"),
                fs("backjob_edit_deadline", "timestamptz"),
            ],
            fks={
                "flaggedBy_id": "accounts_accounts",
                "jobID_id": "jobs",
                "revieweeID_id": "accounts_accounts",
                "reviewerID_id": "accounts_accounts",
                "revieweeAgencyID_id": "accounts_agency",
                "revieweeEmployeeID_id": "agency_employees",
                "revieweeProfileID_id": "accounts_profile",
            },
        ),
        "review_skill_tags": TableSpec(
            name="review_skill_tags",
            pk="tagID",
            fields=[
                fs("tagID", "int8"),
                fs("createdAt", "timestamptz"),
                fs("reviewID_id", "int8"),
                fs("workerSpecializationID_id", "int8"),
            ],
            fks={
                "reviewID_id": "job_reviews",
                "workerSpecializationID_id": "accounts_workerspecialization",
            },
        ),
        "job_materials": TableSpec(
            name="job_materials",
            pk="jobMaterialID",
            fields=[
                fs("jobMaterialID", "int8"),
                fs("name", "varchar"),
                fs("description", "text"),
                fs("quantity", "int4"),
                fs("unit", "varchar"),
                fs("source", "varchar"),
                fs("purchase_price", "numeric"),
                fs("receipt_image_url", "varchar"),
                fs("client_approved", "bool"),
                fs("client_approved_at", "timestamptz"),
                fs("client_rejected", "bool"),
                fs("rejection_reason", "text"),
                fs("added_by", "varchar"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("jobID_id", "int8"),
                fs("workerMaterialID_id", "int8"),
            ],
            fks={"jobID_id": "jobs", "workerMaterialID_id": "worker_materials"},
        ),
        "job_photos": TableSpec(
            name="job_photos",
            pk="photoID",
            fields=[
                fs("photoID", "int8"),
                fs("photoURL", "varchar"),
                fs("fileName", "varchar"),
                fs("uploadedAt", "timestamptz"),
                fs("jobID_id", "int8"),
            ],
            fks={"jobID_id": "jobs"},
        ),
        "daily_attendance": TableSpec(
            name="daily_attendance",
            pk="attendanceID",
            fields=[
                fs("attendanceID", "int8"),
                fs("date", "date"),
                fs("time_in", "timestamptz"),
                fs("time_out", "timestamptz"),
                fs("status", "varchar"),
                fs("worker_confirmed", "bool"),
                fs("worker_confirmed_at", "timestamptz"),
                fs("client_confirmed", "bool"),
                fs("client_confirmed_at", "timestamptz"),
                fs("amount_earned", "numeric"),
                fs("payment_processed", "bool"),
                fs("payment_processed_at", "timestamptz"),
                fs("notes", "text"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("jobID_id", "int8"),
                fs("workerID_id", "int8"),
                fs("assignmentID_id", "int8"),
                fs("employeeID_id", "int8"),
                fs("absent_penalty_amount", "numeric"),
                fs("absent_penalty_applied", "bool"),
                fs("absent_penalty_applied_at", "timestamptz"),
                fs("absent_penalty_percent", "numeric"),
                fs("cash_payment_proof_url", "varchar"),
                fs("cash_payment_verified", "bool"),
                fs("cash_payment_verified_at", "timestamptz"),
                fs("cash_proof_uploaded_at", "timestamptz"),
                fs("payment_method", "varchar"),
            ],
            fks={
                "jobID_id": "jobs",
                "workerID_id": "accounts_workerprofile",
                "assignmentID_id": "job_worker_assignments",
                "employeeID_id": "agency_employees",
            },
        ),
        "daily_job_extensions": TableSpec(
            name="daily_job_extensions",
            pk="extensionID",
            fields=[
                fs("extensionID", "int8"),
                fs("additional_days", "int4"),
                fs("additional_escrow", "numeric"),
                fs("reason", "text"),
                fs("status", "varchar"),
                fs("requested_by", "varchar"),
                fs("client_approved", "bool"),
                fs("client_approved_at", "timestamptz"),
                fs("worker_approved", "bool"),
                fs("worker_approved_at", "timestamptz"),
                fs("escrow_collected", "bool"),
                fs("escrow_collected_at", "timestamptz"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("jobID_id", "int8"),
                fs("requestedByUser_id", "int8"),
            ],
            fks={"jobID_id": "jobs", "requestedByUser_id": "accounts_accounts"},
        ),
        "daily_rate_changes": TableSpec(
            name="daily_rate_changes",
            pk="changeID",
            fields=[
                fs("changeID", "int8"),
                fs("old_rate", "numeric"),
                fs("new_rate", "numeric"),
                fs("reason", "text"),
                fs("effective_date", "date"),
                fs("status", "varchar"),
                fs("requested_by", "varchar"),
                fs("client_approved", "bool"),
                fs("client_approved_at", "timestamptz"),
                fs("worker_approved", "bool"),
                fs("worker_approved_at", "timestamptz"),
                fs("escrow_adjusted", "bool"),
                fs("escrow_adjustment_amount", "numeric"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("jobID_id", "int8"),
                fs("requestedByUser_id", "int8"),
            ],
            fks={"jobID_id": "jobs", "requestedByUser_id": "accounts_accounts"},
        ),
        "daily_skip_day_requests": TableSpec(
            name="daily_skip_day_requests",
            pk="skipRequestID",
            fields=[
                fs("skipRequestID", "int8"),
                fs("request_date", "date"),
                fs("status", "varchar"),
                fs("requested_by", "varchar"),
                fs("requested_account_ids", "jsonb"),
                fs("requested_count", "int4"),
                fs("total_required", "int4"),
                fs("requires_all_team_workers", "bool"),
                fs("all_workers_requested", "bool"),
                fs("reviewedAt", "timestamptz"),
                fs("client_rejection_reason", "text"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("jobID_id", "int8"),
                fs("requestedByUser_id", "int8"),
                fs("reviewedByUser_id", "int8"),
                fs("target_employee_id", "int8"),
                fs("target_type", "varchar"),
                fs("target_worker_account_id", "int8"),
            ],
            fks={
                "jobID_id": "jobs",
                "requestedByUser_id": "accounts_accounts",
                "reviewedByUser_id": "accounts_accounts",
                "target_employee_id": "agency_employees",
                "target_worker_account_id": "accounts_accounts",
            },
        ),
        # MODULE 5
        "accounts_kyc": TableSpec(
            name="accounts_kyc",
            pk="kycID",
            fields=[
                fs("kycID", "int8"),
                fs("kyc_status", "varchar"),
                fs("reviewedAt", "timestamptz"),
                fs("notes", "text"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("accountFK_id", "int8"),
                fs("reviewedBy_id", "int8"),
                fs("rejectionCategory", "varchar"),
                fs("rejectionReason", "text"),
                fs("resubmissionCount", "int4"),
                fs("maxResubmissions", "int4"),
            ],
            fks={"accountFK_id": "accounts_accounts", "reviewedBy_id": "accounts_accounts"},
        ),
        "accounts_kycfiles": TableSpec(
            name="accounts_kycfiles",
            pk="kycFileID",
            fields=[
                fs("kycFileID", "int8"),
                fs("idType", "varchar"),
                fs("fileURL", "varchar"),
                fs("fileName", "varchar"),
                fs("fileSize", "int4"),
                fs("uploadedAt", "timestamptz"),
                fs("kycID_id", "int8"),
                fs("ai_verification_status", "varchar"),
                fs("face_detected", "bool"),
                fs("face_count", "int4"),
                fs("face_confidence", "float8"),
                fs("ocr_text", "text"),
                fs("ocr_confidence", "float8"),
                fs("quality_score", "float8"),
                fs("ai_confidence_score", "float8"),
                fs("ai_rejection_reason", "varchar"),
                fs("ai_rejection_message", "varchar"),
                fs("ai_warnings", "jsonb"),
                fs("ai_details", "jsonb"),
                fs("verified_at", "timestamptz"),
            ],
            fks={"kycID_id": "accounts_kyc"},
        ),
        "kyc_extracted_data": TableSpec(
            name="kyc_extracted_data",
            pk="extractedDataID",
            fields=[
                fs("extractedDataID", "int8"),
                fs("extracted_full_name", "varchar"),
                fs("extracted_first_name", "varchar"),
                fs("extracted_middle_name", "varchar"),
                fs("extracted_last_name", "varchar"),
                fs("extracted_birth_date", "date"),
                fs("extracted_address", "text"),
                fs("extracted_id_number", "varchar"),
                fs("extracted_id_type", "varchar"),
                fs("extracted_expiry_date", "date"),
                fs("extracted_nationality", "varchar"),
                fs("extracted_sex", "varchar"),
                fs("confidence_full_name", "float8"),
                fs("confidence_birth_date", "float8"),
                fs("confidence_address", "float8"),
                fs("confidence_id_number", "float8"),
                fs("overall_confidence", "float8"),
                fs("confirmed_full_name", "varchar"),
                fs("confirmed_first_name", "varchar"),
                fs("confirmed_middle_name", "varchar"),
                fs("confirmed_last_name", "varchar"),
                fs("confirmed_birth_date", "date"),
                fs("confirmed_address", "text"),
                fs("confirmed_id_number", "varchar"),
                fs("extraction_status", "varchar"),
                fs("extraction_source", "varchar"),
                fs("user_edited_fields", "jsonb"),
                fs("confirmed_at", "timestamptz"),
                fs("extracted_at", "timestamptz"),
                fs("raw_extraction_data", "jsonb"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("kycID_id", "int8"),
                fs("extracted_place_of_birth", "varchar"),
                fs("extracted_clearance_number", "varchar"),
                fs("extracted_clearance_type", "varchar"),
                fs("extracted_clearance_issue_date", "date"),
                fs("extracted_clearance_validity_date", "date"),
                fs("confidence_place_of_birth", "float8"),
                fs("confidence_clearance_number", "float8"),
                fs("confirmed_nationality", "varchar"),
                fs("confirmed_sex", "varchar"),
                fs("confirmed_place_of_birth", "varchar"),
                fs("confirmed_clearance_number", "varchar"),
                fs("confirmed_clearance_type", "varchar"),
                fs("confirmed_clearance_issue_date", "date"),
                fs("confirmed_clearance_validity_date", "date"),
                fs("face_match_completed", "bool"),
                fs("face_match_score", "float8"),
            ],
            fks={"kycID_id": "accounts_kyc"},
            unique_fks={"kycID_id"},
        ),
        "agency_agencykyc": TableSpec(
            name="agency_agencykyc",
            pk="agencyKycID",
            fields=[
                fs("agencyKycID", "int8"),
                fs("status", "varchar"),
                fs("reviewedAt", "timestamptz"),
                fs("notes", "varchar"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("accountFK_id", "int8"),
                fs("reviewedBy_id", "int8"),
                fs("rejectionCategory", "varchar"),
                fs("rejectionReason", "text"),
                fs("resubmissionCount", "int4"),
                fs("maxResubmissions", "int4"),
                fs("face_similarity_score", "float8"),
            ],
            fks={"accountFK_id": "accounts_accounts", "reviewedBy_id": "accounts_accounts"},
        ),
        "agency_agencykycfile": TableSpec(
            name="agency_agencykycfile",
            pk="fileID",
            fields=[
                fs("fileID", "int8"),
                fs("fileType", "varchar"),
                fs("fileURL", "varchar"),
                fs("fileName", "varchar"),
                fs("fileSize", "int4"),
                fs("uploadedAt", "timestamptz"),
                fs("agencyKyc_id", "int8"),
                fs("ai_verification_status", "varchar"),
                fs("face_detected", "bool"),
                fs("face_count", "int4"),
                fs("face_confidence", "float8"),
                fs("ocr_text", "text"),
                fs("ocr_confidence", "float8"),
                fs("quality_score", "float8"),
                fs("ai_confidence_score", "float8"),
                fs("ai_rejection_reason", "varchar"),
                fs("ai_rejection_message", "varchar"),
                fs("ai_warnings", "jsonb"),
                fs("ai_details", "jsonb"),
                fs("verified_at", "timestamptz"),
            ],
            fks={"agencyKyc_id": "agency_agencykyc"},
        ),
        "agency_kyc_extracted_data": TableSpec(
            name="agency_kyc_extracted_data",
            pk="extractedDataID",
            fields=[
                fs("extractedDataID", "int8"),
                fs("extracted_business_name", "varchar"),
                fs("extracted_business_type", "varchar"),
                fs("extracted_business_address", "text"),
                fs("extracted_permit_number", "varchar"),
                fs("extracted_permit_issue_date", "date"),
                fs("extracted_permit_expiry_date", "date"),
                fs("extracted_dti_number", "varchar"),
                fs("extracted_sec_number", "varchar"),
                fs("extracted_tin", "varchar"),
                fs("extracted_rep_full_name", "varchar"),
                fs("extracted_rep_id_number", "varchar"),
                fs("extracted_rep_id_type", "varchar"),
                fs("extracted_rep_birth_date", "date"),
                fs("extracted_rep_address", "text"),
                fs("confirmed_business_name", "varchar"),
                fs("confirmed_business_type", "varchar"),
                fs("confirmed_business_address", "text"),
                fs("confirmed_permit_number", "varchar"),
                fs("confirmed_permit_issue_date", "date"),
                fs("confirmed_permit_expiry_date", "date"),
                fs("confirmed_dti_number", "varchar"),
                fs("confirmed_sec_number", "varchar"),
                fs("confirmed_tin", "varchar"),
                fs("confirmed_rep_full_name", "varchar"),
                fs("confirmed_rep_id_number", "varchar"),
                fs("confirmed_rep_birth_date", "date"),
                fs("confirmed_rep_address", "text"),
                fs("confidence_business_name", "float8"),
                fs("confidence_business_address", "float8"),
                fs("confidence_permit_number", "float8"),
                fs("confidence_rep_name", "float8"),
                fs("overall_confidence", "float8"),
                fs("extraction_status", "varchar"),
                fs("extraction_source", "varchar"),
                fs("extracted_at", "timestamptz"),
                fs("confirmed_at", "timestamptz"),
                fs("user_edited_fields", "jsonb"),
                fs("raw_extraction_data", "jsonb"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("agencyKyc_id", "int8"),
            ],
            fks={"agencyKyc_id": "agency_agencykyc"},
            unique_fks={"agencyKyc_id"},
        ),
        "adminpanel_kyclogs": TableSpec(
            name="adminpanel_kyclogs",
            pk="kycLogID",
            fields=[
                fs("kycLogID", "int8"),
                fs("action", "varchar"),
                fs("reviewedAt", "timestamptz"),
                fs("reason", "text"),
                fs("userEmail", "varchar"),
                fs("userAccountID", "int8"),
                fs("createdAt", "timestamptz"),
                fs("accountFK_id", "int8"),
                fs("kycID", "int8"),
                fs("reviewedBy_id", "int8"),
                fs("kycType", "varchar"),
            ],
            fks={"accountFK_id": "accounts_accounts", "reviewedBy_id": "accounts_accounts"},
        ),
        # MODULE 6
        "adminpanel_adminaccount": TableSpec(
            name="adminpanel_adminaccount",
            pk="adminID",
            fields=[
                fs("adminID", "int8"),
                fs("role", "varchar"),
                fs("permissions", "jsonb"),
                fs("isActive", "bool"),
                fs("lastLogin", "timestamptz"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("accountFK_id", "int8"),
            ],
            fks={"accountFK_id": "accounts_accounts"},
            unique_fks={"accountFK_id"},
        ),
        "adminpanel_auditlog": TableSpec(
            name="adminpanel_auditlog",
            pk="auditLogID",
            fields=[
                fs("auditLogID", "int8"),
                fs("adminEmail", "varchar"),
                fs("action", "varchar"),
                fs("entityType", "varchar"),
                fs("entityID", "varchar"),
                fs("details", "jsonb"),
                fs("beforeValue", "jsonb"),
                fs("afterValue", "jsonb"),
                fs("ipAddress", "inet"),
                fs("userAgent", "text"),
                fs("createdAt", "timestamptz"),
                fs("adminFK_id", "int8"),
            ],
            fks={"adminFK_id": "accounts_accounts"},
        ),
        "adminpanel_supportticket": TableSpec(
            name="adminpanel_supportticket",
            pk="ticketID",
            fields=[
                fs("ticketID", "int8"),
                fs("subject", "varchar"),
                fs("category", "varchar"),
                fs("priority", "varchar"),
                fs("status", "varchar"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("lastReplyAt", "timestamptz"),
                fs("resolvedAt", "timestamptz"),
                fs("assignedTo_id", "int8"),
                fs("userFK_id", "int8"),
                fs("agencyFK_id", "int8"),
                fs("ticketType", "varchar"),
                fs("platform", "varchar"),
                fs("deviceInfo", "text"),
                fs("appVersion", "varchar"),
            ],
            fks={
                "assignedTo_id": "accounts_accounts",
                "userFK_id": "accounts_accounts",
                "agencyFK_id": "accounts_agency",
            },
        ),
        "adminpanel_supportticketreply": TableSpec(
            name="adminpanel_supportticketreply",
            pk="replyID",
            fields=[
                fs("replyID", "int8"),
                fs("content", "text"),
                fs("isSystemMessage", "bool"),
                fs("attachmentURL", "varchar"),
                fs("createdAt", "timestamptz"),
                fs("senderFK_id", "int8"),
                fs("ticketFK_id", "int8"),
            ],
            fks={
                "senderFK_id": "accounts_accounts",
                "ticketFK_id": "adminpanel_supportticket",
            },
        ),
        "adminpanel_userreport": TableSpec(
            name="adminpanel_userreport",
            pk="reportID",
            fields=[
                fs("reportID", "int8"),
                fs("reportType", "varchar"),
                fs("reason", "varchar"),
                fs("description", "text"),
                fs("relatedContentID", "int8"),
                fs("status", "varchar"),
                fs("adminNotes", "text"),
                fs("actionTaken", "varchar"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("resolvedAt", "timestamptz"),
                fs("reportedUserFK_id", "int8"),
                fs("reporterFK_id", "int8"),
                fs("reviewedBy_id", "int8"),
            ],
            fks={
                "reportedUserFK_id": "accounts_accounts",
                "reporterFK_id": "accounts_accounts",
                "reviewedBy_id": "accounts_accounts",
            },
        ),
        "adminpanel_platformsettings": TableSpec(
            name="adminpanel_platformsettings",
            pk="settingsID",
            fields=[
                fs("settingsID", "int8"),
                fs("platformFeePercentage", "numeric"),
                fs("escrowHoldingDays", "int4"),
                fs("maxJobBudget", "numeric"),
                fs("minJobBudget", "numeric"),
                fs("workerVerificationRequired", "bool"),
                fs("autoApproveKYC", "bool"),
                fs("kycDocumentExpiryDays", "int4"),
                fs("maintenanceMode", "bool"),
                fs("sessionTimeoutMinutes", "int4"),
                fs("maxUploadSizeMB", "int4"),
                fs("lastUpdated", "timestamptz"),
                fs("updatedBy_id", "int8"),
                fs("kycAutoApproveMinConfidence", "numeric"),
                fs("kycFaceMatchMinSimilarity", "numeric"),
                fs("kycRequireUserConfirmation", "bool"),
            ],
            fks={"updatedBy_id": "accounts_accounts"},
        ),
        "adminpanel_cannedresponse": TableSpec(
            name="adminpanel_cannedresponse",
            pk="responseID",
            fields=[
                fs("responseID", "int8"),
                fs("title", "varchar"),
                fs("content", "text"),
                fs("category", "varchar"),
                fs("shortcuts", "jsonb"),
                fs("usageCount", "int4"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("createdBy_id", "int8"),
            ],
            fks={"createdBy_id": "accounts_accounts"},
        ),
        "adminpanel_contentmoderationterm": TableSpec(
            name="adminpanel_contentmoderationterm",
            pk="termID",
            fields=[
                fs("termID", "int8"),
                fs("term", "varchar"),
                fs("normalizedTerm", "varchar"),
                fs("isActive", "bool"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("createdBy_id", "int8"),
                fs("updatedBy_id", "int8"),
            ],
            fks={"createdBy_id": "accounts_accounts", "updatedBy_id": "accounts_accounts"},
        ),
        "adminpanel_faq": TableSpec(
            name="adminpanel_faq",
            pk="faqID",
            fields=[
                fs("faqID", "int8"),
                fs("question", "varchar"),
                fs("answer", "text"),
                fs("category", "varchar"),
                fs("sortOrder", "int4"),
                fs("viewCount", "int4"),
                fs("isPublished", "bool"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
            ],
        ),
        "adminpanel_systemroles": TableSpec(
            name="adminpanel_systemroles",
            pk="systemRoleID",
            fields=[
                fs("systemRoleID", "int8"),
                fs("systemRole", "varchar"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("accountID_id", "int8"),
            ],
            fks={"accountID_id": "accounts_accounts"},
        ),
        "accounts_notification": TableSpec(
            name="accounts_notification",
            pk="notificationID",
            fields=[
                fs("notificationID", "int8"),
                fs("notificationType", "varchar"),
                fs("title", "varchar"),
                fs("message", "text"),
                fs("isRead", "bool"),
                fs("relatedKYCLogID", "int8"),
                fs("createdAt", "timestamptz"),
                fs("readAt", "timestamptz"),
                fs("accountFK_id", "int8"),
                fs("relatedJobID", "int8"),
                fs("relatedApplicationID", "int8"),
                fs("profile_type", "varchar"),
            ],
            fks={"accountFK_id": "accounts_accounts"},
        ),
        "conversation": TableSpec(
            name="conversation",
            pk="conversationID",
            fields=[
                fs("conversationID", "int8"),
                fs("lastMessageText", "text"),
                fs("lastMessageTime", "timestamptz"),
                fs("unreadCountClient", "int4"),
                fs("unreadCountWorker", "int4"),
                fs("status", "varchar"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("client_id", "int8"),
                fs("lastMessageSender_id", "int8"),
                fs("relatedJobPosting_id", "int8"),
                fs("worker_id", "int8"),
                fs("archivedByClient", "bool"),
                fs("archivedByWorker", "bool"),
                fs("agency_id", "int8"),
                fs("conversation_type", "varchar"),
            ],
            fks={
                "client_id": "accounts_profile",
                "lastMessageSender_id": "accounts_profile",
                "relatedJobPosting_id": "jobs",
                "worker_id": "accounts_profile",
                "agency_id": "accounts_agency",
            },
        ),
        "conversation_participants": TableSpec(
            name="conversation_participants",
            pk="participantID",
            fields=[
                fs("participantID", "int8"),
                fs("participant_type", "varchar"),
                fs("unread_count", "int4"),
                fs("is_archived", "bool"),
                fs("joined_at", "timestamptz"),
                fs("last_read_at", "timestamptz"),
                fs("conversation_id", "int8"),
                fs("profile_id", "int8"),
                fs("skill_slot_id", "int8"),
                fs("admin_account_id", "int8"),
            ],
            fks={
                "conversation_id": "conversation",
                "profile_id": "accounts_profile",
                "skill_slot_id": "job_skill_slots",
                "admin_account_id": "accounts_accounts",
            },
        ),
        "message": TableSpec(
            name="message",
            pk="messageID",
            fields=[
                fs("messageID", "int8"),
                fs("messageText", "text"),
                fs("messageType", "varchar"),
                fs("locationAddress", "varchar"),
                fs("locationLandmark", "varchar"),
                fs("locationLatitude", "numeric"),
                fs("locationLongitude", "numeric"),
                fs("isRead", "bool"),
                fs("readAt", "timestamptz"),
                fs("createdAt", "timestamptz"),
                fs("conversationID_id", "int8"),
                fs("sender_id", "int8"),
                fs("senderAgency_id", "int8"),
                fs("sender_admin_id", "int8"),
            ],
            fks={
                "conversationID_id": "conversation",
                "sender_id": "accounts_profile",
                "senderAgency_id": "accounts_agency",
                "sender_admin_id": "accounts_accounts",
            },
        ),
        "message_attachment": TableSpec(
            name="message_attachment",
            pk="attachmentID",
            fields=[
                fs("attachmentID", "int8"),
                fs("fileURL", "varchar"),
                fs("fileName", "varchar"),
                fs("fileSize", "int4"),
                fs("fileType", "varchar"),
                fs("uploadedAt", "timestamptz"),
                fs("messageID_id", "int8"),
            ],
            fks={"messageID_id": "message"},
        ),
        "accounts_transaction": TableSpec(
            name="accounts_transaction",
            pk="transactionID",
            fields=[
                fs("transactionID", "int8"),
                fs("transactionType", "varchar"),
                fs("amount", "numeric"),
                fs("balanceAfter", "numeric"),
                fs("status", "varchar"),
                fs("description", "varchar"),
                fs("referenceNumber", "varchar"),
                fs("paymentMethod", "varchar"),
                fs("createdAt", "timestamptz"),
                fs("completedAt", "timestamptz"),
                fs("relatedJobPosting_id", "int8"),
                fs("walletID_id", "int8"),
                fs("invoiceURL", "varchar"),
                fs("xenditExternalID", "varchar"),
                fs("xenditInvoiceID", "varchar"),
                fs("xenditPaymentChannel", "varchar"),
                fs("xenditPaymentID", "varchar"),
                fs("xenditPaymentMethod", "varchar"),
                fs("adminReferenceNumber", "varchar"),
                fs("processedAt", "timestamptz"),
                fs("processedByAdmin_id", "int8"),
                fs("paymongoPaymentId", "varchar"),
                fs("paymongoTransferId", "varchar"),
                fs("paymongoTransferStatus", "varchar"),
            ],
            fks={
                "relatedJobPosting_id": "jobs",
                "walletID_id": "accounts_wallet",
                "processedByAdmin_id": "accounts_accounts",
            },
        ),
        "agency_employees": TableSpec(
            name="agency_employees",
            pk="employeeID",
            fields=[
                fs("employeeID", "int8"),
                fs("name", "varchar"),
                fs("email", "varchar"),
                fs("role", "varchar"),
                fs("avatar", "varchar"),
                fs("rating", "numeric"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("agency_id", "int8"),
                fs("employeeOfTheMonth", "bool"),
                fs("employeeOfTheMonthDate", "timestamptz"),
                fs("employeeOfTheMonthReason", "text"),
                fs("isActive", "bool"),
                fs("lastRatingUpdate", "timestamptz"),
                fs("totalEarnings", "numeric"),
                fs("totalJobsCompleted", "int4"),
                fs("firstName", "varchar"),
                fs("middleName", "varchar"),
                fs("lastName", "varchar"),
                fs("specializations", "text"),
                fs("daily_rate", "numeric"),
                fs("hourly_rate", "numeric"),
                fs("is_available_daily_jobs", "bool"),
                fs("mobile", "varchar"),
            ],
            # Corrected audit mapping: references accounts_accounts(accountID), not accounts_agency.
            fks={"agency_id": "accounts_accounts"},
        ),
        "worker_certifications": TableSpec(
            name="worker_certifications",
            pk="certificationID",
            fields=[
                fs("certificationID", "int8"),
                fs("name", "varchar"),
                fs("issuing_organization", "varchar"),
                fs("issue_date", "date"),
                fs("expiry_date", "date"),
                fs("certificate_url", "varchar"),
                fs("is_verified", "bool"),
                fs("verified_at", "timestamptz"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("verified_by_id", "int8"),
                fs("workerID_id", "int8"),
                fs("specializationID_id", "int8"),
            ],
            # Corrected audit mapping: specializationID_id references accounts_workerspecialization(id).
            fks={
                "verified_by_id": "accounts_accounts",
                "workerID_id": "accounts_workerprofile",
                "specializationID_id": "accounts_workerspecialization",
            },
        ),
        "certification_logs": TableSpec(
            name="certification_logs",
            pk="certLogID",
            fields=[
                fs("certLogID", "int8"),
                fs("certificationID", "int8"),
                fs("action", "varchar"),
                fs("reviewedAt", "timestamptz"),
                fs("reason", "text"),
                fs("workerEmail", "varchar"),
                fs("workerAccountID", "int8"),
                fs("certificationName", "varchar"),
                fs("reviewedBy_id", "int8"),
                fs("workerID_id", "int8"),
            ],
            # Corrected audit mapping: workerID_id -> accounts_workerprofile.
            fks={"reviewedBy_id": "accounts_accounts", "workerID_id": "accounts_workerprofile"},
        ),
        "worker_materials": TableSpec(
            name="worker_materials",
            pk="materialID",
            fields=[
                fs("materialID", "int8"),
                fs("name", "varchar"),
                fs("description", "text"),
                fs("price", "numeric"),
                fs("unit", "varchar"),
                fs("image_url", "varchar"),
                fs("is_available", "bool"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("workerID_id", "int8"),
                fs("quantity", "numeric"),
                fs("categoryID_id", "int8"),
                fs("agencyID_id", "int8"),
            ],
            fks={
                "workerID_id": "accounts_workerprofile",
                "categoryID_id": "specializations",
                "agencyID_id": "accounts_agency",
            },
        ),
        "worker_portfolio": TableSpec(
            name="worker_portfolio",
            pk="portfolioID",
            fields=[
                fs("portfolioID", "int8"),
                fs("image_url", "varchar"),
                fs("caption", "text"),
                fs("display_order", "int4"),
                fs("file_name", "varchar"),
                fs("file_size", "int4"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("workerID_id", "int8"),
            ],
            fks={"workerID_id": "accounts_workerprofile"},
        ),
        "profiles_workerproduct": TableSpec(
            name="profiles_workerproduct",
            pk="productID",
            fields=[
                fs("productID", "int8"),
                fs("productName", "varchar"),
                fs("description", "text"),
                fs("price", "numeric"),
                fs("priceUnit", "varchar"),
                fs("inStock", "bool"),
                fs("stockQuantity", "int4"),
                fs("productImage", "varchar"),
                fs("isActive", "bool"),
                fs("createdAt", "timestamptz"),
                fs("updatedAt", "timestamptz"),
                fs("categoryID_id", "int8"),
                fs("workerID_id", "int8"),
            ],
            fks={
                "categoryID_id": "specializations",
                "workerID_id": "accounts_workerprofile",
            },
        ),
    }


def build_module_specs() -> List[ModuleSpec]:
    return [
        ModuleSpec(
            title="MODULE 2 - Profiles, Location, Wallet & Specializations",
            filename="erd_v2_module2_profiles.png",
            table_names=[
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
            n_cols=3,
        ),
        ModuleSpec(
            title="MODULE 3 - Jobs, Applications & Assignments",
            filename="erd_v2_module3_jobs.png",
            table_names=[
                "jobs",
                "job_skill_slots",
                "job_applications",
                "price_negotiations",
                "job_worker_assignments",
                "job_employee_assignments",
                "job_logs",
                "saved_jobs",
            ],
            n_cols=3,
        ),
        ModuleSpec(
            title="MODULE 4 - Disputes, Reviews, Daily Operations & Attendance",
            filename="erd_v2_module4_disputes.png",
            table_names=[
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
            n_cols=3,
        ),
        ModuleSpec(
            title="MODULE 5 - KYC Verification (Individual & Agency)",
            filename="erd_v2_module5_kyc.png",
            table_names=[
                "accounts_kyc",
                "accounts_kycfiles",
                "kyc_extracted_data",
                "agency_agencykyc",
                "agency_agencykycfile",
                "agency_kyc_extracted_data",
                "adminpanel_kyclogs",
            ],
            n_cols=2,
        ),
        ModuleSpec(
            title="MODULE 6 - Admin Panel, Messaging, Notifications & Worker Assets",
            filename="erd_v2_module6_admin.png",
            table_names=[
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
            n_cols=4,
        ),
    ]


class Theme:
    bg = "#FFFFFF"
    header = "#1F3B5B"
    border = "#2D3748"
    row_alt = "#F5F7FA"
    text = "#111827"
    fk_text = "#1E5AA8"
    rel_line = "#4A5568"
    pk_gold = "#D4AF37"
    external_bg = "#EEF2F7"


class Renderer:
    def __init__(self) -> None:
        self.margin = 40
        self.title_h = 70
        self.header_h = 30
        self.row_h = 18
        self.row_pad_x = 10
        self.col_gap = 55
        self.row_gap = 35
        self.ext_width = 260
        self.ext_gap = 40

        self.font_regular = self._load_font("DejaVuSans.ttf", 12)
        self.font_italic = self._load_font("DejaVuSans-Oblique.ttf", 12)
        self.font_bold = self._load_font("DejaVuSans-Bold.ttf", 12)
        self.font_title = self._load_font("DejaVuSans-Bold.ttf", 22)
        self.font_subtitle = self._load_font("DejaVuSans.ttf", 13)
        self.font_header = self._load_font("DejaVuSans-Bold.ttf", 13)
        self.font_pk = self._load_font("DejaVuSans-Bold.ttf", 10)
        self.font_external = self._load_font("DejaVuSans-Bold.ttf", 12)

    @staticmethod
    def _load_font(name: str, size: int) -> ImageFont.ImageFont:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            return ImageFont.load_default()

    def text_size(self, text: str, font: ImageFont.ImageFont) -> Tuple[int, int]:
        scratch = Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(scratch)
        l, t, r, b = draw.textbbox((0, 0), text, font=font)
        return r - l, b - t

    def table_dimensions(self, table: TableSpec) -> Tuple[int, int]:
        widest = self.text_size(table.name, self.font_header)[0]
        for fld in table.fields:
            text = self.field_display_text(table, fld)
            w, _ = self.text_size(text, self.font_regular)
            widest = max(widest, w)
        width = widest + self.row_pad_x * 2 + 65
        height = self.header_h + len(table.fields) * self.row_h + 2
        return width, height

    @staticmethod
    def field_display_text(table: TableSpec, fld: FieldSpec) -> str:
        if fld.name in table.fks:
            return f"{fld.name} | {fld.dtype} -> {table.fks[fld.name]}"
        return f"{fld.name} | {fld.dtype}"

    def layout_tables(
        self, tables: List[TableSpec], n_cols: int
    ) -> Tuple[Dict[str, Tuple[int, int]], Dict[str, Tuple[int, int]], int, int]:
        dims = {tbl.name: self.table_dimensions(tbl) for tbl in tables}
        col_items: List[List[Tuple[str, int]]] = [[] for _ in range(n_cols)]
        col_heights = [self.margin + self.title_h for _ in range(n_cols)]

        for tbl in tables:
            col = min(range(n_cols), key=lambda idx: col_heights[idx])
            col_items[col].append((tbl.name, col_heights[col]))
            col_heights[col] += dims[tbl.name][1] + self.row_gap

        col_widths = []
        for col in range(n_cols):
            if col_items[col]:
                col_widths.append(max(dims[name][0] for name, _ in col_items[col]))
            else:
                col_widths.append(400)

        x_positions = []
        x = self.margin
        for width in col_widths:
            x_positions.append(x)
            x += width + self.col_gap

        positions: Dict[str, Tuple[int, int]] = {}
        for col in range(n_cols):
            for name, y in col_items[col]:
                table_w = dims[name][0]
                offset = (col_widths[col] - table_w) // 2
                positions[name] = (x_positions[col] + offset, y)

        canvas_w = x - self.col_gap + self.margin
        canvas_h = max(col_heights) + self.margin
        return positions, dims, canvas_w, canvas_h

    @staticmethod
    def draw_crowfoot(draw: ImageDraw.ImageDraw, x: int, y: int, direction: int) -> None:
        d = 8 * direction
        draw.line((x, y, x + d, y), fill=Theme.rel_line, width=2)
        draw.line((x, y, x + d, y - 6), fill=Theme.rel_line, width=2)
        draw.line((x, y, x + d, y + 6), fill=Theme.rel_line, width=2)

    @staticmethod
    def draw_one_marker(draw: ImageDraw.ImageDraw, x: int, y: int, direction: int) -> None:
        draw.line((x, y - 6, x, y + 6), fill=Theme.rel_line, width=2)
        draw.line((x, y, x + 8 * direction, y), fill=Theme.rel_line, width=2)

    def draw_pk_badge(self, draw: ImageDraw.ImageDraw, right_x: int, y_top: int) -> None:
        badge_w = 26
        badge_h = 12
        x0 = right_x - badge_w - 6
        y0 = y_top + (self.row_h - badge_h) // 2
        x1 = x0 + badge_w
        y1 = y0 + badge_h
        draw.rounded_rectangle((x0, y0, x1, y1), radius=3, fill=Theme.pk_gold, outline="#B38B1D")
        draw.text((x0 + 5, y0 + 1), "PK", fill="#1A1A1A", font=self.font_pk)

    def render_module(
        self,
        module: ModuleSpec,
        all_tables: Dict[str, TableSpec],
        out_dir: Path,
    ) -> Path:
        tables = [all_tables[name] for name in module.table_names]
        table_set = {t.name for t in tables}

        positions, dims, base_w, base_h = self.layout_tables(tables, module.n_cols)

        external_targets: List[str] = sorted(
            {
                target
                for tbl in tables
                for target in tbl.fks.values()
                if target not in table_set
            }
        )

        ext_positions: Dict[str, Tuple[int, int, int, int]] = {}
        ext_x = base_w + self.ext_gap
        ext_y = self.margin + self.title_h
        ext_h = 26
        for name in external_targets:
            ext_positions[name] = (ext_x, ext_y, self.ext_width, ext_h)
            ext_y += ext_h + 10

        canvas_w = base_w + (self.ext_gap + self.ext_width + self.margin if external_targets else 0)
        canvas_h = max(base_h, ext_y + self.margin)

        img = Image.new("RGB", (canvas_w, canvas_h), Theme.bg)
        draw = ImageDraw.Draw(img)

        draw.text((self.margin, 18), module.title, fill="#0F172A", font=self.font_title)
        draw.text(
            (self.margin, 46),
            f"Tables: {len(module.table_names)}",
            fill="#475569",
            font=self.font_subtitle,
        )

        # Draw external refs first so relationship lines can connect visibly.
        for name, (x, y, w, h) in ext_positions.items():
            draw.rounded_rectangle((x, y, x + w, y + h), radius=4, fill=Theme.external_bg, outline=Theme.border)
            draw.text((x + 8, y + 5), f"Ref: {name}", fill="#334155", font=self.font_external)

        # Draw tables and capture row anchors.
        row_anchors: Dict[Tuple[str, str], Tuple[int, int]] = {}
        pk_anchors: Dict[str, Tuple[int, int]] = {}
        for tbl in tables:
            x, y = positions[tbl.name]
            w, h = dims[tbl.name]

            draw.rectangle((x, y, x + w, y + h), fill=Theme.bg, outline=Theme.border, width=2)
            draw.rectangle((x, y, x + w, y + self.header_h), fill=Theme.header, outline=Theme.border, width=2)
            draw.text((x + 8, y + 7), tbl.name, fill="#FFFFFF", font=self.font_header)

            for idx, fld in enumerate(tbl.fields):
                y0 = y + self.header_h + idx * self.row_h
                y1 = y0 + self.row_h
                row_color = Theme.row_alt if idx % 2 else Theme.bg
                draw.rectangle((x + 1, y0, x + w - 1, y1), fill=row_color)
                draw.line((x, y1, x + w, y1), fill="#E5E7EB", width=1)

                is_pk = fld.name == tbl.pk
                is_fk = fld.name in tbl.fks
                txt = self.field_display_text(tbl, fld)
                font = self.font_bold if is_pk else (self.font_italic if is_fk else self.font_regular)
                color = self.fk_text if is_fk else Theme.text
                draw.text((x + self.row_pad_x, y0 + 3), txt, fill=color, font=font)

                if is_pk:
                    self.draw_pk_badge(draw, x + w, y0)
                    pk_anchors[tbl.name] = (x + 1, y0 + self.row_h // 2)

                row_anchors[(tbl.name, fld.name)] = (x + w - 1, y0 + self.row_h // 2)

            if tbl.name not in pk_anchors:
                pk_anchors[tbl.name] = (x + 1, y + self.header_h + self.row_h // 2)

        # Draw relationships using crow's foot notation from FK side.
        for tbl in tables:
            sx, sy = positions[tbl.name]
            sw, _ = dims[tbl.name]
            for field_name, target in tbl.fks.items():
                source = row_anchors[(tbl.name, field_name)]
                src_x, src_y = source

                if target in table_set:
                    tx, ty = pk_anchors[target]
                else:
                    ex, ey, _, eh = ext_positions[target]
                    tx, ty = ex, ey + eh // 2

                direction = 1 if tx >= src_x else -1
                mid_x = src_x + (tx - src_x) // 2

                draw.line((src_x, src_y, mid_x, src_y), fill=Theme.rel_line, width=2)
                draw.line((mid_x, src_y, mid_x, ty), fill=Theme.rel_line, width=2)
                draw.line((mid_x, ty, tx, ty), fill=Theme.rel_line, width=2)

                if field_name in tbl.unique_fks:
                    self.draw_one_marker(draw, src_x, src_y, direction)
                else:
                    self.draw_crowfoot(draw, src_x, src_y, direction)
                self.draw_one_marker(draw, tx, ty, -direction)

        output_path = out_dir / module.filename
        img.save(output_path)
        return output_path

    @property
    def fk_text(self) -> str:
        return Theme.fk_text


def main() -> None:
    out_dir = Path(".").resolve()
    tables = build_table_specs()
    modules = build_module_specs()
    renderer = Renderer()

    for module in modules:
        output = renderer.render_module(module, tables, out_dir)
        print(f"Generated: {output.name}")


if __name__ == "__main__":
    main()
