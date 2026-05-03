from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SCHEMA_SQL = r"""
CREATE TABLE "accounts_agency" (
  "agencyId" int8 NOT NULL,
  "businessName" varchar NOT NULL,
  "businessDesc" varchar NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "accountFK_id" int8 NOT NULL,
  "city" varchar NOT NULL,
  "country" varchar NOT NULL,
  "postal_code" varchar NOT NULL,
  "province" varchar NOT NULL,
  "street_address" varchar NOT NULL,
  "contactNumber" varchar NOT NULL,
  "barangay" varchar NOT NULL
);

CREATE TABLE "accounts_barangay" (
  "barangayID" int4 NOT NULL,
  "name" varchar NOT NULL,
  "zipCode" varchar,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "city_id" int4 NOT NULL
);

CREATE TABLE "accounts_city" (
  "cityID" int4 NOT NULL,
  "name" varchar NOT NULL,
  "province" varchar NOT NULL,
  "region" varchar NOT NULL,
  "zipCode" varchar,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL
);

CREATE TABLE "accounts_clientprofile" (
  "id" int8 NOT NULL,
  "description" varchar NOT NULL,
  "totalJobsPosted" int4 NOT NULL,
  "clientRating" int4 NOT NULL,
  "profileID_id" int8 NOT NULL,
  "activeJobsCount" int4 NOT NULL
);

CREATE TABLE "accounts_interestedjobs" (
  "id" int8 NOT NULL,
  "clientID_id" int8 NOT NULL,
  "specializationID_id" int8 NOT NULL
);

CREATE TABLE "accounts_kyc" (
  "kycID" int8 NOT NULL,
  "kyc_status" varchar NOT NULL,
  "reviewedAt" timestamptz NOT NULL,
  "notes" text NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "accountFK_id" int8 NOT NULL,
  "reviewedBy_id" int8,
  "rejectionCategory" varchar,
  "rejectionReason" text NOT NULL,
  "resubmissionCount" int4 NOT NULL,
  "maxResubmissions" int4 NOT NULL
);

CREATE TABLE "accounts_kycfiles" (
  "kycFileID" int8 NOT NULL,
  "idType" varchar,
  "fileURL" varchar NOT NULL,
  "fileName" varchar,
  "fileSize" int4,
  "uploadedAt" timestamptz NOT NULL,
  "kycID_id" int8 NOT NULL,
  "ai_verification_status" varchar NOT NULL,
  "face_detected" bool,
  "face_count" int4,
  "face_confidence" float8,
  "ocr_text" text,
  "ocr_confidence" float8,
  "quality_score" float8,
  "ai_confidence_score" float8,
  "ai_rejection_reason" varchar,
  "ai_rejection_message" varchar,
  "ai_warnings" jsonb,
  "ai_details" jsonb,
  "verified_at" timestamptz
);

CREATE TABLE "accounts_notification" (
  "notificationID" int8 NOT NULL,
  "notificationType" varchar NOT NULL,
  "title" varchar NOT NULL,
  "message" text NOT NULL,
  "isRead" bool NOT NULL,
  "relatedKYCLogID" int8,
  "createdAt" timestamptz NOT NULL,
  "readAt" timestamptz,
  "accountFK_id" int8 NOT NULL,
  "relatedJobID" int8,
  "relatedApplicationID" int8,
  "profile_type" varchar
);

CREATE TABLE "accounts_notificationsettings" (
  "settingsID" int8 NOT NULL,
  "pushEnabled" bool NOT NULL,
  "soundEnabled" bool NOT NULL,
  "jobUpdates" bool NOT NULL,
  "messages" bool NOT NULL,
  "payments" bool NOT NULL,
  "reviews" bool NOT NULL,
  "kycUpdates" bool NOT NULL,
  "doNotDisturbStart" time,
  "doNotDisturbEnd" time,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "accountFK_id" int8 NOT NULL
);

CREATE TABLE "accounts_profile" (
  "profileID" int8 NOT NULL,
  "profileImg" varchar,
  "firstName" varchar NOT NULL,
  "lastName" varchar NOT NULL,
  "contactNum" varchar,
  "birthDate" date,
  "profileType" varchar,
  "accountFK_id" int8 NOT NULL,
  "middleName" varchar,
  "latitude" numeric,
  "location_sharing_enabled" bool NOT NULL,
  "location_updated_at" timestamptz,
  "longitude" numeric
);

CREATE TABLE "accounts_pushtoken" (
  "tokenID" int8 NOT NULL,
  "pushToken" varchar NOT NULL,
  "deviceType" varchar NOT NULL,
  "isActive" bool NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "lastUsed" timestamptz NOT NULL,
  "accountFK_id" int8 NOT NULL
);

CREATE TABLE "specializations" (
  "specializationID" int8 NOT NULL,
  "specializationName" varchar NOT NULL,
  "averageProjectCostMax" numeric NOT NULL,
  "averageProjectCostMin" numeric NOT NULL,
  "description" text,
  "minimumRate" numeric NOT NULL,
  "rateType" varchar NOT NULL,
  "skillLevel" varchar NOT NULL,
  "is_custom" bool NOT NULL,
  "created_by_agency_id" int8,
  "created_by_worker_id" int8
);

CREATE TABLE "accounts_transaction" (
  "transactionID" int8 NOT NULL,
  "transactionType" varchar NOT NULL,
  "amount" numeric NOT NULL,
  "balanceAfter" numeric NOT NULL,
  "status" varchar NOT NULL,
  "description" varchar,
  "referenceNumber" varchar,
  "paymentMethod" varchar,
  "createdAt" timestamptz NOT NULL,
  "completedAt" timestamptz,
  "relatedJobPosting_id" int8,
  "walletID_id" int8 NOT NULL,
  "invoiceURL" varchar,
  "xenditExternalID" varchar,
  "xenditInvoiceID" varchar,
  "xenditPaymentChannel" varchar,
  "xenditPaymentID" varchar,
  "xenditPaymentMethod" varchar,
  "adminReferenceNumber" varchar,
  "processedAt" timestamptz,
  "processedByAdmin_id" int8,
  "paymongoPaymentId" varchar,
  "paymongoTransferId" varchar,
  "paymongoTransferStatus" varchar
);

CREATE TABLE "accounts_userpaymentmethod" (
  "id" int8 NOT NULL,
  "methodType" varchar NOT NULL,
  "accountName" varchar NOT NULL,
  "accountNumber" varchar NOT NULL,
  "bankName" varchar,
  "isPrimary" bool NOT NULL,
  "isVerified" bool NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "accountFK_id" int8 NOT NULL,
  "bankCode" varchar,
  "paymongoRecipientId" varchar
);

CREATE TABLE "accounts_wallet" (
  "walletID" int8 NOT NULL,
  "balance" numeric NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "accountFK_id" int8 NOT NULL,
  "reservedBalance" numeric NOT NULL,
  "pendingEarnings" numeric NOT NULL,
  "autoWithdrawEnabled" bool NOT NULL,
  "preferredPaymentMethodID_id" int8,
  "lastAutoWithdrawAt" timestamptz
);

CREATE TABLE "accounts_workerprofile" (
  "id" int8 NOT NULL,
  "description" varchar NOT NULL,
  "workerRating" int4 NOT NULL,
  "totalEarningGross" numeric NOT NULL,
  "availability_status" varchar NOT NULL,
  "profileID_id" int8 NOT NULL,
  "bio" varchar NOT NULL,
  "hourly_rate" numeric,
  "profile_completion_percentage" int4 NOT NULL,
  "soft_skills" text NOT NULL,
  "daily_rate" numeric,
  "is_available_daily_jobs" bool NOT NULL
);

CREATE TABLE "accounts_workerspecialization" (
  "id" int8 NOT NULL,
  "experienceYears" int4 NOT NULL,
  "certification" varchar NOT NULL,
  "specializationID_id" int8 NOT NULL,
  "workerID_id" int8 NOT NULL,
  "skillType" varchar NOT NULL,
  "displayOrder" int4 NOT NULL
);

CREATE TABLE "adminpanel_adminaccount" (
  "adminID" int8 NOT NULL,
  "role" varchar NOT NULL,
  "permissions" jsonb NOT NULL,
  "isActive" bool NOT NULL,
  "lastLogin" timestamptz,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "accountFK_id" int8 NOT NULL
);

CREATE TABLE "adminpanel_auditlog" (
  "auditLogID" int8 NOT NULL,
  "adminEmail" varchar NOT NULL,
  "action" varchar NOT NULL,
  "entityType" varchar NOT NULL,
  "entityID" varchar NOT NULL,
  "details" jsonb NOT NULL,
  "beforeValue" jsonb,
  "afterValue" jsonb,
  "ipAddress" inet,
  "userAgent" text NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "adminFK_id" int8
);

CREATE TABLE "adminpanel_cannedresponse" (
  "responseID" int8 NOT NULL,
  "title" varchar NOT NULL,
  "content" text NOT NULL,
  "category" varchar NOT NULL,
  "shortcuts" jsonb NOT NULL,
  "usageCount" int4 NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "createdBy_id" int8
);

CREATE TABLE "adminpanel_contentmoderationterm" (
  "termID" int8 NOT NULL,
  "term" varchar NOT NULL,
  "normalizedTerm" varchar NOT NULL,
  "isActive" bool NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "createdBy_id" int8,
  "updatedBy_id" int8
);

CREATE TABLE "adminpanel_faq" (
  "faqID" int8 NOT NULL,
  "question" varchar NOT NULL,
  "answer" text NOT NULL,
  "category" varchar NOT NULL,
  "sortOrder" int4 NOT NULL,
  "viewCount" int4 NOT NULL,
  "isPublished" bool NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL
);

CREATE TABLE "adminpanel_kyclogs" (
  "kycLogID" int8 NOT NULL,
  "action" varchar NOT NULL,
  "reviewedAt" timestamptz NOT NULL,
  "reason" text NOT NULL,
  "userEmail" varchar NOT NULL,
  "userAccountID" int8 NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "accountFK_id" int8 NOT NULL,
  "kycID" int8 NOT NULL,
  "reviewedBy_id" int8,
  "kycType" varchar NOT NULL
);

CREATE TABLE "adminpanel_platformsettings" (
  "settingsID" int8 NOT NULL,
  "platformFeePercentage" numeric NOT NULL,
  "escrowHoldingDays" int4 NOT NULL,
  "maxJobBudget" numeric NOT NULL,
  "minJobBudget" numeric NOT NULL,
  "workerVerificationRequired" bool NOT NULL,
  "autoApproveKYC" bool NOT NULL,
  "kycDocumentExpiryDays" int4 NOT NULL,
  "maintenanceMode" bool NOT NULL,
  "sessionTimeoutMinutes" int4 NOT NULL,
  "maxUploadSizeMB" int4 NOT NULL,
  "lastUpdated" timestamptz NOT NULL,
  "updatedBy_id" int8,
  "kycAutoApproveMinConfidence" numeric NOT NULL,
  "kycFaceMatchMinSimilarity" numeric NOT NULL,
  "kycRequireUserConfirmation" bool NOT NULL
);

CREATE TABLE "adminpanel_supportticket" (
  "ticketID" int8 NOT NULL,
  "subject" varchar NOT NULL,
  "category" varchar NOT NULL,
  "priority" varchar NOT NULL,
  "status" varchar NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "lastReplyAt" timestamptz,
  "resolvedAt" timestamptz,
  "assignedTo_id" int8,
  "userFK_id" int8 NOT NULL,
  "agencyFK_id" int8,
  "ticketType" varchar NOT NULL,
  "platform" varchar NOT NULL,
  "deviceInfo" text,
  "appVersion" varchar
);

CREATE TABLE "adminpanel_supportticketreply" (
  "replyID" int8 NOT NULL,
  "content" text NOT NULL,
  "isSystemMessage" bool NOT NULL,
  "attachmentURL" varchar,
  "createdAt" timestamptz NOT NULL,
  "senderFK_id" int8 NOT NULL,
  "ticketFK_id" int8 NOT NULL
);

CREATE TABLE "adminpanel_systemroles" (
  "systemRoleID" int8 NOT NULL,
  "systemRole" varchar NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "accountID_id" int8 NOT NULL
);

CREATE TABLE "adminpanel_userreport" (
  "reportID" int8 NOT NULL,
  "reportType" varchar NOT NULL,
  "reason" varchar NOT NULL,
  "description" text NOT NULL,
  "relatedContentID" int8,
  "status" varchar NOT NULL,
  "adminNotes" text NOT NULL,
  "actionTaken" varchar NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "resolvedAt" timestamptz,
  "reportedUserFK_id" int8,
  "reporterFK_id" int8 NOT NULL,
  "reviewedBy_id" int8
);

CREATE TABLE "agency_agencykyc" (
  "agencyKycID" int8 NOT NULL,
  "status" varchar NOT NULL,
  "reviewedAt" timestamptz,
  "notes" varchar NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "accountFK_id" int8 NOT NULL,
  "reviewedBy_id" int8,
  "rejectionCategory" varchar,
  "rejectionReason" text NOT NULL,
  "resubmissionCount" int4 NOT NULL,
  "maxResubmissions" int4 NOT NULL,
  "face_similarity_score" float8
);

CREATE TABLE "agency_agencykycfile" (
  "fileID" int8 NOT NULL,
  "fileType" varchar,
  "fileURL" varchar NOT NULL,
  "fileName" varchar,
  "fileSize" int4,
  "uploadedAt" timestamptz NOT NULL,
  "agencyKyc_id" int8 NOT NULL,
  "ai_verification_status" varchar NOT NULL,
  "face_detected" bool,
  "face_count" int4,
  "face_confidence" float8,
  "ocr_text" text,
  "ocr_confidence" float8,
  "quality_score" float8,
  "ai_confidence_score" float8,
  "ai_rejection_reason" varchar,
  "ai_rejection_message" varchar,
  "ai_warnings" jsonb,
  "ai_details" jsonb,
  "verified_at" timestamptz
);

CREATE TABLE "agency_employees" (
  "employeeID" int8 NOT NULL,
  "name" varchar NOT NULL,
  "email" varchar NOT NULL,
  "role" varchar NOT NULL,
  "avatar" varchar,
  "rating" numeric,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "agency_id" int8 NOT NULL,
  "employeeOfTheMonth" bool NOT NULL,
  "employeeOfTheMonthDate" timestamptz,
  "employeeOfTheMonthReason" text NOT NULL,
  "isActive" bool NOT NULL,
  "lastRatingUpdate" timestamptz,
  "totalEarnings" numeric NOT NULL,
  "totalJobsCompleted" int4 NOT NULL,
  "firstName" varchar NOT NULL,
  "middleName" varchar NOT NULL,
  "lastName" varchar NOT NULL,
  "specializations" text NOT NULL,
  "daily_rate" numeric,
  "hourly_rate" numeric,
  "is_available_daily_jobs" bool NOT NULL,
  "mobile" varchar NOT NULL
);

CREATE TABLE "agency_kyc_extracted_data" (
  "extractedDataID" int8 NOT NULL,
  "extracted_business_name" varchar NOT NULL,
  "extracted_business_type" varchar NOT NULL,
  "extracted_business_address" text NOT NULL,
  "extracted_permit_number" varchar NOT NULL,
  "extracted_permit_issue_date" date,
  "extracted_permit_expiry_date" date,
  "extracted_dti_number" varchar NOT NULL,
  "extracted_sec_number" varchar NOT NULL,
  "extracted_tin" varchar NOT NULL,
  "extracted_rep_full_name" varchar NOT NULL,
  "extracted_rep_id_number" varchar NOT NULL,
  "extracted_rep_id_type" varchar NOT NULL,
  "extracted_rep_birth_date" date,
  "extracted_rep_address" text NOT NULL,
  "confirmed_business_name" varchar NOT NULL,
  "confirmed_business_type" varchar NOT NULL,
  "confirmed_business_address" text NOT NULL,
  "confirmed_permit_number" varchar NOT NULL,
  "confirmed_permit_issue_date" date,
  "confirmed_permit_expiry_date" date,
  "confirmed_dti_number" varchar NOT NULL,
  "confirmed_sec_number" varchar NOT NULL,
  "confirmed_tin" varchar NOT NULL,
  "confirmed_rep_full_name" varchar NOT NULL,
  "confirmed_rep_id_number" varchar NOT NULL,
  "confirmed_rep_birth_date" date,
  "confirmed_rep_address" text NOT NULL,
  "confidence_business_name" float8 NOT NULL,
  "confidence_business_address" float8 NOT NULL,
  "confidence_permit_number" float8 NOT NULL,
  "confidence_rep_name" float8 NOT NULL,
  "overall_confidence" float8 NOT NULL,
  "extraction_status" varchar NOT NULL,
  "extraction_source" varchar NOT NULL,
  "extracted_at" timestamptz,
  "confirmed_at" timestamptz,
  "user_edited_fields" jsonb NOT NULL,
  "raw_extraction_data" jsonb NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "agencyKyc_id" int8 NOT NULL
);

CREATE TABLE "backjob_schedule_confirmations" (
  "confirmationID" int8 NOT NULL,
  "confirmed" bool NOT NULL,
  "confirmedAt" timestamptz NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "assignmentID_id" int8 NOT NULL,
  "confirmedBy_id" int8,
  "disputeID_id" int8 NOT NULL
);

CREATE TABLE "certification_logs" (
  "certLogID" int8 NOT NULL,
  "certificationID" int8 NOT NULL,
  "action" varchar NOT NULL,
  "reviewedAt" timestamptz NOT NULL,
  "reason" text NOT NULL,
  "workerEmail" varchar NOT NULL,
  "workerAccountID" int8 NOT NULL,
  "certificationName" varchar NOT NULL,
  "reviewedBy_id" int8,
  "workerID_id" int8 NOT NULL
);

CREATE TABLE "conversation" (
  "conversationID" int8 NOT NULL,
  "lastMessageText" text,
  "lastMessageTime" timestamptz,
  "unreadCountClient" int4 NOT NULL,
  "unreadCountWorker" int4 NOT NULL,
  "status" varchar NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "client_id" int8 NOT NULL,
  "lastMessageSender_id" int8,
  "relatedJobPosting_id" int8 NOT NULL,
  "worker_id" int8,
  "archivedByClient" bool NOT NULL,
  "archivedByWorker" bool NOT NULL,
  "agency_id" int8,
  "conversation_type" varchar NOT NULL
);

CREATE TABLE "conversation_participants" (
  "participantID" int8 NOT NULL,
  "participant_type" varchar NOT NULL,
  "unread_count" int4 NOT NULL,
  "is_archived" bool NOT NULL,
  "joined_at" timestamptz NOT NULL,
  "last_read_at" timestamptz,
  "conversation_id" int8 NOT NULL,
  "profile_id" int8,
  "skill_slot_id" int8,
  "admin_account_id" int8
);

CREATE TABLE "daily_attendance" (
  "attendanceID" int8 NOT NULL,
  "date" date NOT NULL,
  "time_in" timestamptz,
  "time_out" timestamptz,
  "status" varchar NOT NULL,
  "worker_confirmed" bool NOT NULL,
  "worker_confirmed_at" timestamptz,
  "client_confirmed" bool NOT NULL,
  "client_confirmed_at" timestamptz,
  "amount_earned" numeric NOT NULL,
  "payment_processed" bool NOT NULL,
  "payment_processed_at" timestamptz,
  "notes" text NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "jobID_id" int8 NOT NULL,
  "workerID_id" int8,
  "assignmentID_id" int8,
  "employeeID_id" int8,
  "absent_penalty_amount" numeric NOT NULL,
  "absent_penalty_applied" bool NOT NULL,
  "absent_penalty_applied_at" timestamptz,
  "absent_penalty_percent" numeric NOT NULL,
  "cash_payment_proof_url" varchar,
  "cash_payment_verified" bool NOT NULL,
  "cash_payment_verified_at" timestamptz,
  "cash_proof_uploaded_at" timestamptz,
  "payment_method" varchar NOT NULL
);

CREATE TABLE "daily_job_extensions" (
  "extensionID" int8 NOT NULL,
  "additional_days" int4 NOT NULL,
  "additional_escrow" numeric NOT NULL,
  "reason" text NOT NULL,
  "status" varchar NOT NULL,
  "requested_by" varchar NOT NULL,
  "client_approved" bool NOT NULL,
  "client_approved_at" timestamptz,
  "worker_approved" bool NOT NULL,
  "worker_approved_at" timestamptz,
  "escrow_collected" bool NOT NULL,
  "escrow_collected_at" timestamptz,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "jobID_id" int8 NOT NULL,
  "requestedByUser_id" int8
);

CREATE TABLE "daily_rate_changes" (
  "changeID" int8 NOT NULL,
  "old_rate" numeric NOT NULL,
  "new_rate" numeric NOT NULL,
  "reason" text NOT NULL,
  "effective_date" date NOT NULL,
  "status" varchar NOT NULL,
  "requested_by" varchar NOT NULL,
  "client_approved" bool NOT NULL,
  "client_approved_at" timestamptz,
  "worker_approved" bool NOT NULL,
  "worker_approved_at" timestamptz,
  "escrow_adjusted" bool NOT NULL,
  "escrow_adjustment_amount" numeric NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "jobID_id" int8 NOT NULL,
  "requestedByUser_id" int8
);

CREATE TABLE "daily_skip_day_requests" (
  "skipRequestID" int8 NOT NULL,
  "request_date" date NOT NULL,
  "status" varchar NOT NULL,
  "requested_by" varchar NOT NULL,
  "requested_account_ids" jsonb NOT NULL,
  "requested_count" int4 NOT NULL,
  "total_required" int4 NOT NULL,
  "requires_all_team_workers" bool NOT NULL,
  "all_workers_requested" bool NOT NULL,
  "reviewedAt" timestamptz,
  "client_rejection_reason" text,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "jobID_id" int8 NOT NULL,
  "requestedByUser_id" int8,
  "reviewedByUser_id" int8,
  "target_employee_id" int8,
  "target_type" varchar NOT NULL,
  "target_worker_account_id" int8
);

CREATE TABLE "dispute_evidence" (
  "evidenceID" int8 NOT NULL,
  "imageURL" varchar NOT NULL,
  "description" text,
  "createdAt" timestamptz NOT NULL,
  "disputeID_id" int8 NOT NULL,
  "uploadedBy_id" int8
);

CREATE TABLE "job_applications" (
  "applicationID" int8 NOT NULL,
  "proposalMessage" text NOT NULL,
  "proposedBudget" numeric NOT NULL,
  "estimatedDuration" varchar,
  "budgetOption" varchar NOT NULL,
  "status" varchar NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "jobID_id" int8 NOT NULL,
  "workerID_id" int8 NOT NULL,
  "applied_skill_slot_id" int8,
  "selected_materials" jsonb NOT NULL,
  "proposed_daily_rate" numeric,
  "proposed_days" int4,
  "negotiation_count" int2 NOT NULL,
  "applied_shift" varchar,
  "clientRejectionReason" text
);

CREATE TABLE "job_disputes" (
  "disputeID" int8 NOT NULL,
  "disputedBy" varchar NOT NULL,
  "reason" varchar NOT NULL,
  "description" text NOT NULL,
  "status" varchar NOT NULL,
  "priority" varchar NOT NULL,
  "jobAmount" numeric NOT NULL,
  "disputedAmount" numeric NOT NULL,
  "resolution" text,
  "resolvedDate" timestamptz,
  "assignedTo" varchar,
  "openedDate" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "jobID_id" int8 NOT NULL,
  "backjobStarted" bool NOT NULL,
  "backjobStartedAt" timestamptz,
  "clientConfirmedBackjob" bool NOT NULL,
  "clientConfirmedBackjobAt" timestamptz,
  "workerMarkedBackjobComplete" bool NOT NULL,
  "workerMarkedBackjobCompleteAt" timestamptz,
  "termsAccepted" bool NOT NULL,
  "termsVersion" varchar,
  "termsAcceptedAt" timestamptz,
  "adminRejectedAt" timestamptz,
  "adminRejectionReason" text,
  "in_negotiation_at" timestamptz,
  "scheduled_date" date,
  "workerScheduleConfirmed" bool NOT NULL,
  "workerScheduleConfirmedAt" timestamptz
);

CREATE TABLE "job_employee_assignments" (
  "assignmentID" int8 NOT NULL,
  "assignedAt" timestamptz NOT NULL,
  "notes" text NOT NULL,
  "isPrimaryContact" bool NOT NULL,
  "status" varchar NOT NULL,
  "employeeMarkedComplete" bool NOT NULL,
  "employeeMarkedCompleteAt" timestamptz,
  "completionNotes" text NOT NULL,
  "assignedBy_id" int8,
  "employee_id" int8 NOT NULL,
  "job_id" int8 NOT NULL,
  "skill_slot_id" int8,
  "dispatched" bool NOT NULL,
  "dispatchedAt" timestamptz,
  "clientConfirmedArrival" bool NOT NULL,
  "clientConfirmedArrivalAt" timestamptz,
  "agencyMarkedComplete" bool NOT NULL,
  "agencyMarkedCompleteAt" timestamptz,
  "paymentAmount" numeric,
  "clientApproved" bool NOT NULL,
  "clientApprovedAt" timestamptz,
  "early_completed" bool NOT NULL,
  "early_completed_at" timestamptz,
  "early_completion_payout" numeric
);

CREATE TABLE "job_logs" (
  "logID" int8 NOT NULL,
  "oldStatus" varchar,
  "newStatus" varchar,
  "notes" text,
  "createdAt" timestamptz NOT NULL,
  "changedBy_id" int8,
  "jobID_id" int8 NOT NULL,
  "actionType" varchar NOT NULL,
  "metadata" jsonb
);

CREATE TABLE "job_materials" (
  "jobMaterialID" int8 NOT NULL,
  "name" varchar NOT NULL,
  "description" text,
  "quantity" int4 NOT NULL,
  "unit" varchar,
  "source" varchar NOT NULL,
  "purchase_price" numeric,
  "receipt_image_url" varchar,
  "client_approved" bool NOT NULL,
  "client_approved_at" timestamptz,
  "client_rejected" bool NOT NULL,
  "rejection_reason" text,
  "added_by" varchar NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "jobID_id" int8 NOT NULL,
  "workerMaterialID_id" int8
);

CREATE TABLE "job_photos" (
  "photoID" int8 NOT NULL,
  "photoURL" varchar NOT NULL,
  "fileName" varchar,
  "uploadedAt" timestamptz NOT NULL,
  "jobID_id" int8 NOT NULL
);

CREATE TABLE "job_reviews" (
  "reviewID" int8 NOT NULL,
  "reviewerType" varchar NOT NULL,
  "rating" numeric NOT NULL,
  "comment" text NOT NULL,
  "status" varchar NOT NULL,
  "isFlagged" bool NOT NULL,
  "flagReason" text,
  "flaggedAt" timestamptz,
  "helpfulCount" int4 NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "flaggedBy_id" int8,
  "jobID_id" int8 NOT NULL,
  "revieweeID_id" int8,
  "reviewerID_id" int8 NOT NULL,
  "revieweeAgencyID_id" int8,
  "revieweeEmployeeID_id" int8,
  "revieweeProfileID_id" int8,
  "rating_communication" numeric,
  "rating_professionalism" numeric,
  "rating_punctuality" numeric,
  "rating_quality" numeric,
  "agency_response" text,
  "agency_response_at" timestamptz,
  "backjob_edit_deadline" timestamptz
);

CREATE TABLE "job_skill_slots" (
  "skillSlotID" int8 NOT NULL,
  "workers_needed" int4 NOT NULL,
  "budget_allocated" numeric NOT NULL,
  "skill_level_required" varchar NOT NULL,
  "status" varchar NOT NULL,
  "notes" text,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "jobID_id" int8 NOT NULL,
  "specializationID_id" int8 NOT NULL,
  "invited_agency_id" int8,
  "agency_invite_status" varchar,
  "agency_invite_responded_at" timestamptz,
  "last_rejected_agency_id" int8,
  "last_rejected_agency_name" varchar,
  "last_rejected_at" timestamptz,
  "last_rejection_reason" text
);

CREATE TABLE "job_worker_assignments" (
  "assignmentID" int8 NOT NULL,
  "slot_position" int4 NOT NULL,
  "assignment_status" varchar NOT NULL,
  "worker_marked_complete" bool NOT NULL,
  "worker_marked_complete_at" timestamptz,
  "completion_notes" text,
  "individual_rating" numeric,
  "assignedAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "jobID_id" int8 NOT NULL,
  "skillSlotID_id" int8 NOT NULL,
  "workerID_id" int8 NOT NULL,
  "client_confirmed_arrival" bool NOT NULL,
  "client_confirmed_arrival_at" timestamptz,
  "daily_rate_at_assignment" numeric,
  "days_worked" int4 NOT NULL,
  "total_earned" numeric NOT NULL,
  "early_completed" bool NOT NULL,
  "early_completed_at" timestamptz,
  "early_completion_payout" numeric,
  "assigned_shift" varchar
);

CREATE TABLE "jobs" (
  "jobID" int8 NOT NULL,
  "title" varchar NOT NULL,
  "description" text NOT NULL,
  "budget" numeric NOT NULL,
  "location" varchar NOT NULL,
  "expectedDuration" varchar,
  "urgency" varchar NOT NULL,
  "preferredStartDate" date,
  "materialsNeeded" jsonb NOT NULL,
  "status" varchar NOT NULL,
  "completedAt" timestamptz,
  "cancellationReason" text,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "assignedWorkerID_id" int8,
  "categoryID_id" int8,
  "clientID_id" int8 NOT NULL,
  "clientMarkedComplete" bool NOT NULL,
  "clientMarkedCompleteAt" timestamptz,
  "workerMarkedComplete" bool NOT NULL,
  "workerMarkedCompleteAt" timestamptz,
  "escrowAmount" numeric NOT NULL,
  "escrowPaid" bool NOT NULL,
  "escrowPaidAt" timestamptz,
  "remainingPayment" numeric NOT NULL,
  "remainingPaymentPaid" bool NOT NULL,
  "remainingPaymentPaidAt" timestamptz,
  "finalPaymentMethod" varchar,
  "cashPaymentProofUrl" varchar,
  "paymentMethodSelectedAt" timestamptz,
  "cashProofUploadedAt" timestamptz,
  "cashPaymentApproved" bool NOT NULL,
  "cashPaymentApprovedAt" timestamptz,
  "cashPaymentApprovedBy_id" int8,
  "assignedAgencyFK_id" int8,
  "jobType" varchar NOT NULL,
  "inviteRejectionReason" text,
  "inviteRespondedAt" timestamptz,
  "inviteStatus" varchar,
  "clientConfirmedWorkStarted" bool NOT NULL,
  "clientConfirmedWorkStartedAt" timestamptz,
  "assignedEmployeeID_id" int8,
  "assignmentNotes" text,
  "employeeAssignedAt" timestamptz,
  "is_team_job" bool NOT NULL,
  "budget_allocation_type" varchar NOT NULL,
  "team_job_start_threshold" numeric NOT NULL,
  "paymentReleaseDate" timestamptz,
  "paymentReleasedToWorker" bool NOT NULL,
  "paymentReleasedAt" timestamptz,
  "paymentHeldReason" varchar,
  "job_scope" varchar NOT NULL,
  "skill_level_required" varchar NOT NULL,
  "work_environment" varchar NOT NULL,
  "payment_model" varchar NOT NULL,
  "duration_days" int4,
  "daily_rate_agreed" numeric,
  "actual_start_date" date,
  "total_days_worked" int4 NOT NULL,
  "daily_escrow_total" numeric NOT NULL,
  "materialsCost" numeric NOT NULL,
  "materials_status" varchar NOT NULL,
  "scheduled_end_date" date,
  "qa_day_offset" int4 NOT NULL,
  "workerMarkedOnTheWay" bool NOT NULL,
  "workerMarkedOnTheWayAt" timestamptz,
  "workerMarkedJobStarted" bool NOT NULL,
  "workerMarkedJobStartedAt" timestamptz,
  "is_early_completed" bool NOT NULL,
  "early_completed_at" timestamptz,
  "early_completion_payout" numeric,
  "shift_type" varchar NOT NULL,
  "cancelledAt" timestamptz,
  "cancelledByRole" varchar,
  "cancelledByAccountID_id" int8,
  "cancellationStage" varchar,
  "clientRefundAmount" numeric,
  "workerCompensationAmount" numeric,
  "agency_flow_mode" varchar
);

CREATE TABLE "kyc_extracted_data" (
  "extractedDataID" int8 NOT NULL,
  "extracted_full_name" varchar NOT NULL,
  "extracted_first_name" varchar NOT NULL,
  "extracted_middle_name" varchar NOT NULL,
  "extracted_last_name" varchar NOT NULL,
  "extracted_birth_date" date,
  "extracted_address" text NOT NULL,
  "extracted_id_number" varchar NOT NULL,
  "extracted_id_type" varchar NOT NULL,
  "extracted_expiry_date" date,
  "extracted_nationality" varchar NOT NULL,
  "extracted_sex" varchar NOT NULL,
  "confidence_full_name" float8,
  "confidence_birth_date" float8,
  "confidence_address" float8,
  "confidence_id_number" float8,
  "overall_confidence" float8,
  "confirmed_full_name" varchar NOT NULL,
  "confirmed_first_name" varchar NOT NULL,
  "confirmed_middle_name" varchar NOT NULL,
  "confirmed_last_name" varchar NOT NULL,
  "confirmed_birth_date" date,
  "confirmed_address" text NOT NULL,
  "confirmed_id_number" varchar NOT NULL,
  "extraction_status" varchar NOT NULL,
  "extraction_source" varchar NOT NULL,
  "user_edited_fields" jsonb NOT NULL,
  "confirmed_at" timestamptz,
  "extracted_at" timestamptz,
  "raw_extraction_data" jsonb NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "kycID_id" int8 NOT NULL,
  "extracted_place_of_birth" varchar NOT NULL,
  "extracted_clearance_number" varchar NOT NULL,
  "extracted_clearance_type" varchar NOT NULL,
  "extracted_clearance_issue_date" date,
  "extracted_clearance_validity_date" date,
  "confidence_place_of_birth" float8,
  "confidence_clearance_number" float8,
  "confirmed_nationality" varchar NOT NULL,
  "confirmed_sex" varchar NOT NULL,
  "confirmed_place_of_birth" varchar NOT NULL,
  "confirmed_clearance_number" varchar NOT NULL,
  "confirmed_clearance_type" varchar NOT NULL,
  "confirmed_clearance_issue_date" date,
  "confirmed_clearance_validity_date" date,
  "face_match_completed" bool NOT NULL,
  "face_match_score" float8
);

CREATE TABLE "message" (
  "messageID" int8 NOT NULL,
  "messageText" text NOT NULL,
  "messageType" varchar NOT NULL,
  "locationAddress" varchar,
  "locationLandmark" varchar,
  "locationLatitude" numeric,
  "locationLongitude" numeric,
  "isRead" bool NOT NULL,
  "readAt" timestamptz,
  "createdAt" timestamptz NOT NULL,
  "conversationID_id" int8 NOT NULL,
  "sender_id" int8,
  "senderAgency_id" int8,
  "sender_admin_id" int8
);

CREATE TABLE "message_attachment" (
  "attachmentID" int8 NOT NULL,
  "fileURL" varchar NOT NULL,
  "fileName" varchar,
  "fileSize" int4,
  "fileType" varchar,
  "uploadedAt" timestamptz NOT NULL,
  "messageID_id" int8 NOT NULL
);

CREATE TABLE "price_negotiations" (
  "negotiationID" int8 NOT NULL,
  "application_id" int8 NOT NULL,
  "actor" varchar NOT NULL,
  "round_number" int2 NOT NULL,
  "proposed_budget" numeric NOT NULL,
  "proposed_daily_rate" numeric,
  "proposed_days" int4,
  "message" text NOT NULL,
  "status" varchar NOT NULL,
  "createdAt" timestamptz NOT NULL
);

CREATE TABLE "profiles_workerproduct" (
  "productID" int8 NOT NULL,
  "productName" varchar NOT NULL,
  "description" text,
  "price" numeric NOT NULL,
  "priceUnit" varchar NOT NULL,
  "inStock" bool NOT NULL,
  "stockQuantity" int4,
  "productImage" varchar,
  "isActive" bool NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "categoryID_id" int8,
  "workerID_id" int8 NOT NULL
);

CREATE TABLE "review_skill_tags" (
  "tagID" int8 NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "reviewID_id" int8 NOT NULL,
  "workerSpecializationID_id" int8 NOT NULL
);

CREATE TABLE "saved_jobs" (
  "savedJobID" int8 NOT NULL,
  "savedAt" timestamptz NOT NULL,
  "jobID_id" int8 NOT NULL,
  "workerID_id" int8 NOT NULL
);

CREATE TABLE "worker_certifications" (
  "certificationID" int8 NOT NULL,
  "name" varchar NOT NULL,
  "issuing_organization" varchar NOT NULL,
  "issue_date" date,
  "expiry_date" date,
  "certificate_url" varchar NOT NULL,
  "is_verified" bool NOT NULL,
  "verified_at" timestamptz,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "verified_by_id" int8,
  "workerID_id" int8 NOT NULL,
  "specializationID_id" int8 NOT NULL
);

CREATE TABLE "worker_materials" (
  "materialID" int8 NOT NULL,
  "name" varchar NOT NULL,
  "description" text NOT NULL,
  "price" numeric NOT NULL,
  "unit" varchar NOT NULL,
  "image_url" varchar NOT NULL,
  "is_available" bool NOT NULL,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "workerID_id" int8,
  "quantity" numeric NOT NULL,
  "categoryID_id" int8,
  "agencyID_id" int8
);

CREATE TABLE "worker_portfolio" (
  "portfolioID" int8 NOT NULL,
  "image_url" varchar NOT NULL,
  "caption" text NOT NULL,
  "display_order" int4 NOT NULL,
  "file_name" varchar NOT NULL,
  "file_size" int4,
  "createdAt" timestamptz NOT NULL,
  "updatedAt" timestamptz NOT NULL,
  "workerID_id" int8 NOT NULL
);
"""


@dataclass
class FieldDef:
    name: str
    dtype: str
    not_null: bool
    pk: bool = False
    fk_target: str | None = None
    unique: bool = False


@dataclass
class TableDef:
    name: str
    fields: list[FieldDef]
    external_ref: bool = False


@dataclass
class ModuleDef:
    number: int
    title: str
    filename: str
    tables: list[str]
    refs: list[str]
    columns: list[list[str]]


@dataclass
class TableBox:
    table: TableDef
    x: int
    y: int
    w: int
    h: int
    field_centers: dict[str, tuple[int, int]] = field(default_factory=dict)
    pk_center: tuple[int, int] | None = None


BG = "#FFFFFF"
HEADER = "#16324F"
REF_HEADER = "#4A5568"
HEADER_TEXT = "#FFFFFF"
BORDER = "#B8C2CC"
GRID = "#D9E1E8"
ROW_A = "#FFFFFF"
ROW_B = "#F7F9FB"
TEXT = "#1B2430"
MUTED = "#667788"
FK_BLUE = "#1D5FA7"
PK_GOLD = "#D4A017"
LINE = "#6B7C93"
SEPARATOR = "#E4EAF0"
UNIQUE_BADGE = "#7A869A"

TITLE_FONT_SIZE = 28
NOTE_FONT_SIZE = 14
HEADER_FONT_SIZE = 16
ROW_FONT_SIZE = 12
SMALL_FONT_SIZE = 11
ROW_H = 22
HEADER_H = 30
TABLE_W = 640
REF_W = 360
FIELD_SPLIT = 370
COL_GAP = 42
ROW_GAP = 26
MARGIN_X = 36
TOP_PAD = 110
BOTTOM_PAD = 40


def load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    candidates = {
        "regular": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/dejavu/DejaVuSans.ttf",
        ],
        "bold": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
        ],
        "italic": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
            "/usr/share/fonts/dejavu/DejaVuSans-Oblique.ttf",
        ],
        "bold_italic": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf",
            "/usr/share/fonts/dejavu/DejaVuSans-BoldOblique.ttf",
        ],
    }[name]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


FONTS = {
    "title": load_font("bold", TITLE_FONT_SIZE),
    "note": load_font("regular", NOTE_FONT_SIZE),
    "header": load_font("bold", HEADER_FONT_SIZE),
    "row": load_font("regular", ROW_FONT_SIZE),
    "row_bold": load_font("bold", ROW_FONT_SIZE),
    "row_italic": load_font("italic", ROW_FONT_SIZE),
    "small": load_font("regular", SMALL_FONT_SIZE),
    "small_bold": load_font("bold", SMALL_FONT_SIZE),
}


UNIQUE_FIELDS = {
    "accounts_city": {"name"},
    "accounts_clientprofile": {"profileID_id"},
    "accounts_notificationsettings": {"accountFK_id"},
    "accounts_pushtoken": {"pushToken"},
    "accounts_wallet": {"accountFK_id"},
    "accounts_workerprofile": {"profileID_id"},
    "adminpanel_adminaccount": {"accountFK_id"},
    "agency_kyc_extracted_data": {"agencyKyc_id"},
    "conversation": {"relatedJobPosting_id"},
    "kyc_extracted_data": {"kycID_id"},
}


FK_MAP = {
    "accounts_profile": {
        "accountFK_id": "accounts_accounts",
    },
    "accounts_workerprofile": {
        "profileID_id": "accounts_profile",
    },
    "accounts_clientprofile": {
        "profileID_id": "accounts_profile",
    },
    "accounts_agency": {
        "accountFK_id": "accounts_accounts",
    },
    "accounts_barangay": {
        "city_id": "accounts_city",
    },
    "specializations": {
        "created_by_agency_id": "accounts_agency",
        "created_by_worker_id": "accounts_accounts",
    },
    "accounts_interestedjobs": {
        "clientID_id": "accounts_clientprofile",
        "specializationID_id": "specializations",
    },
    "accounts_userpaymentmethod": {
        "accountFK_id": "accounts_accounts",
    },
    "accounts_wallet": {
        "accountFK_id": "accounts_accounts",
        "preferredPaymentMethodID_id": "accounts_userpaymentmethod",
    },
    "accounts_workerspecialization": {
        "specializationID_id": "specializations",
        "workerID_id": "accounts_workerprofile",
    },
    "accounts_pushtoken": {
        "accountFK_id": "accounts_accounts",
    },
    "accounts_notificationsettings": {
        "accountFK_id": "accounts_accounts",
    },
    "jobs": {
        "assignedWorkerID_id": "accounts_workerprofile",
        "categoryID_id": "specializations",
        "clientID_id": "accounts_clientprofile",
        "cashPaymentApprovedBy_id": "accounts_accounts",
        "assignedAgencyFK_id": "accounts_agency",
        "assignedEmployeeID_id": "agency_employees",
        "cancelledByAccountID_id": "accounts_accounts",
    },
    "job_skill_slots": {
        "jobID_id": "jobs",
        "specializationID_id": "specializations",
        "invited_agency_id": "accounts_agency",
    },
    "job_applications": {
        "jobID_id": "jobs",
        "workerID_id": "accounts_workerprofile",
        "applied_skill_slot_id": "job_skill_slots",
    },
    "price_negotiations": {
        "application_id": "job_applications",
    },
    "job_worker_assignments": {
        "jobID_id": "jobs",
        "skillSlotID_id": "job_skill_slots",
        "workerID_id": "accounts_workerprofile",
    },
    "job_employee_assignments": {
        "assignedBy_id": "accounts_accounts",
        "employee_id": "agency_employees",
        "job_id": "jobs",
        "skill_slot_id": "job_skill_slots",
    },
    "job_logs": {
        "changedBy_id": "accounts_accounts",
        "jobID_id": "jobs",
    },
    "saved_jobs": {
        "jobID_id": "jobs",
        "workerID_id": "accounts_workerprofile",
    },
    "job_disputes": {
        "jobID_id": "jobs",
    },
    "dispute_evidence": {
        "disputeID_id": "job_disputes",
        "uploadedBy_id": "accounts_accounts",
    },
    "backjob_schedule_confirmations": {
        "assignmentID_id": "job_worker_assignments",
        "confirmedBy_id": "accounts_accounts",
        "disputeID_id": "job_disputes",
    },
    "job_reviews": {
        "flaggedBy_id": "accounts_accounts",
        "jobID_id": "jobs",
        "revieweeID_id": "accounts_accounts",
        "reviewerID_id": "accounts_accounts",
        "revieweeAgencyID_id": "accounts_agency",
        "revieweeEmployeeID_id": "agency_employees",
        "revieweeProfileID_id": "accounts_profile",
    },
    "review_skill_tags": {
        "reviewID_id": "job_reviews",
        "workerSpecializationID_id": "accounts_workerspecialization",
    },
    "job_materials": {
        "jobID_id": "jobs",
        "workerMaterialID_id": "worker_materials",
    },
    "job_photos": {
        "jobID_id": "jobs",
    },
    "daily_attendance": {
        "jobID_id": "jobs",
        "workerID_id": "accounts_workerprofile",
        "assignmentID_id": "job_worker_assignments",
        "employeeID_id": "agency_employees",
    },
    "daily_job_extensions": {
        "jobID_id": "jobs",
        "requestedByUser_id": "accounts_accounts",
    },
    "daily_rate_changes": {
        "jobID_id": "jobs",
        "requestedByUser_id": "accounts_accounts",
    },
    "daily_skip_day_requests": {
        "jobID_id": "jobs",
        "requestedByUser_id": "accounts_accounts",
        "reviewedByUser_id": "accounts_accounts",
        "target_employee_id": "agency_employees",
        "target_worker_account_id": "accounts_accounts",
    },
    "accounts_kyc": {
        "accountFK_id": "accounts_accounts",
        "reviewedBy_id": "accounts_accounts",
    },
    "accounts_kycfiles": {
        "kycID_id": "accounts_kyc",
    },
    "kyc_extracted_data": {
        "kycID_id": "accounts_kyc",
    },
    "agency_agencykyc": {
        "accountFK_id": "accounts_accounts",
        "reviewedBy_id": "accounts_accounts",
    },
    "agency_agencykycfile": {
        "agencyKyc_id": "agency_agencykyc",
    },
    "agency_kyc_extracted_data": {
        "agencyKyc_id": "agency_agencykyc",
    },
    "adminpanel_kyclogs": {
        "accountFK_id": "accounts_accounts",
        "reviewedBy_id": "accounts_accounts",
    },
    "adminpanel_adminaccount": {
        "accountFK_id": "accounts_accounts",
    },
    "adminpanel_auditlog": {
        "adminFK_id": "accounts_accounts",
    },
    "adminpanel_supportticket": {
        "assignedTo_id": "accounts_accounts",
        "userFK_id": "accounts_accounts",
        "agencyFK_id": "accounts_agency",
    },
    "adminpanel_supportticketreply": {
        "senderFK_id": "accounts_accounts",
        "ticketFK_id": "adminpanel_supportticket",
    },
    "adminpanel_userreport": {
        "reportedUserFK_id": "accounts_accounts",
        "reporterFK_id": "accounts_accounts",
        "reviewedBy_id": "accounts_accounts",
    },
    "adminpanel_platformsettings": {
        "updatedBy_id": "accounts_accounts",
    },
    "adminpanel_cannedresponse": {
        "createdBy_id": "accounts_accounts",
    },
    "adminpanel_contentmoderationterm": {
        "createdBy_id": "accounts_accounts",
        "updatedBy_id": "accounts_accounts",
    },
    "adminpanel_systemroles": {
        "accountID_id": "accounts_accounts",
    },
    "accounts_notification": {
        "accountFK_id": "accounts_accounts",
    },
    "conversation": {
        "client_id": "accounts_profile",
        "lastMessageSender_id": "accounts_profile",
        "relatedJobPosting_id": "jobs",
        "worker_id": "accounts_profile",
        "agency_id": "accounts_agency",
    },
    "conversation_participants": {
        "conversation_id": "conversation",
        "profile_id": "accounts_profile",
        "skill_slot_id": "job_skill_slots",
        "admin_account_id": "accounts_accounts",
    },
    "message": {
        "conversationID_id": "conversation",
        "sender_id": "accounts_profile",
        "senderAgency_id": "accounts_agency",
        "sender_admin_id": "accounts_accounts",
    },
    "message_attachment": {
        "messageID_id": "message",
    },
    "accounts_transaction": {
        "relatedJobPosting_id": "jobs",
        "walletID_id": "accounts_wallet",
        "processedByAdmin_id": "accounts_accounts",
    },
    "agency_employees": {
        "agency_id": "accounts_accounts",
    },
    "worker_certifications": {
        "verified_by_id": "accounts_accounts",
        "workerID_id": "accounts_workerprofile",
        "specializationID_id": "accounts_workerspecialization",
    },
    "certification_logs": {
        "reviewedBy_id": "accounts_accounts",
        "workerID_id": "accounts_workerprofile",
    },
    "worker_materials": {
        "workerID_id": "accounts_workerprofile",
        "categoryID_id": "specializations",
        "agencyID_id": "accounts_agency",
    },
    "worker_portfolio": {
        "workerID_id": "accounts_workerprofile",
    },
    "profiles_workerproduct": {
        "categoryID_id": "specializations",
        "workerID_id": "accounts_workerprofile",
    },
}


MODULES = [
    ModuleDef(
        number=2,
        title="MODULE 2 - Profiles, Location, Wallet & Specializations",
        filename="erd_v2_module2_profiles.png",
        tables=[
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
        refs=["accounts_accounts"],
        columns=[
            ["accounts_profile", "accounts_workerprofile", "accounts_clientprofile", "accounts_pushtoken", "accounts_notificationsettings"],
            ["accounts_agency", "specializations", "accounts_workerspecialization", "accounts_interestedjobs"],
            ["accounts_city", "accounts_barangay", "accounts_userpaymentmethod", "accounts_wallet"],
            ["accounts_accounts"],
        ],
    ),
    ModuleDef(
        number=3,
        title="MODULE 3 - Jobs, Applications & Assignments",
        filename="erd_v2_module3_jobs.png",
        tables=[
            "jobs",
            "job_skill_slots",
            "job_applications",
            "price_negotiations",
            "job_worker_assignments",
            "job_employee_assignments",
            "job_logs",
            "saved_jobs",
        ],
        refs=[
            "accounts_clientprofile",
            "accounts_workerprofile",
            "accounts_agency",
            "agency_employees",
            "specializations",
            "accounts_accounts",
        ],
        columns=[
            ["jobs"],
            ["job_skill_slots", "job_applications", "price_negotiations", "saved_jobs"],
            ["job_worker_assignments", "job_employee_assignments", "job_logs"],
            ["accounts_clientprofile", "accounts_workerprofile", "accounts_agency", "agency_employees", "specializations", "accounts_accounts"],
        ],
    ),
    ModuleDef(
        number=4,
        title="MODULE 4 - Disputes, Reviews, Daily Operations & Attendance",
        filename="erd_v2_module4_disputes.png",
        tables=[
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
        refs=[
            "jobs",
            "job_worker_assignments",
            "accounts_accounts",
            "accounts_agency",
            "agency_employees",
            "accounts_profile",
            "accounts_workerspecialization",
            "worker_materials",
            "accounts_workerprofile",
        ],
        columns=[
            ["jobs", "job_worker_assignments", "accounts_accounts", "accounts_agency", "agency_employees", "accounts_profile", "accounts_workerspecialization", "worker_materials", "accounts_workerprofile"],
            ["job_disputes", "dispute_evidence", "backjob_schedule_confirmations"],
            ["job_reviews", "review_skill_tags", "job_materials", "job_photos"],
            ["daily_attendance", "daily_job_extensions", "daily_rate_changes", "daily_skip_day_requests"],
        ],
    ),
    ModuleDef(
        number=5,
        title="MODULE 5 - KYC Verification (Individual & Agency)",
        filename="erd_v2_module5_kyc.png",
        tables=[
            "accounts_kyc",
            "accounts_kycfiles",
            "kyc_extracted_data",
            "agency_agencykyc",
            "agency_agencykycfile",
            "agency_kyc_extracted_data",
            "adminpanel_kyclogs",
        ],
        refs=["accounts_accounts"],
        columns=[
            ["accounts_accounts"],
            ["accounts_kyc", "accounts_kycfiles", "kyc_extracted_data"],
            ["agency_agencykyc", "agency_agencykycfile", "agency_kyc_extracted_data"],
            ["adminpanel_kyclogs"],
        ],
    ),
    ModuleDef(
        number=6,
        title="MODULE 6 - Admin Panel, Messaging, Notifications & Worker Assets",
        filename="erd_v2_module6_admin.png",
        tables=[
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
        refs=[
            "accounts_accounts",
            "accounts_agency",
            "accounts_profile",
            "jobs",
            "job_skill_slots",
            "accounts_wallet",
            "accounts_workerprofile",
            "accounts_workerspecialization",
            "specializations",
        ],
        columns=[
            ["accounts_accounts", "accounts_agency", "accounts_profile", "jobs", "job_skill_slots", "accounts_wallet", "accounts_workerprofile", "accounts_workerspecialization", "specializations"],
            ["adminpanel_adminaccount", "adminpanel_auditlog", "adminpanel_systemroles", "adminpanel_platformsettings", "adminpanel_cannedresponse", "adminpanel_contentmoderationterm", "adminpanel_faq"],
            ["adminpanel_supportticket", "adminpanel_supportticketreply", "adminpanel_userreport", "accounts_notification", "accounts_transaction"],
            ["conversation", "conversation_participants", "message", "message_attachment"],
            ["agency_employees", "worker_certifications", "certification_logs", "worker_materials", "worker_portfolio", "profiles_workerproduct"],
        ],
    ),
]


def parse_schema(sql_text: str) -> dict[str, TableDef]:
    tables: dict[str, TableDef] = {}
    pattern = re.compile(r'CREATE TABLE "([^"]+)" \((.*?)\n\);', re.S)
    field_pattern = re.compile(r'"([^"]+)"\s+([a-z0-9_]+)', re.I)
    for table_name, body in pattern.findall(sql_text):
        fields: list[FieldDef] = []
        for raw_line in body.splitlines():
            line = raw_line.strip().rstrip(",")
            if not line.startswith('"'):
                continue
            match = field_pattern.match(line)
            if not match:
                continue
            field_name, dtype = match.groups()
            fields.append(FieldDef(name=field_name, dtype=dtype, not_null="NOT NULL" in line))
        if not fields:
            raise ValueError(f"No fields parsed for {table_name}")
        fields[0].pk = True
        tables[table_name] = TableDef(name=table_name, fields=fields)
    return tables


def pk_stub(name: str, full_tables: dict[str, TableDef]) -> TableDef:
    if name in full_tables:
        field = full_tables[name].fields[0]
        return TableDef(name=name, fields=[FieldDef(field.name, field.dtype, field.not_null, pk=True)], external_ref=True)
    defaults = {
        "accounts_accounts": ("accountID", "int8"),
    }
    pk_name, dtype = defaults[name]
    return TableDef(name=name, fields=[FieldDef(pk_name, dtype, True, pk=True)], external_ref=True)


def apply_relationship_metadata(tables: dict[str, TableDef]) -> None:
    for table_name, table in tables.items():
        unique_fields = UNIQUE_FIELDS.get(table_name, set())
        fk_fields = FK_MAP.get(table_name, {})
        for field_def in table.fields:
            if field_def.name in unique_fields:
                field_def.unique = True
            if field_def.name in fk_fields:
                field_def.fk_target = fk_fields[field_def.name]


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_key_icon(draw: ImageDraw.ImageDraw, x: int, y: int) -> int:
    ring_r = 4
    draw.ellipse((x, y + 4, x + ring_r * 2, y + 4 + ring_r * 2), outline=PK_GOLD, width=2)
    shaft_x = x + ring_r * 2 + 2
    center_y = y + 4 + ring_r
    draw.line((shaft_x, center_y, shaft_x + 12, center_y), fill=PK_GOLD, width=2)
    draw.line((shaft_x + 8, center_y, shaft_x + 8, center_y + 4), fill=PK_GOLD, width=2)
    draw.line((shaft_x + 11, center_y, shaft_x + 11, center_y + 3), fill=PK_GOLD, width=2)
    return shaft_x + 16


def draw_badge(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, fill: str, text_fill: str = "white") -> int:
    tw, th = text_size(draw, label, FONTS["small_bold"])
    w = tw + 10
    h = th + 4
    draw.rounded_rectangle((x, y, x + w, y + h), radius=5, fill=fill)
    draw.text((x + 5, y + 2), label, font=FONTS["small_bold"], fill=text_fill)
    return w


def draw_table(draw: ImageDraw.ImageDraw, table: TableDef, x: int, y: int) -> TableBox:
    width = REF_W if table.external_ref else TABLE_W
    header_fill = REF_HEADER if table.external_ref else HEADER
    height = HEADER_H + len(table.fields) * ROW_H
    draw.rounded_rectangle((x, y, x + width, y + height), radius=8, outline=BORDER, width=2, fill=BG)
    draw.rounded_rectangle((x, y, x + width, y + HEADER_H), radius=8, fill=header_fill)
    draw.rectangle((x, y + HEADER_H - 8, x + width, y + HEADER_H), fill=header_fill)
    header_label = f"{table.name} [ref]" if table.external_ref else table.name
    draw.text((x + 12, y + 6), header_label, font=FONTS["header"], fill=HEADER_TEXT)

    split_x = x + (150 if table.external_ref else FIELD_SPLIT)
    field_centers: dict[str, tuple[int, int]] = {}
    pk_center: tuple[int, int] | None = None

    for index, field_def in enumerate(table.fields):
        row_y = y + HEADER_H + index * ROW_H
        row_fill = ROW_A if index % 2 == 0 else ROW_B
        draw.rectangle((x + 1, row_y, x + width - 1, row_y + ROW_H), fill=row_fill)
        draw.line((x + 1, row_y, x + width - 1, row_y), fill=SEPARATOR, width=1)
        draw.line((split_x, row_y + 1, split_x, row_y + ROW_H - 1), fill=SEPARATOR, width=1)

        left_x = x + 10
        if field_def.pk:
            left_x = draw_key_icon(draw, left_x, row_y + 1) + 2
            badge_w = draw_badge(draw, left_x, row_y + 3, "PK", PK_GOLD)
            left_x += badge_w + 8
            draw.text((left_x, row_y + 4), field_def.name, font=FONTS["row_bold"], fill=TEXT)
            pk_center = (x + width, row_y + ROW_H // 2)
        else:
            font = FONTS["row_italic"] if field_def.fk_target else FONTS["row"]
            color = FK_BLUE if field_def.fk_target else TEXT
            draw.text((left_x, row_y + 4), field_def.name, font=font, fill=color)

        right_x = split_x + 10
        right_fill = FK_BLUE if field_def.fk_target else MUTED
        dtype_text = field_def.dtype
        draw.text((right_x, row_y + 4), dtype_text, font=FONTS["row"], fill=right_fill)
        dx, _ = text_size(draw, dtype_text, FONTS["row"])
        current_x = right_x + dx + 8
        if field_def.unique:
            current_x += draw_badge(draw, current_x, row_y + 3, "UQ", UNIQUE_BADGE) + 6
        if field_def.fk_target:
            arrow_label = f"→ {field_def.fk_target}"
            draw.text((current_x, row_y + 4), arrow_label, font=FONTS["row"], fill=FK_BLUE)

        field_centers[field_def.name] = (x, row_y + ROW_H // 2)

    draw.line((x + 1, y + height, x + width - 1, y + height), fill=BORDER, width=2)
    return TableBox(table=table, x=x, y=y, w=width, h=height, field_centers=field_centers, pk_center=pk_center)


def draw_one_marker(draw: ImageDraw.ImageDraw, point: tuple[int, int], side: str) -> None:
    x, y = point
    if side == "left":
        draw.line((x + 4, y - 7, x + 4, y + 7), fill=LINE, width=2)
    else:
        draw.line((x - 4, y - 7, x - 4, y + 7), fill=LINE, width=2)


def draw_crowfoot(draw: ImageDraw.ImageDraw, point: tuple[int, int], side: str) -> None:
    x, y = point
    if side == "left":
        base_x = x - 12
        draw.line((base_x, y, x, y), fill=LINE, width=2)
        draw.line((base_x, y, x, y - 8), fill=LINE, width=2)
        draw.line((base_x, y, x, y + 8), fill=LINE, width=2)
        draw.line((x + 4, y - 7, x + 4, y + 7), fill=LINE, width=2)
    else:
        base_x = x + 12
        draw.line((base_x, y, x, y), fill=LINE, width=2)
        draw.line((base_x, y, x, y - 8), fill=LINE, width=2)
        draw.line((base_x, y, x, y + 8), fill=LINE, width=2)
        draw.line((x - 4, y - 7, x - 4, y + 7), fill=LINE, width=2)


def draw_relation(draw: ImageDraw.ImageDraw, parent: TableBox, child: TableBox, child_field_name: str) -> None:
    child_anchor_left = child.x
    child_anchor_right = child.x + child.w
    parent_anchor_left = parent.x
    parent_anchor_right = parent.x + parent.w

    child_side = "left" if parent.x < child.x else "right"
    parent_side = "right" if child_side == "left" else "left"

    start = (
        parent_anchor_right if parent_side == "right" else parent_anchor_left,
        parent.pk_center[1] if parent.pk_center else parent.y + HEADER_H + ROW_H // 2,
    )
    end = (
        child_anchor_left if child_side == "left" else child_anchor_right,
        child.field_centers[child_field_name][1],
    )

    start_step = 16 if parent_side == "right" else -16
    end_step = -16 if child_side == "left" else 16
    mid_x = (start[0] + end[0]) // 2
    points = [
        start,
        (start[0] + start_step, start[1]),
        (mid_x, start[1]),
        (mid_x, end[1]),
        (end[0] + end_step, end[1]),
        end,
    ]
    draw.line(points, fill=LINE, width=2, joint="curve")
    draw_one_marker(draw, start, parent_side)
    draw_crowfoot(draw, end, child_side)


def draw_legend(draw: ImageDraw.ImageDraw, canvas_w: int) -> None:
    legend_x = canvas_w - 520
    legend_y = 16
    draw.rounded_rectangle((legend_x, legend_y, legend_x + 480, legend_y + 66), radius=8, outline=BORDER, fill="#FBFCFE")
    draw.text((legend_x + 12, legend_y + 8), "Legend", font=FONTS["small_bold"], fill=TEXT)
    icon_end = draw_key_icon(draw, legend_x + 12, legend_y + 26)
    badge_w = draw_badge(draw, icon_end + 2, legend_y + 28, "PK", PK_GOLD)
    draw.text((icon_end + badge_w + 12, legend_y + 29), "Primary key field", font=FONTS["small"], fill=TEXT)
    draw.text((legend_x + 12, legend_y + 47), "Italic blue field = foreign key, crow's foot line = one-to-many", font=FONTS["small"], fill=FK_BLUE)


def build_module_tables(module: ModuleDef, full_tables: dict[str, TableDef]) -> dict[str, TableDef]:
    built: dict[str, TableDef] = {}
    for name in module.tables:
        built[name] = full_tables[name]
    for name in module.refs:
        if name not in built:
            built[name] = pk_stub(name, full_tables)
    return built


def validate_module(module: ModuleDef, tables: dict[str, TableDef]) -> None:
    ordered = [name for col in module.columns for name in col]
    missing = set(module.tables + module.refs) - set(ordered)
    if missing:
        raise ValueError(f"Layout missing tables for module {module.number}: {sorted(missing)}")
    for table_name in module.tables:
        for field in tables[table_name].fields:
            if field.fk_target and field.fk_target not in tables:
                raise ValueError(f"{table_name}.{field.name} points to missing target {field.fk_target} in module {module.number}")


def render_module(module: ModuleDef, full_tables: dict[str, TableDef], out_dir: Path) -> Path:
    module_tables = build_module_tables(module, full_tables)
    validate_module(module, module_tables)

    col_heights: list[int] = []
    col_widths: list[int] = []
    for column in module.columns:
        total_h = 0
        max_w = 0
        for index, table_name in enumerate(column):
            table = module_tables[table_name]
            box_h = HEADER_H + len(table.fields) * ROW_H
            total_h += box_h
            if index > 0:
                total_h += ROW_GAP
            max_w = max(max_w, REF_W if table.external_ref else TABLE_W)
        col_heights.append(total_h)
        col_widths.append(max_w)

    canvas_w = MARGIN_X * 2 + sum(col_widths) + COL_GAP * (len(col_widths) - 1)
    canvas_h = TOP_PAD + max(col_heights) + BOTTOM_PAD
    image = Image.new("RGB", (canvas_w, canvas_h), BG)
    draw = ImageDraw.Draw(image)

    draw.text((MARGIN_X, 18), module.title, font=FONTS["title"], fill=TEXT)
    note = f"{len(module.tables)} core tables, {len(module.refs)} external references"
    draw.text((MARGIN_X, 58), note, font=FONTS["note"], fill=MUTED)
    draw_legend(draw, canvas_w)

    boxes: dict[str, TableBox] = {}
    current_x = MARGIN_X
    for col_idx, column in enumerate(module.columns):
        current_y = TOP_PAD
        col_w = col_widths[col_idx]
        for table_name in column:
            table = module_tables[table_name]
            box_w = REF_W if table.external_ref else TABLE_W
            box_x = current_x + (col_w - box_w) // 2
            box = draw_table(draw, table, box_x, current_y)
            boxes[table_name] = box
            current_y += box.h + ROW_GAP
        current_x += col_w + COL_GAP

    for table_name in module.tables:
        child_box = boxes[table_name]
        for field_def in module_tables[table_name].fields:
            if field_def.fk_target:
                parent_box = boxes[field_def.fk_target]
                draw_relation(draw, parent_box, child_box, field_def.name)

    output_path = out_dir / module.filename
    image.save(output_path)
    return output_path


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    full_tables = parse_schema(SCHEMA_SQL)
    apply_relationship_metadata(full_tables)
    generated = []
    for module in MODULES:
        generated.append(render_module(module, full_tables, out_dir))
    for path in generated:
        print(path.name)


if __name__ == "__main__":
    main()
