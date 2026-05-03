#!/usr/bin/env python3
"""Generate corrected ERD v2 module diagrams as PNG images.

This renderer uses hand-curated table/field specs from the provided SQL and
explicit FK targets from the audit notes. It emits SVG first, then rasterizes
to PNG via CairoSVG for deterministic exports.
"""

from __future__ import annotations

import html
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import cairosvg


ARROW = "\u2192"

OUT_DIR = Path("/workspace")
TMP_DIR = OUT_DIR / ".erd_tmp"
TMP_DIR.mkdir(exist_ok=True)


TABLE_SPECS_RAW: Dict[str, str] = {
    # Module 2
    "accounts_profile": """
profileID|int8|PK
profileImg|varchar|
firstName|varchar|
lastName|varchar|
contactNum|varchar|
birthDate|date|
profileType|varchar|
accountFK_id|int8|FK=accounts_accounts
middleName|varchar|
latitude|numeric|
location_sharing_enabled|bool|
location_updated_at|timestamptz|
longitude|numeric|
""",
    "accounts_workerprofile": """
id|int8|PK
description|varchar|
workerRating|int4|
totalEarningGross|numeric|
availability_status|varchar|
profileID_id|int8|FK=accounts_profile;UNIQUE
bio|varchar|
hourly_rate|numeric|
profile_completion_percentage|int4|
soft_skills|text|
daily_rate|numeric|
is_available_daily_jobs|bool|
""",
    "accounts_clientprofile": """
id|int8|PK
description|varchar|
totalJobsPosted|int4|
clientRating|int4|
profileID_id|int8|FK=accounts_profile;UNIQUE
activeJobsCount|int4|
""",
    "accounts_agency": """
agencyId|int8|PK
businessName|varchar|
businessDesc|varchar|
createdAt|timestamptz|
accountFK_id|int8|FK=accounts_accounts
city|varchar|
country|varchar|
postal_code|varchar|
province|varchar|
street_address|varchar|
contactNumber|varchar|
barangay|varchar|
""",
    "accounts_barangay": """
barangayID|int4|PK
name|varchar|
zipCode|varchar|
createdAt|timestamptz|
updatedAt|timestamptz|
city_id|int4|FK=accounts_city
""",
    "accounts_city": """
cityID|int4|PK
name|varchar|UNIQUE
province|varchar|
region|varchar|
zipCode|varchar|
createdAt|timestamptz|
updatedAt|timestamptz|
""",
    "specializations": """
specializationID|int8|PK
specializationName|varchar|
averageProjectCostMax|numeric|
averageProjectCostMin|numeric|
description|text|
minimumRate|numeric|
rateType|varchar|
skillLevel|varchar|
is_custom|bool|
created_by_agency_id|int8|FK=accounts_agency
created_by_worker_id|int8|FK=accounts_accounts
""",
    "accounts_workerspecialization": """
id|int8|PK
experienceYears|int4|
certification|varchar|
specializationID_id|int8|FK=specializations
workerID_id|int8|FK=accounts_workerprofile
skillType|varchar|
displayOrder|int4|
""",
    "accounts_interestedjobs": """
id|int8|PK
clientID_id|int8|FK=accounts_clientprofile
specializationID_id|int8|FK=specializations
""",
    "accounts_wallet": """
walletID|int8|PK
balance|numeric|
createdAt|timestamptz|
updatedAt|timestamptz|
accountFK_id|int8|FK=accounts_accounts;UNIQUE
reservedBalance|numeric|
pendingEarnings|numeric|
autoWithdrawEnabled|bool|
preferredPaymentMethodID_id|int8|FK=accounts_userpaymentmethod
lastAutoWithdrawAt|timestamptz|
""",
    "accounts_userpaymentmethod": """
id|int8|PK
methodType|varchar|
accountName|varchar|
accountNumber|varchar|
bankName|varchar|
isPrimary|bool|
isVerified|bool|
createdAt|timestamptz|
updatedAt|timestamptz|
accountFK_id|int8|FK=accounts_accounts
bankCode|varchar|
paymongoRecipientId|varchar|
""",
    "accounts_pushtoken": """
tokenID|int8|PK
pushToken|varchar|UNIQUE
deviceType|varchar|
isActive|bool|
createdAt|timestamptz|
updatedAt|timestamptz|
lastUsed|timestamptz|
accountFK_id|int8|FK=accounts_accounts
""",
    "accounts_notificationsettings": """
settingsID|int8|PK
pushEnabled|bool|
soundEnabled|bool|
jobUpdates|bool|
messages|bool|
payments|bool|
reviews|bool|
kycUpdates|bool|
doNotDisturbStart|time|
doNotDisturbEnd|time|
createdAt|timestamptz|
updatedAt|timestamptz|
accountFK_id|int8|FK=accounts_accounts;UNIQUE
""",
    # Module 3
    "jobs": """
jobID|int8|PK
title|varchar|
description|text|
budget|numeric|
location|varchar|
expectedDuration|varchar|
urgency|varchar|
preferredStartDate|date|
materialsNeeded|jsonb|
status|varchar|
completedAt|timestamptz|
cancellationReason|text|
createdAt|timestamptz|
updatedAt|timestamptz|
assignedWorkerID_id|int8|FK=accounts_workerprofile
categoryID_id|int8|FK=specializations
clientID_id|int8|FK=accounts_clientprofile
clientMarkedComplete|bool|
clientMarkedCompleteAt|timestamptz|
workerMarkedComplete|bool|
workerMarkedCompleteAt|timestamptz|
escrowAmount|numeric|
escrowPaid|bool|
escrowPaidAt|timestamptz|
remainingPayment|numeric|
remainingPaymentPaid|bool|
remainingPaymentPaidAt|timestamptz|
finalPaymentMethod|varchar|
cashPaymentProofUrl|varchar|
paymentMethodSelectedAt|timestamptz|
cashProofUploadedAt|timestamptz|
cashPaymentApproved|bool|
cashPaymentApprovedAt|timestamptz|
cashPaymentApprovedBy_id|int8|FK=accounts_accounts
assignedAgencyFK_id|int8|FK=accounts_agency
jobType|varchar|
inviteRejectionReason|text|
inviteRespondedAt|timestamptz|
inviteStatus|varchar|
clientConfirmedWorkStarted|bool|
clientConfirmedWorkStartedAt|timestamptz|
assignedEmployeeID_id|int8|FK=agency_employees
assignmentNotes|text|
employeeAssignedAt|timestamptz|
is_team_job|bool|
budget_allocation_type|varchar|
team_job_start_threshold|numeric|
paymentReleaseDate|timestamptz|
paymentReleasedToWorker|bool|
paymentReleasedAt|timestamptz|
paymentHeldReason|varchar|
job_scope|varchar|
skill_level_required|varchar|
work_environment|varchar|
payment_model|varchar|
duration_days|int4|
daily_rate_agreed|numeric|
actual_start_date|date|
total_days_worked|int4|
daily_escrow_total|numeric|
materialsCost|numeric|
materials_status|varchar|
scheduled_end_date|date|
qa_day_offset|int4|
workerMarkedOnTheWay|bool|
workerMarkedOnTheWayAt|timestamptz|
workerMarkedJobStarted|bool|
workerMarkedJobStartedAt|timestamptz|
is_early_completed|bool|
early_completed_at|timestamptz|
early_completion_payout|numeric|
shift_type|varchar|
cancelledAt|timestamptz|
cancelledByRole|varchar|
cancelledByAccountID_id|int8|FK=accounts_accounts
cancellationStage|varchar|
clientRefundAmount|numeric|
workerCompensationAmount|numeric|
agency_flow_mode|varchar|
""",
    "job_skill_slots": """
skillSlotID|int8|PK
workers_needed|int4|
budget_allocated|numeric|
skill_level_required|varchar|
status|varchar|
notes|text|
createdAt|timestamptz|
updatedAt|timestamptz|
jobID_id|int8|FK=jobs
specializationID_id|int8|FK=specializations
invited_agency_id|int8|FK=accounts_agency
agency_invite_status|varchar|
agency_invite_responded_at|timestamptz|
last_rejected_agency_id|int8|
last_rejected_agency_name|varchar|
last_rejected_at|timestamptz|
last_rejection_reason|text|
""",
    "job_applications": """
applicationID|int8|PK
proposalMessage|text|
proposedBudget|numeric|
estimatedDuration|varchar|
budgetOption|varchar|
status|varchar|
createdAt|timestamptz|
updatedAt|timestamptz|
jobID_id|int8|FK=jobs
workerID_id|int8|FK=accounts_workerprofile
applied_skill_slot_id|int8|FK=job_skill_slots
selected_materials|jsonb|
proposed_daily_rate|numeric|
proposed_days|int4|
negotiation_count|int2|
applied_shift|varchar|
clientRejectionReason|text|
""",
    "price_negotiations": """
negotiationID|int8|PK
application_id|int8|FK=job_applications
actor|varchar|
round_number|int2|
proposed_budget|numeric|
proposed_daily_rate|numeric|
proposed_days|int4|
message|text|
status|varchar|
createdAt|timestamptz|
""",
    "job_worker_assignments": """
assignmentID|int8|PK
slot_position|int4|
assignment_status|varchar|
worker_marked_complete|bool|
worker_marked_complete_at|timestamptz|
completion_notes|text|
individual_rating|numeric|
assignedAt|timestamptz|
updatedAt|timestamptz|
jobID_id|int8|FK=jobs
skillSlotID_id|int8|FK=job_skill_slots
workerID_id|int8|FK=accounts_workerprofile
client_confirmed_arrival|bool|
client_confirmed_arrival_at|timestamptz|
daily_rate_at_assignment|numeric|
days_worked|int4|
total_earned|numeric|
early_completed|bool|
early_completed_at|timestamptz|
early_completion_payout|numeric|
assigned_shift|varchar|
""",
    "job_employee_assignments": """
assignmentID|int8|PK
assignedAt|timestamptz|
notes|text|
isPrimaryContact|bool|
status|varchar|
employeeMarkedComplete|bool|
employeeMarkedCompleteAt|timestamptz|
completionNotes|text|
assignedBy_id|int8|FK=accounts_accounts
employee_id|int8|FK=agency_employees
job_id|int8|FK=jobs
skill_slot_id|int8|FK=job_skill_slots
dispatched|bool|
dispatchedAt|timestamptz|
clientConfirmedArrival|bool|
clientConfirmedArrivalAt|timestamptz|
agencyMarkedComplete|bool|
agencyMarkedCompleteAt|timestamptz|
paymentAmount|numeric|
clientApproved|bool|
clientApprovedAt|timestamptz|
early_completed|bool|
early_completed_at|timestamptz|
early_completion_payout|numeric|
""",
    "job_logs": """
logID|int8|PK
oldStatus|varchar|
newStatus|varchar|
notes|text|
createdAt|timestamptz|
changedBy_id|int8|FK=accounts_accounts
jobID_id|int8|FK=jobs
actionType|varchar|
metadata|jsonb|
""",
    "saved_jobs": """
savedJobID|int8|PK
savedAt|timestamptz|
jobID_id|int8|FK=jobs
workerID_id|int8|FK=accounts_workerprofile
""",
    # Module 4
    "job_disputes": """
disputeID|int8|PK
disputedBy|varchar|
reason|varchar|
description|text|
status|varchar|
priority|varchar|
jobAmount|numeric|
disputedAmount|numeric|
resolution|text|
resolvedDate|timestamptz|
assignedTo|varchar|
openedDate|timestamptz|
updatedAt|timestamptz|
jobID_id|int8|FK=jobs
backjobStarted|bool|
backjobStartedAt|timestamptz|
clientConfirmedBackjob|bool|
clientConfirmedBackjobAt|timestamptz|
workerMarkedBackjobComplete|bool|
workerMarkedBackjobCompleteAt|timestamptz|
termsAccepted|bool|
termsVersion|varchar|
termsAcceptedAt|timestamptz|
adminRejectedAt|timestamptz|
adminRejectionReason|text|
in_negotiation_at|timestamptz|
scheduled_date|date|
workerScheduleConfirmed|bool|
workerScheduleConfirmedAt|timestamptz|
""",
    "dispute_evidence": """
evidenceID|int8|PK
imageURL|varchar|
description|text|
createdAt|timestamptz|
disputeID_id|int8|FK=job_disputes
uploadedBy_id|int8|FK=accounts_accounts
""",
    "backjob_schedule_confirmations": """
confirmationID|int8|PK
confirmed|bool|
confirmedAt|timestamptz|
createdAt|timestamptz|
updatedAt|timestamptz|
assignmentID_id|int8|FK=job_worker_assignments
confirmedBy_id|int8|FK=accounts_accounts
disputeID_id|int8|FK=job_disputes
""",
    "job_reviews": """
reviewID|int8|PK
reviewerType|varchar|
rating|numeric|
comment|text|
status|varchar|
isFlagged|bool|
flagReason|text|
flaggedAt|timestamptz|
helpfulCount|int4|
createdAt|timestamptz|
updatedAt|timestamptz|
flaggedBy_id|int8|FK=accounts_accounts
jobID_id|int8|FK=jobs
revieweeID_id|int8|FK=accounts_accounts
reviewerID_id|int8|FK=accounts_accounts
revieweeAgencyID_id|int8|FK=accounts_agency
revieweeEmployeeID_id|int8|FK=agency_employees
revieweeProfileID_id|int8|FK=accounts_profile
rating_communication|numeric|
rating_professionalism|numeric|
rating_punctuality|numeric|
rating_quality|numeric|
agency_response|text|
agency_response_at|timestamptz|
backjob_edit_deadline|timestamptz|
""",
    "review_skill_tags": """
tagID|int8|PK
createdAt|timestamptz|
reviewID_id|int8|FK=job_reviews
workerSpecializationID_id|int8|FK=accounts_workerspecialization
""",
    "job_materials": """
jobMaterialID|int8|PK
name|varchar|
description|text|
quantity|int4|
unit|varchar|
source|varchar|
purchase_price|numeric|
receipt_image_url|varchar|
client_approved|bool|
client_approved_at|timestamptz|
client_rejected|bool|
rejection_reason|text|
added_by|varchar|
createdAt|timestamptz|
updatedAt|timestamptz|
jobID_id|int8|FK=jobs
workerMaterialID_id|int8|FK=worker_materials
""",
    "job_photos": """
photoID|int8|PK
photoURL|varchar|
fileName|varchar|
uploadedAt|timestamptz|
jobID_id|int8|FK=jobs
""",
    "daily_attendance": """
attendanceID|int8|PK
date|date|
time_in|timestamptz|
time_out|timestamptz|
status|varchar|
worker_confirmed|bool|
worker_confirmed_at|timestamptz|
client_confirmed|bool|
client_confirmed_at|timestamptz|
amount_earned|numeric|
payment_processed|bool|
payment_processed_at|timestamptz|
notes|text|
createdAt|timestamptz|
updatedAt|timestamptz|
jobID_id|int8|FK=jobs
workerID_id|int8|FK=accounts_workerprofile
assignmentID_id|int8|FK=job_worker_assignments
employeeID_id|int8|FK=agency_employees
absent_penalty_amount|numeric|
absent_penalty_applied|bool|
absent_penalty_applied_at|timestamptz|
absent_penalty_percent|numeric|
cash_payment_proof_url|varchar|
cash_payment_verified|bool|
cash_payment_verified_at|timestamptz|
cash_proof_uploaded_at|timestamptz|
payment_method|varchar|
""",
    "daily_job_extensions": """
extensionID|int8|PK
additional_days|int4|
additional_escrow|numeric|
reason|text|
status|varchar|
requested_by|varchar|
client_approved|bool|
client_approved_at|timestamptz|
worker_approved|bool|
worker_approved_at|timestamptz|
escrow_collected|bool|
escrow_collected_at|timestamptz|
createdAt|timestamptz|
updatedAt|timestamptz|
jobID_id|int8|FK=jobs
requestedByUser_id|int8|FK=accounts_accounts
""",
    "daily_rate_changes": """
changeID|int8|PK
old_rate|numeric|
new_rate|numeric|
reason|text|
effective_date|date|
status|varchar|
requested_by|varchar|
client_approved|bool|
client_approved_at|timestamptz|
worker_approved|bool|
worker_approved_at|timestamptz|
escrow_adjusted|bool|
escrow_adjustment_amount|numeric|
createdAt|timestamptz|
updatedAt|timestamptz|
jobID_id|int8|FK=jobs
requestedByUser_id|int8|FK=accounts_accounts
""",
    "daily_skip_day_requests": """
skipRequestID|int8|PK
request_date|date|
status|varchar|
requested_by|varchar|
requested_account_ids|jsonb|
requested_count|int4|
total_required|int4|
requires_all_team_workers|bool|
all_workers_requested|bool|
reviewedAt|timestamptz|
client_rejection_reason|text|
createdAt|timestamptz|
updatedAt|timestamptz|
jobID_id|int8|FK=jobs
requestedByUser_id|int8|FK=accounts_accounts
reviewedByUser_id|int8|FK=accounts_accounts
target_employee_id|int8|FK=agency_employees
target_type|varchar|
target_worker_account_id|int8|FK=accounts_accounts
""",
    # Module 5
    "accounts_kyc": """
kycID|int8|PK
kyc_status|varchar|
reviewedAt|timestamptz|
notes|text|
createdAt|timestamptz|
updatedAt|timestamptz|
accountFK_id|int8|FK=accounts_accounts
reviewedBy_id|int8|FK=accounts_accounts
rejectionCategory|varchar|
rejectionReason|text|
resubmissionCount|int4|
maxResubmissions|int4|
""",
    "accounts_kycfiles": """
kycFileID|int8|PK
idType|varchar|
fileURL|varchar|
fileName|varchar|
fileSize|int4|
uploadedAt|timestamptz|
kycID_id|int8|FK=accounts_kyc
ai_verification_status|varchar|
face_detected|bool|
face_count|int4|
face_confidence|float8|
ocr_text|text|
ocr_confidence|float8|
quality_score|float8|
ai_confidence_score|float8|
ai_rejection_reason|varchar|
ai_rejection_message|varchar|
ai_warnings|jsonb|
ai_details|jsonb|
verified_at|timestamptz|
""",
    "kyc_extracted_data": """
extractedDataID|int8|PK
extracted_full_name|varchar|
extracted_first_name|varchar|
extracted_middle_name|varchar|
extracted_last_name|varchar|
extracted_birth_date|date|
extracted_address|text|
extracted_id_number|varchar|
extracted_id_type|varchar|
extracted_expiry_date|date|
extracted_nationality|varchar|
extracted_sex|varchar|
confidence_full_name|float8|
confidence_birth_date|float8|
confidence_address|float8|
confidence_id_number|float8|
overall_confidence|float8|
confirmed_full_name|varchar|
confirmed_first_name|varchar|
confirmed_middle_name|varchar|
confirmed_last_name|varchar|
confirmed_birth_date|date|
confirmed_address|text|
confirmed_id_number|varchar|
extraction_status|varchar|
extraction_source|varchar|
user_edited_fields|jsonb|
confirmed_at|timestamptz|
extracted_at|timestamptz|
raw_extraction_data|jsonb|
createdAt|timestamptz|
updatedAt|timestamptz|
kycID_id|int8|FK=accounts_kyc;UNIQUE
extracted_place_of_birth|varchar|
extracted_clearance_number|varchar|
extracted_clearance_type|varchar|
extracted_clearance_issue_date|date|
extracted_clearance_validity_date|date|
confidence_place_of_birth|float8|
confidence_clearance_number|float8|
confirmed_nationality|varchar|
confirmed_sex|varchar|
confirmed_place_of_birth|varchar|
confirmed_clearance_number|varchar|
confirmed_clearance_type|varchar|
confirmed_clearance_issue_date|date|
confirmed_clearance_validity_date|date|
face_match_completed|bool|
face_match_score|float8|
""",
    "agency_agencykyc": """
agencyKycID|int8|PK
status|varchar|
reviewedAt|timestamptz|
notes|varchar|
createdAt|timestamptz|
updatedAt|timestamptz|
accountFK_id|int8|FK=accounts_accounts
reviewedBy_id|int8|FK=accounts_accounts
rejectionCategory|varchar|
rejectionReason|text|
resubmissionCount|int4|
maxResubmissions|int4|
face_similarity_score|float8|
""",
    "agency_agencykycfile": """
fileID|int8|PK
fileType|varchar|
fileURL|varchar|
fileName|varchar|
fileSize|int4|
uploadedAt|timestamptz|
agencyKyc_id|int8|FK=agency_agencykyc
ai_verification_status|varchar|
face_detected|bool|
face_count|int4|
face_confidence|float8|
ocr_text|text|
ocr_confidence|float8|
quality_score|float8|
ai_confidence_score|float8|
ai_rejection_reason|varchar|
ai_rejection_message|varchar|
ai_warnings|jsonb|
ai_details|jsonb|
verified_at|timestamptz|
""",
    "agency_kyc_extracted_data": """
extractedDataID|int8|PK
extracted_business_name|varchar|
extracted_business_type|varchar|
extracted_business_address|text|
extracted_permit_number|varchar|
extracted_permit_issue_date|date|
extracted_permit_expiry_date|date|
extracted_dti_number|varchar|
extracted_sec_number|varchar|
extracted_tin|varchar|
extracted_rep_full_name|varchar|
extracted_rep_id_number|varchar|
extracted_rep_id_type|varchar|
extracted_rep_birth_date|date|
extracted_rep_address|text|
confirmed_business_name|varchar|
confirmed_business_type|varchar|
confirmed_business_address|text|
confirmed_permit_number|varchar|
confirmed_permit_issue_date|date|
confirmed_permit_expiry_date|date|
confirmed_dti_number|varchar|
confirmed_sec_number|varchar|
confirmed_tin|varchar|
confirmed_rep_full_name|varchar|
confirmed_rep_id_number|varchar|
confirmed_rep_birth_date|date|
confirmed_rep_address|text|
confidence_business_name|float8|
confidence_business_address|float8|
confidence_permit_number|float8|
confidence_rep_name|float8|
overall_confidence|float8|
extraction_status|varchar|
extraction_source|varchar|
extracted_at|timestamptz|
confirmed_at|timestamptz|
user_edited_fields|jsonb|
raw_extraction_data|jsonb|
createdAt|timestamptz|
updatedAt|timestamptz|
agencyKyc_id|int8|FK=agency_agencykyc;UNIQUE
""",
    "adminpanel_kyclogs": """
kycLogID|int8|PK
action|varchar|
reviewedAt|timestamptz|
reason|text|
userEmail|varchar|
userAccountID|int8|
createdAt|timestamptz|
accountFK_id|int8|FK=accounts_accounts
kycID|int8|
reviewedBy_id|int8|FK=accounts_accounts
kycType|varchar|
""",
    # Module 6
    "adminpanel_adminaccount": """
adminID|int8|PK
role|varchar|
permissions|jsonb|
isActive|bool|
lastLogin|timestamptz|
createdAt|timestamptz|
updatedAt|timestamptz|
accountFK_id|int8|FK=accounts_accounts;UNIQUE
""",
    "adminpanel_auditlog": """
auditLogID|int8|PK
adminEmail|varchar|
action|varchar|
entityType|varchar|
entityID|varchar|
details|jsonb|
beforeValue|jsonb|
afterValue|jsonb|
ipAddress|inet|
userAgent|text|
createdAt|timestamptz|
adminFK_id|int8|FK=accounts_accounts
""",
    "adminpanel_supportticket": """
ticketID|int8|PK
subject|varchar|
category|varchar|
priority|varchar|
status|varchar|
createdAt|timestamptz|
updatedAt|timestamptz|
lastReplyAt|timestamptz|
resolvedAt|timestamptz|
assignedTo_id|int8|FK=accounts_accounts
userFK_id|int8|FK=accounts_accounts
agencyFK_id|int8|FK=accounts_agency
ticketType|varchar|
platform|varchar|
deviceInfo|text|
appVersion|varchar|
""",
    "adminpanel_supportticketreply": """
replyID|int8|PK
content|text|
isSystemMessage|bool|
attachmentURL|varchar|
createdAt|timestamptz|
senderFK_id|int8|FK=accounts_accounts
ticketFK_id|int8|FK=adminpanel_supportticket
""",
    "adminpanel_userreport": """
reportID|int8|PK
reportType|varchar|
reason|varchar|
description|text|
relatedContentID|int8|
status|varchar|
adminNotes|text|
actionTaken|varchar|
createdAt|timestamptz|
updatedAt|timestamptz|
resolvedAt|timestamptz|
reportedUserFK_id|int8|FK=accounts_accounts
reporterFK_id|int8|FK=accounts_accounts
reviewedBy_id|int8|FK=accounts_accounts
""",
    "adminpanel_platformsettings": """
settingsID|int8|PK
platformFeePercentage|numeric|
escrowHoldingDays|int4|
maxJobBudget|numeric|
minJobBudget|numeric|
workerVerificationRequired|bool|
autoApproveKYC|bool|
kycDocumentExpiryDays|int4|
maintenanceMode|bool|
sessionTimeoutMinutes|int4|
maxUploadSizeMB|int4|
lastUpdated|timestamptz|
updatedBy_id|int8|FK=accounts_accounts
kycAutoApproveMinConfidence|numeric|
kycFaceMatchMinSimilarity|numeric|
kycRequireUserConfirmation|bool|
""",
    "adminpanel_cannedresponse": """
responseID|int8|PK
title|varchar|
content|text|
category|varchar|
shortcuts|jsonb|
usageCount|int4|
createdAt|timestamptz|
updatedAt|timestamptz|
createdBy_id|int8|FK=accounts_accounts
""",
    "adminpanel_contentmoderationterm": """
termID|int8|PK
term|varchar|
normalizedTerm|varchar|UNIQUE
isActive|bool|
createdAt|timestamptz|
updatedAt|timestamptz|
createdBy_id|int8|FK=accounts_accounts
updatedBy_id|int8|FK=accounts_accounts
""",
    "adminpanel_faq": """
faqID|int8|PK
question|varchar|
answer|text|
category|varchar|
sortOrder|int4|
viewCount|int4|
isPublished|bool|
createdAt|timestamptz|
updatedAt|timestamptz|
""",
    "adminpanel_systemroles": """
systemRoleID|int8|PK
systemRole|varchar|
createdAt|timestamptz|
updatedAt|timestamptz|
accountID_id|int8|FK=accounts_accounts
""",
    "accounts_notification": """
notificationID|int8|PK
notificationType|varchar|
title|varchar|
message|text|
isRead|bool|
relatedKYCLogID|int8|
createdAt|timestamptz|
readAt|timestamptz|
accountFK_id|int8|FK=accounts_accounts
relatedJobID|int8|
relatedApplicationID|int8|
profile_type|varchar|
""",
    "conversation": """
conversationID|int8|PK
lastMessageText|text|
lastMessageTime|timestamptz|
unreadCountClient|int4|
unreadCountWorker|int4|
status|varchar|
createdAt|timestamptz|
updatedAt|timestamptz|
client_id|int8|FK=accounts_profile
lastMessageSender_id|int8|FK=accounts_profile
relatedJobPosting_id|int8|FK=jobs;UNIQUE
worker_id|int8|FK=accounts_profile
archivedByClient|bool|
archivedByWorker|bool|
agency_id|int8|FK=accounts_agency
conversation_type|varchar|
""",
    "conversation_participants": """
participantID|int8|PK
participant_type|varchar|
unread_count|int4|
is_archived|bool|
joined_at|timestamptz|
last_read_at|timestamptz|
conversation_id|int8|FK=conversation
profile_id|int8|FK=accounts_profile
skill_slot_id|int8|FK=job_skill_slots
admin_account_id|int8|FK=accounts_accounts
""",
    "message": """
messageID|int8|PK
messageText|text|
messageType|varchar|
locationAddress|varchar|
locationLandmark|varchar|
locationLatitude|numeric|
locationLongitude|numeric|
isRead|bool|
readAt|timestamptz|
createdAt|timestamptz|
conversationID_id|int8|FK=conversation
sender_id|int8|FK=accounts_profile
senderAgency_id|int8|FK=accounts_agency
sender_admin_id|int8|FK=accounts_accounts
""",
    "message_attachment": """
attachmentID|int8|PK
fileURL|varchar|
fileName|varchar|
fileSize|int4|
fileType|varchar|
uploadedAt|timestamptz|
messageID_id|int8|FK=message
""",
    "accounts_transaction": """
transactionID|int8|PK
transactionType|varchar|
amount|numeric|
balanceAfter|numeric|
status|varchar|
description|varchar|
referenceNumber|varchar|
paymentMethod|varchar|
createdAt|timestamptz|
completedAt|timestamptz|
relatedJobPosting_id|int8|FK=jobs
walletID_id|int8|FK=accounts_wallet
invoiceURL|varchar|
xenditExternalID|varchar|
xenditInvoiceID|varchar|UNIQUE
xenditPaymentChannel|varchar|
xenditPaymentID|varchar|
xenditPaymentMethod|varchar|
adminReferenceNumber|varchar|
processedAt|timestamptz|
processedByAdmin_id|int8|FK=accounts_accounts
paymongoPaymentId|varchar|
paymongoTransferId|varchar|
paymongoTransferStatus|varchar|
""",
    "agency_employees": """
employeeID|int8|PK
name|varchar|
email|varchar|
role|varchar|
avatar|varchar|
rating|numeric|
createdAt|timestamptz|
updatedAt|timestamptz|
agency_id|int8|FK=accounts_accounts
employeeOfTheMonth|bool|
employeeOfTheMonthDate|timestamptz|
employeeOfTheMonthReason|text|
isActive|bool|
lastRatingUpdate|timestamptz|
totalEarnings|numeric|
totalJobsCompleted|int4|
firstName|varchar|
middleName|varchar|
lastName|varchar|
specializations|text|
daily_rate|numeric|
hourly_rate|numeric|
is_available_daily_jobs|bool|
mobile|varchar|
""",
    "worker_certifications": """
certificationID|int8|PK
name|varchar|
issuing_organization|varchar|
issue_date|date|
expiry_date|date|
certificate_url|varchar|
is_verified|bool|
verified_at|timestamptz|
createdAt|timestamptz|
updatedAt|timestamptz|
verified_by_id|int8|FK=accounts_accounts
workerID_id|int8|FK=accounts_workerprofile
specializationID_id|int8|FK=accounts_workerspecialization
""",
    "certification_logs": """
certLogID|int8|PK
certificationID|int8|
action|varchar|
reviewedAt|timestamptz|
reason|text|
workerEmail|varchar|
workerAccountID|int8|
certificationName|varchar|
reviewedBy_id|int8|FK=accounts_accounts
workerID_id|int8|FK=accounts_workerprofile
""",
    "worker_materials": """
materialID|int8|PK
name|varchar|
description|text|
price|numeric|
unit|varchar|
image_url|varchar|
is_available|bool|
createdAt|timestamptz|
updatedAt|timestamptz|
workerID_id|int8|FK=accounts_workerprofile
quantity|numeric|
categoryID_id|int8|FK=specializations
agencyID_id|int8|FK=accounts_agency
""",
    "worker_portfolio": """
portfolioID|int8|PK
image_url|varchar|
caption|text|
display_order|int4|
file_name|varchar|
file_size|int4|
createdAt|timestamptz|
updatedAt|timestamptz|
workerID_id|int8|FK=accounts_workerprofile
""",
    "profiles_workerproduct": """
productID|int8|PK
productName|varchar|
description|text|
price|numeric|
priceUnit|varchar|
inStock|bool|
stockQuantity|int4|
productImage|varchar|
isActive|bool|
createdAt|timestamptz|
updatedAt|timestamptz|
categoryID_id|int8|FK=specializations
workerID_id|int8|FK=accounts_workerprofile
""",
    "socialaccount_socialtoken": """
id|int4|PK
token|text|
token_secret|text|
expires_at|timestamptz|
account_id|int4|FK=socialaccount_socialaccount
app_id|int4|
""",
}


REF_TABLES_RAW: Dict[str, str] = {
    "accounts_accounts": """
accountID|int8|PK
""",
    "socialaccount_socialaccount": """
id|int4|PK
""",
}


@dataclass
class Field:
    name: str
    data_type: str
    pk: bool = False
    fk: Optional[str] = None
    unique: bool = False


@dataclass
class Table:
    name: str
    fields: List[Field]

    @property
    def pk_field(self) -> Field:
        for field in self.fields:
            if field.pk:
                return field
        return self.fields[0]


@dataclass
class TableBox:
    table: Table
    x: float
    y: float
    w: float
    h: float
    compact: bool
    primary: bool
    row_h: float
    header_h: float


@dataclass
class Module:
    number: int
    title: str
    filename: str
    primary_tables: Sequence[str]
    columns: Sequence[Sequence[str]]


def parse_spec(name: str, raw: str) -> Table:
    fields: List[Field] = []
    for line in raw.strip().splitlines():
        parts = [part.strip() for part in line.strip().split("|")]
        field_name = parts[0]
        data_type = parts[1]
        flags = parts[2] if len(parts) > 2 else ""
        pk = "PK" in flags
        unique = "UNIQUE" in flags
        fk = None
        for flag in flags.split(";"):
            flag = flag.strip()
            if flag.startswith("FK="):
                fk = flag.split("=", 1)[1]
        fields.append(Field(field_name, data_type, pk=pk, fk=fk, unique=unique))
    return Table(name, fields)


TABLES: Dict[str, Table] = {
    name: parse_spec(name, raw) for name, raw in {**TABLE_SPECS_RAW, **REF_TABLES_RAW}.items()
}


MODULES: List[Module] = [
    Module(
        number=2,
        title="Module 2 - Profiles, Location, Wallet & Specializations Tables",
        filename="erd_v2_module2_profiles.png",
        primary_tables=[
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
        columns=[
            ["accounts_accounts", "accounts_city", "accounts_barangay", "accounts_agency"],
            ["accounts_profile", "accounts_clientprofile", "accounts_workerprofile"],
            ["specializations", "accounts_workerspecialization", "accounts_interestedjobs"],
            ["accounts_userpaymentmethod", "accounts_wallet", "accounts_pushtoken", "accounts_notificationsettings"],
        ],
    ),
    Module(
        number=3,
        title="Module 3 - Jobs, Applications & Assignments Tables",
        filename="erd_v2_module3_jobs.png",
        primary_tables=[
            "jobs",
            "job_skill_slots",
            "job_applications",
            "price_negotiations",
            "job_worker_assignments",
            "job_employee_assignments",
            "job_logs",
            "saved_jobs",
        ],
        columns=[
            ["accounts_accounts", "accounts_clientprofile", "accounts_workerprofile", "accounts_agency", "agency_employees", "specializations"],
            ["jobs"],
            ["job_skill_slots", "job_applications", "price_negotiations", "job_worker_assignments"],
            ["job_employee_assignments", "job_logs", "saved_jobs"],
        ],
    ),
    Module(
        number=4,
        title="Module 4 - Disputes, Reviews, Daily Operations & Attendance Tables",
        filename="erd_v2_module4_disputes.png",
        primary_tables=[
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
        columns=[
            ["accounts_accounts", "accounts_workerprofile", "agency_employees", "accounts_profile", "accounts_agency", "accounts_workerspecialization", "worker_materials"],
            ["jobs", "job_worker_assignments"],
            ["job_disputes", "dispute_evidence", "backjob_schedule_confirmations"],
            ["job_reviews", "review_skill_tags", "job_materials", "job_photos"],
            ["daily_attendance", "daily_job_extensions", "daily_rate_changes", "daily_skip_day_requests"],
        ],
    ),
    Module(
        number=5,
        title="Module 5 - KYC Verification (Individual & Agency) Tables",
        filename="erd_v2_module5_kyc.png",
        primary_tables=[
            "accounts_kyc",
            "accounts_kycfiles",
            "kyc_extracted_data",
            "agency_agencykyc",
            "agency_agencykycfile",
            "agency_kyc_extracted_data",
            "adminpanel_kyclogs",
        ],
        columns=[
            ["accounts_accounts"],
            ["accounts_kyc", "accounts_kycfiles", "kyc_extracted_data"],
            ["agency_agencykyc", "agency_agencykycfile", "agency_kyc_extracted_data"],
            ["adminpanel_kyclogs"],
        ],
    ),
    Module(
        number=6,
        title="Module 6 - Admin Panel, Messaging, Notifications & Worker Assets Tables",
        filename="erd_v2_module6_admin.png",
        primary_tables=[
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
            "socialaccount_socialtoken",
        ],
        columns=[
            ["accounts_accounts", "accounts_profile", "accounts_agency", "accounts_workerprofile", "accounts_wallet", "specializations", "accounts_workerspecialization", "jobs", "job_skill_slots", "socialaccount_socialaccount"],
            ["adminpanel_adminaccount", "adminpanel_auditlog", "adminpanel_supportticket", "adminpanel_supportticketreply", "adminpanel_userreport"],
            ["adminpanel_platformsettings", "adminpanel_cannedresponse", "adminpanel_contentmoderationterm", "adminpanel_faq", "adminpanel_systemroles", "accounts_notification", "socialaccount_socialtoken"],
            ["conversation", "conversation_participants", "message", "message_attachment", "accounts_transaction"],
            ["agency_employees", "worker_certifications", "certification_logs", "worker_materials", "worker_portfolio", "profiles_workerproduct"],
        ],
    ),
]


PRIMARY_WIDTH = 520
COMPACT_WIDTH = 255
HEADER_H = 30
ROW_H = 20
GAP_X = 60
GAP_Y = 32
MARGIN_X = 40
TITLE_H = 90
CANVAS_PAD_Y = 30
FIELD_FONT = 10.3
TYPE_FONT = 10.0
HEADER_FONT = 14.5
TITLE_FONT = 26
NOTE_FONT = 12.5


COLORS = {
    "bg": "#FFFFFF",
    "header": "#213B63",
    "header_ref": "#536A86",
    "header_text": "#FFFFFF",
    "table_border": "#BFC8D2",
    "row_a": "#FFFFFF",
    "row_b": "#F5F7FA",
    "text": "#243446",
    "muted": "#66788A",
    "fk": "#1E63B5",
    "line": "#6D7B88",
    "key": "#D4A72C",
    "legend": "#51606F",
}


def compact_table_for(name: str) -> Table:
    base = TABLES[name]
    return Table(name, [base.pk_field])


def measure_width(table: Table, compact: bool) -> float:
    if compact:
        return COMPACT_WIDTH
    longest_left = 0
    longest_right = 0
    for field in table.fields:
        left = field.name
        if field.fk:
            left += f" {ARROW} {field.fk}"
        longest_left = max(longest_left, len(left))
        right = field.data_type + (" UNIQUE" if field.unique and not field.pk else "")
        longest_right = max(longest_right, len(right))
    width = 24 + longest_left * 6.0 + 18 + longest_right * 5.8 + 24
    return max(PRIMARY_WIDTH, min(width, 620))


def table_height(table: Table) -> float:
    return HEADER_H + len(table.fields) * ROW_H


def compute_layout(module: Module) -> Tuple[Dict[str, TableBox], float, float]:
    boxes: Dict[str, TableBox] = {}
    x = MARGIN_X
    max_h = 0.0
    for column in module.columns:
        y = TITLE_H
        col_width = 0.0
        pending: List[Tuple[str, Table, bool, bool]] = []
        for name in column:
            primary = name in module.primary_tables
            table = TABLES[name] if primary else compact_table_for(name)
            compact = not primary
            width = measure_width(table, compact)
            col_width = max(col_width, width)
            pending.append((name, table, compact, primary))
        for name, table, compact, primary in pending:
            width = measure_width(table, compact)
            box = TableBox(
                table=table,
                x=x + (col_width - width) / 2,
                y=y,
                w=width,
                h=table_height(table),
                compact=compact,
                primary=primary,
                row_h=ROW_H,
                header_h=HEADER_H,
            )
            boxes[name] = box
            y += box.h + GAP_Y
        max_h = max(max_h, y)
        x += col_width + GAP_X
    width = x - GAP_X + MARGIN_X
    height = max_h + CANVAS_PAD_Y
    return boxes, width, height


def field_anchor(box: TableBox, field_name: str, side: str) -> Tuple[float, float]:
    idx = next(i for i, field in enumerate(box.table.fields) if field.name == field_name)
    y = box.y + box.header_h + idx * box.row_h + box.row_h / 2
    if side == "left":
        return box.x, y
    if side == "right":
        return box.x + box.w, y
    if side == "top":
        return box.x + box.w / 2, box.y
    return box.x + box.w / 2, box.y + box.h


def box_anchor(box: TableBox, side: str) -> Tuple[float, float]:
    if side == "left":
        return box.x, box.y + box.h / 2
    if side == "right":
        return box.x + box.w, box.y + box.h / 2
    if side == "top":
        return box.x + box.w / 2, box.y
    return box.x + box.w / 2, box.y + box.h


def choose_sides(source: TableBox, target: TableBox) -> Tuple[str, str]:
    sx = source.x + source.w / 2
    sy = source.y + source.h / 2
    tx = target.x + target.w / 2
    ty = target.y + target.h / 2
    dx = tx - sx
    dy = ty - sy
    if abs(dx) >= abs(dy):
        return ("right", "left") if dx >= 0 else ("left", "right")
    return ("bottom", "top") if dy >= 0 else ("top", "bottom")


def shift_point(point: Tuple[float, float], side: str, distance: float) -> Tuple[float, float]:
    x, y = point
    if side == "left":
        return x - distance, y
    if side == "right":
        return x + distance, y
    if side == "top":
        return x, y - distance
    return x, y + distance


def orthogonal_points(start: Tuple[float, float], end: Tuple[float, float], side_a: str, side_b: str) -> List[Tuple[float, float]]:
    a1 = shift_point(start, side_a, 18)
    b1 = shift_point(end, side_b, 18)
    points = [start, a1]
    if side_a in {"left", "right"} and side_b in {"left", "right"}:
        mid_x = (a1[0] + b1[0]) / 2
        points.extend([(mid_x, a1[1]), (mid_x, b1[1])])
    elif side_a in {"top", "bottom"} and side_b in {"top", "bottom"}:
        mid_y = (a1[1] + b1[1]) / 2
        points.extend([(a1[0], mid_y), (b1[0], mid_y)])
    else:
        points.append((a1[0], b1[1]))
    points.extend([b1, end])
    deduped: List[Tuple[float, float]] = []
    for pt in points:
        if not deduped or deduped[-1] != pt:
            deduped.append(pt)
    return deduped


def crowfoot_svg(x: float, y: float, side: str) -> str:
    d = 10
    s = 6
    if side == "right":
        lines = [((x, y), (x + d, y)), ((x, y), (x + d, y - s)), ((x, y), (x + d, y + s))]
    elif side == "left":
        lines = [((x, y), (x - d, y)), ((x, y), (x - d, y - s)), ((x, y), (x - d, y + s))]
    elif side == "bottom":
        lines = [((x, y), (x, y + d)), ((x, y), (x - s, y + d)), ((x, y), (x + s, y + d))]
    else:
        lines = [((x, y), (x, y - d)), ((x, y), (x - s, y - d)), ((x, y), (x + s, y - d))]
    parts = []
    for (x1, y1), (x2, y2) in lines:
        parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{COLORS["line"]}" stroke-width="1.5" />'
        )
    return "".join(parts)


def one_bar_svg(x: float, y: float, side: str) -> str:
    d = 6
    if side in {"left", "right"}:
        x1, y1, x2, y2 = x, y - d, x, y + d
    else:
        x1, y1, x2, y2 = x - d, y, x + d, y
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{COLORS["line"]}" stroke-width="1.5" />'
    )


def key_icon_svg(x: float, y: float) -> str:
    parts = [
        f'<circle cx="{x + 6:.1f}" cy="{y:.1f}" r="4.2" fill="none" stroke="{COLORS["key"]}" stroke-width="1.6" />',
        f'<line x1="{x + 10.2:.1f}" y1="{y:.1f}" x2="{x + 20:.1f}" y2="{y:.1f}" stroke="{COLORS["key"]}" stroke-width="1.6" />',
        f'<line x1="{x + 16.2:.1f}" y1="{y:.1f}" x2="{x + 16.2:.1f}" y2="{y + 3.2:.1f}" stroke="{COLORS["key"]}" stroke-width="1.6" />',
        f'<line x1="{x + 19.2:.1f}" y1="{y:.1f}" x2="{x + 19.2:.1f}" y2="{y + 2.6:.1f}" stroke="{COLORS["key"]}" stroke-width="1.6" />',
        f'<text x="{x + 25:.1f}" y="{y + 3.5:.1f}" font-family="DejaVu Sans, Arial, sans-serif" font-size="9.5" font-weight="700" fill="{COLORS["key"]}">PK</text>',
    ]
    return "".join(parts)


def text_svg(
    x: float,
    y: float,
    content: str,
    size: float,
    fill: str,
    weight: str = "400",
    style: str = "normal",
    anchor: str = "start",
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-family="DejaVu Sans, Arial, sans-serif" font-size="{size}" '
        f'font-weight="{weight}" font-style="{style}" fill="{fill}">{html.escape(content)}</text>'
    )


def relation_paths(boxes: Dict[str, TableBox]) -> List[str]:
    segments: List[str] = []
    seen = set()
    for source_name, source_box in boxes.items():
        for field in source_box.table.fields:
            if not field.fk or field.fk not in boxes:
                continue
            key = (source_name, field.name, field.fk)
            if key in seen:
                continue
            seen.add(key)
            target_box = boxes[field.fk]
            side_a, side_b = choose_sides(source_box, target_box)
            start = field_anchor(source_box, field.name, side_a)
            end = box_anchor(target_box, side_b)
            points = orthogonal_points(start, end, side_a, side_b)
            point_text = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
            segments.append(
                f'<polyline points="{point_text}" fill="none" stroke="{COLORS["line"]}" '
                f'stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" />'
            )
            segments.append(crowfoot_svg(start[0], start[1], side_a))
            segments.append(one_bar_svg(end[0], end[1], side_b))
    return segments


def render_table(box: TableBox) -> str:
    parts = [
        f'<rect x="{box.x:.1f}" y="{box.y:.1f}" width="{box.w:.1f}" height="{box.h:.1f}" '
        f'rx="6" ry="6" fill="{COLORS["bg"]}" stroke="{COLORS["table_border"]}" stroke-width="1.2" />',
        f'<rect x="{box.x:.1f}" y="{box.y:.1f}" width="{box.w:.1f}" height="{box.header_h:.1f}" '
        f'rx="6" ry="6" fill="{COLORS["header"] if box.primary else COLORS["header_ref"]}" />',
        f'<rect x="{box.x:.1f}" y="{box.y + box.header_h - 6:.1f}" width="{box.w:.1f}" height="6" '
        f'fill="{COLORS["header"] if box.primary else COLORS["header_ref"]}" />',
        text_svg(box.x + box.w / 2, box.y + 20, box.table.name, HEADER_FONT, COLORS["header_text"], weight="700", anchor="middle"),
    ]
    split_x = box.x + box.w * (0.76 if not box.compact else 0.62)
    parts.append(
        f'<line x1="{split_x:.1f}" y1="{box.y + box.header_h:.1f}" x2="{split_x:.1f}" y2="{box.y + box.h:.1f}" '
        f'stroke="{COLORS["table_border"]}" stroke-width="1" />'
    )
    for idx, field in enumerate(box.table.fields):
        y = box.y + box.header_h + idx * box.row_h
        fill = COLORS["row_a"] if idx % 2 == 0 else COLORS["row_b"]
        parts.append(
            f'<rect x="{box.x:.1f}" y="{y:.1f}" width="{box.w:.1f}" height="{box.row_h:.1f}" '
            f'fill="{fill}" />'
        )
        parts.append(
            f'<line x1="{box.x:.1f}" y1="{y + box.row_h:.1f}" x2="{box.x + box.w:.1f}" y2="{y + box.row_h:.1f}" '
            f'stroke="{COLORS["table_border"]}" stroke-width="0.8" />'
        )
        baseline = y + 13.8
        left_x = box.x + 10
        if field.pk:
            parts.append(key_icon_svg(left_x, y + box.row_h / 2))
            left_x += 48
        label = field.name if not field.fk else f"{field.name} {ARROW} {field.fk}"
        parts.append(
            text_svg(
                left_x,
                baseline,
                label,
                FIELD_FONT,
                COLORS["fk"] if field.fk else COLORS["text"],
                weight="700" if field.pk else "400",
                style="italic" if field.fk else "normal",
            )
        )
        type_label = field.data_type + (" UNIQUE" if field.unique and not field.pk else "")
        parts.append(
            text_svg(
                split_x + 8,
                baseline,
                type_label,
                TYPE_FONT,
                COLORS["muted"],
                anchor="start",
            )
        )
    return "".join(parts)


def render_module(module: Module) -> Tuple[str, int, int]:
    boxes, width, height = compute_layout(module)
    width_i = int(math.ceil(width))
    height_i = int(math.ceil(height))
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width_i}" height="{height_i}" viewBox="0 0 {width_i} {height_i}">',
        f'<rect x="0" y="0" width="{width_i}" height="{height_i}" fill="{COLORS["bg"]}" />',
        text_svg(MARGIN_X, 34, module.title, TITLE_FONT, COLORS["text"], weight="700"),
        text_svg(
            MARGIN_X,
            58,
            f"{len(module.primary_tables)} tables shown. Compact reference anchors included for cross-module FK lines.",
            NOTE_FONT,
            COLORS["legend"],
        ),
        text_svg(width_i - MARGIN_X, 34, "Crow's foot notation | Gold PK | Blue italic FK", NOTE_FONT, COLORS["legend"], anchor="end"),
    ]
    parts.extend(relation_paths(boxes))
    for column in module.columns:
        for name in column:
            parts.append(render_table(boxes[name]))
    parts.append("</svg>")
    return "".join(parts), width_i, height_i


def rasterize(svg_text: str, svg_path: Path, png_path: Path, width: int, height: int) -> None:
    svg_path.write_text(svg_text, encoding="utf-8")
    cairosvg.svg2png(
        bytestring=svg_text.encode("utf-8"),
        write_to=str(png_path),
        output_width=width,
        output_height=height,
        background_color="white",
    )


def main() -> None:
    selected = {int(arg) for arg in sys.argv[1:]} if len(sys.argv) > 1 else None
    for module in MODULES:
        if selected and module.number not in selected:
            continue
        svg_text, width, height = render_module(module)
        stem = module.filename.rsplit(".", 1)[0]
        svg_path = TMP_DIR / f"{stem}.svg"
        png_path = OUT_DIR / module.filename
        rasterize(svg_text, svg_path, png_path, width, height)
        print(f"Generated {png_path.name} ({width}x{height})")


if __name__ == "__main__":
    main()
