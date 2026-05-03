"""
Generate ERD diagrams (Modules 2-6) for the JobMatch PostgreSQL schema.

Style:
- White background, professional
- Each table = HTML-table with a dark header (white bold table name)
- Rows show: [PK/FK badge] | field name | data type [-> target]
- PK fields: bold black, gold "PK" badge
- FK fields: blue italic, "FK" badge, with arrow label "-> target_table"
- Alternating white / very light gray rows
- Crow's foot notation for relationship lines (in-module FKs)
- Title at top, table-count note
"""

from graphviz import Digraph
import os

# ---------------------------------------------------------------------------
# Style constants
# ---------------------------------------------------------------------------
BG = "white"
ROW_A = "white"
ROW_B = "#F4F4F6"          # very light gray
HEADER_TEXT = "white"
PK_BADGE_BG = "#E8B530"     # gold
PK_BADGE_FG = "#3A2A00"
FK_BADGE_BG = "#DCE9F8"
FK_BADGE_FG = "#1D4FB1"
PK_FIELD_FG = "#111111"
FK_FIELD_FG = "#1D4FB1"     # blue
FIELD_FG    = "#1F1F1F"
TYPE_FG     = "#5A5A5A"
TARGET_FG   = "#1D4FB1"
BORDER      = "#B7B7B7"
TABLE_BORDER = "#999999"
FONT        = "Helvetica"

MODULE_COLORS = {
    2: "#1F6FB2",   # blue
    3: "#6E3FA0",   # purple
    4: "#B23A48",   # red
    5: "#2E7D5B",   # green
    6: "#374151",   # dark slate
}

# Crow's-foot edge style mapping
# child end (the table containing the FK) -> "many"
# parent end (the table being referenced)  -> "one"
CROW_HEAD = "crow"      # many
CROW_TAIL_REQ = "tee"   # exactly one (NOT NULL FK)
CROW_TAIL_OPT = "teeodot"  # zero or one (nullable FK)


# ---------------------------------------------------------------------------
# Field structure: (name, type, kind, target)
#   kind: 'pk', 'fk', 'pkfk', 'plain'
#   target: only used for fk / pkfk -> target_table_name (or None)
#   For unique FK indicate by adding ' UNIQUE' to type or note (visually we just show the type; the relationship will be one-to-one based on edge spec)
# ---------------------------------------------------------------------------

def F(name, dtype, kind="plain", target=None, note=None):
    return {"name": name, "type": dtype, "kind": kind, "target": target, "note": note}


# ---------------------------------------------------------------------------
# MODULE 2 - Profiles, Location, Wallet & Specializations
# ---------------------------------------------------------------------------
MODULE2 = {
    "title": "MODULE 2 — Profiles, Location, Wallet & Specializations",
    "tables": {
        "accounts_profile": [
            F("profileID", "int8", "pk"),
            F("profileImg", "varchar"),
            F("firstName", "varchar"),
            F("lastName", "varchar"),
            F("middleName", "varchar"),
            F("contactNum", "varchar"),
            F("birthDate", "date"),
            F("profileType", "varchar"),
            F("latitude", "numeric"),
            F("longitude", "numeric"),
            F("location_sharing_enabled", "bool"),
            F("location_updated_at", "timestamptz"),
            F("accountFK_id", "int8", "fk", "accounts_accounts"),
        ],
        "accounts_workerprofile": [
            F("id", "int8", "pk"),
            F("description", "varchar"),
            F("workerRating", "int4"),
            F("totalEarningGross", "numeric"),
            F("availability_status", "varchar"),
            F("bio", "varchar"),
            F("hourly_rate", "numeric"),
            F("daily_rate", "numeric"),
            F("profile_completion_percentage", "int4"),
            F("soft_skills", "text"),
            F("is_available_daily_jobs", "bool"),
            F("profileID_id", "int8 UNIQUE", "fk", "accounts_profile"),
        ],
        "accounts_clientprofile": [
            F("id", "int8", "pk"),
            F("description", "varchar"),
            F("totalJobsPosted", "int4"),
            F("clientRating", "int4"),
            F("activeJobsCount", "int4"),
            F("profileID_id", "int8 UNIQUE", "fk", "accounts_profile"),
        ],
        "accounts_agency": [
            F("agencyId", "int8", "pk"),
            F("businessName", "varchar"),
            F("businessDesc", "varchar"),
            F("contactNumber", "varchar"),
            F("city", "varchar"),
            F("country", "varchar"),
            F("postal_code", "varchar"),
            F("province", "varchar"),
            F("street_address", "varchar"),
            F("barangay", "varchar"),
            F("createdAt", "timestamptz"),
            F("accountFK_id", "int8", "fk", "accounts_accounts"),
        ],
        "accounts_barangay": [
            F("barangayID", "int4", "pk"),
            F("name", "varchar"),
            F("zipCode", "varchar"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("city_id", "int4", "fk", "accounts_city"),
        ],
        "accounts_city": [
            F("cityID", "int4", "pk"),
            F("name", "varchar"),
            F("province", "varchar"),
            F("region", "varchar"),
            F("zipCode", "varchar"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
        ],
        "specializations": [
            F("specializationID", "int8", "pk"),
            F("specializationName", "varchar"),
            F("averageProjectCostMax", "numeric"),
            F("averageProjectCostMin", "numeric"),
            F("description", "text"),
            F("minimumRate", "numeric"),
            F("rateType", "varchar"),
            F("skillLevel", "varchar"),
            F("is_custom", "bool"),
            F("created_by_agency_id", "int8", "fk", "accounts_agency"),
            F("created_by_worker_id", "int8", "fk", "accounts_accounts"),
        ],
        "accounts_workerspecialization": [
            F("id", "int8", "pk"),
            F("experienceYears", "int4"),
            F("certification", "varchar"),
            F("skillType", "varchar"),
            F("displayOrder", "int4"),
            F("workerID_id", "int8", "fk", "accounts_workerprofile"),
            F("specializationID_id", "int8", "fk", "specializations"),
        ],
        "accounts_interestedjobs": [
            F("id", "int8", "pk"),
            F("clientID_id", "int8", "fk", "accounts_clientprofile"),
            F("specializationID_id", "int8", "fk", "specializations"),
        ],
        "accounts_wallet": [
            F("walletID", "int8", "pk"),
            F("balance", "numeric"),
            F("reservedBalance", "numeric"),
            F("pendingEarnings", "numeric"),
            F("autoWithdrawEnabled", "bool"),
            F("lastAutoWithdrawAt", "timestamptz"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("accountFK_id", "int8 UNIQUE", "fk", "accounts_accounts"),
            F("preferredPaymentMethodID_id", "int8 (nullable)", "fk", "accounts_userpaymentmethod"),
        ],
        "accounts_userpaymentmethod": [
            F("id", "int8", "pk"),
            F("methodType", "varchar"),
            F("accountName", "varchar"),
            F("accountNumber", "varchar"),
            F("bankName", "varchar"),
            F("bankCode", "varchar"),
            F("isPrimary", "bool"),
            F("isVerified", "bool"),
            F("paymongoRecipientId", "varchar"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("accountFK_id", "int8", "fk", "accounts_accounts"),
        ],
        "accounts_pushtoken": [
            F("tokenID", "int8", "pk"),
            F("pushToken", "varchar UNIQUE"),
            F("deviceType", "varchar"),
            F("isActive", "bool"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("lastUsed", "timestamptz"),
            F("accountFK_id", "int8", "fk", "accounts_accounts"),
        ],
        "accounts_notificationsettings": [
            F("settingsID", "int8", "pk"),
            F("pushEnabled", "bool"),
            F("soundEnabled", "bool"),
            F("jobUpdates", "bool"),
            F("messages", "bool"),
            F("payments", "bool"),
            F("reviews", "bool"),
            F("kycUpdates", "bool"),
            F("doNotDisturbStart", "time"),
            F("doNotDisturbEnd", "time"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("accountFK_id", "int8 UNIQUE", "fk", "accounts_accounts"),
        ],
    },
    # Edges to draw (only when target is in same module). Format:
    # (child_table, child_field, parent_table, "one_to_many" | "one_to_one")
    "edges": [
        ("accounts_workerprofile", "profileID_id", "accounts_profile", "one_to_one"),
        ("accounts_clientprofile", "profileID_id", "accounts_profile", "one_to_one"),
        ("accounts_barangay", "city_id", "accounts_city", "one_to_many"),
        ("accounts_workerspecialization", "workerID_id", "accounts_workerprofile", "one_to_many"),
        ("accounts_workerspecialization", "specializationID_id", "specializations", "one_to_many"),
        ("accounts_interestedjobs", "clientID_id", "accounts_clientprofile", "one_to_many"),
        ("accounts_interestedjobs", "specializationID_id", "specializations", "one_to_many"),
        ("accounts_wallet", "preferredPaymentMethodID_id", "accounts_userpaymentmethod", "one_to_many_opt"),
        ("specializations", "created_by_agency_id", "accounts_agency", "one_to_many_opt"),
    ],
    # Explicit grid layout: rows of tables (top to bottom). Tables in a row are
    # placed at the same rank.
    "layout": [
        ["accounts_profile", "accounts_workerprofile", "accounts_clientprofile"],
        ["accounts_agency", "specializations", "accounts_workerspecialization", "accounts_interestedjobs"],
        ["accounts_city", "accounts_barangay", "accounts_wallet", "accounts_userpaymentmethod"],
        ["accounts_pushtoken", "accounts_notificationsettings"],
    ],
    "module_num": 2,
    "filename": "erd_v2_module2_profiles.png",
}


# ---------------------------------------------------------------------------
# MODULE 3 - Jobs, Applications & Assignments
# ---------------------------------------------------------------------------

JOBS_FIELDS = [
    F("jobID", "int8", "pk"),
    F("title", "varchar"),
    F("description", "text"),
    F("budget", "numeric"),
    F("location", "varchar"),
    F("expectedDuration", "varchar"),
    F("urgency", "varchar"),
    F("preferredStartDate", "date"),
    F("materialsNeeded", "jsonb"),
    F("status", "varchar"),
    F("completedAt", "timestamptz"),
    F("cancellationReason", "text"),
    F("createdAt", "timestamptz"),
    F("updatedAt", "timestamptz"),
    F("clientMarkedComplete", "bool"),
    F("clientMarkedCompleteAt", "timestamptz"),
    F("workerMarkedComplete", "bool"),
    F("workerMarkedCompleteAt", "timestamptz"),
    F("escrowAmount", "numeric"),
    F("escrowPaid", "bool"),
    F("escrowPaidAt", "timestamptz"),
    F("remainingPayment", "numeric"),
    F("remainingPaymentPaid", "bool"),
    F("remainingPaymentPaidAt", "timestamptz"),
    F("finalPaymentMethod", "varchar"),
    F("cashPaymentProofUrl", "varchar"),
    F("paymentMethodSelectedAt", "timestamptz"),
    F("cashProofUploadedAt", "timestamptz"),
    F("cashPaymentApproved", "bool"),
    F("cashPaymentApprovedAt", "timestamptz"),
    F("jobType", "varchar"),
    F("inviteRejectionReason", "text"),
    F("inviteRespondedAt", "timestamptz"),
    F("inviteStatus", "varchar"),
    F("clientConfirmedWorkStarted", "bool"),
    F("clientConfirmedWorkStartedAt", "timestamptz"),
    F("assignmentNotes", "text"),
    F("employeeAssignedAt", "timestamptz"),
    F("is_team_job", "bool"),
    F("budget_allocation_type", "varchar"),
    F("team_job_start_threshold", "numeric"),
    F("paymentReleaseDate", "timestamptz"),
    F("paymentReleasedToWorker", "bool"),
    F("paymentReleasedAt", "timestamptz"),
    F("paymentHeldReason", "varchar"),
    F("job_scope", "varchar"),
    F("skill_level_required", "varchar"),
    F("work_environment", "varchar"),
    F("payment_model", "varchar"),
    F("duration_days", "int4"),
    F("daily_rate_agreed", "numeric"),
    F("actual_start_date", "date"),
    F("total_days_worked", "int4"),
    F("daily_escrow_total", "numeric"),
    F("materialsCost", "numeric"),
    F("materials_status", "varchar"),
    F("scheduled_end_date", "date"),
    F("qa_day_offset", "int4"),
    F("workerMarkedOnTheWay", "bool"),
    F("workerMarkedOnTheWayAt", "timestamptz"),
    F("workerMarkedJobStarted", "bool"),
    F("workerMarkedJobStartedAt", "timestamptz"),
    F("is_early_completed", "bool"),
    F("early_completed_at", "timestamptz"),
    F("early_completion_payout", "numeric"),
    F("shift_type", "varchar"),
    F("cancelledAt", "timestamptz"),
    F("cancelledByRole", "varchar"),
    F("cancellationStage", "varchar"),
    F("clientRefundAmount", "numeric"),
    F("workerCompensationAmount", "numeric"),
    F("agency_flow_mode", "varchar"),
    F("clientID_id", "int8", "fk", "accounts_clientprofile"),
    F("assignedWorkerID_id", "int8", "fk", "accounts_workerprofile"),
    F("assignedAgencyFK_id", "int8", "fk", "accounts_agency"),
    F("assignedEmployeeID_id", "int8", "fk", "agency_employees"),
    F("categoryID_id", "int8", "fk", "specializations"),
    F("cancelledByAccountID_id", "int8", "fk", "accounts_accounts"),
    F("cashPaymentApprovedBy_id", "int8", "fk", "accounts_accounts"),
]

MODULE3 = {
    "title": "MODULE 3 — Jobs, Applications & Assignments",
    "tables": {
        "jobs": JOBS_FIELDS,
        "job_skill_slots": [
            F("skillSlotID", "int8", "pk"),
            F("workers_needed", "int4"),
            F("budget_allocated", "numeric"),
            F("skill_level_required", "varchar"),
            F("status", "varchar"),
            F("notes", "text"),
            F("agency_invite_status", "varchar"),
            F("agency_invite_responded_at", "timestamptz"),
            F("last_rejected_agency_id", "int8"),
            F("last_rejected_agency_name", "varchar"),
            F("last_rejected_at", "timestamptz"),
            F("last_rejection_reason", "text"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("jobID_id", "int8", "fk", "jobs"),
            F("specializationID_id", "int8", "fk", "specializations"),
            F("invited_agency_id", "int8", "fk", "accounts_agency"),
        ],
        "job_applications": [
            F("applicationID", "int8", "pk"),
            F("proposalMessage", "text"),
            F("proposedBudget", "numeric"),
            F("estimatedDuration", "varchar"),
            F("budgetOption", "varchar"),
            F("status", "varchar"),
            F("selected_materials", "jsonb"),
            F("proposed_daily_rate", "numeric"),
            F("proposed_days", "int4"),
            F("negotiation_count", "int2"),
            F("applied_shift", "varchar"),
            F("clientRejectionReason", "text"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("jobID_id", "int8", "fk", "jobs"),
            F("workerID_id", "int8", "fk", "accounts_workerprofile"),
            F("applied_skill_slot_id", "int8", "fk", "job_skill_slots"),
        ],
        "price_negotiations": [
            F("negotiationID", "int8", "pk"),
            F("actor", "varchar"),
            F("round_number", "int2"),
            F("proposed_budget", "numeric"),
            F("proposed_daily_rate", "numeric"),
            F("proposed_days", "int4"),
            F("message", "text"),
            F("status", "varchar"),
            F("createdAt", "timestamptz"),
            F("application_id", "int8", "fk", "job_applications"),
        ],
        "job_worker_assignments": [
            F("assignmentID", "int8", "pk"),
            F("slot_position", "int4"),
            F("assignment_status", "varchar"),
            F("assigned_shift", "varchar"),
            F("worker_marked_complete", "bool"),
            F("worker_marked_complete_at", "timestamptz"),
            F("completion_notes", "text"),
            F("individual_rating", "numeric"),
            F("client_confirmed_arrival", "bool"),
            F("client_confirmed_arrival_at", "timestamptz"),
            F("daily_rate_at_assignment", "numeric"),
            F("days_worked", "int4"),
            F("total_earned", "numeric"),
            F("early_completed", "bool"),
            F("early_completed_at", "timestamptz"),
            F("early_completion_payout", "numeric"),
            F("assignedAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("jobID_id", "int8", "fk", "jobs"),
            F("skillSlotID_id", "int8", "fk", "job_skill_slots"),
            F("workerID_id", "int8", "fk", "accounts_workerprofile"),
        ],
        "job_employee_assignments": [
            F("assignmentID", "int8", "pk"),
            F("assignedAt", "timestamptz"),
            F("notes", "text"),
            F("isPrimaryContact", "bool"),
            F("status", "varchar"),
            F("dispatched", "bool"),
            F("dispatchedAt", "timestamptz"),
            F("clientConfirmedArrival", "bool"),
            F("clientConfirmedArrivalAt", "timestamptz"),
            F("agencyMarkedComplete", "bool"),
            F("agencyMarkedCompleteAt", "timestamptz"),
            F("employeeMarkedComplete", "bool"),
            F("employeeMarkedCompleteAt", "timestamptz"),
            F("completionNotes", "text"),
            F("paymentAmount", "numeric"),
            F("clientApproved", "bool"),
            F("clientApprovedAt", "timestamptz"),
            F("early_completed", "bool"),
            F("early_completed_at", "timestamptz"),
            F("early_completion_payout", "numeric"),
            F("job_id", "int8", "fk", "jobs"),
            F("employee_id", "int8", "fk", "agency_employees"),
            F("skill_slot_id", "int8", "fk", "job_skill_slots"),
            F("assignedBy_id", "int8", "fk", "accounts_accounts"),
        ],
        "job_logs": [
            F("logID", "int8", "pk"),
            F("oldStatus", "varchar"),
            F("newStatus", "varchar"),
            F("notes", "text"),
            F("actionType", "varchar"),
            F("metadata", "jsonb"),
            F("createdAt", "timestamptz"),
            F("jobID_id", "int8", "fk", "jobs"),
            F("changedBy_id", "int8", "fk", "accounts_accounts"),
        ],
        "saved_jobs": [
            F("savedJobID", "int8", "pk"),
            F("savedAt", "timestamptz"),
            F("jobID_id", "int8", "fk", "jobs"),
            F("workerID_id", "int8", "fk", "accounts_workerprofile"),
        ],
    },
    "edges": [
        ("job_skill_slots", "jobID_id", "jobs", "one_to_many"),
        ("job_applications", "jobID_id", "jobs", "one_to_many"),
        ("job_applications", "applied_skill_slot_id", "job_skill_slots", "one_to_many_opt"),
        ("price_negotiations", "application_id", "job_applications", "one_to_many"),
        ("job_worker_assignments", "jobID_id", "jobs", "one_to_many"),
        ("job_worker_assignments", "skillSlotID_id", "job_skill_slots", "one_to_many"),
        ("job_employee_assignments", "job_id", "jobs", "one_to_many"),
        ("job_employee_assignments", "skill_slot_id", "job_skill_slots", "one_to_many_opt"),
        ("job_logs", "jobID_id", "jobs", "one_to_many"),
        ("saved_jobs", "jobID_id", "jobs", "one_to_many"),
    ],
    # jobs is the central, very tall table. Place it on one rank and the related
    # tables in a column to its left, so edges flow horizontally.
    "layout": [
        ["job_skill_slots", "jobs"],
        ["job_applications", "jobs"],
        ["price_negotiations", "jobs"],
        ["job_worker_assignments", "jobs"],
        ["job_employee_assignments", "jobs"],
        ["job_logs", "jobs"],
        ["saved_jobs", "jobs"],
    ],
    # Use rankdir=LR with an explicit chain of left-side tables top-to-bottom
    "left_chain": ["job_skill_slots", "job_applications", "price_negotiations",
                   "job_worker_assignments", "job_employee_assignments",
                   "job_logs", "saved_jobs"],
    "right_chain": ["jobs"],
    "module_num": 3,
    "filename": "erd_v2_module3_jobs.png",
}


# ---------------------------------------------------------------------------
# MODULE 4 - Disputes, Reviews, Daily Operations & Attendance
# ---------------------------------------------------------------------------
MODULE4 = {
    "title": "MODULE 4 — Disputes, Reviews, Daily Operations & Attendance",
    "tables": {
        "job_disputes": [
            F("disputeID", "int8", "pk"),
            F("disputedBy", "varchar"),
            F("reason", "varchar"),
            F("description", "text"),
            F("status", "varchar"),
            F("priority", "varchar"),
            F("jobAmount", "numeric"),
            F("disputedAmount", "numeric"),
            F("resolution", "text"),
            F("resolvedDate", "timestamptz"),
            F("assignedTo", "varchar"),
            F("openedDate", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("backjobStarted", "bool"),
            F("backjobStartedAt", "timestamptz"),
            F("clientConfirmedBackjob", "bool"),
            F("clientConfirmedBackjobAt", "timestamptz"),
            F("workerMarkedBackjobComplete", "bool"),
            F("workerMarkedBackjobCompleteAt", "timestamptz"),
            F("termsAccepted", "bool"),
            F("termsVersion", "varchar"),
            F("termsAcceptedAt", "timestamptz"),
            F("adminRejectedAt", "timestamptz"),
            F("adminRejectionReason", "text"),
            F("in_negotiation_at", "timestamptz"),
            F("scheduled_date", "date"),
            F("workerScheduleConfirmed", "bool"),
            F("workerScheduleConfirmedAt", "timestamptz"),
            F("jobID_id", "int8", "fk", "jobs"),
        ],
        "dispute_evidence": [
            F("evidenceID", "int8", "pk"),
            F("imageURL", "varchar"),
            F("description", "text"),
            F("createdAt", "timestamptz"),
            F("disputeID_id", "int8", "fk", "job_disputes"),
            F("uploadedBy_id", "int8", "fk", "accounts_accounts"),
        ],
        "backjob_schedule_confirmations": [
            F("confirmationID", "int8", "pk"),
            F("confirmed", "bool"),
            F("confirmedAt", "timestamptz"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("disputeID_id", "int8", "fk", "job_disputes"),
            F("assignmentID_id", "int8", "fk", "job_worker_assignments"),
            F("confirmedBy_id", "int8", "fk", "accounts_accounts"),
        ],
        "job_reviews": [
            F("reviewID", "int8", "pk"),
            F("reviewerType", "varchar"),
            F("rating", "numeric"),
            F("rating_communication", "numeric"),
            F("rating_professionalism", "numeric"),
            F("rating_punctuality", "numeric"),
            F("rating_quality", "numeric"),
            F("comment", "text"),
            F("status", "varchar"),
            F("isFlagged", "bool"),
            F("flagReason", "text"),
            F("flaggedAt", "timestamptz"),
            F("helpfulCount", "int4"),
            F("agency_response", "text"),
            F("agency_response_at", "timestamptz"),
            F("backjob_edit_deadline", "timestamptz"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("jobID_id", "int8", "fk", "jobs"),
            F("reviewerID_id", "int8", "fk", "accounts_accounts"),
            F("revieweeID_id", "int8", "fk", "accounts_accounts"),
            F("revieweeProfileID_id", "int8", "fk", "accounts_profile"),
            F("revieweeAgencyID_id", "int8", "fk", "accounts_agency"),
            F("revieweeEmployeeID_id", "int8", "fk", "agency_employees"),
            F("flaggedBy_id", "int8", "fk", "accounts_accounts"),
        ],
        "review_skill_tags": [
            F("tagID", "int8", "pk"),
            F("createdAt", "timestamptz"),
            F("reviewID_id", "int8", "fk", "job_reviews"),
            F("workerSpecializationID_id", "int8", "fk", "accounts_workerspecialization"),
        ],
        "job_materials": [
            F("jobMaterialID", "int8", "pk"),
            F("name", "varchar"),
            F("description", "text"),
            F("quantity", "int4"),
            F("unit", "varchar"),
            F("source", "varchar"),
            F("purchase_price", "numeric"),
            F("receipt_image_url", "varchar"),
            F("client_approved", "bool"),
            F("client_approved_at", "timestamptz"),
            F("client_rejected", "bool"),
            F("rejection_reason", "text"),
            F("added_by", "varchar"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("jobID_id", "int8", "fk", "jobs"),
            F("workerMaterialID_id", "int8", "fk", "worker_materials"),
        ],
        "job_photos": [
            F("photoID", "int8", "pk"),
            F("photoURL", "varchar"),
            F("fileName", "varchar"),
            F("uploadedAt", "timestamptz"),
            F("jobID_id", "int8", "fk", "jobs"),
        ],
        "daily_attendance": [
            F("attendanceID", "int8", "pk"),
            F("date", "date"),
            F("time_in", "timestamptz"),
            F("time_out", "timestamptz"),
            F("status", "varchar"),
            F("worker_confirmed", "bool"),
            F("worker_confirmed_at", "timestamptz"),
            F("client_confirmed", "bool"),
            F("client_confirmed_at", "timestamptz"),
            F("amount_earned", "numeric"),
            F("payment_processed", "bool"),
            F("payment_processed_at", "timestamptz"),
            F("payment_method", "varchar"),
            F("cash_payment_proof_url", "varchar"),
            F("cash_payment_verified", "bool"),
            F("cash_payment_verified_at", "timestamptz"),
            F("cash_proof_uploaded_at", "timestamptz"),
            F("absent_penalty_amount", "numeric"),
            F("absent_penalty_applied", "bool"),
            F("absent_penalty_applied_at", "timestamptz"),
            F("absent_penalty_percent", "numeric"),
            F("notes", "text"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("jobID_id", "int8", "fk", "jobs"),
            F("workerID_id", "int8", "fk", "accounts_workerprofile"),
            F("assignmentID_id", "int8", "fk", "job_worker_assignments"),
            F("employeeID_id", "int8", "fk", "agency_employees"),
        ],
        "daily_job_extensions": [
            F("extensionID", "int8", "pk"),
            F("additional_days", "int4"),
            F("additional_escrow", "numeric"),
            F("reason", "text"),
            F("status", "varchar"),
            F("requested_by", "varchar"),
            F("client_approved", "bool"),
            F("client_approved_at", "timestamptz"),
            F("worker_approved", "bool"),
            F("worker_approved_at", "timestamptz"),
            F("escrow_collected", "bool"),
            F("escrow_collected_at", "timestamptz"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("jobID_id", "int8", "fk", "jobs"),
            F("requestedByUser_id", "int8", "fk", "accounts_accounts"),
        ],
        "daily_rate_changes": [
            F("changeID", "int8", "pk"),
            F("old_rate", "numeric"),
            F("new_rate", "numeric"),
            F("reason", "text"),
            F("effective_date", "date"),
            F("status", "varchar"),
            F("requested_by", "varchar"),
            F("client_approved", "bool"),
            F("client_approved_at", "timestamptz"),
            F("worker_approved", "bool"),
            F("worker_approved_at", "timestamptz"),
            F("escrow_adjusted", "bool"),
            F("escrow_adjustment_amount", "numeric"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("jobID_id", "int8", "fk", "jobs"),
            F("requestedByUser_id", "int8", "fk", "accounts_accounts"),
        ],
        "daily_skip_day_requests": [
            F("skipRequestID", "int8", "pk"),
            F("request_date", "date"),
            F("status", "varchar"),
            F("requested_by", "varchar"),
            F("requested_account_ids", "jsonb"),
            F("requested_count", "int4"),
            F("total_required", "int4"),
            F("requires_all_team_workers", "bool"),
            F("all_workers_requested", "bool"),
            F("target_type", "varchar"),
            F("reviewedAt", "timestamptz"),
            F("client_rejection_reason", "text"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("jobID_id", "int8", "fk", "jobs"),
            F("requestedByUser_id", "int8", "fk", "accounts_accounts"),
            F("reviewedByUser_id", "int8", "fk", "accounts_accounts"),
            F("target_employee_id", "int8", "fk", "agency_employees"),
            F("target_worker_account_id", "int8", "fk", "accounts_accounts"),
        ],
    },
    "edges": [
        ("dispute_evidence", "disputeID_id", "job_disputes", "one_to_many"),
        ("backjob_schedule_confirmations", "disputeID_id", "job_disputes", "one_to_many"),
        ("review_skill_tags", "reviewID_id", "job_reviews", "one_to_many"),
    ],
    "layout": [
        ["job_disputes", "dispute_evidence", "backjob_schedule_confirmations"],
        ["job_reviews", "review_skill_tags"],
        ["job_materials", "job_photos"],
        ["daily_attendance", "daily_job_extensions"],
        ["daily_rate_changes", "daily_skip_day_requests"],
    ],
    "module_num": 4,
    "filename": "erd_v2_module4_disputes.png",
}


# ---------------------------------------------------------------------------
# MODULE 5 - KYC Verification (Individual & Agency)
# ---------------------------------------------------------------------------
MODULE5 = {
    "title": "MODULE 5 — KYC Verification (Individual & Agency)",
    "tables": {
        "accounts_kyc": [
            F("kycID", "int8", "pk"),
            F("kyc_status", "varchar"),
            F("reviewedAt", "timestamptz"),
            F("notes", "text"),
            F("rejectionCategory", "varchar"),
            F("rejectionReason", "text"),
            F("resubmissionCount", "int4"),
            F("maxResubmissions", "int4"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("accountFK_id", "int8", "fk", "accounts_accounts"),
            F("reviewedBy_id", "int8", "fk", "accounts_accounts"),
        ],
        "accounts_kycfiles": [
            F("kycFileID", "int8", "pk"),
            F("idType", "varchar"),
            F("fileURL", "varchar"),
            F("fileName", "varchar"),
            F("fileSize", "int4"),
            F("uploadedAt", "timestamptz"),
            F("ai_verification_status", "varchar"),
            F("face_detected", "bool"),
            F("face_count", "int4"),
            F("face_confidence", "float8"),
            F("ocr_text", "text"),
            F("ocr_confidence", "float8"),
            F("quality_score", "float8"),
            F("ai_confidence_score", "float8"),
            F("ai_rejection_reason", "varchar"),
            F("ai_rejection_message", "varchar"),
            F("ai_warnings", "jsonb"),
            F("ai_details", "jsonb"),
            F("verified_at", "timestamptz"),
            F("kycID_id", "int8", "fk", "accounts_kyc"),
        ],
        "kyc_extracted_data": [
            F("extractedDataID", "int8", "pk"),
            F("extracted_full_name", "varchar"),
            F("extracted_first_name", "varchar"),
            F("extracted_middle_name", "varchar"),
            F("extracted_last_name", "varchar"),
            F("extracted_birth_date", "date"),
            F("extracted_address", "text"),
            F("extracted_id_number", "varchar"),
            F("extracted_id_type", "varchar"),
            F("extracted_expiry_date", "date"),
            F("extracted_nationality", "varchar"),
            F("extracted_sex", "varchar"),
            F("extracted_place_of_birth", "varchar"),
            F("extracted_clearance_number", "varchar"),
            F("extracted_clearance_type", "varchar"),
            F("extracted_clearance_issue_date", "date"),
            F("extracted_clearance_validity_date", "date"),
            F("confirmed_full_name", "varchar"),
            F("confirmed_first_name", "varchar"),
            F("confirmed_middle_name", "varchar"),
            F("confirmed_last_name", "varchar"),
            F("confirmed_birth_date", "date"),
            F("confirmed_address", "text"),
            F("confirmed_id_number", "varchar"),
            F("confirmed_nationality", "varchar"),
            F("confirmed_sex", "varchar"),
            F("confirmed_place_of_birth", "varchar"),
            F("confirmed_clearance_number", "varchar"),
            F("confirmed_clearance_type", "varchar"),
            F("confirmed_clearance_issue_date", "date"),
            F("confirmed_clearance_validity_date", "date"),
            F("confidence_full_name", "float8"),
            F("confidence_birth_date", "float8"),
            F("confidence_address", "float8"),
            F("confidence_id_number", "float8"),
            F("confidence_place_of_birth", "float8"),
            F("confidence_clearance_number", "float8"),
            F("overall_confidence", "float8"),
            F("extraction_status", "varchar"),
            F("extraction_source", "varchar"),
            F("face_match_completed", "bool"),
            F("face_match_score", "float8"),
            F("user_edited_fields", "jsonb"),
            F("raw_extraction_data", "jsonb"),
            F("extracted_at", "timestamptz"),
            F("confirmed_at", "timestamptz"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("kycID_id", "int8 UNIQUE", "fk", "accounts_kyc"),
        ],
        "agency_agencykyc": [
            F("agencyKycID", "int8", "pk"),
            F("status", "varchar"),
            F("reviewedAt", "timestamptz"),
            F("notes", "varchar"),
            F("rejectionCategory", "varchar"),
            F("rejectionReason", "text"),
            F("resubmissionCount", "int4"),
            F("maxResubmissions", "int4"),
            F("face_similarity_score", "float8"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("accountFK_id", "int8", "fk", "accounts_accounts"),
            F("reviewedBy_id", "int8", "fk", "accounts_accounts"),
        ],
        "agency_agencykycfile": [
            F("fileID", "int8", "pk"),
            F("fileType", "varchar"),
            F("fileURL", "varchar"),
            F("fileName", "varchar"),
            F("fileSize", "int4"),
            F("uploadedAt", "timestamptz"),
            F("ai_verification_status", "varchar"),
            F("face_detected", "bool"),
            F("face_count", "int4"),
            F("face_confidence", "float8"),
            F("ocr_text", "text"),
            F("ocr_confidence", "float8"),
            F("quality_score", "float8"),
            F("ai_confidence_score", "float8"),
            F("ai_rejection_reason", "varchar"),
            F("ai_rejection_message", "varchar"),
            F("ai_warnings", "jsonb"),
            F("ai_details", "jsonb"),
            F("verified_at", "timestamptz"),
            F("agencyKyc_id", "int8", "fk", "agency_agencykyc"),
        ],
        "agency_kyc_extracted_data": [
            F("extractedDataID", "int8", "pk"),
            F("extracted_business_name", "varchar"),
            F("extracted_business_type", "varchar"),
            F("extracted_business_address", "text"),
            F("extracted_permit_number", "varchar"),
            F("extracted_permit_issue_date", "date"),
            F("extracted_permit_expiry_date", "date"),
            F("extracted_dti_number", "varchar"),
            F("extracted_sec_number", "varchar"),
            F("extracted_tin", "varchar"),
            F("extracted_rep_full_name", "varchar"),
            F("extracted_rep_id_number", "varchar"),
            F("extracted_rep_id_type", "varchar"),
            F("extracted_rep_birth_date", "date"),
            F("extracted_rep_address", "text"),
            F("confirmed_business_name", "varchar"),
            F("confirmed_business_type", "varchar"),
            F("confirmed_business_address", "text"),
            F("confirmed_permit_number", "varchar"),
            F("confirmed_permit_issue_date", "date"),
            F("confirmed_permit_expiry_date", "date"),
            F("confirmed_dti_number", "varchar"),
            F("confirmed_sec_number", "varchar"),
            F("confirmed_tin", "varchar"),
            F("confirmed_rep_full_name", "varchar"),
            F("confirmed_rep_id_number", "varchar"),
            F("confirmed_rep_birth_date", "date"),
            F("confirmed_rep_address", "text"),
            F("confidence_business_name", "float8"),
            F("confidence_business_address", "float8"),
            F("confidence_permit_number", "float8"),
            F("confidence_rep_name", "float8"),
            F("overall_confidence", "float8"),
            F("extraction_status", "varchar"),
            F("extraction_source", "varchar"),
            F("user_edited_fields", "jsonb"),
            F("raw_extraction_data", "jsonb"),
            F("extracted_at", "timestamptz"),
            F("confirmed_at", "timestamptz"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("agencyKyc_id", "int8 UNIQUE", "fk", "agency_agencykyc"),
        ],
        "adminpanel_kyclogs": [
            F("kycLogID", "int8", "pk"),
            F("action", "varchar"),
            F("reviewedAt", "timestamptz"),
            F("reason", "text"),
            F("userEmail", "varchar"),
            F("userAccountID", "int8"),
            F("kycID", "int8"),
            F("kycType", "varchar"),
            F("createdAt", "timestamptz"),
            F("accountFK_id", "int8", "fk", "accounts_accounts"),
            F("reviewedBy_id", "int8", "fk", "accounts_accounts"),
        ],
    },
    "edges": [
        ("accounts_kycfiles", "kycID_id", "accounts_kyc", "one_to_many"),
        ("kyc_extracted_data", "kycID_id", "accounts_kyc", "one_to_one"),
        ("agency_agencykycfile", "agencyKyc_id", "agency_agencykyc", "one_to_many"),
        ("agency_kyc_extracted_data", "agencyKyc_id", "agency_agencykyc", "one_to_one"),
    ],
    "layout": [
        ["accounts_kycfiles", "accounts_kyc", "kyc_extracted_data"],
        ["agency_agencykycfile", "agency_agencykyc", "agency_kyc_extracted_data"],
        ["adminpanel_kyclogs"],
    ],
    "module_num": 5,
    "filename": "erd_v2_module5_kyc.png",
}


# ---------------------------------------------------------------------------
# MODULE 6 - Admin Panel, Messaging, Notifications & Worker Assets
# ---------------------------------------------------------------------------
MODULE6 = {
    "title": "MODULE 6 — Admin Panel, Messaging, Notifications & Worker Assets",
    "tables": {
        "adminpanel_adminaccount": [
            F("adminID", "int8", "pk"),
            F("role", "varchar"),
            F("permissions", "jsonb"),
            F("isActive", "bool"),
            F("lastLogin", "timestamptz"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("accountFK_id", "int8 UNIQUE", "fk", "accounts_accounts"),
        ],
        "adminpanel_auditlog": [
            F("auditLogID", "int8", "pk"),
            F("adminEmail", "varchar"),
            F("action", "varchar"),
            F("entityType", "varchar"),
            F("entityID", "varchar"),
            F("details", "jsonb"),
            F("beforeValue", "jsonb"),
            F("afterValue", "jsonb"),
            F("ipAddress", "inet"),
            F("userAgent", "text"),
            F("createdAt", "timestamptz"),
            F("adminFK_id", "int8", "fk", "accounts_accounts"),
        ],
        "adminpanel_supportticket": [
            F("ticketID", "int8", "pk"),
            F("subject", "varchar"),
            F("category", "varchar"),
            F("priority", "varchar"),
            F("status", "varchar"),
            F("ticketType", "varchar"),
            F("platform", "varchar"),
            F("deviceInfo", "text"),
            F("appVersion", "varchar"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("lastReplyAt", "timestamptz"),
            F("resolvedAt", "timestamptz"),
            F("userFK_id", "int8", "fk", "accounts_accounts"),
            F("assignedTo_id", "int8", "fk", "accounts_accounts"),
            F("agencyFK_id", "int8", "fk", "accounts_agency"),
        ],
        "adminpanel_supportticketreply": [
            F("replyID", "int8", "pk"),
            F("content", "text"),
            F("isSystemMessage", "bool"),
            F("attachmentURL", "varchar"),
            F("createdAt", "timestamptz"),
            F("ticketFK_id", "int8", "fk", "adminpanel_supportticket"),
            F("senderFK_id", "int8", "fk", "accounts_accounts"),
        ],
        "adminpanel_userreport": [
            F("reportID", "int8", "pk"),
            F("reportType", "varchar"),
            F("reason", "varchar"),
            F("description", "text"),
            F("relatedContentID", "int8"),
            F("status", "varchar"),
            F("adminNotes", "text"),
            F("actionTaken", "varchar"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("resolvedAt", "timestamptz"),
            F("reporterFK_id", "int8", "fk", "accounts_accounts"),
            F("reportedUserFK_id", "int8", "fk", "accounts_accounts"),
            F("reviewedBy_id", "int8", "fk", "accounts_accounts"),
        ],
        "adminpanel_platformsettings": [
            F("settingsID", "int8", "pk"),
            F("platformFeePercentage", "numeric"),
            F("escrowHoldingDays", "int4"),
            F("maxJobBudget", "numeric"),
            F("minJobBudget", "numeric"),
            F("workerVerificationRequired", "bool"),
            F("autoApproveKYC", "bool"),
            F("kycDocumentExpiryDays", "int4"),
            F("kycAutoApproveMinConfidence", "numeric"),
            F("kycFaceMatchMinSimilarity", "numeric"),
            F("kycRequireUserConfirmation", "bool"),
            F("maintenanceMode", "bool"),
            F("sessionTimeoutMinutes", "int4"),
            F("maxUploadSizeMB", "int4"),
            F("lastUpdated", "timestamptz"),
            F("updatedBy_id", "int8", "fk", "accounts_accounts"),
        ],
        "adminpanel_cannedresponse": [
            F("responseID", "int8", "pk"),
            F("title", "varchar"),
            F("content", "text"),
            F("category", "varchar"),
            F("shortcuts", "jsonb"),
            F("usageCount", "int4"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("createdBy_id", "int8", "fk", "accounts_accounts"),
        ],
        "adminpanel_contentmoderationterm": [
            F("termID", "int8", "pk"),
            F("term", "varchar"),
            F("normalizedTerm", "varchar UNIQUE"),
            F("isActive", "bool"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("createdBy_id", "int8", "fk", "accounts_accounts"),
            F("updatedBy_id", "int8", "fk", "accounts_accounts"),
        ],
        "adminpanel_faq": [
            F("faqID", "int8", "pk"),
            F("question", "varchar"),
            F("answer", "text"),
            F("category", "varchar"),
            F("sortOrder", "int4"),
            F("viewCount", "int4"),
            F("isPublished", "bool"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
        ],
        "adminpanel_systemroles": [
            F("systemRoleID", "int8", "pk"),
            F("systemRole", "varchar"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("accountID_id", "int8", "fk", "accounts_accounts"),
        ],
        "accounts_notification": [
            F("notificationID", "int8", "pk"),
            F("notificationType", "varchar"),
            F("title", "varchar"),
            F("message", "text"),
            F("isRead", "bool"),
            F("relatedKYCLogID", "int8"),
            F("relatedJobID", "int8"),
            F("relatedApplicationID", "int8"),
            F("profile_type", "varchar"),
            F("createdAt", "timestamptz"),
            F("readAt", "timestamptz"),
            F("accountFK_id", "int8", "fk", "accounts_accounts"),
        ],
        "conversation": [
            F("conversationID", "int8", "pk"),
            F("conversation_type", "varchar"),
            F("status", "varchar"),
            F("lastMessageText", "text"),
            F("lastMessageTime", "timestamptz"),
            F("unreadCountClient", "int4"),
            F("unreadCountWorker", "int4"),
            F("archivedByClient", "bool"),
            F("archivedByWorker", "bool"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("client_id", "int8", "fk", "accounts_profile"),
            F("worker_id", "int8", "fk", "accounts_profile"),
            F("agency_id", "int8", "fk", "accounts_agency"),
            F("relatedJobPosting_id", "int8 UNIQUE", "fk", "jobs"),
            F("lastMessageSender_id", "int8", "fk", "accounts_profile"),
        ],
        "conversation_participants": [
            F("participantID", "int8", "pk"),
            F("participant_type", "varchar"),
            F("unread_count", "int4"),
            F("is_archived", "bool"),
            F("joined_at", "timestamptz"),
            F("last_read_at", "timestamptz"),
            F("conversation_id", "int8", "fk", "conversation"),
            F("profile_id", "int8", "fk", "accounts_profile"),
            F("skill_slot_id", "int8", "fk", "job_skill_slots"),
            F("admin_account_id", "int8", "fk", "accounts_accounts"),
        ],
        "message": [
            F("messageID", "int8", "pk"),
            F("messageText", "text"),
            F("messageType", "varchar"),
            F("locationAddress", "varchar"),
            F("locationLandmark", "varchar"),
            F("locationLatitude", "numeric"),
            F("locationLongitude", "numeric"),
            F("isRead", "bool"),
            F("readAt", "timestamptz"),
            F("createdAt", "timestamptz"),
            F("conversationID_id", "int8", "fk", "conversation"),
            F("sender_id", "int8", "fk", "accounts_profile"),
            F("senderAgency_id", "int8", "fk", "accounts_agency"),
            F("sender_admin_id", "int8", "fk", "accounts_accounts"),
        ],
        "message_attachment": [
            F("attachmentID", "int8", "pk"),
            F("fileURL", "varchar"),
            F("fileName", "varchar"),
            F("fileSize", "int4"),
            F("fileType", "varchar"),
            F("uploadedAt", "timestamptz"),
            F("messageID_id", "int8", "fk", "message"),
        ],
        "accounts_transaction": [
            F("transactionID", "int8", "pk"),
            F("transactionType", "varchar"),
            F("amount", "numeric"),
            F("balanceAfter", "numeric"),
            F("status", "varchar"),
            F("description", "varchar"),
            F("referenceNumber", "varchar"),
            F("paymentMethod", "varchar"),
            F("invoiceURL", "varchar"),
            F("xenditExternalID", "varchar"),
            F("xenditInvoiceID", "varchar UNIQUE"),
            F("xenditPaymentChannel", "varchar"),
            F("xenditPaymentID", "varchar"),
            F("xenditPaymentMethod", "varchar"),
            F("paymongoPaymentId", "varchar"),
            F("paymongoTransferId", "varchar"),
            F("paymongoTransferStatus", "varchar"),
            F("adminReferenceNumber", "varchar"),
            F("createdAt", "timestamptz"),
            F("completedAt", "timestamptz"),
            F("processedAt", "timestamptz"),
            F("walletID_id", "int8", "fk", "accounts_wallet"),
            F("relatedJobPosting_id", "int8", "fk", "jobs"),
            F("processedByAdmin_id", "int8", "fk", "accounts_accounts"),
        ],
        "agency_employees": [
            F("employeeID", "int8", "pk"),
            F("name", "varchar"),
            F("firstName", "varchar"),
            F("middleName", "varchar"),
            F("lastName", "varchar"),
            F("email", "varchar"),
            F("mobile", "varchar"),
            F("role", "varchar"),
            F("avatar", "varchar"),
            F("rating", "numeric"),
            F("specializations", "text"),
            F("daily_rate", "numeric"),
            F("hourly_rate", "numeric"),
            F("is_available_daily_jobs", "bool"),
            F("isActive", "bool"),
            F("employeeOfTheMonth", "bool"),
            F("employeeOfTheMonthDate", "timestamptz"),
            F("employeeOfTheMonthReason", "text"),
            F("totalEarnings", "numeric"),
            F("totalJobsCompleted", "int4"),
            F("lastRatingUpdate", "timestamptz"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("agency_id", "int8", "fk", "accounts_accounts"),
        ],
        "worker_certifications": [
            F("certificationID", "int8", "pk"),
            F("name", "varchar"),
            F("issuing_organization", "varchar"),
            F("issue_date", "date"),
            F("expiry_date", "date"),
            F("certificate_url", "varchar"),
            F("is_verified", "bool"),
            F("verified_at", "timestamptz"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("workerID_id", "int8", "fk", "accounts_workerprofile"),
            F("specializationID_id", "int8", "fk", "accounts_workerspecialization"),
            F("verified_by_id", "int8", "fk", "accounts_accounts"),
        ],
        "certification_logs": [
            F("certLogID", "int8", "pk"),
            F("certificationID", "int8"),
            F("action", "varchar"),
            F("reviewedAt", "timestamptz"),
            F("reason", "text"),
            F("workerEmail", "varchar"),
            F("workerAccountID", "int8"),
            F("certificationName", "varchar"),
            F("workerID_id", "int8", "fk", "accounts_workerprofile"),
            F("reviewedBy_id", "int8", "fk", "accounts_accounts"),
        ],
        "worker_materials": [
            F("materialID", "int8", "pk"),
            F("name", "varchar"),
            F("description", "text"),
            F("price", "numeric"),
            F("quantity", "numeric"),
            F("unit", "varchar"),
            F("image_url", "varchar"),
            F("is_available", "bool"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("workerID_id", "int8", "fk", "accounts_workerprofile"),
            F("agencyID_id", "int8", "fk", "accounts_agency"),
            F("categoryID_id", "int8", "fk", "specializations"),
        ],
        "worker_portfolio": [
            F("portfolioID", "int8", "pk"),
            F("image_url", "varchar"),
            F("caption", "text"),
            F("display_order", "int4"),
            F("file_name", "varchar"),
            F("file_size", "int4"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("workerID_id", "int8", "fk", "accounts_workerprofile"),
        ],
        "profiles_workerproduct": [
            F("productID", "int8", "pk"),
            F("productName", "varchar"),
            F("description", "text"),
            F("price", "numeric"),
            F("priceUnit", "varchar"),
            F("inStock", "bool"),
            F("stockQuantity", "int4"),
            F("productImage", "varchar"),
            F("isActive", "bool"),
            F("createdAt", "timestamptz"),
            F("updatedAt", "timestamptz"),
            F("workerID_id", "int8", "fk", "accounts_workerprofile"),
            F("categoryID_id", "int8", "fk", "specializations"),
        ],
    },
    "edges": [
        ("adminpanel_supportticketreply", "ticketFK_id", "adminpanel_supportticket", "one_to_many"),
        ("conversation_participants", "conversation_id", "conversation", "one_to_many"),
        ("message", "conversationID_id", "conversation", "one_to_many"),
        ("message_attachment", "messageID_id", "message", "one_to_many"),
    ],
    "layout": [
        ["adminpanel_adminaccount", "adminpanel_auditlog", "adminpanel_systemroles", "adminpanel_platformsettings"],
        ["adminpanel_supportticket", "adminpanel_supportticketreply", "adminpanel_userreport", "adminpanel_cannedresponse"],
        ["adminpanel_contentmoderationterm", "adminpanel_faq", "accounts_notification", "accounts_transaction"],
        ["conversation", "conversation_participants", "message", "message_attachment"],
        ["agency_employees", "worker_certifications", "certification_logs"],
        ["worker_materials", "worker_portfolio", "profiles_workerproduct"],
    ],
    "module_num": 6,
    "filename": "erd_v2_module6_admin.png",
}


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------
def html_escape(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


def field_row_html(field, idx, header_color):
    bg = ROW_A if (idx % 2 == 0) else ROW_B
    name = html_escape(field["name"])
    dtype = html_escape(field["type"])
    kind = field["kind"]
    target = field.get("target")

    # badge cell
    if kind == "pk":
        badge = f'<TD BGCOLOR="{PK_BADGE_BG}" WIDTH="34" ALIGN="CENTER"><FONT COLOR="{PK_BADGE_FG}" POINT-SIZE="9"><B>PK</B></FONT></TD>'
    elif kind == "fk":
        badge = f'<TD BGCOLOR="{FK_BADGE_BG}" WIDTH="34" ALIGN="CENTER"><FONT COLOR="{FK_BADGE_FG}" POINT-SIZE="9"><B>FK</B></FONT></TD>'
    elif kind == "pkfk":
        badge = (
            f'<TD BGCOLOR="{PK_BADGE_BG}" WIDTH="34" ALIGN="CENTER">'
            f'<FONT COLOR="{PK_BADGE_FG}" POINT-SIZE="9"><B>PK/FK</B></FONT></TD>'
        )
    else:
        badge = f'<TD BGCOLOR="{bg}" WIDTH="34"></TD>'

    # name cell
    if kind == "pk" or kind == "pkfk":
        name_cell = (
            f'<TD BGCOLOR="{bg}" ALIGN="LEFT">'
            f'<FONT COLOR="{PK_FIELD_FG}" POINT-SIZE="10"><B>{name}</B></FONT></TD>'
        )
    elif kind == "fk":
        name_cell = (
            f'<TD BGCOLOR="{bg}" ALIGN="LEFT">'
            f'<FONT COLOR="{FK_FIELD_FG}" POINT-SIZE="10"><I>{name}</I></FONT></TD>'
        )
    else:
        name_cell = (
            f'<TD BGCOLOR="{bg}" ALIGN="LEFT">'
            f'<FONT COLOR="{FIELD_FG}" POINT-SIZE="10">{name}</FONT></TD>'
        )

    # type cell (with FK target arrow appended in italic blue)
    type_html = (
        f'<FONT COLOR="{TYPE_FG}" POINT-SIZE="9">{dtype}</FONT>'
    )
    if kind == "fk" and target:
        type_html += (
            f'  <FONT COLOR="{TARGET_FG}" POINT-SIZE="9"><I>&#8594; {html_escape(target)}</I></FONT>'
        )

    type_cell = f'<TD BGCOLOR="{bg}" ALIGN="LEFT">{type_html}</TD>'

    return f'<TR>{badge}{name_cell}{type_cell}</TR>'


def table_html(table_name: str, fields: list, header_color: str) -> str:
    rows = "".join(field_row_html(f, i, header_color) for i, f in enumerate(fields))
    header = (
        f'<TR><TD COLSPAN="3" BGCOLOR="{header_color}" ALIGN="CENTER" CELLPADDING="6">'
        f'<FONT COLOR="{HEADER_TEXT}" POINT-SIZE="13"><B>{html_escape(table_name)}</B></FONT>'
        f'</TD></TR>'
    )
    return (
        f'<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" '
        f'COLOR="{TABLE_BORDER}" CELLPADDING="3">'
        f'{header}{rows}</TABLE>>'
    )


def add_edge(g: Digraph, child: str, child_field: str, parent: str, kind: str):
    """
    Crow's foot: at the child end (FK side) we use crow ("many"),
    at the parent end we use tee ("one") or teeodot for nullable/optional.
    For one_to_one we use tee on both ends.
    """
    if kind == "one_to_one":
        head, tail = "tee", "tee"
    elif kind == "one_to_many":
        head, tail = "crow", "tee"
    elif kind == "one_to_many_opt":
        head, tail = "crow", "teeodot"
    else:
        head, tail = "crow", "tee"

    # Edge from child:fieldport -> parent:headerport
    g.edge(
        f'{child}:{child_field}_p:e',
        f'{parent}:header_p:w',
        arrowhead=tail,        # at parent end (one)
        arrowtail=head,        # at child end (many/etc.)
        dir="both",
        color="#3F4A55",
        penwidth="1.2",
    )


def field_row_html_with_port(field, idx, table_name):
    bg = ROW_A if (idx % 2 == 0) else ROW_B
    name = html_escape(field["name"])
    dtype = html_escape(field["type"])
    kind = field["kind"]
    target = field.get("target")
    port = f'{field["name"]}_p'

    if kind == "pk":
        badge = f'<TD BGCOLOR="{PK_BADGE_BG}" WIDTH="34" ALIGN="CENTER"><FONT COLOR="{PK_BADGE_FG}" POINT-SIZE="9"><B>PK</B></FONT></TD>'
    elif kind == "fk":
        badge = f'<TD BGCOLOR="{FK_BADGE_BG}" WIDTH="34" ALIGN="CENTER"><FONT COLOR="{FK_BADGE_FG}" POINT-SIZE="9"><B>FK</B></FONT></TD>'
    else:
        badge = f'<TD BGCOLOR="{bg}" WIDTH="34"></TD>'

    if kind == "pk":
        name_cell = (
            f'<TD BGCOLOR="{bg}" ALIGN="LEFT" PORT="{port}">'
            f'<FONT COLOR="{PK_FIELD_FG}" POINT-SIZE="10"><B>{name}</B></FONT></TD>'
        )
    elif kind == "fk":
        name_cell = (
            f'<TD BGCOLOR="{bg}" ALIGN="LEFT" PORT="{port}">'
            f'<FONT COLOR="{FK_FIELD_FG}" POINT-SIZE="10"><I>{name}</I></FONT></TD>'
        )
    else:
        name_cell = (
            f'<TD BGCOLOR="{bg}" ALIGN="LEFT" PORT="{port}">'
            f'<FONT COLOR="{FIELD_FG}" POINT-SIZE="10">{name}</FONT></TD>'
        )

    type_html = f'<FONT COLOR="{TYPE_FG}" POINT-SIZE="9">{dtype}</FONT>'
    if kind == "fk" and target:
        type_html += (
            f'  <FONT COLOR="{TARGET_FG}" POINT-SIZE="9"><I>&#8594; {html_escape(target)}</I></FONT>'
        )
    type_cell = f'<TD BGCOLOR="{bg}" ALIGN="LEFT">{type_html}</TD>'
    return f'<TR>{badge}{name_cell}{type_cell}</TR>'


def table_html_with_ports(table_name: str, fields: list, header_color: str) -> str:
    rows = "".join(field_row_html_with_port(f, i, table_name) for i, f in enumerate(fields))
    header = (
        f'<TR><TD COLSPAN="3" BGCOLOR="{header_color}" ALIGN="CENTER" CELLPADDING="6" PORT="header_p">'
        f'<FONT COLOR="{HEADER_TEXT}" POINT-SIZE="13"><B>{html_escape(table_name)}</B></FONT>'
        f'</TD></TR>'
    )
    return (
        f'<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" '
        f'COLOR="{TABLE_BORDER}" CELLPADDING="3">'
        f'{header}{rows}</TABLE>>'
    )


def render_module(module: dict, out_dir: str = "."):
    num = module["module_num"]
    header_color = MODULE_COLORS[num]
    title = module["title"]
    tables = module["tables"]
    edges = module.get("edges", [])
    table_count = len(tables)
    layout = module.get("layout")

    # Use TB for grid-style layouts, LR for module 3 (one giant central table).
    rankdir = "LR" if num == 3 else "TB"

    g = Digraph("ERD", format="png")
    g.attr(
        rankdir=rankdir,
        bgcolor=BG,
        splines="spline",
        nodesep="0.6",
        ranksep="1.1",
        pad="0.6",
        fontname=FONT,
        labelloc="t",
        label=(
            f'<<FONT POINT-SIZE="22" COLOR="#202020"><B>{html_escape(title)}</B></FONT>'
            f'<BR/><FONT POINT-SIZE="12" COLOR="#5A5A5A">'
            f'{table_count} tables &#183; ERD v2 (audit-corrected)'
            f'</FONT>>'
        ),
        newrank="true",
    )
    g.attr("node", shape="plaintext", fontname=FONT)
    g.attr("edge", color="#3F4A55")

    for tname, fields in tables.items():
        g.node(tname, label=table_html_with_ports(tname, fields, header_color))

    if num == 3:
        # Module 3 special: jobs on the right, side tables stacked on the left.
        # Use invisible edges between left tables to preserve order top-to-bottom.
        left = module.get("left_chain", [])
        for a, b in zip(left, left[1:]):
            g.edge(a, b, style="invis", weight="100")
    elif layout:
        # Group each row at the same rank.
        for i, row in enumerate(layout):
            with g.subgraph(name=f"cluster_row_{i}") as s:
                s.attr(rank="same", style="invis")
                for t in row:
                    s.node(t)
        # Add invisible edges between consecutive rows' first tables to enforce
        # top-to-bottom order.
        for i in range(len(layout) - 1):
            if layout[i] and layout[i + 1]:
                g.edge(layout[i][0], layout[i + 1][0], style="invis", weight="50")
        # Add invisible edges within a row to preserve left-to-right order.
        for row in layout:
            for a, b in zip(row, row[1:]):
                g.edge(a, b, style="invis", weight="20")

    for child, field, parent, kind in edges:
        add_edge(g, child, field, parent, kind)

    out_path = os.path.join(out_dir, module["filename"])
    base, _ = os.path.splitext(out_path)
    g.render(filename=base, cleanup=True, format="png")
    return out_path


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    for mod in (MODULE2, MODULE3, MODULE4, MODULE5, MODULE6):
        path = render_module(mod, out_dir)
        print("Wrote:", path)
