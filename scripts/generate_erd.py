from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple
import math
import textwrap
import zipfile


@dataclass
class FieldDef:
    name: str
    dtype: str
    pk: bool = False
    fk: bool = False


@dataclass
class TableDef:
    name: str
    fields: List[FieldDef]


@dataclass
class Relation:
    source: str
    target: str
    label: str
    cardinality: str = "many-to-one"


@dataclass
class ModuleDef:
    title: str
    filename: str
    color: str
    light: str
    tables: List[TableDef]
    relations: List[Relation] = field(default_factory=list)


OUTPUT_DIR = Path("/workspace/erd")


def esc(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def field(name: str, dtype: str, *, pk: bool = False, fk: bool = False) -> FieldDef:
    return FieldDef(name=name, dtype=dtype, pk=pk, fk=fk)


modules: List[ModuleDef] = [
    ModuleDef(
        title="Module 1 - Auth & Accounts",
        filename="module-1-auth-accounts.svg",
        color="#2563eb",
        light="#eff6ff",
        tables=[
            TableDef(
                "accounts_accounts",
                [
                    field("accountID", "int8", pk=True),
                    field("email", "varchar"),
                    field("password", "varchar"),
                    field("isVerified", "bool"),
                    field("is_active", "bool"),
                    field("is_staff", "bool"),
                    field("KYCVerified", "bool"),
                    field("verification_level", "int4"),
                    field("banned_by_id", "int8", fk=True),
                    field("createdAt", "timestamptz"),
                    field("updatedAt", "timestamptz"),
                ],
            ),
            TableDef(
                "account_emailaddress",
                [
                    field("id", "int4", pk=True),
                    field("email", "varchar"),
                    field("verified", "bool"),
                    field("primary", "bool"),
                    field("user_id", "int8", fk=True),
                ],
            ),
            TableDef(
                "account_emailconfirmation",
                [
                    field("id", "int4", pk=True),
                    field("created", "timestamptz"),
                    field("sent", "timestamptz"),
                    field("key", "varchar"),
                    field("email_address_id", "int4", fk=True),
                ],
            ),
            TableDef(
                "socialaccount_socialaccount",
                [
                    field("id", "int4", pk=True),
                    field("provider", "varchar"),
                    field("uid", "varchar"),
                    field("user_id", "int8", fk=True),
                ],
            ),
            TableDef(
                "socialaccount_socialapp",
                [
                    field("id", "int4", pk=True),
                    field("provider", "varchar"),
                    field("name", "varchar"),
                    field("client_id", "varchar"),
                ],
            ),
            TableDef(
                "socialaccount_socialtoken",
                [
                    field("id", "int4", pk=True),
                    field("account_id", "int4", fk=True),
                    field("app_id", "int4", fk=True),
                    field("expires_at", "timestamptz"),
                ],
            ),
            TableDef(
                "auth_group",
                [
                    field("id", "int4", pk=True),
                    field("name", "varchar"),
                ],
            ),
            TableDef(
                "auth_permission",
                [
                    field("id", "int4", pk=True),
                    field("name", "varchar"),
                    field("content_type_id", "int4", fk=True),
                    field("codename", "varchar"),
                ],
            ),
            TableDef(
                "accounts_accounts_groups",
                [
                    field("id", "int8", pk=True),
                    field("accounts_id", "int8", fk=True),
                    field("group_id", "int4", fk=True),
                ],
            ),
            TableDef(
                "accounts_accounts_user_permissions",
                [
                    field("id", "int8", pk=True),
                    field("accounts_id", "int8", fk=True),
                    field("permission_id", "int4", fk=True),
                ],
            ),
            TableDef(
                "auth_group_permissions",
                [
                    field("id", "int8", pk=True),
                    field("group_id", "int4", fk=True),
                    field("permission_id", "int4", fk=True),
                ],
            ),
            TableDef(
                "django_session",
                [
                    field("session_key", "varchar", pk=True),
                    field("session_data", "text"),
                    field("expire_date", "timestamptz"),
                ],
            ),
            TableDef(
                "django_content_type",
                [
                    field("id", "int4", pk=True),
                    field("app_label", "varchar"),
                    field("model", "varchar"),
                ],
            ),
            TableDef(
                "django_admin_log",
                [
                    field("id", "int4", pk=True),
                    field("content_type_id", "int4", fk=True),
                    field("user_id", "int8", fk=True),
                    field("action_time", "timestamptz"),
                ],
            ),
            TableDef(
                "django_migrations",
                [
                    field("id", "int8", pk=True),
                    field("app", "varchar"),
                    field("name", "varchar"),
                    field("applied", "timestamptz"),
                ],
            ),
        ],
        relations=[
            Relation("account_emailaddress", "accounts_accounts", "belongs to"),
            Relation("account_emailconfirmation", "account_emailaddress", "confirms"),
            Relation("socialaccount_socialaccount", "accounts_accounts", "belongs to"),
            Relation("socialaccount_socialtoken", "socialaccount_socialaccount", "stores token for"),
            Relation("socialaccount_socialtoken", "socialaccount_socialapp", "uses app"),
            Relation("accounts_accounts_groups", "accounts_accounts", "maps account"),
            Relation("accounts_accounts_groups", "auth_group", "maps group"),
            Relation("accounts_accounts_user_permissions", "accounts_accounts", "grants to"),
            Relation("accounts_accounts_user_permissions", "auth_permission", "uses permission"),
            Relation("auth_group_permissions", "auth_group", "belongs to"),
            Relation("auth_group_permissions", "auth_permission", "includes"),
            Relation("auth_permission", "django_content_type", "describes"),
            Relation("django_admin_log", "accounts_accounts", "logged by"),
            Relation("django_admin_log", "django_content_type", "targets"),
        ],
    ),
    ModuleDef(
        title="Module 2 - Profiles & Specializations",
        filename="module-2-profiles-specializations.svg",
        color="#16a34a",
        light="#f0fdf4",
        tables=[
            TableDef(
                "accounts_profile",
                [
                    field("profileID", "int8", pk=True),
                    field("accountFK_id", "int8", fk=True),
                    field("firstName", "varchar"),
                    field("lastName", "varchar"),
                    field("profileType", "varchar"),
                    field("birthDate", "date"),
                    field("contactNum", "varchar"),
                ],
            ),
            TableDef(
                "accounts_clientprofile",
                [
                    field("id", "int8", pk=True),
                    field("profileID_id", "int8", fk=True),
                    field("clientRating", "int4"),
                    field("totalJobsPosted", "int4"),
                    field("activeJobsCount", "int4"),
                ],
            ),
            TableDef(
                "accounts_workerprofile",
                [
                    field("id", "int8", pk=True),
                    field("profileID_id", "int8", fk=True),
                    field("workerRating", "int4"),
                    field("availability_status", "varchar"),
                    field("hourly_rate", "numeric"),
                    field("daily_rate", "numeric"),
                ],
            ),
            TableDef(
                "accounts_agency",
                [
                    field("agencyId", "int8", pk=True),
                    field("accountFK_id", "int8", fk=True),
                    field("businessName", "varchar"),
                    field("city", "varchar"),
                    field("country", "varchar"),
                    field("contactNumber", "varchar"),
                ],
            ),
            TableDef(
                "specializations",
                [
                    field("specializationID", "int8", pk=True),
                    field("specializationName", "varchar"),
                    field("minimumRate", "numeric"),
                    field("rateType", "varchar"),
                    field("skillLevel", "varchar"),
                    field("created_by_agency_id", "int8", fk=True),
                    field("created_by_worker_id", "int8", fk=True),
                ],
            ),
            TableDef(
                "accounts_workerspecialization",
                [
                    field("id", "int8", pk=True),
                    field("specializationID_id", "int8", fk=True),
                    field("workerID_id", "int8", fk=True),
                    field("experienceYears", "int4"),
                    field("skillType", "varchar"),
                ],
            ),
            TableDef(
                "accounts_interestedjobs",
                [
                    field("id", "int8", pk=True),
                    field("clientID_id", "int8", fk=True),
                    field("specializationID_id", "int8", fk=True),
                ],
            ),
            TableDef(
                "accounts_city",
                [
                    field("cityID", "int4", pk=True),
                    field("name", "varchar"),
                    field("province", "varchar"),
                    field("region", "varchar"),
                ],
            ),
            TableDef(
                "accounts_barangay",
                [
                    field("barangayID", "int4", pk=True),
                    field("city_id", "int4", fk=True),
                    field("name", "varchar"),
                    field("zipCode", "varchar"),
                ],
            ),
        ],
        relations=[
            Relation("accounts_profile", "accounts_accounts", "belongs to"),
            Relation("accounts_clientprofile", "accounts_profile", "extends"),
            Relation("accounts_workerprofile", "accounts_profile", "extends"),
            Relation("accounts_agency", "accounts_accounts", "owned by"),
            Relation("accounts_workerspecialization", "accounts_workerprofile", "belongs to"),
            Relation("accounts_workerspecialization", "specializations", "references"),
            Relation("accounts_interestedjobs", "accounts_clientprofile", "belongs to"),
            Relation("accounts_interestedjobs", "specializations", "targets"),
            Relation("accounts_barangay", "accounts_city", "belongs to"),
            Relation("specializations", "accounts_agency", "created by"),
            Relation("specializations", "accounts_accounts", "created by"),
        ],
    ),
    ModuleDef(
        title="Module 3 - KYC Verification",
        filename="module-3-kyc-verification.svg",
        color="#ea580c",
        light="#fff7ed",
        tables=[
            TableDef(
                "accounts_kyc",
                [
                    field("kycID", "int8", pk=True),
                    field("accountFK_id", "int8", fk=True),
                    field("reviewedBy_id", "int8", fk=True),
                    field("kyc_status", "varchar"),
                    field("resubmissionCount", "int4"),
                    field("maxResubmissions", "int4"),
                ],
            ),
            TableDef(
                "accounts_kycfiles",
                [
                    field("kycFileID", "int8", pk=True),
                    field("kycID_id", "int8", fk=True),
                    field("fileURL", "varchar"),
                    field("idType", "varchar"),
                    field("ai_verification_status", "varchar"),
                ],
            ),
            TableDef(
                "kyc_extracted_data",
                [
                    field("extractedDataID", "int8", pk=True),
                    field("kycID_id", "int8", fk=True),
                    field("extracted_full_name", "varchar"),
                    field("confirmed_full_name", "varchar"),
                    field("extraction_status", "varchar"),
                ],
            ),
            TableDef(
                "agency_agencykyc",
                [
                    field("agencyKycID", "int8", pk=True),
                    field("accountFK_id", "int8", fk=True),
                    field("reviewedBy_id", "int8", fk=True),
                    field("status", "varchar"),
                    field("resubmissionCount", "int4"),
                ],
            ),
            TableDef(
                "agency_agencykycfile",
                [
                    field("fileID", "int8", pk=True),
                    field("agencyKyc_id", "int8", fk=True),
                    field("fileURL", "varchar"),
                    field("fileType", "varchar"),
                    field("ai_verification_status", "varchar"),
                ],
            ),
            TableDef(
                "agency_kyc_extracted_data",
                [
                    field("extractedDataID", "int8", pk=True),
                    field("agencyKyc_id", "int8", fk=True),
                    field("extracted_business_name", "varchar"),
                    field("confirmed_business_name", "varchar"),
                    field("extraction_status", "varchar"),
                ],
            ),
        ],
        relations=[
            Relation("accounts_kyc", "accounts_accounts", "submitted by"),
            Relation("accounts_kyc", "accounts_accounts", "reviewed by"),
            Relation("accounts_kycfiles", "accounts_kyc", "has file"),
            Relation("kyc_extracted_data", "accounts_kyc", "extracts"),
            Relation("agency_agencykyc", "accounts_accounts", "submitted by"),
            Relation("agency_agencykyc", "accounts_accounts", "reviewed by"),
            Relation("agency_agencykycfile", "agency_agencykyc", "has file"),
            Relation("agency_kyc_extracted_data", "agency_agencykyc", "extracts"),
        ],
    ),
    ModuleDef(
        title="Module 4 - Jobs & Applications",
        filename="module-4-jobs-applications.svg",
        color="#7c3aed",
        light="#faf5ff",
        tables=[
            TableDef(
                "jobs",
                [
                    field("jobID", "int8", pk=True),
                    field("clientID_id", "int8", fk=True),
                    field("categoryID_id", "int8", fk=True),
                    field("assignedWorkerID_id", "int8", fk=True),
                    field("assignedAgencyFK_id", "int8", fk=True),
                    field("assignedEmployeeID_id", "int8", fk=True),
                    field("cashPaymentApprovedBy_id", "int8", fk=True),
                    field("cancelledByAccountID_id", "int8", fk=True),
                    field("title", "varchar"),
                    field("status", "varchar"),
                    field("budget", "numeric"),
                ],
            ),
            TableDef(
                "job_skill_slots",
                [
                    field("skillSlotID", "int8", pk=True),
                    field("jobID_id", "int8", fk=True),
                    field("specializationID_id", "int8", fk=True),
                    field("invited_agency_id", "int8", fk=True),
                    field("workers_needed", "int4"),
                    field("status", "varchar"),
                ],
            ),
            TableDef(
                "job_applications",
                [
                    field("applicationID", "int8", pk=True),
                    field("jobID_id", "int8", fk=True),
                    field("workerID_id", "int8", fk=True),
                    field("applied_skill_slot_id", "int8", fk=True),
                    field("status", "varchar"),
                    field("proposedBudget", "numeric"),
                ],
            ),
            TableDef(
                "job_worker_assignments",
                [
                    field("assignmentID", "int8", pk=True),
                    field("jobID_id", "int8", fk=True),
                    field("skillSlotID_id", "int8", fk=True),
                    field("workerID_id", "int8", fk=True),
                    field("assignment_status", "varchar"),
                    field("slot_position", "int4"),
                ],
            ),
            TableDef(
                "job_employee_assignments",
                [
                    field("assignmentID", "int8", pk=True),
                    field("job_id", "int8", fk=True),
                    field("employee_id", "int8", fk=True),
                    field("skill_slot_id", "int8", fk=True),
                    field("assignedBy_id", "int8", fk=True),
                    field("status", "varchar"),
                ],
            ),
            TableDef(
                "price_negotiations",
                [
                    field("negotiationID", "int8", pk=True),
                    field("application_id", "int8", fk=True),
                    field("actor", "varchar"),
                    field("round_number", "int2"),
                    field("status", "varchar"),
                ],
            ),
            TableDef(
                "saved_jobs",
                [
                    field("savedJobID", "int8", pk=True),
                    field("jobID_id", "int8", fk=True),
                    field("workerID_id", "int8", fk=True),
                    field("savedAt", "timestamptz"),
                ],
            ),
        ],
        relations=[
            Relation("jobs", "accounts_clientprofile", "posted by"),
            Relation("jobs", "specializations", "categorized as"),
            Relation("jobs", "accounts_workerprofile", "assigned worker"),
            Relation("jobs", "accounts_agency", "assigned agency"),
            Relation("jobs", "agency_employees", "assigned employee"),
            Relation("jobs", "accounts_accounts", "approved by"),
            Relation("jobs", "accounts_accounts", "cancelled by"),
            Relation("job_skill_slots", "jobs", "belongs to"),
            Relation("job_skill_slots", "specializations", "requires"),
            Relation("job_skill_slots", "accounts_agency", "invites"),
            Relation("job_applications", "jobs", "applies to"),
            Relation("job_applications", "accounts_workerprofile", "submitted by"),
            Relation("job_applications", "job_skill_slots", "targets"),
            Relation("job_worker_assignments", "jobs", "belongs to"),
            Relation("job_worker_assignments", "job_skill_slots", "fills"),
            Relation("job_worker_assignments", "accounts_workerprofile", "assigns"),
            Relation("job_employee_assignments", "jobs", "belongs to"),
            Relation("job_employee_assignments", "agency_employees", "assigns"),
            Relation("job_employee_assignments", "job_skill_slots", "fills"),
            Relation("job_employee_assignments", "accounts_accounts", "assigned by"),
            Relation("price_negotiations", "job_applications", "negotiates"),
            Relation("saved_jobs", "jobs", "saves"),
            Relation("saved_jobs", "accounts_workerprofile", "saved by"),
        ],
    ),
    ModuleDef(
        title="Module 5 - Job Operations",
        filename="module-5-job-operations.svg",
        color="#d97706",
        light="#fffbeb",
        tables=[
            TableDef(
                "job_logs",
                [
                    field("logID", "int8", pk=True),
                    field("jobID_id", "int8", fk=True),
                    field("changedBy_id", "int8", fk=True),
                    field("actionType", "varchar"),
                    field("newStatus", "varchar"),
                ],
            ),
            TableDef(
                "job_materials",
                [
                    field("jobMaterialID", "int8", pk=True),
                    field("jobID_id", "int8", fk=True),
                    field("workerMaterialID_id", "int8", fk=True),
                    field("name", "varchar"),
                    field("source", "varchar"),
                ],
            ),
            TableDef(
                "job_photos",
                [
                    field("photoID", "int8", pk=True),
                    field("jobID_id", "int8", fk=True),
                    field("photoURL", "varchar"),
                ],
            ),
            TableDef(
                "job_reviews",
                [
                    field("reviewID", "int8", pk=True),
                    field("jobID_id", "int8", fk=True),
                    field("flaggedBy_id", "int8", fk=True),
                    field("revieweeID_id", "int8", fk=True),
                    field("reviewerID_id", "int8", fk=True),
                    field("revieweeAgencyID_id", "int8", fk=True),
                    field("revieweeEmployeeID_id", "int8", fk=True),
                    field("revieweeProfileID_id", "int8", fk=True),
                    field("rating", "numeric"),
                    field("status", "varchar"),
                ],
            ),
            TableDef(
                "job_disputes",
                [
                    field("disputeID", "int8", pk=True),
                    field("jobID_id", "int8", fk=True),
                    field("status", "varchar"),
                    field("priority", "varchar"),
                    field("reason", "varchar"),
                ],
            ),
            TableDef(
                "dispute_evidence",
                [
                    field("evidenceID", "int8", pk=True),
                    field("disputeID_id", "int8", fk=True),
                    field("uploadedBy_id", "int8", fk=True),
                    field("imageURL", "varchar"),
                ],
            ),
            TableDef(
                "review_skill_tags",
                [
                    field("tagID", "int8", pk=True),
                    field("reviewID_id", "int8", fk=True),
                    field("workerSpecializationID_id", "int8", fk=True),
                ],
            ),
        ],
        relations=[
            Relation("job_logs", "jobs", "belongs to"),
            Relation("job_logs", "accounts_accounts", "changed by"),
            Relation("job_materials", "jobs", "belongs to"),
            Relation("job_materials", "worker_materials", "references"),
            Relation("job_photos", "jobs", "belongs to"),
            Relation("job_reviews", "jobs", "belongs to"),
            Relation("job_reviews", "accounts_accounts", "flagged by"),
            Relation("job_reviews", "accounts_accounts", "reviews"),
            Relation("job_reviews", "accounts_accounts", "reviewed"),
            Relation("job_reviews", "accounts_agency", "reviews agency"),
            Relation("job_reviews", "agency_employees", "reviews employee"),
            Relation("job_reviews", "accounts_profile", "reviews profile"),
            Relation("job_disputes", "jobs", "belongs to"),
            Relation("dispute_evidence", "job_disputes", "supports"),
            Relation("dispute_evidence", "accounts_accounts", "uploaded by"),
            Relation("review_skill_tags", "job_reviews", "tags"),
            Relation("review_skill_tags", "accounts_workerspecialization", "references"),
        ],
    ),
    ModuleDef(
        title="Module 6 - Daily Jobs",
        filename="module-6-daily-jobs.svg",
        color="#db2777",
        light="#fdf2f8",
        tables=[
            TableDef(
                "daily_attendance",
                [
                    field("attendanceID", "int8", pk=True),
                    field("jobID_id", "int8", fk=True),
                    field("workerID_id", "int8", fk=True),
                    field("assignmentID_id", "int8", fk=True),
                    field("employeeID_id", "int8", fk=True),
                    field("date", "date"),
                    field("status", "varchar"),
                ],
            ),
            TableDef(
                "daily_job_extensions",
                [
                    field("extensionID", "int8", pk=True),
                    field("jobID_id", "int8", fk=True),
                    field("requestedByUser_id", "int8", fk=True),
                    field("additional_days", "int4"),
                    field("status", "varchar"),
                ],
            ),
            TableDef(
                "daily_rate_changes",
                [
                    field("changeID", "int8", pk=True),
                    field("jobID_id", "int8", fk=True),
                    field("requestedByUser_id", "int8", fk=True),
                    field("old_rate", "numeric"),
                    field("new_rate", "numeric"),
                    field("status", "varchar"),
                ],
            ),
            TableDef(
                "daily_skip_day_requests",
                [
                    field("skipRequestID", "int8", pk=True),
                    field("jobID_id", "int8", fk=True),
                    field("requestedByUser_id", "int8", fk=True),
                    field("reviewedByUser_id", "int8", fk=True),
                    field("target_employee_id", "int8", fk=True),
                    field("target_worker_account_id", "int8", fk=True),
                    field("status", "varchar"),
                    field("request_date", "date"),
                ],
            ),
            TableDef(
                "backjob_schedule_confirmations",
                [
                    field("confirmationID", "int8", pk=True),
                    field("assignmentID_id", "int8", fk=True),
                    field("confirmedBy_id", "int8", fk=True),
                    field("disputeID_id", "int8", fk=True),
                    field("confirmed", "bool"),
                ],
            ),
        ],
        relations=[
            Relation("daily_attendance", "jobs", "belongs to"),
            Relation("daily_attendance", "accounts_workerprofile", "tracks worker"),
            Relation("daily_attendance", "job_worker_assignments", "tracks assignment"),
            Relation("daily_attendance", "agency_employees", "tracks employee"),
            Relation("daily_job_extensions", "jobs", "extends"),
            Relation("daily_job_extensions", "accounts_accounts", "requested by"),
            Relation("daily_rate_changes", "jobs", "changes rate for"),
            Relation("daily_rate_changes", "accounts_accounts", "requested by"),
            Relation("daily_skip_day_requests", "jobs", "belongs to"),
            Relation("daily_skip_day_requests", "accounts_accounts", "requested by"),
            Relation("daily_skip_day_requests", "accounts_accounts", "reviewed by"),
            Relation("daily_skip_day_requests", "agency_employees", "targets employee"),
            Relation("daily_skip_day_requests", "accounts_accounts", "targets worker"),
            Relation("backjob_schedule_confirmations", "job_worker_assignments", "confirms"),
            Relation("backjob_schedule_confirmations", "accounts_accounts", "confirmed by"),
            Relation("backjob_schedule_confirmations", "job_disputes", "belongs to"),
        ],
    ),
    ModuleDef(
        title="Module 7 - Finance & Payments",
        filename="module-7-finance-payments.svg",
        color="#0f766e",
        light="#f0fdfa",
        tables=[
            TableDef(
                "accounts_userpaymentmethod",
                [
                    field("id", "int8", pk=True),
                    field("accountFK_id", "int8", fk=True),
                    field("methodType", "varchar"),
                    field("accountName", "varchar"),
                    field("isPrimary", "bool"),
                    field("isVerified", "bool"),
                ],
            ),
            TableDef(
                "accounts_wallet",
                [
                    field("walletID", "int8", pk=True),
                    field("accountFK_id", "int8", fk=True),
                    field("preferredPaymentMethodID_id", "int8", fk=True),
                    field("balance", "numeric"),
                    field("reservedBalance", "numeric"),
                    field("pendingEarnings", "numeric"),
                ],
            ),
            TableDef(
                "accounts_transaction",
                [
                    field("transactionID", "int8", pk=True),
                    field("walletID_id", "int8", fk=True),
                    field("relatedJobPosting_id", "int8", fk=True),
                    field("processedByAdmin_id", "int8", fk=True),
                    field("transactionType", "varchar"),
                    field("amount", "numeric"),
                    field("status", "varchar"),
                ],
            ),
        ],
        relations=[
            Relation("accounts_userpaymentmethod", "accounts_accounts", "belongs to"),
            Relation("accounts_wallet", "accounts_accounts", "belongs to"),
            Relation("accounts_wallet", "accounts_userpaymentmethod", "prefers"),
            Relation("accounts_transaction", "accounts_wallet", "belongs to"),
            Relation("accounts_transaction", "jobs", "related to"),
            Relation("accounts_transaction", "accounts_accounts", "processed by"),
        ],
    ),
    ModuleDef(
        title="Module 8 - Messaging",
        filename="module-8-messaging.svg",
        color="#7c3aed",
        light="#f5f3ff",
        tables=[
            TableDef(
                "conversation",
                [
                    field("conversationID", "int8", pk=True),
                    field("client_id", "int8", fk=True),
                    field("worker_id", "int8", fk=True),
                    field("agency_id", "int8", fk=True),
                    field("lastMessageSender_id", "int8", fk=True),
                    field("relatedJobPosting_id", "int8", fk=True),
                    field("status", "varchar"),
                ],
            ),
            TableDef(
                "conversation_participants",
                [
                    field("participantID", "int8", pk=True),
                    field("conversation_id", "int8", fk=True),
                    field("profile_id", "int8", fk=True),
                    field("skill_slot_id", "int8", fk=True),
                    field("admin_account_id", "int8", fk=True),
                    field("participant_type", "varchar"),
                ],
            ),
            TableDef(
                "message",
                [
                    field("messageID", "int8", pk=True),
                    field("conversationID_id", "int8", fk=True),
                    field("sender_id", "int8", fk=True),
                    field("senderAgency_id", "int8", fk=True),
                    field("sender_admin_id", "int8", fk=True),
                    field("messageType", "varchar"),
                ],
            ),
            TableDef(
                "message_attachment",
                [
                    field("attachmentID", "int8", pk=True),
                    field("messageID_id", "int8", fk=True),
                    field("fileURL", "varchar"),
                    field("fileType", "varchar"),
                ],
            ),
        ],
        relations=[
            Relation("conversation", "accounts_profile", "has client"),
            Relation("conversation", "accounts_profile", "has worker"),
            Relation("conversation", "accounts_agency", "has agency"),
            Relation("conversation", "accounts_profile", "last sender"),
            Relation("conversation", "jobs", "about job"),
            Relation("conversation_participants", "conversation", "belongs to"),
            Relation("conversation_participants", "accounts_profile", "joins"),
            Relation("conversation_participants", "job_skill_slots", "represents slot"),
            Relation("conversation_participants", "accounts_accounts", "joins admin"),
            Relation("message", "conversation", "belongs to"),
            Relation("message", "accounts_profile", "sent by"),
            Relation("message", "accounts_agency", "sent by agency"),
            Relation("message", "accounts_accounts", "sent by admin"),
            Relation("message_attachment", "message", "attached to"),
        ],
    ),
    ModuleDef(
        title="Module 9 - Admin Panel",
        filename="module-9-admin-panel.svg",
        color="#4b5563",
        light="#f8fafc",
        tables=[
            TableDef(
                "adminpanel_adminaccount",
                [
                    field("adminID", "int8", pk=True),
                    field("accountFK_id", "int8", fk=True),
                    field("role", "varchar"),
                    field("isActive", "bool"),
                ],
            ),
            TableDef(
                "adminpanel_auditlog",
                [
                    field("auditLogID", "int8", pk=True),
                    field("adminFK_id", "int8", fk=True),
                    field("entityType", "varchar"),
                    field("entityID", "varchar"),
                    field("action", "varchar"),
                ],
            ),
            TableDef(
                "adminpanel_kyclogs",
                [
                    field("kycLogID", "int8", pk=True),
                    field("accountFK_id", "int8", fk=True),
                    field("reviewedBy_id", "int8", fk=True),
                    field("kycID", "int8"),
                    field("action", "varchar"),
                ],
            ),
            TableDef(
                "adminpanel_supportticket",
                [
                    field("ticketID", "int8", pk=True),
                    field("assignedTo_id", "int8", fk=True),
                    field("userFK_id", "int8", fk=True),
                    field("agencyFK_id", "int8", fk=True),
                    field("status", "varchar"),
                    field("priority", "varchar"),
                ],
            ),
            TableDef(
                "adminpanel_supportticketreply",
                [
                    field("replyID", "int8", pk=True),
                    field("senderFK_id", "int8", fk=True),
                    field("ticketFK_id", "int8", fk=True),
                    field("isSystemMessage", "bool"),
                ],
            ),
            TableDef(
                "adminpanel_userreport",
                [
                    field("reportID", "int8", pk=True),
                    field("reportedUserFK_id", "int8", fk=True),
                    field("reporterFK_id", "int8", fk=True),
                    field("reviewedBy_id", "int8", fk=True),
                    field("status", "varchar"),
                ],
            ),
            TableDef(
                "adminpanel_platformsettings",
                [
                    field("settingsID", "int8", pk=True),
                    field("updatedBy_id", "int8", fk=True),
                    field("platformFeePercentage", "numeric"),
                    field("maintenanceMode", "bool"),
                ],
            ),
            TableDef(
                "adminpanel_cannedresponse",
                [
                    field("responseID", "int8", pk=True),
                    field("createdBy_id", "int8", fk=True),
                    field("title", "varchar"),
                    field("category", "varchar"),
                ],
            ),
            TableDef(
                "adminpanel_contentmoderationterm",
                [
                    field("termID", "int8", pk=True),
                    field("createdBy_id", "int8", fk=True),
                    field("updatedBy_id", "int8", fk=True),
                    field("term", "varchar"),
                    field("isActive", "bool"),
                ],
            ),
            TableDef(
                "adminpanel_faq",
                [
                    field("faqID", "int8", pk=True),
                    field("question", "varchar"),
                    field("category", "varchar"),
                    field("isPublished", "bool"),
                ],
            ),
            TableDef(
                "adminpanel_systemroles",
                [
                    field("systemRoleID", "int8", pk=True),
                    field("accountID_id", "int8", fk=True),
                    field("systemRole", "varchar"),
                ],
            ),
        ],
        relations=[
            Relation("adminpanel_adminaccount", "accounts_accounts", "belongs to"),
            Relation("adminpanel_auditlog", "accounts_accounts", "logged by"),
            Relation("adminpanel_kyclogs", "accounts_accounts", "about account"),
            Relation("adminpanel_kyclogs", "accounts_accounts", "reviewed by"),
            Relation("adminpanel_supportticket", "accounts_accounts", "opened by"),
            Relation("adminpanel_supportticket", "accounts_agency", "for agency"),
            Relation("adminpanel_supportticket", "accounts_accounts", "assigned to"),
            Relation("adminpanel_supportticketreply", "accounts_accounts", "sent by"),
            Relation("adminpanel_supportticketreply", "adminpanel_supportticket", "belongs to"),
            Relation("adminpanel_userreport", "accounts_accounts", "reports"),
            Relation("adminpanel_userreport", "accounts_accounts", "reported by"),
            Relation("adminpanel_userreport", "accounts_accounts", "reviewed by"),
            Relation("adminpanel_platformsettings", "accounts_accounts", "updated by"),
            Relation("adminpanel_cannedresponse", "accounts_accounts", "created by"),
            Relation("adminpanel_contentmoderationterm", "accounts_accounts", "created by"),
            Relation("adminpanel_contentmoderationterm", "accounts_accounts", "updated by"),
            Relation("adminpanel_systemroles", "accounts_accounts", "assigned to"),
        ],
    ),
    ModuleDef(
        title="Module 10 - Workers & Agencies",
        filename="module-10-workers-agencies.svg",
        color="#dc2626",
        light="#fff1f2",
        tables=[
            TableDef(
                "agency_employees",
                [
                    field("employeeID", "int8", pk=True),
                    field("agency_id", "int8", fk=True),
                    field("email", "varchar"),
                    field("role", "varchar"),
                    field("isActive", "bool"),
                ],
            ),
            TableDef(
                "worker_certifications",
                [
                    field("certificationID", "int8", pk=True),
                    field("verified_by_id", "int8", fk=True),
                    field("workerID_id", "int8", fk=True),
                    field("specializationID_id", "int8", fk=True),
                    field("name", "varchar"),
                    field("is_verified", "bool"),
                ],
            ),
            TableDef(
                "worker_materials",
                [
                    field("materialID", "int8", pk=True),
                    field("workerID_id", "int8", fk=True),
                    field("categoryID_id", "int8", fk=True),
                    field("agencyID_id", "int8", fk=True),
                    field("name", "varchar"),
                    field("is_available", "bool"),
                ],
            ),
            TableDef(
                "worker_portfolio",
                [
                    field("portfolioID", "int8", pk=True),
                    field("workerID_id", "int8", fk=True),
                    field("image_url", "varchar"),
                    field("display_order", "int4"),
                ],
            ),
            TableDef(
                "profiles_workerproduct",
                [
                    field("productID", "int8", pk=True),
                    field("categoryID_id", "int8", fk=True),
                    field("workerID_id", "int8", fk=True),
                    field("productName", "varchar"),
                    field("price", "numeric"),
                ],
            ),
            TableDef(
                "accounts_notification",
                [
                    field("notificationID", "int8", pk=True),
                    field("accountFK_id", "int8", fk=True),
                    field("relatedKYCLogID", "int8"),
                    field("relatedJobID", "int8"),
                    field("relatedApplicationID", "int8"),
                    field("title", "varchar"),
                    field("isRead", "bool"),
                ],
            ),
            TableDef(
                "accounts_notificationsettings",
                [
                    field("settingsID", "int8", pk=True),
                    field("accountFK_id", "int8", fk=True),
                    field("pushEnabled", "bool"),
                    field("messages", "bool"),
                    field("payments", "bool"),
                ],
            ),
            TableDef(
                "accounts_pushtoken",
                [
                    field("tokenID", "int8", pk=True),
                    field("accountFK_id", "int8", fk=True),
                    field("pushToken", "varchar"),
                    field("deviceType", "varchar"),
                    field("isActive", "bool"),
                ],
            ),
            TableDef(
                "certification_logs",
                [
                    field("certLogID", "int8", pk=True),
                    field("reviewedBy_id", "int8", fk=True),
                    field("workerID_id", "int8", fk=True),
                    field("certificationID", "int8"),
                    field("action", "varchar"),
                ],
            ),
        ],
        relations=[
            Relation("agency_employees", "accounts_accounts", "belongs to agency"),
            Relation("worker_certifications", "accounts_accounts", "verified by"),
            Relation("worker_certifications", "accounts_workerprofile", "belongs to worker"),
            Relation("worker_certifications", "accounts_workerspecialization", "for specialization"),
            Relation("worker_materials", "accounts_workerprofile", "belongs to worker"),
            Relation("worker_materials", "specializations", "categorized as"),
            Relation("worker_materials", "accounts_agency", "owned by agency"),
            Relation("worker_portfolio", "accounts_workerprofile", "belongs to"),
            Relation("profiles_workerproduct", "specializations", "categorized as"),
            Relation("profiles_workerproduct", "accounts_workerprofile", "belongs to"),
            Relation("accounts_notification", "accounts_accounts", "belongs to"),
            Relation("accounts_notificationsettings", "accounts_accounts", "belongs to"),
            Relation("accounts_pushtoken", "accounts_accounts", "belongs to"),
            Relation("certification_logs", "accounts_accounts", "reviewed by"),
            Relation("certification_logs", "accounts_workerprofile", "belongs to"),
        ],
    ),
]


def draw_marker_defs() -> str:
    return """
    <marker id="one" viewBox="0 0 12 12" refX="2" refY="6" markerWidth="10" markerHeight="10" orient="auto">
      <path d="M 2 1 L 2 11" stroke="#475569" stroke-width="1.8" fill="none" stroke-linecap="round"/>
    </marker>
    <marker id="crow" viewBox="0 0 16 12" refX="14" refY="6" markerWidth="12" markerHeight="12" orient="auto">
      <path d="M 1 6 L 14 6 M 14 6 L 2 1 M 14 6 L 2 11" stroke="#475569" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
    """


def style_block() -> str:
    return """
    <style>
      .title { font: 700 28px Inter, Arial, sans-serif; fill: #0f172a; }
      .subtitle { font: 400 15px Inter, Arial, sans-serif; fill: #475569; }
      .module-title { font: 700 18px Inter, Arial, sans-serif; }
      .table-title { font: 700 15px Inter, Arial, sans-serif; fill: #ffffff; }
      .colhead { font: 700 11px Inter, Arial, sans-serif; fill: #475569; }
      .cell { font: 11px Inter, Arial, sans-serif; fill: #111827; }
      .dtype { font: 11px "SFMono-Regular", Consolas, monospace; fill: #475569; }
      .badge { font: 700 10px Inter, Arial, sans-serif; }
      .line-label {
        font: 600 12px Inter, Arial, sans-serif;
        fill: #334155;
        paint-order: stroke;
        stroke: #ffffff;
        stroke-width: 4px;
        stroke-linejoin: round;
      }
      .connector {
        fill: none;
        stroke: #475569;
        stroke-width: 1.8;
        marker-start: url(#one);
        marker-end: url(#crow);
      }
    </style>
    """


def table_dimensions(table: TableDef) -> Tuple[int, int]:
    row_h = 20
    header_h = 34
    top_h = 26
    height = top_h + header_h + len(table.fields) * row_h + 12
    width = 330
    return width, height


def render_table(table: TableDef, x: int, y: int, color: str, light: str) -> Tuple[str, int, int]:
    width, height = table_dimensions(table)
    top_h = 26
    header_h = 34
    row_h = 20
    parts = [
        f'<g>',
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="14" ry="14" fill="{light}" stroke="{color}" stroke-width="2"/>',
        f'<rect x="{x}" y="{y}" width="{width}" height="{top_h}" rx="14" ry="14" fill="{color}"/>',
        f'<rect x="{x}" y="{y + top_h}" width="{width}" height="{header_h}" fill="#ffffff" stroke="none"/>',
        f'<text x="{x + 14}" y="{y + 18}" class="table-title">{esc(table.name)}</text>',
        f'<text x="{x + 14}" y="{y + top_h + 18}" class="colhead">Key</text>',
        f'<text x="{x + 72}" y="{y + top_h + 18}" class="colhead">Field</text>',
        f'<text x="{x + width - 80}" y="{y + top_h + 18}" class="colhead">Type</text>',
    ]

    cy = y + top_h + header_h
    for idx, fdef in enumerate(table.fields):
        fy = cy + idx * row_h
        if idx % 2 == 0:
            parts.append(f'<rect x="{x+1}" y="{fy}" width="{width-2}" height="{row_h}" fill="#f8fafc"/>')
        badge = []
        if fdef.pk:
            badge.append(("PK", "#f59e0b", "#ffffff"))
        if fdef.fk:
            badge.append(("FK", "#2563eb", "#ffffff"))
        bx = x + 10
        for label, bg, fg in badge:
            parts.append(
                f'<rect x="{bx}" y="{fy + 4}" width="24" height="12" rx="6" ry="6" fill="{bg}"/>'
                f'<text x="{bx + 12}" y="{fy + 13}" text-anchor="middle" class="badge" fill="{fg}">{label}</text>'
            )
            bx += 28
        parts.append(f'<text x="{x + 72}" y="{fy + 14}" class="cell">{esc(fdef.name)}</text>')
        parts.append(f'<text x="{x + width - 80}" y="{fy + 14}" class="dtype">{esc(fdef.dtype)}</text>')
    parts.append("</g>")
    return "\n".join(parts), width, height


def module_table_positions(module: ModuleDef) -> Dict[str, Tuple[int, int, int, int]]:
    cols = 3
    margin_x = 40
    margin_top = 108
    col_w = 360
    gap_y = 36
    positions: Dict[str, Tuple[int, int, int, int]] = {}
    col_heights = [margin_top] * cols
    for index, table in enumerate(module.tables):
        width, height = table_dimensions(table)
        col = index % cols
        x = margin_x + col * col_w
        y = col_heights[col]
        positions[table.name] = (x, y, width, height)
        col_heights[col] += height + gap_y
    return positions


def side_anchor(src: Tuple[int, int, int, int], dst: Tuple[int, int, int, int]) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    sx, sy, sw, sh = src
    dx, dy, dw, dh = dst
    scy = sy + sh / 2
    dcy = dy + dh / 2
    if sx + sw <= dx:
        return (sx + sw, scy), (dx, dcy)
    if dx + dw <= sx:
        return (sx, scy), (dx + dw, dcy)
    if scy <= dcy:
        return (sx + sw / 2, sy), (dx + dw / 2, dy)
    return (sx + sw / 2, sy + sh), (dx + dw / 2, dy + dh)


def connector_path(start: Tuple[float, float], end: Tuple[float, float]) -> Tuple[str, Tuple[float, float]]:
    sx, sy = start
    ex, ey = end
    # Prefer side connections; if top/bottom are selected, still create orthogonal path.
    if abs(sx - ex) > abs(sy - ey):
        midx = (sx + ex) / 2
        d = f"M {sx:.1f} {sy:.1f} L {midx:.1f} {sy:.1f} L {midx:.1f} {ey:.1f} L {ex:.1f} {ey:.1f}"
        label_pt = (midx, (sy + ey) / 2 - 8)
    else:
        midy = (sy + ey) / 2
        d = f"M {sx:.1f} {sy:.1f} L {sx:.1f} {midy:.1f} L {ex:.1f} {midy:.1f} L {ex:.1f} {ey:.1f}"
        label_pt = ((sx + ex) / 2, midy - 8)
    return d, label_pt


def render_module(module: ModuleDef) -> str:
    width = 1200
    height = 1650
    positions = module_table_positions(module)
    fragments = []
    for table in module.tables:
        x, y, _, _ = positions[table.name]
        svg, _, _ = render_table(table, x, y, module.color, module.light)
        fragments.append(svg)

    connectors = []
    labels = []
    for rel in module.relations:
        if rel.source not in positions or rel.target not in positions:
            continue
        start, end = side_anchor(positions[rel.source], positions[rel.target])
        if start[0] == positions[rel.source][0] + positions[rel.source][2] / 2 or end[0] == positions[rel.target][0] + positions[rel.target][2] / 2:
            # force side anchors only
            sx, sy, sw, sh = positions[rel.source]
            tx, ty, tw, th = positions[rel.target]
            if sx < tx:
                start = (sx + sw, sy + sh / 2)
                end = (tx, ty + th / 2)
            else:
                start = (sx, sy + sh / 2)
                end = (tx + tw, ty + th / 2)
        path_d, label_pt = connector_path(start, end)
        connectors.append(f'<path class="connector" d="{path_d}"/>')
        labels.append(
            f'<text x="{label_pt[0]:.1f}" y="{label_pt[1]:.1f}" text-anchor="middle" class="line-label">{esc(rel.label)}</text>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
  <title>{esc(module.title)}</title>
  <defs>
    {draw_marker_defs()}
    {style_block()}
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#0f172a" flood-opacity="0.10"/>
    </filter>
  </defs>
  <rect width="{width}" height="{height}" fill="#ffffff"/>
  <text x="40" y="48" class="title">{esc(module.title)}</text>
  <text x="40" y="72" class="subtitle">PK and FK fields shown. Crow's foot connectors use side-only routing with relationship labels.</text>
  <g filter="url(#shadow)">
    {' '.join(connectors)}
    {' '.join(fragments)}
    {' '.join(labels)}
  </g>
</svg>
"""


def render_overview(modules: List[ModuleDef]) -> str:
    width, height = 1600, 1000
    positions = [
        (40, 120), (540, 120), (1040, 120),
        (40, 360), (540, 360), (1040, 360),
        (40, 650), (540, 650), (1040, 650), (540, 820),
    ]
    cards = []
    for module, (x, y) in zip(modules, positions):
        lines = [table.name for table in module.tables[:8]]
        box_h = 180 if len(lines) <= 7 else 220
        line_text = "".join(
            f'<text x="{x+18}" y="{y+72+i*18}" class="cell">{esc(line)}</text>'
            for i, line in enumerate(lines)
        )
        cards.append(
            f'<g filter="url(#shadow)">'
            f'<rect x="{x}" y="{y}" width="420" height="{box_h}" rx="20" ry="20" fill="{module.light}" stroke="{module.color}" stroke-width="2"/>'
            f'<rect x="{x}" y="{y}" width="420" height="44" rx="20" ry="20" fill="{module.color}"/>'
            f'<text x="{x+18}" y="{y+28}" fill="#ffffff" class="module-title">{esc(module.title)}</text>'
            f'{line_text}'
            f'</g>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    {style_block()}
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#0f172a" flood-opacity="0.10"/>
    </filter>
  </defs>
  <rect width="{width}" height="{height}" fill="#ffffff"/>
  <text x="800" y="48" text-anchor="middle" class="title">Platform Database - Module ERD Overview</text>
  <text x="800" y="74" text-anchor="middle" class="subtitle">Detailed ERD pack is divided by module so PK/FK fields remain readable in paper documents.</text>
  {' '.join(cards)}
</svg>
"""


def write_files() -> List[Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    files: List[Path] = []
    overview = OUTPUT_DIR / "00-overview.svg"
    overview.write_text(render_overview(modules), encoding="utf-8")
    files.append(overview)
    for module in modules:
        path = OUTPUT_DIR / module.filename
        path.write_text(render_module(module), encoding="utf-8")
        files.append(path)
    return files


def zip_outputs(files: List[Path]) -> Path:
    zip_path = OUTPUT_DIR / "erd-module-pack.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            zf.write(file, arcname=file.name)
    return zip_path


def main() -> None:
    files = write_files()
    zip_path = zip_outputs(files)
    print(f"Generated {len(files)} SVG files")
    print(zip_path)


if __name__ == "__main__":
    main()
