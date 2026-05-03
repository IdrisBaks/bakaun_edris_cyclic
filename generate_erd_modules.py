#!/usr/bin/env python3
"""Render corrected ERD PNGs for database schema modules 2 through 6."""

from __future__ import annotations

import math
import os
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

from PIL import Image, ImageDraw, ImageFont


SQL = r'''
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
'''


PRIMARY_KEYS: Dict[str, str] = {
    "accounts_agency": "agencyId",
    "accounts_barangay": "barangayID",
    "accounts_city": "cityID",
    "accounts_clientprofile": "id",
    "accounts_interestedjobs": "id",
    "accounts_kyc": "kycID",
    "accounts_kycfiles": "kycFileID",
    "accounts_notification": "notificationID",
    "accounts_notificationsettings": "settingsID",
    "accounts_profile": "profileID",
    "accounts_pushtoken": "tokenID",
    "accounts_transaction": "transactionID",
    "accounts_userpaymentmethod": "id",
    "accounts_wallet": "walletID",
    "accounts_workerprofile": "id",
    "accounts_workerspecialization": "id",
    "adminpanel_adminaccount": "adminID",
    "adminpanel_auditlog": "auditLogID",
    "adminpanel_cannedresponse": "responseID",
    "adminpanel_contentmoderationterm": "termID",
    "adminpanel_faq": "faqID",
    "adminpanel_kyclogs": "kycLogID",
    "adminpanel_platformsettings": "settingsID",
    "adminpanel_supportticket": "ticketID",
    "adminpanel_supportticketreply": "replyID",
    "adminpanel_systemroles": "systemRoleID",
    "adminpanel_userreport": "reportID",
    "agency_agencykyc": "agencyKycID",
    "agency_agencykycfile": "fileID",
    "agency_employees": "employeeID",
    "agency_kyc_extracted_data": "extractedDataID",
    "backjob_schedule_confirmations": "confirmationID",
    "certification_logs": "certLogID",
    "conversation": "conversationID",
    "conversation_participants": "participantID",
    "daily_attendance": "attendanceID",
    "daily_job_extensions": "extensionID",
    "daily_rate_changes": "changeID",
    "daily_skip_day_requests": "skipRequestID",
    "dispute_evidence": "evidenceID",
    "job_applications": "applicationID",
    "job_disputes": "disputeID",
    "job_employee_assignments": "assignmentID",
    "job_logs": "logID",
    "job_materials": "jobMaterialID",
    "job_photos": "photoID",
    "job_reviews": "reviewID",
    "job_skill_slots": "skillSlotID",
    "job_worker_assignments": "assignmentID",
    "jobs": "jobID",
    "kyc_extracted_data": "extractedDataID",
    "message": "messageID",
    "message_attachment": "attachmentID",
    "price_negotiations": "negotiationID",
    "profiles_workerproduct": "productID",
    "review_skill_tags": "tagID",
    "saved_jobs": "savedJobID",
    "specializations": "specializationID",
    "worker_certifications": "certificationID",
    "worker_materials": "materialID",
    "worker_portfolio": "portfolioID",
}


UNIQUE_FIELDS = {
    ("accounts_clientprofile", "profileID_id"),
    ("accounts_notificationsettings", "accountFK_id"),
    ("accounts_pushtoken", "pushToken"),
    ("accounts_wallet", "accountFK_id"),
    ("accounts_workerprofile", "profileID_id"),
    ("adminpanel_adminaccount", "accountFK_id"),
    ("agency_kyc_extracted_data", "agencyKyc_id"),
    ("conversation", "relatedJobPosting_id"),
    ("kyc_extracted_data", "kycID_id"),
}


NULLABLE_FIELDS = {
    ("accounts_wallet", "preferredPaymentMethodID_id"),
}


FK_TARGETS: Dict[Tuple[str, str], str] = {
    ("accounts_profile", "accountFK_id"): "accounts_accounts",
    ("accounts_workerprofile", "profileID_id"): "accounts_profile",
    ("accounts_clientprofile", "profileID_id"): "accounts_profile",
    ("accounts_agency", "accountFK_id"): "accounts_accounts",
    ("accounts_barangay", "city_id"): "accounts_city",
    ("accounts_workerspecialization", "workerID_id"): "accounts_workerprofile",
    ("accounts_workerspecialization", "specializationID_id"): "specializations",
    ("accounts_interestedjobs", "clientID_id"): "accounts_clientprofile",
    ("accounts_interestedjobs", "specializationID_id"): "specializations",
    ("accounts_wallet", "accountFK_id"): "accounts_accounts",
    ("accounts_wallet", "preferredPaymentMethodID_id"): "accounts_userpaymentmethod",
    ("accounts_userpaymentmethod", "accountFK_id"): "accounts_accounts",
    ("accounts_pushtoken", "accountFK_id"): "accounts_accounts",
    ("accounts_notificationsettings", "accountFK_id"): "accounts_accounts",
    ("specializations", "created_by_agency_id"): "accounts_agency",
    ("specializations", "created_by_worker_id"): "accounts_accounts",
    ("jobs", "clientID_id"): "accounts_clientprofile",
    ("jobs", "assignedWorkerID_id"): "accounts_workerprofile",
    ("jobs", "assignedAgencyFK_id"): "accounts_agency",
    ("jobs", "assignedEmployeeID_id"): "agency_employees",
    ("jobs", "categoryID_id"): "specializations",
    ("jobs", "cancelledByAccountID_id"): "accounts_accounts",
    ("jobs", "cashPaymentApprovedBy_id"): "accounts_accounts",
    ("job_skill_slots", "jobID_id"): "jobs",
    ("job_skill_slots", "specializationID_id"): "specializations",
    ("job_skill_slots", "invited_agency_id"): "accounts_agency",
    ("job_applications", "jobID_id"): "jobs",
    ("job_applications", "workerID_id"): "accounts_workerprofile",
    ("job_applications", "applied_skill_slot_id"): "job_skill_slots",
    ("price_negotiations", "application_id"): "job_applications",
    ("job_worker_assignments", "jobID_id"): "jobs",
    ("job_worker_assignments", "skillSlotID_id"): "job_skill_slots",
    ("job_worker_assignments", "workerID_id"): "accounts_workerprofile",
    ("job_employee_assignments", "job_id"): "jobs",
    ("job_employee_assignments", "employee_id"): "agency_employees",
    ("job_employee_assignments", "skill_slot_id"): "job_skill_slots",
    ("job_employee_assignments", "assignedBy_id"): "accounts_accounts",
    ("job_logs", "jobID_id"): "jobs",
    ("job_logs", "changedBy_id"): "accounts_accounts",
    ("saved_jobs", "jobID_id"): "jobs",
    ("saved_jobs", "workerID_id"): "accounts_workerprofile",
    ("job_disputes", "jobID_id"): "jobs",
    ("dispute_evidence", "disputeID_id"): "job_disputes",
    ("dispute_evidence", "uploadedBy_id"): "accounts_accounts",
    ("backjob_schedule_confirmations", "disputeID_id"): "job_disputes",
    ("backjob_schedule_confirmations", "assignmentID_id"): "job_worker_assignments",
    ("backjob_schedule_confirmations", "confirmedBy_id"): "accounts_accounts",
    ("job_reviews", "jobID_id"): "jobs",
    ("job_reviews", "reviewerID_id"): "accounts_accounts",
    ("job_reviews", "revieweeID_id"): "accounts_accounts",
    ("job_reviews", "revieweeProfileID_id"): "accounts_profile",
    ("job_reviews", "revieweeAgencyID_id"): "accounts_agency",
    ("job_reviews", "revieweeEmployeeID_id"): "agency_employees",
    ("job_reviews", "flaggedBy_id"): "accounts_accounts",
    ("review_skill_tags", "reviewID_id"): "job_reviews",
    ("review_skill_tags", "workerSpecializationID_id"): "accounts_workerspecialization",
    ("job_materials", "jobID_id"): "jobs",
    ("job_materials", "workerMaterialID_id"): "worker_materials",
    ("job_photos", "jobID_id"): "jobs",
    ("daily_attendance", "jobID_id"): "jobs",
    ("daily_attendance", "workerID_id"): "accounts_workerprofile",
    ("daily_attendance", "assignmentID_id"): "job_worker_assignments",
    ("daily_attendance", "employeeID_id"): "agency_employees",
    ("daily_job_extensions", "jobID_id"): "jobs",
    ("daily_job_extensions", "requestedByUser_id"): "accounts_accounts",
    ("daily_rate_changes", "jobID_id"): "jobs",
    ("daily_rate_changes", "requestedByUser_id"): "accounts_accounts",
    ("daily_skip_day_requests", "jobID_id"): "jobs",
    ("daily_skip_day_requests", "requestedByUser_id"): "accounts_accounts",
    ("daily_skip_day_requests", "reviewedByUser_id"): "accounts_accounts",
    ("daily_skip_day_requests", "target_employee_id"): "agency_employees",
    ("daily_skip_day_requests", "target_worker_account_id"): "accounts_accounts",
    ("accounts_kyc", "accountFK_id"): "accounts_accounts",
    ("accounts_kyc", "reviewedBy_id"): "accounts_accounts",
    ("accounts_kycfiles", "kycID_id"): "accounts_kyc",
    ("kyc_extracted_data", "kycID_id"): "accounts_kyc",
    ("agency_agencykyc", "accountFK_id"): "accounts_accounts",
    ("agency_agencykyc", "reviewedBy_id"): "accounts_accounts",
    ("agency_agencykycfile", "agencyKyc_id"): "agency_agencykyc",
    ("agency_kyc_extracted_data", "agencyKyc_id"): "agency_agencykyc",
    ("adminpanel_kyclogs", "accountFK_id"): "accounts_accounts",
    ("adminpanel_kyclogs", "reviewedBy_id"): "accounts_accounts",
    ("adminpanel_adminaccount", "accountFK_id"): "accounts_accounts",
    ("adminpanel_auditlog", "adminFK_id"): "accounts_accounts",
    ("adminpanel_supportticket", "userFK_id"): "accounts_accounts",
    ("adminpanel_supportticket", "assignedTo_id"): "accounts_accounts",
    ("adminpanel_supportticket", "agencyFK_id"): "accounts_agency",
    ("adminpanel_supportticketreply", "ticketFK_id"): "adminpanel_supportticket",
    ("adminpanel_supportticketreply", "senderFK_id"): "accounts_accounts",
    ("adminpanel_userreport", "reporterFK_id"): "accounts_accounts",
    ("adminpanel_userreport", "reportedUserFK_id"): "accounts_accounts",
    ("adminpanel_userreport", "reviewedBy_id"): "accounts_accounts",
    ("adminpanel_platformsettings", "updatedBy_id"): "accounts_accounts",
    ("adminpanel_cannedresponse", "createdBy_id"): "accounts_accounts",
    ("adminpanel_contentmoderationterm", "createdBy_id"): "accounts_accounts",
    ("adminpanel_contentmoderationterm", "updatedBy_id"): "accounts_accounts",
    ("adminpanel_systemroles", "accountID_id"): "accounts_accounts",
    ("accounts_notification", "accountFK_id"): "accounts_accounts",
    ("conversation", "client_id"): "accounts_profile",
    ("conversation", "worker_id"): "accounts_profile",
    ("conversation", "agency_id"): "accounts_agency",
    ("conversation", "relatedJobPosting_id"): "jobs",
    ("conversation", "lastMessageSender_id"): "accounts_profile",
    ("conversation_participants", "conversation_id"): "conversation",
    ("conversation_participants", "profile_id"): "accounts_profile",
    ("conversation_participants", "skill_slot_id"): "job_skill_slots",
    ("conversation_participants", "admin_account_id"): "accounts_accounts",
    ("message", "conversationID_id"): "conversation",
    ("message", "sender_id"): "accounts_profile",
    ("message", "senderAgency_id"): "accounts_agency",
    ("message", "sender_admin_id"): "accounts_accounts",
    ("message_attachment", "messageID_id"): "message",
    ("accounts_transaction", "walletID_id"): "accounts_wallet",
    ("accounts_transaction", "relatedJobPosting_id"): "jobs",
    ("accounts_transaction", "processedByAdmin_id"): "accounts_accounts",
    ("agency_employees", "agency_id"): "accounts_accounts",
    ("worker_certifications", "workerID_id"): "accounts_workerprofile",
    ("worker_certifications", "specializationID_id"): "accounts_workerspecialization",
    ("worker_certifications", "verified_by_id"): "accounts_accounts",
    ("certification_logs", "workerID_id"): "accounts_workerprofile",
    ("certification_logs", "reviewedBy_id"): "accounts_accounts",
    ("worker_materials", "workerID_id"): "accounts_workerprofile",
    ("worker_materials", "agencyID_id"): "accounts_agency",
    ("worker_materials", "categoryID_id"): "specializations",
    ("worker_portfolio", "workerID_id"): "accounts_workerprofile",
    ("profiles_workerproduct", "workerID_id"): "accounts_workerprofile",
    ("profiles_workerproduct", "categoryID_id"): "specializations",
}


MODULES = [
    {
        "number": 2,
        "title": "Module 2 - Profiles, Location, Wallet & Specializations",
        "filename": "erd_v2_module2_profiles.png",
        "tables": [
            "accounts_profile", "accounts_workerprofile", "accounts_clientprofile",
            "accounts_agency", "accounts_barangay", "accounts_city",
            "specializations", "accounts_workerspecialization",
            "accounts_interestedjobs", "accounts_wallet",
            "accounts_userpaymentmethod", "accounts_pushtoken",
            "accounts_notificationsettings",
        ],
        "cols": 4,
        "external": ["accounts_accounts"],
    },
    {
        "number": 3,
        "title": "Module 3 - Jobs, Applications & Assignments",
        "filename": "erd_v2_module3_jobs.png",
        "tables": [
            "jobs", "job_skill_slots", "job_applications", "price_negotiations",
            "job_worker_assignments", "job_employee_assignments", "job_logs",
            "saved_jobs",
        ],
        "cols": 3,
        "external": [
            "accounts_clientprofile", "accounts_workerprofile", "accounts_agency",
            "agency_employees", "specializations", "accounts_accounts",
        ],
    },
    {
        "number": 4,
        "title": "Module 4 - Disputes, Reviews, Daily Operations & Attendance",
        "filename": "erd_v2_module4_disputes.png",
        "tables": [
            "job_disputes", "dispute_evidence", "backjob_schedule_confirmations",
            "job_reviews", "review_skill_tags", "job_materials", "job_photos",
            "daily_attendance", "daily_job_extensions", "daily_rate_changes",
            "daily_skip_day_requests",
        ],
        "cols": 4,
        "external": [
            "jobs", "job_worker_assignments", "accounts_accounts", "accounts_profile",
            "accounts_agency", "agency_employees", "accounts_workerspecialization",
            "worker_materials", "accounts_workerprofile",
        ],
    },
    {
        "number": 5,
        "title": "Module 5 - KYC Verification (Individual & Agency)",
        "filename": "erd_v2_module5_kyc.png",
        "tables": [
            "accounts_kyc", "accounts_kycfiles", "kyc_extracted_data",
            "agency_agencykyc", "agency_agencykycfile",
            "agency_kyc_extracted_data", "adminpanel_kyclogs",
        ],
        "cols": 3,
        "external": ["accounts_accounts"],
    },
    {
        "number": 6,
        "title": "Module 6 - Admin Panel, Messaging, Notifications & Worker Assets",
        "filename": "erd_v2_module6_admin.png",
        "tables": [
            "adminpanel_adminaccount", "adminpanel_auditlog",
            "adminpanel_supportticket", "adminpanel_supportticketreply",
            "adminpanel_userreport", "adminpanel_platformsettings",
            "adminpanel_cannedresponse", "adminpanel_contentmoderationterm",
            "adminpanel_faq", "adminpanel_systemroles", "accounts_notification",
            "conversation", "conversation_participants", "message",
            "message_attachment", "accounts_transaction", "agency_employees",
            "worker_certifications", "certification_logs", "worker_materials",
            "worker_portfolio", "profiles_workerproduct",
        ],
        "cols": 5,
        "external": [
            "accounts_accounts", "accounts_agency", "accounts_profile", "jobs",
            "job_skill_slots", "accounts_wallet", "accounts_workerprofile",
            "accounts_workerspecialization", "specializations",
        ],
    },
]


@dataclass(frozen=True)
class Field:
    name: str
    dtype: str


@dataclass
class TableBox:
    name: str
    x: int
    y: int
    w: int
    h: int


def parse_sql(sql: str) -> Dict[str, List[Field]]:
    tables: Dict[str, List[Field]] = {}
    chunks = sql.split("CREATE TABLE ")[1:]
    for chunk in chunks:
        header, rest = chunk.split("(", 1)
        table_name = header.strip().strip('"').strip()
        body = rest.rsplit(");", 1)[0]
        fields: List[Field] = []
        for raw_line in body.splitlines():
            line = raw_line.strip().rstrip(",")
            if not line or not line.startswith('"'):
                continue
            name, after = line[1:].split('"', 1)
            dtype = after.strip().split()[0]
            fields.append(Field(name=name, dtype=dtype))
        tables[table_name] = fields
    return tables


def load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    paths = [
        f"/usr/share/fonts/truetype/dejavu/{name}.ttf",
        f"/usr/share/fonts/truetype/liberation2/{name}.ttf",
    ]
    for path in paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


FONT_TITLE = load_font("DejaVuSans-Bold", 36)
FONT_SUBTITLE = load_font("DejaVuSans", 20)
FONT_HEADER = load_font("DejaVuSans-Bold", 17)
FONT_ROW = load_font("DejaVuSans", 14)
FONT_ROW_BOLD = load_font("DejaVuSans-Bold", 14)
FONT_ROW_ITALIC = load_font("DejaVuSans-Oblique", 14)
FONT_SMALL = load_font("DejaVuSans", 12)
FONT_SMALL_ITALIC = load_font("DejaVuSans-Oblique", 12)


COLORS = {
    "bg": (255, 255, 255),
    "header": (30, 61, 89),
    "border": (60, 72, 88),
    "row": (255, 255, 255),
    "row_alt": (246, 248, 251),
    "fk": (28, 92, 181),
    "pk_gold": (212, 157, 38),
    "line": (71, 85, 105),
    "external": (231, 237, 245),
    "text": (24, 31, 42),
}


def table_height(field_count: int, row_h: int = 22) -> int:
    return 32 + field_count * row_h


def draw_key(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    draw.ellipse((x, y + 5, x + 9, y + 14), outline=COLORS["pk_gold"], width=2)
    draw.line((x + 9, y + 9, x + 19, y + 9), fill=COLORS["pk_gold"], width=2)
    draw.line((x + 15, y + 9, x + 15, y + 13), fill=COLORS["pk_gold"], width=2)
    draw.text((x + 24, y + 3), "PK", font=FONT_SMALL, fill=COLORS["pk_gold"])


def wrap_text(text: str, font: ImageFont.ImageFont, max_width: int) -> str:
    if ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(text, font=font) <= max_width:
        return text
    ell = "..."
    while text and ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(text + ell, font=font) > max_width:
        text = text[:-1]
    return text + ell


def draw_table(
    draw: ImageDraw.ImageDraw,
    box: TableBox,
    fields: List[Field],
    pk: str,
    fks: Dict[str, str],
    external: bool = False,
) -> None:
    header_color = (79, 96, 121) if external else COLORS["header"]
    draw.rounded_rectangle((box.x, box.y, box.x + box.w, box.y + box.h), radius=5, fill=COLORS["bg"], outline=COLORS["border"], width=2)
    draw.rounded_rectangle((box.x, box.y, box.x + box.w, box.y + 32), radius=5, fill=header_color, outline=header_color)
    draw.rectangle((box.x, box.y + 24, box.x + box.w, box.y + 32), fill=header_color)
    title = wrap_text(box.name, FONT_HEADER, box.w - 18)
    draw.text((box.x + 9, box.y + 7), title, font=FONT_HEADER, fill=(255, 255, 255))

    y = box.y + 32
    row_h = 22
    for idx, field in enumerate(fields):
        fill = COLORS["row_alt"] if idx % 2 else COLORS["row"]
        draw.rectangle((box.x + 1, y, box.x + box.w - 1, y + row_h), fill=fill)
        is_pk = field.name == pk
        fk_target = fks.get(field.name)
        dtype = field.dtype
        extras = []
        if (box.name, field.name) in UNIQUE_FIELDS:
            extras.append("UNIQUE")
        if (box.name, field.name) in NULLABLE_FIELDS:
            extras.append("nullable")
        dtype_text = dtype + (f" ({', '.join(extras)})" if extras else "")
        if is_pk:
            draw_key(draw, box.x + 7, y)
            text_x = box.x + 60
            font = FONT_ROW_BOLD
            fill_text = COLORS["text"]
        elif fk_target:
            text_x = box.x + 10
            font = FONT_ROW_ITALIC
            fill_text = COLORS["fk"]
        else:
            text_x = box.x + 10
            font = FONT_ROW
            fill_text = COLORS["text"]

        label = f"{field.name} | {dtype_text}"
        if fk_target:
            label = f"{label}  \\u2192 {fk_target}"
        label = label.encode("utf-8").decode("unicode_escape")
        draw.text((text_x, y + 4), wrap_text(label, font, box.w - (text_x - box.x) - 8), font=font, fill=fill_text)
        y += row_h


def edge_point(a: TableBox, b: TableBox) -> Tuple[int, int, int, int]:
    ax, ay = a.x + a.w / 2, a.y + a.h / 2
    bx, by = b.x + b.w / 2, b.y + b.h / 2
    if abs(bx - ax) > abs(by - ay):
        x1 = a.x + a.w if bx > ax else a.x
        y1 = int(ay)
        x2 = b.x if bx > ax else b.x + b.w
        y2 = int(by)
    else:
        x1 = int(ax)
        y1 = a.y + a.h if by > ay else a.y
        x2 = int(bx)
        y2 = b.y if by > ay else b.y + b.h
    return int(x1), int(y1), int(x2), int(y2)


def draw_crows_foot(draw: ImageDraw.ImageDraw, x: int, y: int, toward_x: int, toward_y: int) -> None:
    angle = math.atan2(toward_y - y, toward_x - x) + math.pi
    for delta in (-0.45, 0, 0.45):
        ex = x + int(math.cos(angle + delta) * 13)
        ey = y + int(math.sin(angle + delta) * 13)
        draw.line((x, y, ex, ey), fill=COLORS["line"], width=2)


def draw_relationships(
    draw: ImageDraw.ImageDraw,
    boxes: Dict[str, TableBox],
    module_tables: Iterable[str],
) -> None:
    tables = set(module_tables)
    for (src, field), target in FK_TARGETS.items():
        if src not in tables or src not in boxes:
            continue
        if target not in boxes:
            continue
        sx, sy, tx, ty = edge_point(boxes[src], boxes[target])
        draw.line((sx, sy, tx, ty), fill=COLORS["line"], width=2)
        draw_crows_foot(draw, sx, sy, tx, ty)
        draw.text((tx - 10, ty - 16), "1", font=FONT_SMALL, fill=COLORS["line"])
        mx, my = (sx + tx) // 2, (sy + ty) // 2
        label = f"{field} -> {target}"
        label = wrap_text(label, FONT_SMALL_ITALIC, 220)
        tw = int(draw.textlength(label, font=FONT_SMALL_ITALIC))
        draw.rectangle((mx - tw // 2 - 3, my - 9, mx + tw // 2 + 3, my + 8), fill=(255, 255, 255))
        draw.text((mx - tw // 2, my - 8), label, font=FONT_SMALL_ITALIC, fill=COLORS["fk"])


def layout_boxes(module: dict, tables: Dict[str, List[Field]]) -> Tuple[Dict[str, TableBox], int, int]:
    cols = module["cols"]
    row_h = 22
    top = 125
    margin_x = 45
    gap_x = 36
    gap_y = 42
    width = 500 if cols >= 4 else 580
    if module["number"] == 6:
        width = 520
    boxes: Dict[str, TableBox] = {}
    row_y = top
    all_tables = list(module["tables"])
    rows = [all_tables[i:i + cols] for i in range(0, len(all_tables), cols)]
    for row in rows:
        heights = []
        for name in row:
            heights.append(table_height(len(tables[name]), row_h))
        row_height = max(heights)
        for c, name in enumerate(row):
            x = margin_x + c * (width + gap_x)
            h = table_height(len(tables[name]), row_h)
            boxes[name] = TableBox(name=name, x=x, y=row_y, w=width, h=h)
        row_y += row_height + gap_y

    ext_names = module.get("external", [])
    ext_y = row_y + 10
    ext_w = min(width, 360)
    ext_h = 64
    for idx, name in enumerate(ext_names):
        c = idx % cols
        r = idx // cols
        x = margin_x + c * (width + gap_x)
        y = ext_y + r * (ext_h + 20)
        boxes[name] = TableBox(name=name, x=x, y=y, w=ext_w, h=ext_h)

    canvas_w = margin_x * 2 + cols * width + (cols - 1) * gap_x
    ext_rows = math.ceil(len(ext_names) / cols)
    canvas_h = ext_y + ext_rows * (ext_h + 20) + 45
    return boxes, canvas_w, canvas_h


def external_fields(name: str) -> List[Field]:
    pk_by_table = {
        "accounts_accounts": ("accountID", "int8"),
        "accounts_profile": ("profileID", "int8"),
        "accounts_agency": ("agencyId", "int8"),
        "accounts_clientprofile": ("id", "int8"),
        "accounts_workerprofile": ("id", "int8"),
        "accounts_workerspecialization": ("id", "int8"),
        "agency_employees": ("employeeID", "int8"),
        "jobs": ("jobID", "int8"),
        "job_skill_slots": ("skillSlotID", "int8"),
        "job_worker_assignments": ("assignmentID", "int8"),
        "specializations": ("specializationID", "int8"),
        "accounts_wallet": ("walletID", "int8"),
        "worker_materials": ("materialID", "int8"),
    }
    field_name, dtype = pk_by_table.get(name, ("id", "int8"))
    return [Field(field_name, dtype)]


def render_module(module: dict, tables: Dict[str, List[Field]]) -> str:
    boxes, canvas_w, canvas_h = layout_boxes(module, tables)
    image = Image.new("RGB", (canvas_w, canvas_h), COLORS["bg"])
    draw = ImageDraw.Draw(image)
    draw.text((45, 28), module["title"], font=FONT_TITLE, fill=COLORS["text"])
    note = f"Table count: {len(module['tables'])} core tables; external reference tables shown in gray"
    draw.text((47, 77), note, font=FONT_SUBTITLE, fill=(82, 94, 110))

    draw_relationships(draw, boxes, module["tables"])

    for name in list(module["tables"]) + module.get("external", []):
        is_external = name not in module["tables"]
        fields = external_fields(name) if is_external else tables[name]
        pk = PRIMARY_KEYS.get(name, fields[0].name)
        fks = {
            field: target
            for (table, field), target in FK_TARGETS.items()
            if table == name
        }
        draw_table(draw, boxes[name], fields, pk, fks, external=is_external)

    image.save(module["filename"])
    return module["filename"]


def validate(tables: Dict[str, List[Field]]) -> None:
    errors: List[str] = []
    for module in MODULES:
        for table in module["tables"]:
            if table not in tables:
                errors.append(f"missing table: {table}")
            elif table not in PRIMARY_KEYS:
                errors.append(f"missing PK: {table}")
    for (table, field), target in FK_TARGETS.items():
        if table in tables and field not in {f.name for f in tables[table]}:
            errors.append(f"missing FK field: {table}.{field}")
        if target in tables or any(target in m.get("external", []) for m in MODULES):
            continue
    if errors:
        raise SystemExit("\\n".join(errors))


def main() -> None:
    tables = parse_sql(SQL)
    validate(tables)
    for module in MODULES:
        output = render_module(module, tables)
        print(output)


if __name__ == "__main__":
    main()
