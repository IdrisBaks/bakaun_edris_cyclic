from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image, ImageDraw, ImageFont


@dataclass
class Column:
    name: str
    dtype: str


@dataclass
class TableDef:
    name: str
    columns: List[Column]
    pk: str
    unique_cols: set[str]
    external: bool = False


Color = Tuple[int, int, int]


BG: Color = (255, 255, 255)
HEADER_BG: Color = (34, 52, 74)
HEADER_TEXT: Color = (255, 255, 255)
ROW_LIGHT: Color = (250, 250, 251)
ROW_DARK: Color = (242, 244, 247)
BORDER: Color = (80, 88, 98)
TEXT: Color = (32, 38, 46)
FK_TEXT: Color = (35, 95, 170)
PK_TEXT: Color = (184, 133, 32)
LINE: Color = (110, 120, 130)

MARGIN_X = 36
MARGIN_Y = 34
TITLE_SPACE = 78
TABLE_W = 500
EXT_TABLE_W = 280
HEADER_H = 28
ROW_H = 20
COL_GAP = 30
ROW_GAP = 28


def col(spec: str) -> Column:
    name, dtype = spec.split(":", 1)
    return Column(name=name, dtype=dtype)


SCHEMA: Dict[str, List[Column]] = {
    # Module 2
    "accounts_profile": list(
        map(
            col,
            [
                "profileID:int8",
                "profileImg:varchar",
                "firstName:varchar",
                "lastName:varchar",
                "contactNum:varchar",
                "birthDate:date",
                "profileType:varchar",
                "accountFK_id:int8",
                "middleName:varchar",
                "latitude:numeric",
                "location_sharing_enabled:bool",
                "location_updated_at:timestamptz",
                "longitude:numeric",
            ],
        )
    ),
    "accounts_workerprofile": list(
        map(
            col,
            [
                "id:int8",
                "description:varchar",
                "workerRating:int4",
                "totalEarningGross:numeric",
                "availability_status:varchar",
                "profileID_id:int8",
                "bio:varchar",
                "hourly_rate:numeric",
                "profile_completion_percentage:int4",
                "soft_skills:text",
                "daily_rate:numeric",
                "is_available_daily_jobs:bool",
            ],
        )
    ),
    "accounts_clientprofile": list(
        map(
            col,
            [
                "id:int8",
                "description:varchar",
                "totalJobsPosted:int4",
                "clientRating:int4",
                "profileID_id:int8",
                "activeJobsCount:int4",
            ],
        )
    ),
    "accounts_agency": list(
        map(
            col,
            [
                "agencyId:int8",
                "businessName:varchar",
                "businessDesc:varchar",
                "createdAt:timestamptz",
                "accountFK_id:int8",
                "city:varchar",
                "country:varchar",
                "postal_code:varchar",
                "province:varchar",
                "street_address:varchar",
                "contactNumber:varchar",
                "barangay:varchar",
            ],
        )
    ),
    "accounts_barangay": list(
        map(
            col,
            [
                "barangayID:int4",
                "name:varchar",
                "zipCode:varchar",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "city_id:int4",
            ],
        )
    ),
    "accounts_city": list(
        map(
            col,
            [
                "cityID:int4",
                "name:varchar",
                "province:varchar",
                "region:varchar",
                "zipCode:varchar",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
            ],
        )
    ),
    "specializations": list(
        map(
            col,
            [
                "specializationID:int8",
                "specializationName:varchar",
                "averageProjectCostMax:numeric",
                "averageProjectCostMin:numeric",
                "description:text",
                "minimumRate:numeric",
                "rateType:varchar",
                "skillLevel:varchar",
                "is_custom:bool",
                "created_by_agency_id:int8",
                "created_by_worker_id:int8",
            ],
        )
    ),
    "accounts_workerspecialization": list(
        map(
            col,
            [
                "id:int8",
                "experienceYears:int4",
                "certification:varchar",
                "specializationID_id:int8",
                "workerID_id:int8",
                "skillType:varchar",
                "displayOrder:int4",
            ],
        )
    ),
    "accounts_interestedjobs": list(
        map(
            col,
            ["id:int8", "clientID_id:int8", "specializationID_id:int8"],
        )
    ),
    "accounts_wallet": list(
        map(
            col,
            [
                "walletID:int8",
                "balance:numeric",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "accountFK_id:int8",
                "reservedBalance:numeric",
                "pendingEarnings:numeric",
                "autoWithdrawEnabled:bool",
                "preferredPaymentMethodID_id:int8",
                "lastAutoWithdrawAt:timestamptz",
            ],
        )
    ),
    "accounts_userpaymentmethod": list(
        map(
            col,
            [
                "id:int8",
                "methodType:varchar",
                "accountName:varchar",
                "accountNumber:varchar",
                "bankName:varchar",
                "isPrimary:bool",
                "isVerified:bool",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "accountFK_id:int8",
                "bankCode:varchar",
                "paymongoRecipientId:varchar",
            ],
        )
    ),
    "accounts_pushtoken": list(
        map(
            col,
            [
                "tokenID:int8",
                "pushToken:varchar",
                "deviceType:varchar",
                "isActive:bool",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "lastUsed:timestamptz",
                "accountFK_id:int8",
            ],
        )
    ),
    "accounts_notificationsettings": list(
        map(
            col,
            [
                "settingsID:int8",
                "pushEnabled:bool",
                "soundEnabled:bool",
                "jobUpdates:bool",
                "messages:bool",
                "payments:bool",
                "reviews:bool",
                "kycUpdates:bool",
                "doNotDisturbStart:time",
                "doNotDisturbEnd:time",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "accountFK_id:int8",
            ],
        )
    ),
    # Module 3
    "jobs": list(
        map(
            col,
            [
                "jobID:int8",
                "title:varchar",
                "description:text",
                "budget:numeric",
                "location:varchar",
                "expectedDuration:varchar",
                "urgency:varchar",
                "preferredStartDate:date",
                "materialsNeeded:jsonb",
                "status:varchar",
                "completedAt:timestamptz",
                "cancellationReason:text",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "assignedWorkerID_id:int8",
                "categoryID_id:int8",
                "clientID_id:int8",
                "clientMarkedComplete:bool",
                "clientMarkedCompleteAt:timestamptz",
                "workerMarkedComplete:bool",
                "workerMarkedCompleteAt:timestamptz",
                "escrowAmount:numeric",
                "escrowPaid:bool",
                "escrowPaidAt:timestamptz",
                "remainingPayment:numeric",
                "remainingPaymentPaid:bool",
                "remainingPaymentPaidAt:timestamptz",
                "finalPaymentMethod:varchar",
                "cashPaymentProofUrl:varchar",
                "paymentMethodSelectedAt:timestamptz",
                "cashProofUploadedAt:timestamptz",
                "cashPaymentApproved:bool",
                "cashPaymentApprovedAt:timestamptz",
                "cashPaymentApprovedBy_id:int8",
                "assignedAgencyFK_id:int8",
                "jobType:varchar",
                "inviteRejectionReason:text",
                "inviteRespondedAt:timestamptz",
                "inviteStatus:varchar",
                "clientConfirmedWorkStarted:bool",
                "clientConfirmedWorkStartedAt:timestamptz",
                "assignedEmployeeID_id:int8",
                "assignmentNotes:text",
                "employeeAssignedAt:timestamptz",
                "is_team_job:bool",
                "budget_allocation_type:varchar",
                "team_job_start_threshold:numeric",
                "paymentReleaseDate:timestamptz",
                "paymentReleasedToWorker:bool",
                "paymentReleasedAt:timestamptz",
                "paymentHeldReason:varchar",
                "job_scope:varchar",
                "skill_level_required:varchar",
                "work_environment:varchar",
                "payment_model:varchar",
                "duration_days:int4",
                "daily_rate_agreed:numeric",
                "actual_start_date:date",
                "total_days_worked:int4",
                "daily_escrow_total:numeric",
                "materialsCost:numeric",
                "materials_status:varchar",
                "scheduled_end_date:date",
                "qa_day_offset:int4",
                "workerMarkedOnTheWay:bool",
                "workerMarkedOnTheWayAt:timestamptz",
                "workerMarkedJobStarted:bool",
                "workerMarkedJobStartedAt:timestamptz",
                "is_early_completed:bool",
                "early_completed_at:timestamptz",
                "early_completion_payout:numeric",
                "shift_type:varchar",
                "cancelledAt:timestamptz",
                "cancelledByRole:varchar",
                "cancelledByAccountID_id:int8",
                "cancellationStage:varchar",
                "clientRefundAmount:numeric",
                "workerCompensationAmount:numeric",
                "agency_flow_mode:varchar",
            ],
        )
    ),
    "job_skill_slots": list(
        map(
            col,
            [
                "skillSlotID:int8",
                "workers_needed:int4",
                "budget_allocated:numeric",
                "skill_level_required:varchar",
                "status:varchar",
                "notes:text",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "jobID_id:int8",
                "specializationID_id:int8",
                "invited_agency_id:int8",
                "agency_invite_status:varchar",
                "agency_invite_responded_at:timestamptz",
                "last_rejected_agency_id:int8",
                "last_rejected_agency_name:varchar",
                "last_rejected_at:timestamptz",
                "last_rejection_reason:text",
            ],
        )
    ),
    "job_applications": list(
        map(
            col,
            [
                "applicationID:int8",
                "proposalMessage:text",
                "proposedBudget:numeric",
                "estimatedDuration:varchar",
                "budgetOption:varchar",
                "status:varchar",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "jobID_id:int8",
                "workerID_id:int8",
                "applied_skill_slot_id:int8",
                "selected_materials:jsonb",
                "proposed_daily_rate:numeric",
                "proposed_days:int4",
                "negotiation_count:int2",
                "applied_shift:varchar",
                "clientRejectionReason:text",
            ],
        )
    ),
    "price_negotiations": list(
        map(
            col,
            [
                "negotiationID:int8",
                "application_id:int8",
                "actor:varchar",
                "round_number:int2",
                "proposed_budget:numeric",
                "proposed_daily_rate:numeric",
                "proposed_days:int4",
                "message:text",
                "status:varchar",
                "createdAt:timestamptz",
            ],
        )
    ),
    "job_worker_assignments": list(
        map(
            col,
            [
                "assignmentID:int8",
                "slot_position:int4",
                "assignment_status:varchar",
                "worker_marked_complete:bool",
                "worker_marked_complete_at:timestamptz",
                "completion_notes:text",
                "individual_rating:numeric",
                "assignedAt:timestamptz",
                "updatedAt:timestamptz",
                "jobID_id:int8",
                "skillSlotID_id:int8",
                "workerID_id:int8",
                "client_confirmed_arrival:bool",
                "client_confirmed_arrival_at:timestamptz",
                "daily_rate_at_assignment:numeric",
                "days_worked:int4",
                "total_earned:numeric",
                "early_completed:bool",
                "early_completed_at:timestamptz",
                "early_completion_payout:numeric",
                "assigned_shift:varchar",
            ],
        )
    ),
    "job_employee_assignments": list(
        map(
            col,
            [
                "assignmentID:int8",
                "assignedAt:timestamptz",
                "notes:text",
                "isPrimaryContact:bool",
                "status:varchar",
                "employeeMarkedComplete:bool",
                "employeeMarkedCompleteAt:timestamptz",
                "completionNotes:text",
                "assignedBy_id:int8",
                "employee_id:int8",
                "job_id:int8",
                "skill_slot_id:int8",
                "dispatched:bool",
                "dispatchedAt:timestamptz",
                "clientConfirmedArrival:bool",
                "clientConfirmedArrivalAt:timestamptz",
                "agencyMarkedComplete:bool",
                "agencyMarkedCompleteAt:timestamptz",
                "paymentAmount:numeric",
                "clientApproved:bool",
                "clientApprovedAt:timestamptz",
                "early_completed:bool",
                "early_completed_at:timestamptz",
                "early_completion_payout:numeric",
            ],
        )
    ),
    "job_logs": list(
        map(
            col,
            [
                "logID:int8",
                "oldStatus:varchar",
                "newStatus:varchar",
                "notes:text",
                "createdAt:timestamptz",
                "changedBy_id:int8",
                "jobID_id:int8",
                "actionType:varchar",
                "metadata:jsonb",
            ],
        )
    ),
    "saved_jobs": list(
        map(
            col,
            ["savedJobID:int8", "savedAt:timestamptz", "jobID_id:int8", "workerID_id:int8"],
        )
    ),
    # Module 4
    "job_disputes": list(
        map(
            col,
            [
                "disputeID:int8",
                "disputedBy:varchar",
                "reason:varchar",
                "description:text",
                "status:varchar",
                "priority:varchar",
                "jobAmount:numeric",
                "disputedAmount:numeric",
                "resolution:text",
                "resolvedDate:timestamptz",
                "assignedTo:varchar",
                "openedDate:timestamptz",
                "updatedAt:timestamptz",
                "jobID_id:int8",
                "backjobStarted:bool",
                "backjobStartedAt:timestamptz",
                "clientConfirmedBackjob:bool",
                "clientConfirmedBackjobAt:timestamptz",
                "workerMarkedBackjobComplete:bool",
                "workerMarkedBackjobCompleteAt:timestamptz",
                "termsAccepted:bool",
                "termsVersion:varchar",
                "termsAcceptedAt:timestamptz",
                "adminRejectedAt:timestamptz",
                "adminRejectionReason:text",
                "in_negotiation_at:timestamptz",
                "scheduled_date:date",
                "workerScheduleConfirmed:bool",
                "workerScheduleConfirmedAt:timestamptz",
            ],
        )
    ),
    "dispute_evidence": list(
        map(
            col,
            [
                "evidenceID:int8",
                "imageURL:varchar",
                "description:text",
                "createdAt:timestamptz",
                "disputeID_id:int8",
                "uploadedBy_id:int8",
            ],
        )
    ),
    "backjob_schedule_confirmations": list(
        map(
            col,
            [
                "confirmationID:int8",
                "confirmed:bool",
                "confirmedAt:timestamptz",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "assignmentID_id:int8",
                "confirmedBy_id:int8",
                "disputeID_id:int8",
            ],
        )
    ),
    "job_reviews": list(
        map(
            col,
            [
                "reviewID:int8",
                "reviewerType:varchar",
                "rating:numeric",
                "comment:text",
                "status:varchar",
                "isFlagged:bool",
                "flagReason:text",
                "flaggedAt:timestamptz",
                "helpfulCount:int4",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "flaggedBy_id:int8",
                "jobID_id:int8",
                "revieweeID_id:int8",
                "reviewerID_id:int8",
                "revieweeAgencyID_id:int8",
                "revieweeEmployeeID_id:int8",
                "revieweeProfileID_id:int8",
                "rating_communication:numeric",
                "rating_professionalism:numeric",
                "rating_punctuality:numeric",
                "rating_quality:numeric",
                "agency_response:text",
                "agency_response_at:timestamptz",
                "backjob_edit_deadline:timestamptz",
            ],
        )
    ),
    "review_skill_tags": list(
        map(
            col,
            [
                "tagID:int8",
                "createdAt:timestamptz",
                "reviewID_id:int8",
                "workerSpecializationID_id:int8",
            ],
        )
    ),
    "job_materials": list(
        map(
            col,
            [
                "jobMaterialID:int8",
                "name:varchar",
                "description:text",
                "quantity:int4",
                "unit:varchar",
                "source:varchar",
                "purchase_price:numeric",
                "receipt_image_url:varchar",
                "client_approved:bool",
                "client_approved_at:timestamptz",
                "client_rejected:bool",
                "rejection_reason:text",
                "added_by:varchar",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "jobID_id:int8",
                "workerMaterialID_id:int8",
            ],
        )
    ),
    "job_photos": list(
        map(
            col,
            ["photoID:int8", "photoURL:varchar", "fileName:varchar", "uploadedAt:timestamptz", "jobID_id:int8"],
        )
    ),
    "daily_attendance": list(
        map(
            col,
            [
                "attendanceID:int8",
                "date:date",
                "time_in:timestamptz",
                "time_out:timestamptz",
                "status:varchar",
                "worker_confirmed:bool",
                "worker_confirmed_at:timestamptz",
                "client_confirmed:bool",
                "client_confirmed_at:timestamptz",
                "amount_earned:numeric",
                "payment_processed:bool",
                "payment_processed_at:timestamptz",
                "notes:text",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "jobID_id:int8",
                "workerID_id:int8",
                "assignmentID_id:int8",
                "employeeID_id:int8",
                "absent_penalty_amount:numeric",
                "absent_penalty_applied:bool",
                "absent_penalty_applied_at:timestamptz",
                "absent_penalty_percent:numeric",
                "cash_payment_proof_url:varchar",
                "cash_payment_verified:bool",
                "cash_payment_verified_at:timestamptz",
                "cash_proof_uploaded_at:timestamptz",
                "payment_method:varchar",
            ],
        )
    ),
    "daily_job_extensions": list(
        map(
            col,
            [
                "extensionID:int8",
                "additional_days:int4",
                "additional_escrow:numeric",
                "reason:text",
                "status:varchar",
                "requested_by:varchar",
                "client_approved:bool",
                "client_approved_at:timestamptz",
                "worker_approved:bool",
                "worker_approved_at:timestamptz",
                "escrow_collected:bool",
                "escrow_collected_at:timestamptz",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "jobID_id:int8",
                "requestedByUser_id:int8",
            ],
        )
    ),
    "daily_rate_changes": list(
        map(
            col,
            [
                "changeID:int8",
                "old_rate:numeric",
                "new_rate:numeric",
                "reason:text",
                "effective_date:date",
                "status:varchar",
                "requested_by:varchar",
                "client_approved:bool",
                "client_approved_at:timestamptz",
                "worker_approved:bool",
                "worker_approved_at:timestamptz",
                "escrow_adjusted:bool",
                "escrow_adjustment_amount:numeric",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "jobID_id:int8",
                "requestedByUser_id:int8",
            ],
        )
    ),
    "daily_skip_day_requests": list(
        map(
            col,
            [
                "skipRequestID:int8",
                "request_date:date",
                "status:varchar",
                "requested_by:varchar",
                "requested_account_ids:jsonb",
                "requested_count:int4",
                "total_required:int4",
                "requires_all_team_workers:bool",
                "all_workers_requested:bool",
                "reviewedAt:timestamptz",
                "client_rejection_reason:text",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "jobID_id:int8",
                "requestedByUser_id:int8",
                "reviewedByUser_id:int8",
                "target_employee_id:int8",
                "target_type:varchar",
                "target_worker_account_id:int8",
            ],
        )
    ),
    # Module 5
    "accounts_kyc": list(
        map(
            col,
            [
                "kycID:int8",
                "kyc_status:varchar",
                "reviewedAt:timestamptz",
                "notes:text",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "accountFK_id:int8",
                "reviewedBy_id:int8",
                "rejectionCategory:varchar",
                "rejectionReason:text",
                "resubmissionCount:int4",
                "maxResubmissions:int4",
            ],
        )
    ),
    "accounts_kycfiles": list(
        map(
            col,
            [
                "kycFileID:int8",
                "idType:varchar",
                "fileURL:varchar",
                "fileName:varchar",
                "fileSize:int4",
                "uploadedAt:timestamptz",
                "kycID_id:int8",
                "ai_verification_status:varchar",
                "face_detected:bool",
                "face_count:int4",
                "face_confidence:float8",
                "ocr_text:text",
                "ocr_confidence:float8",
                "quality_score:float8",
                "ai_confidence_score:float8",
                "ai_rejection_reason:varchar",
                "ai_rejection_message:varchar",
                "ai_warnings:jsonb",
                "ai_details:jsonb",
                "verified_at:timestamptz",
            ],
        )
    ),
    "kyc_extracted_data": list(
        map(
            col,
            [
                "extractedDataID:int8",
                "extracted_full_name:varchar",
                "extracted_first_name:varchar",
                "extracted_middle_name:varchar",
                "extracted_last_name:varchar",
                "extracted_birth_date:date",
                "extracted_address:text",
                "extracted_id_number:varchar",
                "extracted_id_type:varchar",
                "extracted_expiry_date:date",
                "extracted_nationality:varchar",
                "extracted_sex:varchar",
                "confidence_full_name:float8",
                "confidence_birth_date:float8",
                "confidence_address:float8",
                "confidence_id_number:float8",
                "overall_confidence:float8",
                "confirmed_full_name:varchar",
                "confirmed_first_name:varchar",
                "confirmed_middle_name:varchar",
                "confirmed_last_name:varchar",
                "confirmed_birth_date:date",
                "confirmed_address:text",
                "confirmed_id_number:varchar",
                "extraction_status:varchar",
                "extraction_source:varchar",
                "user_edited_fields:jsonb",
                "confirmed_at:timestamptz",
                "extracted_at:timestamptz",
                "raw_extraction_data:jsonb",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "kycID_id:int8",
                "extracted_place_of_birth:varchar",
                "extracted_clearance_number:varchar",
                "extracted_clearance_type:varchar",
                "extracted_clearance_issue_date:date",
                "extracted_clearance_validity_date:date",
                "confidence_place_of_birth:float8",
                "confidence_clearance_number:float8",
                "confirmed_nationality:varchar",
                "confirmed_sex:varchar",
                "confirmed_place_of_birth:varchar",
                "confirmed_clearance_number:varchar",
                "confirmed_clearance_type:varchar",
                "confirmed_clearance_issue_date:date",
                "confirmed_clearance_validity_date:date",
                "face_match_completed:bool",
                "face_match_score:float8",
            ],
        )
    ),
    "agency_agencykyc": list(
        map(
            col,
            [
                "agencyKycID:int8",
                "status:varchar",
                "reviewedAt:timestamptz",
                "notes:varchar",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "accountFK_id:int8",
                "reviewedBy_id:int8",
                "rejectionCategory:varchar",
                "rejectionReason:text",
                "resubmissionCount:int4",
                "maxResubmissions:int4",
                "face_similarity_score:float8",
            ],
        )
    ),
    "agency_agencykycfile": list(
        map(
            col,
            [
                "fileID:int8",
                "fileType:varchar",
                "fileURL:varchar",
                "fileName:varchar",
                "fileSize:int4",
                "uploadedAt:timestamptz",
                "agencyKyc_id:int8",
                "ai_verification_status:varchar",
                "face_detected:bool",
                "face_count:int4",
                "face_confidence:float8",
                "ocr_text:text",
                "ocr_confidence:float8",
                "quality_score:float8",
                "ai_confidence_score:float8",
                "ai_rejection_reason:varchar",
                "ai_rejection_message:varchar",
                "ai_warnings:jsonb",
                "ai_details:jsonb",
                "verified_at:timestamptz",
            ],
        )
    ),
    "agency_kyc_extracted_data": list(
        map(
            col,
            [
                "extractedDataID:int8",
                "extracted_business_name:varchar",
                "extracted_business_type:varchar",
                "extracted_business_address:text",
                "extracted_permit_number:varchar",
                "extracted_permit_issue_date:date",
                "extracted_permit_expiry_date:date",
                "extracted_dti_number:varchar",
                "extracted_sec_number:varchar",
                "extracted_tin:varchar",
                "extracted_rep_full_name:varchar",
                "extracted_rep_id_number:varchar",
                "extracted_rep_id_type:varchar",
                "extracted_rep_birth_date:date",
                "extracted_rep_address:text",
                "confirmed_business_name:varchar",
                "confirmed_business_type:varchar",
                "confirmed_business_address:text",
                "confirmed_permit_number:varchar",
                "confirmed_permit_issue_date:date",
                "confirmed_permit_expiry_date:date",
                "confirmed_dti_number:varchar",
                "confirmed_sec_number:varchar",
                "confirmed_tin:varchar",
                "confirmed_rep_full_name:varchar",
                "confirmed_rep_id_number:varchar",
                "confirmed_rep_birth_date:date",
                "confirmed_rep_address:text",
                "confidence_business_name:float8",
                "confidence_business_address:float8",
                "confidence_permit_number:float8",
                "confidence_rep_name:float8",
                "overall_confidence:float8",
                "extraction_status:varchar",
                "extraction_source:varchar",
                "extracted_at:timestamptz",
                "confirmed_at:timestamptz",
                "user_edited_fields:jsonb",
                "raw_extraction_data:jsonb",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "agencyKyc_id:int8",
            ],
        )
    ),
    "adminpanel_kyclogs": list(
        map(
            col,
            [
                "kycLogID:int8",
                "action:varchar",
                "reviewedAt:timestamptz",
                "reason:text",
                "userEmail:varchar",
                "userAccountID:int8",
                "createdAt:timestamptz",
                "accountFK_id:int8",
                "kycID:int8",
                "reviewedBy_id:int8",
                "kycType:varchar",
            ],
        )
    ),
    # Module 6
    "adminpanel_adminaccount": list(
        map(
            col,
            [
                "adminID:int8",
                "role:varchar",
                "permissions:jsonb",
                "isActive:bool",
                "lastLogin:timestamptz",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "accountFK_id:int8",
            ],
        )
    ),
    "adminpanel_auditlog": list(
        map(
            col,
            [
                "auditLogID:int8",
                "adminEmail:varchar",
                "action:varchar",
                "entityType:varchar",
                "entityID:varchar",
                "details:jsonb",
                "beforeValue:jsonb",
                "afterValue:jsonb",
                "ipAddress:inet",
                "userAgent:text",
                "createdAt:timestamptz",
                "adminFK_id:int8",
            ],
        )
    ),
    "adminpanel_supportticket": list(
        map(
            col,
            [
                "ticketID:int8",
                "subject:varchar",
                "category:varchar",
                "priority:varchar",
                "status:varchar",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "lastReplyAt:timestamptz",
                "resolvedAt:timestamptz",
                "assignedTo_id:int8",
                "userFK_id:int8",
                "agencyFK_id:int8",
                "ticketType:varchar",
                "platform:varchar",
                "deviceInfo:text",
                "appVersion:varchar",
            ],
        )
    ),
    "adminpanel_supportticketreply": list(
        map(
            col,
            [
                "replyID:int8",
                "content:text",
                "isSystemMessage:bool",
                "attachmentURL:varchar",
                "createdAt:timestamptz",
                "senderFK_id:int8",
                "ticketFK_id:int8",
            ],
        )
    ),
    "adminpanel_userreport": list(
        map(
            col,
            [
                "reportID:int8",
                "reportType:varchar",
                "reason:varchar",
                "description:text",
                "relatedContentID:int8",
                "status:varchar",
                "adminNotes:text",
                "actionTaken:varchar",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "resolvedAt:timestamptz",
                "reportedUserFK_id:int8",
                "reporterFK_id:int8",
                "reviewedBy_id:int8",
            ],
        )
    ),
    "adminpanel_platformsettings": list(
        map(
            col,
            [
                "settingsID:int8",
                "platformFeePercentage:numeric",
                "escrowHoldingDays:int4",
                "maxJobBudget:numeric",
                "minJobBudget:numeric",
                "workerVerificationRequired:bool",
                "autoApproveKYC:bool",
                "kycDocumentExpiryDays:int4",
                "maintenanceMode:bool",
                "sessionTimeoutMinutes:int4",
                "maxUploadSizeMB:int4",
                "lastUpdated:timestamptz",
                "updatedBy_id:int8",
                "kycAutoApproveMinConfidence:numeric",
                "kycFaceMatchMinSimilarity:numeric",
                "kycRequireUserConfirmation:bool",
            ],
        )
    ),
    "adminpanel_cannedresponse": list(
        map(
            col,
            [
                "responseID:int8",
                "title:varchar",
                "content:text",
                "category:varchar",
                "shortcuts:jsonb",
                "usageCount:int4",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "createdBy_id:int8",
            ],
        )
    ),
    "adminpanel_contentmoderationterm": list(
        map(
            col,
            [
                "termID:int8",
                "term:varchar",
                "normalizedTerm:varchar",
                "isActive:bool",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "createdBy_id:int8",
                "updatedBy_id:int8",
            ],
        )
    ),
    "adminpanel_faq": list(
        map(
            col,
            [
                "faqID:int8",
                "question:varchar",
                "answer:text",
                "category:varchar",
                "sortOrder:int4",
                "viewCount:int4",
                "isPublished:bool",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
            ],
        )
    ),
    "adminpanel_systemroles": list(
        map(
            col,
            [
                "systemRoleID:int8",
                "systemRole:varchar",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "accountID_id:int8",
            ],
        )
    ),
    "accounts_notification": list(
        map(
            col,
            [
                "notificationID:int8",
                "notificationType:varchar",
                "title:varchar",
                "message:text",
                "isRead:bool",
                "relatedKYCLogID:int8",
                "createdAt:timestamptz",
                "readAt:timestamptz",
                "accountFK_id:int8",
                "relatedJobID:int8",
                "relatedApplicationID:int8",
                "profile_type:varchar",
            ],
        )
    ),
    "conversation": list(
        map(
            col,
            [
                "conversationID:int8",
                "lastMessageText:text",
                "lastMessageTime:timestamptz",
                "unreadCountClient:int4",
                "unreadCountWorker:int4",
                "status:varchar",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "client_id:int8",
                "lastMessageSender_id:int8",
                "relatedJobPosting_id:int8",
                "worker_id:int8",
                "archivedByClient:bool",
                "archivedByWorker:bool",
                "agency_id:int8",
                "conversation_type:varchar",
            ],
        )
    ),
    "conversation_participants": list(
        map(
            col,
            [
                "participantID:int8",
                "participant_type:varchar",
                "unread_count:int4",
                "is_archived:bool",
                "joined_at:timestamptz",
                "last_read_at:timestamptz",
                "conversation_id:int8",
                "profile_id:int8",
                "skill_slot_id:int8",
                "admin_account_id:int8",
            ],
        )
    ),
    "message": list(
        map(
            col,
            [
                "messageID:int8",
                "messageText:text",
                "messageType:varchar",
                "locationAddress:varchar",
                "locationLandmark:varchar",
                "locationLatitude:numeric",
                "locationLongitude:numeric",
                "isRead:bool",
                "readAt:timestamptz",
                "createdAt:timestamptz",
                "conversationID_id:int8",
                "sender_id:int8",
                "senderAgency_id:int8",
                "sender_admin_id:int8",
            ],
        )
    ),
    "message_attachment": list(
        map(
            col,
            [
                "attachmentID:int8",
                "fileURL:varchar",
                "fileName:varchar",
                "fileSize:int4",
                "fileType:varchar",
                "uploadedAt:timestamptz",
                "messageID_id:int8",
            ],
        )
    ),
    "accounts_transaction": list(
        map(
            col,
            [
                "transactionID:int8",
                "transactionType:varchar",
                "amount:numeric",
                "balanceAfter:numeric",
                "status:varchar",
                "description:varchar",
                "referenceNumber:varchar",
                "paymentMethod:varchar",
                "createdAt:timestamptz",
                "completedAt:timestamptz",
                "relatedJobPosting_id:int8",
                "walletID_id:int8",
                "invoiceURL:varchar",
                "xenditExternalID:varchar",
                "xenditInvoiceID:varchar",
                "xenditPaymentChannel:varchar",
                "xenditPaymentID:varchar",
                "xenditPaymentMethod:varchar",
                "adminReferenceNumber:varchar",
                "processedAt:timestamptz",
                "processedByAdmin_id:int8",
                "paymongoPaymentId:varchar",
                "paymongoTransferId:varchar",
                "paymongoTransferStatus:varchar",
            ],
        )
    ),
    "agency_employees": list(
        map(
            col,
            [
                "employeeID:int8",
                "name:varchar",
                "email:varchar",
                "role:varchar",
                "avatar:varchar",
                "rating:numeric",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "agency_id:int8",
                "employeeOfTheMonth:bool",
                "employeeOfTheMonthDate:timestamptz",
                "employeeOfTheMonthReason:text",
                "isActive:bool",
                "lastRatingUpdate:timestamptz",
                "totalEarnings:numeric",
                "totalJobsCompleted:int4",
                "firstName:varchar",
                "middleName:varchar",
                "lastName:varchar",
                "specializations:text",
                "daily_rate:numeric",
                "hourly_rate:numeric",
                "is_available_daily_jobs:bool",
                "mobile:varchar",
            ],
        )
    ),
    "worker_certifications": list(
        map(
            col,
            [
                "certificationID:int8",
                "name:varchar",
                "issuing_organization:varchar",
                "issue_date:date",
                "expiry_date:date",
                "certificate_url:varchar",
                "is_verified:bool",
                "verified_at:timestamptz",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "verified_by_id:int8",
                "workerID_id:int8",
                "specializationID_id:int8",
            ],
        )
    ),
    "certification_logs": list(
        map(
            col,
            [
                "certLogID:int8",
                "certificationID:int8",
                "action:varchar",
                "reviewedAt:timestamptz",
                "reason:text",
                "workerEmail:varchar",
                "workerAccountID:int8",
                "certificationName:varchar",
                "reviewedBy_id:int8",
                "workerID_id:int8",
            ],
        )
    ),
    "worker_materials": list(
        map(
            col,
            [
                "materialID:int8",
                "name:varchar",
                "description:text",
                "price:numeric",
                "unit:varchar",
                "image_url:varchar",
                "is_available:bool",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "workerID_id:int8",
                "quantity:numeric",
                "categoryID_id:int8",
                "agencyID_id:int8",
            ],
        )
    ),
    "worker_portfolio": list(
        map(
            col,
            [
                "portfolioID:int8",
                "image_url:varchar",
                "caption:text",
                "display_order:int4",
                "file_name:varchar",
                "file_size:int4",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "workerID_id:int8",
            ],
        )
    ),
    "profiles_workerproduct": list(
        map(
            col,
            [
                "productID:int8",
                "productName:varchar",
                "description:text",
                "price:numeric",
                "priceUnit:varchar",
                "inStock:bool",
                "stockQuantity:int4",
                "productImage:varchar",
                "isActive:bool",
                "createdAt:timestamptz",
                "updatedAt:timestamptz",
                "categoryID_id:int8",
                "workerID_id:int8",
            ],
        )
    ),
}


PKS = {name: cols[0].name for name, cols in SCHEMA.items()}

UNIQUE_COLS: Dict[str, set[str]] = {
    "accounts_pushtoken": {"pushToken"},
    "accounts_notificationsettings": {"accountFK_id"},
    "kyc_extracted_data": {"kycID_id"},
    "agency_kyc_extracted_data": {"agencyKyc_id"},
    "adminpanel_adminaccount": {"accountFK_id"},
}


MODULES = [
    {
        "id": 2,
        "title": "MODULE 2 – Profiles, Location, Wallet & Specializations",
        "filename": "erd_v2_module2_profiles.png",
        "columns": 3,
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
        "fks": [
            ("accounts_profile", "accountFK_id", "accounts_accounts"),
            ("accounts_workerprofile", "profileID_id", "accounts_profile"),
            ("accounts_clientprofile", "profileID_id", "accounts_profile"),
            ("accounts_agency", "accountFK_id", "accounts_accounts"),
            ("accounts_barangay", "city_id", "accounts_city"),
            ("accounts_workerspecialization", "workerID_id", "accounts_workerprofile"),
            ("accounts_workerspecialization", "specializationID_id", "specializations"),
            ("accounts_interestedjobs", "clientID_id", "accounts_clientprofile"),
            ("accounts_interestedjobs", "specializationID_id", "specializations"),
            ("accounts_wallet", "accountFK_id", "accounts_accounts"),
            ("accounts_wallet", "preferredPaymentMethodID_id", "accounts_userpaymentmethod"),
            ("accounts_userpaymentmethod", "accountFK_id", "accounts_accounts"),
            ("accounts_pushtoken", "accountFK_id", "accounts_accounts"),
            ("accounts_notificationsettings", "accountFK_id", "accounts_accounts"),
            ("specializations", "created_by_agency_id", "accounts_agency"),
            ("specializations", "created_by_worker_id", "accounts_accounts"),
        ],
    },
    {
        "id": 3,
        "title": "MODULE 3 – Jobs, Applications & Assignments",
        "filename": "erd_v2_module3_jobs.png",
        "columns": 2,
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
        "fks": [
            ("jobs", "clientID_id", "accounts_clientprofile"),
            ("jobs", "assignedWorkerID_id", "accounts_workerprofile"),
            ("jobs", "assignedAgencyFK_id", "accounts_agency"),
            ("jobs", "assignedEmployeeID_id", "agency_employees"),
            ("jobs", "categoryID_id", "specializations"),
            ("jobs", "cancelledByAccountID_id", "accounts_accounts"),
            ("jobs", "cashPaymentApprovedBy_id", "accounts_accounts"),
            ("job_skill_slots", "jobID_id", "jobs"),
            ("job_skill_slots", "specializationID_id", "specializations"),
            ("job_skill_slots", "invited_agency_id", "accounts_agency"),
            ("job_applications", "jobID_id", "jobs"),
            ("job_applications", "workerID_id", "accounts_workerprofile"),
            ("job_applications", "applied_skill_slot_id", "job_skill_slots"),
            ("price_negotiations", "application_id", "job_applications"),
            ("job_worker_assignments", "jobID_id", "jobs"),
            ("job_worker_assignments", "skillSlotID_id", "job_skill_slots"),
            ("job_worker_assignments", "workerID_id", "accounts_workerprofile"),
            ("job_employee_assignments", "job_id", "jobs"),
            ("job_employee_assignments", "employee_id", "agency_employees"),
            ("job_employee_assignments", "skill_slot_id", "job_skill_slots"),
            ("job_employee_assignments", "assignedBy_id", "accounts_accounts"),
            ("job_logs", "jobID_id", "jobs"),
            ("job_logs", "changedBy_id", "accounts_accounts"),
            ("saved_jobs", "jobID_id", "jobs"),
            ("saved_jobs", "workerID_id", "accounts_workerprofile"),
        ],
    },
    {
        "id": 4,
        "title": "MODULE 4 – Disputes, Reviews, Daily Operations & Attendance",
        "filename": "erd_v2_module4_disputes.png",
        "columns": 3,
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
        "fks": [
            ("job_disputes", "jobID_id", "jobs"),
            ("dispute_evidence", "disputeID_id", "job_disputes"),
            ("dispute_evidence", "uploadedBy_id", "accounts_accounts"),
            ("backjob_schedule_confirmations", "disputeID_id", "job_disputes"),
            ("backjob_schedule_confirmations", "assignmentID_id", "job_worker_assignments"),
            ("backjob_schedule_confirmations", "confirmedBy_id", "accounts_accounts"),
            ("job_reviews", "jobID_id", "jobs"),
            ("job_reviews", "reviewerID_id", "accounts_accounts"),
            ("job_reviews", "revieweeID_id", "accounts_accounts"),
            ("job_reviews", "revieweeProfileID_id", "accounts_profile"),
            ("job_reviews", "revieweeAgencyID_id", "accounts_agency"),
            ("job_reviews", "revieweeEmployeeID_id", "agency_employees"),
            ("job_reviews", "flaggedBy_id", "accounts_accounts"),
            ("review_skill_tags", "reviewID_id", "job_reviews"),
            ("review_skill_tags", "workerSpecializationID_id", "accounts_workerspecialization"),
            ("job_materials", "jobID_id", "jobs"),
            ("job_materials", "workerMaterialID_id", "worker_materials"),
            ("job_photos", "jobID_id", "jobs"),
            ("daily_attendance", "jobID_id", "jobs"),
            ("daily_attendance", "workerID_id", "accounts_workerprofile"),
            ("daily_attendance", "assignmentID_id", "job_worker_assignments"),
            ("daily_attendance", "employeeID_id", "agency_employees"),
            ("daily_job_extensions", "jobID_id", "jobs"),
            ("daily_job_extensions", "requestedByUser_id", "accounts_accounts"),
            ("daily_rate_changes", "jobID_id", "jobs"),
            ("daily_rate_changes", "requestedByUser_id", "accounts_accounts"),
            ("daily_skip_day_requests", "jobID_id", "jobs"),
            ("daily_skip_day_requests", "requestedByUser_id", "accounts_accounts"),
            ("daily_skip_day_requests", "reviewedByUser_id", "accounts_accounts"),
            ("daily_skip_day_requests", "target_employee_id", "agency_employees"),
            ("daily_skip_day_requests", "target_worker_account_id", "accounts_accounts"),
        ],
    },
    {
        "id": 5,
        "title": "MODULE 5 – KYC Verification (Individual & Agency)",
        "filename": "erd_v2_module5_kyc.png",
        "columns": 2,
        "tables": [
            "accounts_kyc",
            "accounts_kycfiles",
            "kyc_extracted_data",
            "agency_agencykyc",
            "agency_agencykycfile",
            "agency_kyc_extracted_data",
            "adminpanel_kyclogs",
        ],
        "fks": [
            ("accounts_kyc", "accountFK_id", "accounts_accounts"),
            ("accounts_kyc", "reviewedBy_id", "accounts_accounts"),
            ("accounts_kycfiles", "kycID_id", "accounts_kyc"),
            ("kyc_extracted_data", "kycID_id", "accounts_kyc"),
            ("agency_agencykyc", "accountFK_id", "accounts_accounts"),
            ("agency_agencykyc", "reviewedBy_id", "accounts_accounts"),
            ("agency_agencykycfile", "agencyKyc_id", "agency_agencykyc"),
            ("agency_kyc_extracted_data", "agencyKyc_id", "agency_agencykyc"),
            ("adminpanel_kyclogs", "accountFK_id", "accounts_accounts"),
            ("adminpanel_kyclogs", "reviewedBy_id", "accounts_accounts"),
        ],
    },
    {
        "id": 6,
        "title": "MODULE 6 – Admin Panel, Messaging, Notifications & Worker Assets",
        "filename": "erd_v2_module6_admin.png",
        "columns": 4,
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
        "fks": [
            ("adminpanel_adminaccount", "accountFK_id", "accounts_accounts"),
            ("adminpanel_auditlog", "adminFK_id", "accounts_accounts"),
            ("adminpanel_supportticket", "userFK_id", "accounts_accounts"),
            ("adminpanel_supportticket", "assignedTo_id", "accounts_accounts"),
            ("adminpanel_supportticket", "agencyFK_id", "accounts_agency"),
            ("adminpanel_supportticketreply", "ticketFK_id", "adminpanel_supportticket"),
            ("adminpanel_supportticketreply", "senderFK_id", "accounts_accounts"),
            ("adminpanel_userreport", "reporterFK_id", "accounts_accounts"),
            ("adminpanel_userreport", "reportedUserFK_id", "accounts_accounts"),
            ("adminpanel_userreport", "reviewedBy_id", "accounts_accounts"),
            ("adminpanel_platformsettings", "updatedBy_id", "accounts_accounts"),
            ("adminpanel_cannedresponse", "createdBy_id", "accounts_accounts"),
            ("adminpanel_contentmoderationterm", "createdBy_id", "accounts_accounts"),
            ("adminpanel_contentmoderationterm", "updatedBy_id", "accounts_accounts"),
            ("adminpanel_systemroles", "accountID_id", "accounts_accounts"),
            ("accounts_notification", "accountFK_id", "accounts_accounts"),
            ("conversation", "client_id", "accounts_profile"),
            ("conversation", "worker_id", "accounts_profile"),
            ("conversation", "agency_id", "accounts_agency"),
            ("conversation", "relatedJobPosting_id", "jobs"),
            ("conversation", "lastMessageSender_id", "accounts_profile"),
            ("conversation_participants", "conversation_id", "conversation"),
            ("conversation_participants", "profile_id", "accounts_profile"),
            ("conversation_participants", "skill_slot_id", "job_skill_slots"),
            ("conversation_participants", "admin_account_id", "accounts_accounts"),
            ("message", "conversationID_id", "conversation"),
            ("message", "sender_id", "accounts_profile"),
            ("message", "senderAgency_id", "accounts_agency"),
            ("message", "sender_admin_id", "accounts_accounts"),
            ("message_attachment", "messageID_id", "message"),
            ("accounts_transaction", "walletID_id", "accounts_wallet"),
            ("accounts_transaction", "relatedJobPosting_id", "jobs"),
            ("accounts_transaction", "processedByAdmin_id", "accounts_accounts"),
            ("agency_employees", "agency_id", "accounts_accounts"),
            ("worker_certifications", "workerID_id", "accounts_workerprofile"),
            ("worker_certifications", "specializationID_id", "accounts_workerspecialization"),
            ("worker_certifications", "verified_by_id", "accounts_accounts"),
            ("certification_logs", "workerID_id", "accounts_workerprofile"),
            ("certification_logs", "reviewedBy_id", "accounts_accounts"),
            ("worker_materials", "workerID_id", "accounts_workerprofile"),
            ("worker_materials", "agencyID_id", "accounts_agency"),
            ("worker_materials", "categoryID_id", "specializations"),
            ("worker_portfolio", "workerID_id", "accounts_workerprofile"),
            ("profiles_workerproduct", "workerID_id", "accounts_workerprofile"),
            ("profiles_workerproduct", "categoryID_id", "specializations"),
        ],
    },
]


def load_font(size: int, bold: bool = False, italic: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    base = "/usr/share/fonts/truetype/dejavu/"
    name = "DejaVuSans.ttf"
    if bold and italic:
        name = "DejaVuSans-BoldOblique.ttf"
    elif bold:
        name = "DejaVuSans-Bold.ttf"
    elif italic:
        name = "DejaVuSans-Oblique.ttf"
    try:
        return ImageFont.truetype(base + name, size=size)
    except OSError:
        return ImageFont.load_default()


FONT_TITLE = load_font(26, bold=True)
FONT_SUB = load_font(13)
FONT_HEADER = load_font(14, bold=True)
FONT_ROW = load_font(11)
FONT_ROW_BOLD = load_font(11, bold=True)
FONT_ROW_ITALIC = load_font(11, italic=True)
FONT_TAG = load_font(10, bold=True)


def table_height(table: TableDef) -> int:
    return HEADER_H + (len(table.columns) * ROW_H) + 2


def build_table_defs(module: dict) -> Tuple[Dict[str, TableDef], Dict[str, TableDef]]:
    main: Dict[str, TableDef] = {}
    for t in module["tables"]:
        main[t] = TableDef(
            name=t,
            columns=SCHEMA[t],
            pk=PKS[t],
            unique_cols=UNIQUE_COLS.get(t, set()),
            external=False,
        )

    external_targets = sorted({dst for _, _, dst in module["fks"] if dst not in main})
    external: Dict[str, TableDef] = {}
    for t in external_targets:
        if t in SCHEMA:
            pk = PKS[t]
        else:
            # Fallback for external references not in current module schema map.
            pk = {
                "accounts_accounts": "accountID",
                "accounts_profile": "profileID",
                "accounts_workerprofile": "id",
                "accounts_clientprofile": "id",
                "accounts_agency": "agencyId",
                "accounts_wallet": "walletID",
                "accounts_workerspecialization": "id",
                "jobs": "jobID",
                "job_skill_slots": "skillSlotID",
                "job_worker_assignments": "assignmentID",
                "job_disputes": "disputeID",
                "job_reviews": "reviewID",
                "worker_materials": "materialID",
                "specializations": "specializationID",
                "agency_employees": "employeeID",
                "adminpanel_supportticket": "ticketID",
                "conversation": "conversationID",
                "message": "messageID",
                "accounts_kyc": "kycID",
                "agency_agencykyc": "agencyKycID",
                "job_applications": "applicationID",
            }.get(t, "id")
        external[t] = TableDef(
            name=t,
            columns=[Column(pk, "PK reference")],
            pk=pk,
            unique_cols=set(),
            external=True,
        )
    return main, external


def layout(module: dict, main: Dict[str, TableDef], external: Dict[str, TableDef]):
    n_cols = module["columns"]
    main_cols_heights = [TITLE_SPACE + MARGIN_Y] * n_cols
    positions: Dict[str, Tuple[int, int]] = {}

    # Place largest tables first for better balancing.
    ordered = sorted(main.values(), key=table_height, reverse=True)
    for table in ordered:
        idx = min(range(n_cols), key=lambda i: main_cols_heights[i])
        x = MARGIN_X + idx * (TABLE_W + COL_GAP)
        y = main_cols_heights[idx]
        positions[table.name] = (x, y)
        main_cols_heights[idx] += table_height(table) + ROW_GAP

    ext_x = MARGIN_X + n_cols * (TABLE_W + COL_GAP) + 34
    ext_y = TITLE_SPACE + MARGIN_Y
    for t in sorted(external.values(), key=lambda td: td.name):
        positions[t.name] = (ext_x, ext_y)
        ext_y += table_height(t) + 18

    width = ext_x + EXT_TABLE_W + MARGIN_X
    height = max(max(main_cols_heights), ext_y) + MARGIN_Y
    return positions, width, height


def draw_pk_tag(draw: ImageDraw.ImageDraw, x: int, y_center: int):
    # Gold key icon + PK label.
    r = 4
    draw.ellipse((x, y_center - r, x + 2 * r, y_center + r), outline=PK_TEXT, width=1)
    draw.line((x + 2 * r, y_center, x + 16, y_center), fill=PK_TEXT, width=1)
    draw.line((x + 12, y_center, x + 12, y_center - 3), fill=PK_TEXT, width=1)
    draw.line((x + 15, y_center, x + 15, y_center - 2), fill=PK_TEXT, width=1)
    draw.text((x + 20, y_center - 6), "PK", fill=PK_TEXT, font=FONT_TAG)


def draw_crowfoot(draw: ImageDraw.ImageDraw, x: int, y: int, direction: str):
    d = 10
    s = 6
    if direction == "right":
        draw.line((x, y, x + d, y), fill=LINE, width=2)
        draw.line((x, y, x + d, y - s), fill=LINE, width=2)
        draw.line((x, y, x + d, y + s), fill=LINE, width=2)
    elif direction == "left":
        draw.line((x, y, x - d, y), fill=LINE, width=2)
        draw.line((x, y, x - d, y - s), fill=LINE, width=2)
        draw.line((x, y, x - d, y + s), fill=LINE, width=2)
    elif direction == "down":
        draw.line((x, y, x, y + d), fill=LINE, width=2)
        draw.line((x, y, x - s, y + d), fill=LINE, width=2)
        draw.line((x, y, x + s, y + d), fill=LINE, width=2)
    else:  # up
        draw.line((x, y, x, y - d), fill=LINE, width=2)
        draw.line((x, y, x - s, y - d), fill=LINE, width=2)
        draw.line((x, y, x + s, y - d), fill=LINE, width=2)


def draw_one_bar(draw: ImageDraw.ImageDraw, x: int, y: int, direction: str):
    if direction in ("left", "right"):
        draw.line((x, y - 6, x, y + 6), fill=LINE, width=2)
    else:
        draw.line((x - 6, y, x + 6, y), fill=LINE, width=2)


def render_module(module: dict, out_path: Path):
    main, external = build_table_defs(module)
    positions, width, height = layout(module, main, external)
    image = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(image)

    # Title and note
    draw.text((MARGIN_X, MARGIN_Y - 6), module["title"], fill=TEXT, font=FONT_TITLE)
    note = f"Table count: {len(module['tables'])}"
    note_bbox = draw.textbbox((0, 0), note, font=FONT_SUB)
    note_w = note_bbox[2] - note_bbox[0]
    draw.text((width - MARGIN_X - note_w, MARGIN_Y + 4), note, fill=(90, 96, 106), font=FONT_SUB)

    all_tables = {**main, **external}
    anchors: Dict[Tuple[str, str], Dict[str, Tuple[int, int]]] = {}

    # Precompute anchors for FK drawing.
    for table_name, table in all_tables.items():
        x, y = positions[table_name]
        w = EXT_TABLE_W if table.external else TABLE_W
        for idx, c in enumerate(table.columns):
            cy = y + HEADER_H + idx * ROW_H + (ROW_H // 2)
            anchors[(table_name, c.name)] = {
                "left": (x, cy),
                "right": (x + w, cy),
            }
        # PK fallback anchor.
        pk_idx = next((i for i, c in enumerate(table.columns) if c.name == table.pk), 0)
        cy = y + HEADER_H + pk_idx * ROW_H + (ROW_H // 2)
        anchors[(table_name, "__pk__")] = {"left": (x, cy), "right": (x + w, cy)}

    # Relationship lines behind tables.
    for src, field, dst in module["fks"]:
        if (src, field) not in anchors:
            raise ValueError(f"FK field {src}.{field} not found in schema.")
        if dst not in all_tables:
            raise ValueError(f"FK target table {dst} missing from diagram.")

        src_pos = positions[src]
        dst_pos = positions[dst]

        src_side = "right" if dst_pos[0] > src_pos[0] else "left"
        dst_side = "left" if src_side == "right" else "right"
        start = anchors[(src, field)][src_side]
        end = anchors[(dst, "__pk__")][dst_side]

        # orthogonal path
        if src_side == "right":
            p0 = (start[0] + 2, start[1])
            p3 = (end[0] - 2, end[1])
            crow_dir = "right"
            bar_dir = "left"
        else:
            p0 = (start[0] - 2, start[1])
            p3 = (end[0] + 2, end[1])
            crow_dir = "left"
            bar_dir = "right"

        mid_x = (p0[0] + p3[0]) // 2
        p1 = (mid_x, p0[1])
        p2 = (mid_x, p3[1])
        draw.line((p0, p1, p2, p3), fill=LINE, width=2)
        draw_crowfoot(draw, p0[0], p0[1], crow_dir)
        draw_one_bar(draw, p3[0], p3[1], bar_dir)

    # Draw tables over lines.
    fk_targets = {(s, f): d for s, f, d in module["fks"]}
    for table_name, table in all_tables.items():
        x, y = positions[table_name]
        w = EXT_TABLE_W if table.external else TABLE_W
        h = table_height(table)
        draw.rectangle((x, y, x + w, y + h), outline=BORDER, width=2, fill=(255, 255, 255))
        draw.rectangle((x, y, x + w, y + HEADER_H), fill=HEADER_BG)
        draw.text((x + 8, y + 6), table_name, fill=HEADER_TEXT, font=FONT_HEADER)

        for idx, c in enumerate(table.columns):
            ry = y + HEADER_H + idx * ROW_H
            fill = ROW_LIGHT if idx % 2 == 0 else ROW_DARK
            draw.rectangle((x + 1, ry, x + w - 1, ry + ROW_H), fill=fill)

            is_pk = c.name == table.pk
            is_fk = (table_name, c.name) in fk_targets
            is_unique = c.name in table.unique_cols

            suffix = ""
            if is_unique:
                suffix += " UNIQUE"
            if is_fk:
                suffix += f" \u2192 {fk_targets[(table_name, c.name)]}"

            text_str = f"{c.name} | {c.dtype}{suffix}"
            tx = x + 8
            ty = ry + 4

            if is_pk:
                draw_pk_tag(draw, tx, ry + (ROW_H // 2))
                tx += 48
                draw.text((tx, ty), text_str, fill=TEXT, font=FONT_ROW_BOLD)
            elif is_fk:
                draw.text((tx, ty), text_str, fill=FK_TEXT, font=FONT_ROW_ITALIC)
            else:
                draw.text((tx, ty), text_str, fill=TEXT, font=FONT_ROW)

    image.save(out_path)
    print(f"Generated {out_path}")


def validate():
    for module in MODULES:
        for table in module["tables"]:
            if table not in SCHEMA:
                raise ValueError(f"Missing schema definition for table {table}")
        for src, field, dst in module["fks"]:
            if src not in SCHEMA:
                raise ValueError(f"FK source table missing schema: {src}")
            if field not in [c.name for c in SCHEMA[src]]:
                raise ValueError(f"FK field missing: {src}.{field}")
            if dst not in SCHEMA:
                # Allow truly external targets if needed, but most are defined.
                pass


def main():
    validate()
    root = Path(".")
    for module in MODULES:
        render_module(module, root / module["filename"])


if __name__ == "__main__":
    main()
