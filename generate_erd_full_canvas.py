#!/usr/bin/env python3
"""Single-canvas ERD – all 67 tables on one image, matching Module 2-6 style."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Style constants ────────────────────────────────────────────────────────
C = {
    'hdr_bg':   '#1E2D3D',
    'hdr_txt':  '#FFFFFF',
    'pk_bg':    '#F6C90E',
    'pk_txt':   '#5C4500',
    'fk_txt':   '#1565C0',
    'norm_txt': '#1A202C',
    'type_txt': '#718096',
    'row_lt':   '#FFFFFF',
    'row_dk':   '#EDF2F7',
    'border':   '#CBD5E0',
    'bg':       '#FFFFFF',
    'title':    '#1A202C',
    'note':     '#718096',
    'rel_line': '#2B6CB0',
    'shadow':   '#C8D2DC',
}

TW   = 1.80   # table width (inches)
RH   = 0.121  # row height
HDR  = 0.170  # header height
GAP  = 0.24   # gap between tables in same column
CGAP = 0.36   # gap between columns

def tbl_h(n): return HDR + n * RH

def draw_table(ax, x, y_top, name, fields):
    n = len(fields)
    h = tbl_h(n)
    # shadow
    ax.add_patch(mpatches.FancyBboxPatch(
        (x+0.05, y_top-h-0.05), TW, h,
        boxstyle="square,pad=0", linewidth=0, facecolor=C['shadow'], zorder=1))
    # header
    ax.add_patch(mpatches.Rectangle(
        (x, y_top-HDR), TW, HDR,
        linewidth=0, facecolor=C['hdr_bg'], zorder=2))
    ax.text(x+TW/2, y_top-HDR/2, name,
            ha='center', va='center', fontsize=5.8, fontweight='bold',
            color=C['hdr_txt'], zorder=5)
    row_centers = {}
    for i, (fname, ftype, is_pk, is_fk, fk_tgt) in enumerate(fields):
        ry_top = y_top - HDR - i*RH
        ry_ctr = ry_top - RH/2
        ax.add_patch(mpatches.Rectangle(
            (x, ry_top-RH), TW, RH,
            linewidth=0,
            facecolor=C['row_lt'] if i%2==0 else C['row_dk'], zorder=2))
        ax.plot([x, x+TW], [ry_top, ry_top],
                color=C['border'], linewidth=0.18, zorder=3)
        row_centers[fname] = (x+TW/2, ry_ctr)
        if is_pk:
            ax.add_patch(mpatches.FancyBboxPatch(
                (x+0.025, ry_top-RH+0.013), 0.24, RH-0.026,
                boxstyle="round,pad=0.008",
                linewidth=0, facecolor=C['pk_bg'], zorder=3))
            ax.text(x+0.145, ry_ctr, 'PK',
                    ha='center', va='center', fontsize=3.8,
                    fontweight='bold', color=C['pk_txt'], zorder=5)
            ax.text(x+0.29, ry_ctr, fname,
                    ha='left', va='center', fontsize=4.6,
                    fontweight='bold', color=C['norm_txt'], zorder=5)
            ax.text(x+TW-0.04, ry_ctr, ftype,
                    ha='right', va='center', fontsize=3.8,
                    color=C['type_txt'], zorder=5)
        elif is_fk:
            ax.text(x+0.07, ry_ctr, fname,
                    ha='left', va='center', fontsize=4.5,
                    fontstyle='italic', color=C['fk_txt'], zorder=5)
            if fk_tgt:
                ax.text(x+TW-0.04, ry_ctr, f'→{fk_tgt}',
                        ha='right', va='center', fontsize=3.5,
                        color=C['fk_txt'], zorder=5)
        else:
            ax.text(x+0.07, ry_ctr, fname,
                    ha='left', va='center', fontsize=4.5,
                    color=C['norm_txt'], zorder=5)
            ax.text(x+TW-0.04, ry_ctr, ftype,
                    ha='right', va='center', fontsize=3.8,
                    color=C['type_txt'], zorder=5)
    ax.add_patch(mpatches.Rectangle(
        (x, y_top-h), TW, h,
        linewidth=0.7, edgecolor=C['border'], facecolor='none', zorder=4))
    return row_centers, (x, y_top, TW, h)


def draw_rel(ax, x1, y1, x2, y2):
    """Simple line with arrow at destination."""
    ax.annotate('',
        xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle='->', color=C['rel_line'],
            lw=0.55,
            mutation_scale=5,
            connectionstyle='arc3,rad=0.08'),
        zorder=0)


# ══════════════════════════════════════════════════════════════════════════════
# TABLE DATA
# ══════════════════════════════════════════════════════════════════════════════
T = {}

T['accounts_accounts'] = [
    ('accountID','int8',True,False,None),
    ('email','varchar',False,False,None),
    ('password','varchar',False,False,None),
    ('is_active','bool',False,False,None),
    ('is_staff','bool',False,False,None),
    ('is_superuser','bool',False,False,None),
    ('isVerified','bool',False,False,None),
    ('KYCVerified','bool',False,False,None),
    ('verification_level','int4',False,False,None),
    ('city','varchar',False,False,None),
    ('country','varchar',False,False,None),
    ('postal_code','varchar',False,False,None),
    ('province','varchar',False,False,None),
    ('street_address','varchar',False,False,None),
    ('barangay','varchar',False,False,None),
    ('verifyToken','varchar',False,False,None),
    ('verifyTokenExpiry','timestamptz',False,False,None),
    ('email_otp','varchar',False,False,None),
    ('email_otp_attempts','int4',False,False,None),
    ('email_otp_expiry','timestamptz',False,False,None),
    ('is_banned','bool',False,False,None),
    ('banned_at','timestamptz',False,False,None),
    ('banned_reason','text',False,False,None),
    ('is_suspended','bool',False,False,None),
    ('suspended_reason','text',False,False,None),
    ('suspended_until','timestamptz',False,False,None),
    ('auth_revoked_at','timestamptz',False,False,None),
    ('last_login','timestamptz',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('banned_by_id','int8',False,True,'accounts_accounts'),
]

T['account_emailaddress'] = [
    ('id','int4',True,False,None),
    ('email','varchar',False,False,None),
    ('verified','bool',False,False,None),
    ('primary','bool',False,False,None),
    ('user_id','int8',False,True,'accounts_accounts'),
]

T['account_emailconfirmation'] = [
    ('id','int4',True,False,None),
    ('created','timestamptz',False,False,None),
    ('sent','timestamptz',False,False,None),
    ('key','varchar',False,False,None),
    ('email_address_id','int4',False,True,'account_emailaddress'),
]

T['socialaccount_socialaccount'] = [
    ('id','int4',True,False,None),
    ('provider','varchar',False,False,None),
    ('uid','varchar',False,False,None),
    ('last_login','timestamptz',False,False,None),
    ('date_joined','timestamptz',False,False,None),
    ('extra_data','jsonb',False,False,None),
    ('user_id','int8',False,True,'accounts_accounts'),
]

T['socialaccount_socialapp'] = [
    ('id','int4',True,False,None),
    ('provider','varchar',False,False,None),
    ('name','varchar',False,False,None),
    ('client_id','varchar',False,False,None),
    ('secret','varchar',False,False,None),
    ('key','varchar',False,False,None),
    ('provider_id','varchar',False,False,None),
    ('settings','jsonb',False,False,None),
]

T['socialaccount_socialtoken'] = [
    ('id','int4',True,False,None),
    ('token','text',False,False,None),
    ('token_secret','text',False,False,None),
    ('expires_at','timestamptz',False,False,None),
    ('account_id','int4',False,True,'socialaccount_socialaccount'),
    ('app_id','int4',False,True,'socialaccount_socialapp'),
]

T['accounts_profile'] = [
    ('profileID','int8',True,False,None),
    ('profileImg','varchar',False,False,None),
    ('firstName','varchar',False,False,None),
    ('lastName','varchar',False,False,None),
    ('middleName','varchar',False,False,None),
    ('contactNum','varchar',False,False,None),
    ('birthDate','date',False,False,None),
    ('profileType','varchar',False,False,None),
    ('latitude','numeric',False,False,None),
    ('longitude','numeric',False,False,None),
    ('location_sharing_enabled','bool',False,False,None),
    ('location_updated_at','timestamptz',False,False,None),
    ('accountFK_id','int8',False,True,'accounts_accounts'),
]

T['accounts_workerprofile'] = [
    ('id','int8',True,False,None),
    ('description','varchar',False,False,None),
    ('workerRating','int4',False,False,None),
    ('totalEarningGross','numeric',False,False,None),
    ('availability_status','varchar',False,False,None),
    ('bio','varchar',False,False,None),
    ('hourly_rate','numeric',False,False,None),
    ('daily_rate','numeric',False,False,None),
    ('profile_completion_percentage','int4',False,False,None),
    ('soft_skills','text',False,False,None),
    ('is_available_daily_jobs','bool',False,False,None),
    ('profileID_id','int8',False,True,'accounts_profile'),
]

T['accounts_clientprofile'] = [
    ('id','int8',True,False,None),
    ('description','varchar',False,False,None),
    ('totalJobsPosted','int4',False,False,None),
    ('clientRating','int4',False,False,None),
    ('activeJobsCount','int4',False,False,None),
    ('profileID_id','int8',False,True,'accounts_profile'),
]

T['accounts_agency'] = [
    ('agencyId','int8',True,False,None),
    ('businessName','varchar',False,False,None),
    ('businessDesc','varchar',False,False,None),
    ('contactNumber','varchar',False,False,None),
    ('city','varchar',False,False,None),
    ('country','varchar',False,False,None),
    ('postal_code','varchar',False,False,None),
    ('province','varchar',False,False,None),
    ('street_address','varchar',False,False,None),
    ('barangay','varchar',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('accountFK_id','int8',False,True,'accounts_accounts'),
]

T['accounts_barangay'] = [
    ('barangayID','int4',True,False,None),
    ('name','varchar',False,False,None),
    ('zipCode','varchar',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('city_id','int4',False,True,'accounts_city'),
]

T['accounts_city'] = [
    ('cityID','int4',True,False,None),
    ('name','varchar',False,False,None),
    ('province','varchar',False,False,None),
    ('region','varchar',False,False,None),
    ('zipCode','varchar',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
]

T['specializations'] = [
    ('specializationID','int8',True,False,None),
    ('specializationName','varchar',False,False,None),
    ('averageProjectCostMax','numeric',False,False,None),
    ('averageProjectCostMin','numeric',False,False,None),
    ('description','text',False,False,None),
    ('minimumRate','numeric',False,False,None),
    ('rateType','varchar',False,False,None),
    ('skillLevel','varchar',False,False,None),
    ('is_custom','bool',False,False,None),
    ('created_by_agency_id','int8',False,True,'accounts_agency'),
    ('created_by_worker_id','int8',False,True,'accounts_accounts'),
]

T['accounts_workerspecialization'] = [
    ('id','int8',True,False,None),
    ('experienceYears','int4',False,False,None),
    ('certification','varchar',False,False,None),
    ('skillType','varchar',False,False,None),
    ('displayOrder','int4',False,False,None),
    ('workerID_id','int8',False,True,'accounts_workerprofile'),
    ('specializationID_id','int8',False,True,'specializations'),
]

T['accounts_interestedjobs'] = [
    ('id','int8',True,False,None),
    ('clientID_id','int8',False,True,'accounts_clientprofile'),
    ('specializationID_id','int8',False,True,'specializations'),
]

T['accounts_wallet'] = [
    ('walletID','int8',True,False,None),
    ('balance','numeric',False,False,None),
    ('reservedBalance','numeric',False,False,None),
    ('pendingEarnings','numeric',False,False,None),
    ('autoWithdrawEnabled','bool',False,False,None),
    ('lastAutoWithdrawAt','timestamptz',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('accountFK_id','int8',False,True,'accounts_accounts'),
    ('preferredPaymentMethodID_id','int8',False,True,'accounts_userpaymentmethod'),
]

T['accounts_userpaymentmethod'] = [
    ('id','int8',True,False,None),
    ('methodType','varchar',False,False,None),
    ('accountName','varchar',False,False,None),
    ('accountNumber','varchar',False,False,None),
    ('bankName','varchar',False,False,None),
    ('bankCode','varchar',False,False,None),
    ('isPrimary','bool',False,False,None),
    ('isVerified','bool',False,False,None),
    ('paymongoRecipientId','varchar',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('accountFK_id','int8',False,True,'accounts_accounts'),
]

T['accounts_pushtoken'] = [
    ('tokenID','int8',True,False,None),
    ('pushToken','varchar',False,False,None),
    ('deviceType','varchar',False,False,None),
    ('isActive','bool',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('lastUsed','timestamptz',False,False,None),
    ('accountFK_id','int8',False,True,'accounts_accounts'),
]

T['accounts_notificationsettings'] = [
    ('settingsID','int8',True,False,None),
    ('pushEnabled','bool',False,False,None),
    ('soundEnabled','bool',False,False,None),
    ('jobUpdates','bool',False,False,None),
    ('messages','bool',False,False,None),
    ('payments','bool',False,False,None),
    ('reviews','bool',False,False,None),
    ('kycUpdates','bool',False,False,None),
    ('doNotDisturbStart','time',False,False,None),
    ('doNotDisturbEnd','time',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('accountFK_id','int8',False,True,'accounts_accounts'),
]

T['accounts_notification'] = [
    ('notificationID','int8',True,False,None),
    ('notificationType','varchar',False,False,None),
    ('title','varchar',False,False,None),
    ('message','text',False,False,None),
    ('isRead','bool',False,False,None),
    ('profile_type','varchar',False,False,None),
    ('relatedJobID','int8',False,False,None),
    ('relatedApplicationID','int8',False,False,None),
    ('relatedKYCLogID','int8',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('readAt','timestamptz',False,False,None),
    ('accountFK_id','int8',False,True,'accounts_accounts'),
]

T['accounts_transaction'] = [
    ('transactionID','int8',True,False,None),
    ('transactionType','varchar',False,False,None),
    ('amount','numeric',False,False,None),
    ('balanceAfter','numeric',False,False,None),
    ('status','varchar',False,False,None),
    ('description','varchar',False,False,None),
    ('referenceNumber','varchar',False,False,None),
    ('paymentMethod','varchar',False,False,None),
    ('adminReferenceNumber','varchar',False,False,None),
    ('invoiceURL','varchar',False,False,None),
    ('xenditExternalID','varchar',False,False,None),
    ('xenditInvoiceID','varchar',False,False,None),
    ('xenditPaymentChannel','varchar',False,False,None),
    ('xenditPaymentID','varchar',False,False,None),
    ('xenditPaymentMethod','varchar',False,False,None),
    ('paymongoPaymentId','varchar',False,False,None),
    ('paymongoTransferId','varchar',False,False,None),
    ('paymongoTransferStatus','varchar',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('completedAt','timestamptz',False,False,None),
    ('processedAt','timestamptz',False,False,None),
    ('walletID_id','int8',False,True,'accounts_wallet'),
    ('relatedJobPosting_id','int8',False,True,'jobs'),
    ('processedByAdmin_id','int8',False,True,'accounts_accounts'),
]

T['accounts_kyc'] = [
    ('kycID','int8',True,False,None),
    ('kyc_status','varchar',False,False,None),
    ('rejectionCategory','varchar',False,False,None),
    ('rejectionReason','text',False,False,None),
    ('notes','text',False,False,None),
    ('resubmissionCount','int4',False,False,None),
    ('maxResubmissions','int4',False,False,None),
    ('reviewedAt','timestamptz',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('accountFK_id','int8',False,True,'accounts_accounts'),
    ('reviewedBy_id','int8',False,True,'accounts_accounts'),
]

T['accounts_kycfiles'] = [
    ('kycFileID','int8',True,False,None),
    ('idType','varchar',False,False,None),
    ('fileURL','varchar',False,False,None),
    ('fileName','varchar',False,False,None),
    ('fileSize','int4',False,False,None),
    ('uploadedAt','timestamptz',False,False,None),
    ('ai_verification_status','varchar',False,False,None),
    ('face_detected','bool',False,False,None),
    ('face_count','int4',False,False,None),
    ('face_confidence','float8',False,False,None),
    ('ocr_text','text',False,False,None),
    ('ocr_confidence','float8',False,False,None),
    ('quality_score','float8',False,False,None),
    ('ai_confidence_score','float8',False,False,None),
    ('ai_rejection_reason','varchar',False,False,None),
    ('ai_rejection_message','varchar',False,False,None),
    ('ai_warnings','jsonb',False,False,None),
    ('ai_details','jsonb',False,False,None),
    ('verified_at','timestamptz',False,False,None),
    ('kycID_id','int8',False,True,'accounts_kyc'),
]

T['kyc_extracted_data'] = [
    ('extractedDataID','int8',True,False,None),
    ('extracted_full_name','varchar',False,False,None),
    ('extracted_first_name','varchar',False,False,None),
    ('extracted_middle_name','varchar',False,False,None),
    ('extracted_last_name','varchar',False,False,None),
    ('extracted_birth_date','date',False,False,None),
    ('extracted_address','text',False,False,None),
    ('extracted_id_number','varchar',False,False,None),
    ('extracted_id_type','varchar',False,False,None),
    ('extracted_expiry_date','date',False,False,None),
    ('extracted_nationality','varchar',False,False,None),
    ('extracted_sex','varchar',False,False,None),
    ('extracted_place_of_birth','varchar',False,False,None),
    ('extracted_clearance_number','varchar',False,False,None),
    ('extracted_clearance_type','varchar',False,False,None),
    ('extracted_clearance_issue_date','date',False,False,None),
    ('extracted_clearance_validity_date','date',False,False,None),
    ('confirmed_full_name','varchar',False,False,None),
    ('confirmed_first_name','varchar',False,False,None),
    ('confirmed_middle_name','varchar',False,False,None),
    ('confirmed_last_name','varchar',False,False,None),
    ('confirmed_birth_date','date',False,False,None),
    ('confirmed_address','text',False,False,None),
    ('confirmed_id_number','varchar',False,False,None),
    ('confirmed_nationality','varchar',False,False,None),
    ('confirmed_sex','varchar',False,False,None),
    ('confirmed_place_of_birth','varchar',False,False,None),
    ('confirmed_clearance_number','varchar',False,False,None),
    ('confirmed_clearance_type','varchar',False,False,None),
    ('confirmed_clearance_issue_date','date',False,False,None),
    ('confirmed_clearance_validity_date','date',False,False,None),
    ('confidence_full_name','float8',False,False,None),
    ('confidence_birth_date','float8',False,False,None),
    ('confidence_address','float8',False,False,None),
    ('confidence_id_number','float8',False,False,None),
    ('confidence_place_of_birth','float8',False,False,None),
    ('confidence_clearance_number','float8',False,False,None),
    ('overall_confidence','float8',False,False,None),
    ('extraction_status','varchar',False,False,None),
    ('extraction_source','varchar',False,False,None),
    ('face_match_completed','bool',False,False,None),
    ('face_match_score','float8',False,False,None),
    ('raw_extraction_data','jsonb',False,False,None),
    ('user_edited_fields','jsonb',False,False,None),
    ('extracted_at','timestamptz',False,False,None),
    ('confirmed_at','timestamptz',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('kycID_id','int8 UNIQUE',False,True,'accounts_kyc'),
]

T['agency_agencykyc'] = [
    ('agencyKycID','int8',True,False,None),
    ('status','varchar',False,False,None),
    ('rejectionCategory','varchar',False,False,None),
    ('rejectionReason','text',False,False,None),
    ('notes','varchar',False,False,None),
    ('resubmissionCount','int4',False,False,None),
    ('maxResubmissions','int4',False,False,None),
    ('face_similarity_score','float8',False,False,None),
    ('reviewedAt','timestamptz',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('accountFK_id','int8',False,True,'accounts_accounts'),
    ('reviewedBy_id','int8',False,True,'accounts_accounts'),
]

T['agency_agencykycfile'] = [
    ('fileID','int8',True,False,None),
    ('fileType','varchar',False,False,None),
    ('fileURL','varchar',False,False,None),
    ('fileName','varchar',False,False,None),
    ('fileSize','int4',False,False,None),
    ('uploadedAt','timestamptz',False,False,None),
    ('ai_verification_status','varchar',False,False,None),
    ('face_detected','bool',False,False,None),
    ('face_count','int4',False,False,None),
    ('face_confidence','float8',False,False,None),
    ('ocr_text','text',False,False,None),
    ('ocr_confidence','float8',False,False,None),
    ('quality_score','float8',False,False,None),
    ('ai_confidence_score','float8',False,False,None),
    ('ai_rejection_reason','varchar',False,False,None),
    ('ai_rejection_message','varchar',False,False,None),
    ('ai_warnings','jsonb',False,False,None),
    ('ai_details','jsonb',False,False,None),
    ('verified_at','timestamptz',False,False,None),
    ('agencyKyc_id','int8',False,True,'agency_agencykyc'),
]

T['agency_kyc_extracted_data'] = [
    ('extractedDataID','int8',True,False,None),
    ('extracted_business_name','varchar',False,False,None),
    ('extracted_business_type','varchar',False,False,None),
    ('extracted_business_address','text',False,False,None),
    ('extracted_permit_number','varchar',False,False,None),
    ('extracted_permit_issue_date','date',False,False,None),
    ('extracted_permit_expiry_date','date',False,False,None),
    ('extracted_dti_number','varchar',False,False,None),
    ('extracted_sec_number','varchar',False,False,None),
    ('extracted_tin','varchar',False,False,None),
    ('extracted_rep_full_name','varchar',False,False,None),
    ('extracted_rep_id_number','varchar',False,False,None),
    ('extracted_rep_id_type','varchar',False,False,None),
    ('extracted_rep_birth_date','date',False,False,None),
    ('extracted_rep_address','text',False,False,None),
    ('confirmed_business_name','varchar',False,False,None),
    ('confirmed_business_type','varchar',False,False,None),
    ('confirmed_business_address','text',False,False,None),
    ('confirmed_permit_number','varchar',False,False,None),
    ('confirmed_permit_issue_date','date',False,False,None),
    ('confirmed_permit_expiry_date','date',False,False,None),
    ('confirmed_dti_number','varchar',False,False,None),
    ('confirmed_sec_number','varchar',False,False,None),
    ('confirmed_tin','varchar',False,False,None),
    ('confirmed_rep_full_name','varchar',False,False,None),
    ('confirmed_rep_id_number','varchar',False,False,None),
    ('confirmed_rep_birth_date','date',False,False,None),
    ('confirmed_rep_address','text',False,False,None),
    ('confidence_business_name','float8',False,False,None),
    ('confidence_business_address','float8',False,False,None),
    ('confidence_permit_number','float8',False,False,None),
    ('confidence_rep_name','float8',False,False,None),
    ('overall_confidence','float8',False,False,None),
    ('extraction_status','varchar',False,False,None),
    ('extraction_source','varchar',False,False,None),
    ('raw_extraction_data','jsonb',False,False,None),
    ('user_edited_fields','jsonb',False,False,None),
    ('extracted_at','timestamptz',False,False,None),
    ('confirmed_at','timestamptz',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('agencyKyc_id','int8 UNIQUE',False,True,'agency_agencykyc'),
]

T['adminpanel_kyclogs'] = [
    ('kycLogID','int8',True,False,None),
    ('action','varchar',False,False,None),
    ('kycType','varchar',False,False,None),
    ('kycID','int8',False,False,None),
    ('userEmail','varchar',False,False,None),
    ('userAccountID','int8',False,False,None),
    ('reason','text',False,False,None),
    ('reviewedAt','timestamptz',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('accountFK_id','int8',False,True,'accounts_accounts'),
    ('reviewedBy_id','int8',False,True,'accounts_accounts'),
]

T['adminpanel_adminaccount'] = [
    ('adminID','int8',True,False,None),
    ('role','varchar',False,False,None),
    ('permissions','jsonb',False,False,None),
    ('isActive','bool',False,False,None),
    ('lastLogin','timestamptz',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('accountFK_id','int8 UNIQUE',False,True,'accounts_accounts'),
]

T['adminpanel_auditlog'] = [
    ('auditLogID','int8',True,False,None),
    ('adminEmail','varchar',False,False,None),
    ('action','varchar',False,False,None),
    ('entityType','varchar',False,False,None),
    ('entityID','varchar',False,False,None),
    ('details','jsonb',False,False,None),
    ('beforeValue','jsonb',False,False,None),
    ('afterValue','jsonb',False,False,None),
    ('ipAddress','inet',False,False,None),
    ('userAgent','text',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('adminFK_id','int8',False,True,'accounts_accounts'),
]

T['adminpanel_supportticket'] = [
    ('ticketID','int8',True,False,None),
    ('subject','varchar',False,False,None),
    ('category','varchar',False,False,None),
    ('priority','varchar',False,False,None),
    ('status','varchar',False,False,None),
    ('ticketType','varchar',False,False,None),
    ('platform','varchar',False,False,None),
    ('deviceInfo','text',False,False,None),
    ('appVersion','varchar',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('lastReplyAt','timestamptz',False,False,None),
    ('resolvedAt','timestamptz',False,False,None),
    ('userFK_id','int8',False,True,'accounts_accounts'),
    ('assignedTo_id','int8',False,True,'accounts_accounts'),
    ('agencyFK_id','int8',False,True,'accounts_agency'),
]

T['adminpanel_supportticketreply'] = [
    ('replyID','int8',True,False,None),
    ('content','text',False,False,None),
    ('isSystemMessage','bool',False,False,None),
    ('attachmentURL','varchar',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('ticketFK_id','int8',False,True,'adminpanel_supportticket'),
    ('senderFK_id','int8',False,True,'accounts_accounts'),
]

T['adminpanel_userreport'] = [
    ('reportID','int8',True,False,None),
    ('reportType','varchar',False,False,None),
    ('reason','varchar',False,False,None),
    ('description','text',False,False,None),
    ('relatedContentID','int8',False,False,None),
    ('status','varchar',False,False,None),
    ('adminNotes','text',False,False,None),
    ('actionTaken','varchar',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('resolvedAt','timestamptz',False,False,None),
    ('reporterFK_id','int8',False,True,'accounts_accounts'),
    ('reportedUserFK_id','int8',False,True,'accounts_accounts'),
    ('reviewedBy_id','int8',False,True,'accounts_accounts'),
]

T['adminpanel_platformsettings'] = [
    ('settingsID','int8',True,False,None),
    ('platformFeePercentage','numeric',False,False,None),
    ('escrowHoldingDays','int4',False,False,None),
    ('maxJobBudget','numeric',False,False,None),
    ('minJobBudget','numeric',False,False,None),
    ('workerVerificationRequired','bool',False,False,None),
    ('autoApproveKYC','bool',False,False,None),
    ('kycDocumentExpiryDays','int4',False,False,None),
    ('maintenanceMode','bool',False,False,None),
    ('sessionTimeoutMinutes','int4',False,False,None),
    ('maxUploadSizeMB','int4',False,False,None),
    ('kycAutoApproveMinConfidence','numeric',False,False,None),
    ('kycFaceMatchMinSimilarity','numeric',False,False,None),
    ('kycRequireUserConfirmation','bool',False,False,None),
    ('lastUpdated','timestamptz',False,False,None),
    ('updatedBy_id','int8',False,True,'accounts_accounts'),
]

T['adminpanel_cannedresponse'] = [
    ('responseID','int8',True,False,None),
    ('title','varchar',False,False,None),
    ('content','text',False,False,None),
    ('category','varchar',False,False,None),
    ('shortcuts','jsonb',False,False,None),
    ('usageCount','int4',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('createdBy_id','int8',False,True,'accounts_accounts'),
]

T['adminpanel_contentmoderationterm'] = [
    ('termID','int8',True,False,None),
    ('term','varchar',False,False,None),
    ('normalizedTerm','varchar',False,False,None),
    ('isActive','bool',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('createdBy_id','int8',False,True,'accounts_accounts'),
    ('updatedBy_id','int8',False,True,'accounts_accounts'),
]

T['adminpanel_faq'] = [
    ('faqID','int8',True,False,None),
    ('question','varchar',False,False,None),
    ('answer','text',False,False,None),
    ('category','varchar',False,False,None),
    ('sortOrder','int4',False,False,None),
    ('viewCount','int4',False,False,None),
    ('isPublished','bool',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
]

T['adminpanel_systemroles'] = [
    ('systemRoleID','int8',True,False,None),
    ('systemRole','varchar',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('accountID_id','int8',False,True,'accounts_accounts'),
]

T['jobs'] = [
    ('jobID','int8',True,False,None),
    ('title','varchar',False,False,None),
    ('description','text',False,False,None),
    ('budget','numeric',False,False,None),
    ('location','varchar',False,False,None),
    ('expectedDuration','varchar',False,False,None),
    ('urgency','varchar',False,False,None),
    ('preferredStartDate','date',False,False,None),
    ('materialsNeeded','jsonb',False,False,None),
    ('status','varchar',False,False,None),
    ('jobType','varchar',False,False,None),
    ('is_team_job','bool',False,False,None),
    ('budget_allocation_type','varchar',False,False,None),
    ('team_job_start_threshold','numeric',False,False,None),
    ('job_scope','varchar',False,False,None),
    ('skill_level_required','varchar',False,False,None),
    ('work_environment','varchar',False,False,None),
    ('payment_model','varchar',False,False,None),
    ('shift_type','varchar',False,False,None),
    ('duration_days','int4',False,False,None),
    ('daily_rate_agreed','numeric',False,False,None),
    ('actual_start_date','date',False,False,None),
    ('total_days_worked','int4',False,False,None),
    ('daily_escrow_total','numeric',False,False,None),
    ('scheduled_end_date','date',False,False,None),
    ('escrowAmount','numeric',False,False,None),
    ('escrowPaid','bool',False,False,None),
    ('escrowPaidAt','timestamptz',False,False,None),
    ('remainingPayment','numeric',False,False,None),
    ('remainingPaymentPaid','bool',False,False,None),
    ('remainingPaymentPaidAt','timestamptz',False,False,None),
    ('finalPaymentMethod','varchar',False,False,None),
    ('cashPaymentProofUrl','varchar',False,False,None),
    ('paymentMethodSelectedAt','timestamptz',False,False,None),
    ('cashProofUploadedAt','timestamptz',False,False,None),
    ('cashPaymentApproved','bool',False,False,None),
    ('cashPaymentApprovedAt','timestamptz',False,False,None),
    ('paymentReleaseDate','timestamptz',False,False,None),
    ('paymentReleasedToWorker','bool',False,False,None),
    ('paymentReleasedAt','timestamptz',False,False,None),
    ('paymentHeldReason','varchar',False,False,None),
    ('materialsCost','numeric',False,False,None),
    ('materials_status','varchar',False,False,None),
    ('qa_day_offset','int4',False,False,None),
    ('clientMarkedComplete','bool',False,False,None),
    ('clientMarkedCompleteAt','timestamptz',False,False,None),
    ('workerMarkedComplete','bool',False,False,None),
    ('workerMarkedCompleteAt','timestamptz',False,False,None),
    ('workerMarkedOnTheWay','bool',False,False,None),
    ('workerMarkedOnTheWayAt','timestamptz',False,False,None),
    ('workerMarkedJobStarted','bool',False,False,None),
    ('workerMarkedJobStartedAt','timestamptz',False,False,None),
    ('clientConfirmedWorkStarted','bool',False,False,None),
    ('clientConfirmedWorkStartedAt','timestamptz',False,False,None),
    ('is_early_completed','bool',False,False,None),
    ('early_completed_at','timestamptz',False,False,None),
    ('early_completion_payout','numeric',False,False,None),
    ('inviteStatus','varchar',False,False,None),
    ('inviteRejectionReason','text',False,False,None),
    ('inviteRespondedAt','timestamptz',False,False,None),
    ('assignmentNotes','text',False,False,None),
    ('employeeAssignedAt','timestamptz',False,False,None),
    ('cancelledAt','timestamptz',False,False,None),
    ('cancelledByRole','varchar',False,False,None),
    ('cancellationStage','varchar',False,False,None),
    ('cancellationReason','text',False,False,None),
    ('clientRefundAmount','numeric',False,False,None),
    ('workerCompensationAmount','numeric',False,False,None),
    ('agency_flow_mode','varchar',False,False,None),
    ('completedAt','timestamptz',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('clientID_id','int8',False,True,'accounts_clientprofile'),
    ('assignedWorkerID_id','int8',False,True,'accounts_workerprofile'),
    ('assignedAgencyFK_id','int8',False,True,'accounts_agency'),
    ('assignedEmployeeID_id','int8',False,True,'agency_employees'),
    ('categoryID_id','int8',False,True,'specializations'),
    ('cancelledByAccountID_id','int8',False,True,'accounts_accounts'),
    ('cashPaymentApprovedBy_id','int8',False,True,'accounts_accounts'),
]

T['job_skill_slots'] = [
    ('skillSlotID','int8',True,False,None),
    ('workers_needed','int4',False,False,None),
    ('budget_allocated','numeric',False,False,None),
    ('skill_level_required','varchar',False,False,None),
    ('status','varchar',False,False,None),
    ('notes','text',False,False,None),
    ('agency_invite_status','varchar',False,False,None),
    ('agency_invite_responded_at','timestamptz',False,False,None),
    ('last_rejected_agency_id','int8',False,False,None),
    ('last_rejected_agency_name','varchar',False,False,None),
    ('last_rejected_at','timestamptz',False,False,None),
    ('last_rejection_reason','text',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('jobID_id','int8',False,True,'jobs'),
    ('specializationID_id','int8',False,True,'specializations'),
    ('invited_agency_id','int8',False,True,'accounts_agency'),
]

T['job_applications'] = [
    ('applicationID','int8',True,False,None),
    ('proposalMessage','text',False,False,None),
    ('proposedBudget','numeric',False,False,None),
    ('estimatedDuration','varchar',False,False,None),
    ('budgetOption','varchar',False,False,None),
    ('status','varchar',False,False,None),
    ('selected_materials','jsonb',False,False,None),
    ('proposed_daily_rate','numeric',False,False,None),
    ('proposed_days','int4',False,False,None),
    ('negotiation_count','int2',False,False,None),
    ('applied_shift','varchar',False,False,None),
    ('clientRejectionReason','text',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('jobID_id','int8',False,True,'jobs'),
    ('workerID_id','int8',False,True,'accounts_workerprofile'),
    ('applied_skill_slot_id','int8',False,True,'job_skill_slots'),
]

T['price_negotiations'] = [
    ('negotiationID','int8',True,False,None),
    ('actor','varchar',False,False,None),
    ('round_number','int2',False,False,None),
    ('proposed_budget','numeric',False,False,None),
    ('proposed_daily_rate','numeric',False,False,None),
    ('proposed_days','int4',False,False,None),
    ('message','text',False,False,None),
    ('status','varchar',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('application_id','int8',False,True,'job_applications'),
]

T['job_worker_assignments'] = [
    ('assignmentID','int8',True,False,None),
    ('slot_position','int4',False,False,None),
    ('assignment_status','varchar',False,False,None),
    ('worker_marked_complete','bool',False,False,None),
    ('worker_marked_complete_at','timestamptz',False,False,None),
    ('completion_notes','text',False,False,None),
    ('individual_rating','numeric',False,False,None),
    ('client_confirmed_arrival','bool',False,False,None),
    ('client_confirmed_arrival_at','timestamptz',False,False,None),
    ('daily_rate_at_assignment','numeric',False,False,None),
    ('days_worked','int4',False,False,None),
    ('total_earned','numeric',False,False,None),
    ('early_completed','bool',False,False,None),
    ('early_completed_at','timestamptz',False,False,None),
    ('early_completion_payout','numeric',False,False,None),
    ('assigned_shift','varchar',False,False,None),
    ('assignedAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('jobID_id','int8',False,True,'jobs'),
    ('skillSlotID_id','int8',False,True,'job_skill_slots'),
    ('workerID_id','int8',False,True,'accounts_workerprofile'),
]

T['job_employee_assignments'] = [
    ('assignmentID','int8',True,False,None),
    ('assignedAt','timestamptz',False,False,None),
    ('notes','text',False,False,None),
    ('isPrimaryContact','bool',False,False,None),
    ('status','varchar',False,False,None),
    ('dispatched','bool',False,False,None),
    ('dispatchedAt','timestamptz',False,False,None),
    ('clientConfirmedArrival','bool',False,False,None),
    ('clientConfirmedArrivalAt','timestamptz',False,False,None),
    ('employeeMarkedComplete','bool',False,False,None),
    ('employeeMarkedCompleteAt','timestamptz',False,False,None),
    ('agencyMarkedComplete','bool',False,False,None),
    ('agencyMarkedCompleteAt','timestamptz',False,False,None),
    ('completionNotes','text',False,False,None),
    ('paymentAmount','numeric',False,False,None),
    ('clientApproved','bool',False,False,None),
    ('clientApprovedAt','timestamptz',False,False,None),
    ('early_completed','bool',False,False,None),
    ('early_completed_at','timestamptz',False,False,None),
    ('early_completion_payout','numeric',False,False,None),
    ('job_id','int8',False,True,'jobs'),
    ('employee_id','int8',False,True,'agency_employees'),
    ('skill_slot_id','int8',False,True,'job_skill_slots'),
    ('assignedBy_id','int8',False,True,'accounts_accounts'),
]

T['job_logs'] = [
    ('logID','int8',True,False,None),
    ('actionType','varchar',False,False,None),
    ('oldStatus','varchar',False,False,None),
    ('newStatus','varchar',False,False,None),
    ('notes','text',False,False,None),
    ('metadata','jsonb',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('jobID_id','int8',False,True,'jobs'),
    ('changedBy_id','int8',False,True,'accounts_accounts'),
]

T['saved_jobs'] = [
    ('savedJobID','int8',True,False,None),
    ('savedAt','timestamptz',False,False,None),
    ('jobID_id','int8',False,True,'jobs'),
    ('workerID_id','int8',False,True,'accounts_workerprofile'),
]

T['job_disputes'] = [
    ('disputeID','int8',True,False,None),
    ('disputedBy','varchar',False,False,None),
    ('reason','varchar',False,False,None),
    ('description','text',False,False,None),
    ('status','varchar',False,False,None),
    ('priority','varchar',False,False,None),
    ('jobAmount','numeric',False,False,None),
    ('disputedAmount','numeric',False,False,None),
    ('resolution','text',False,False,None),
    ('resolvedDate','timestamptz',False,False,None),
    ('assignedTo','varchar',False,False,None),
    ('openedDate','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('backjobStarted','bool',False,False,None),
    ('backjobStartedAt','timestamptz',False,False,None),
    ('clientConfirmedBackjob','bool',False,False,None),
    ('clientConfirmedBackjobAt','timestamptz',False,False,None),
    ('workerMarkedBackjobComplete','bool',False,False,None),
    ('workerMarkedBackjobCompleteAt','timestamptz',False,False,None),
    ('termsAccepted','bool',False,False,None),
    ('termsVersion','varchar',False,False,None),
    ('termsAcceptedAt','timestamptz',False,False,None),
    ('adminRejectedAt','timestamptz',False,False,None),
    ('adminRejectionReason','text',False,False,None),
    ('in_negotiation_at','timestamptz',False,False,None),
    ('scheduled_date','date',False,False,None),
    ('workerScheduleConfirmed','bool',False,False,None),
    ('workerScheduleConfirmedAt','timestamptz',False,False,None),
    ('jobID_id','int8',False,True,'jobs'),
]

T['dispute_evidence'] = [
    ('evidenceID','int8',True,False,None),
    ('imageURL','varchar',False,False,None),
    ('description','text',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('disputeID_id','int8',False,True,'job_disputes'),
    ('uploadedBy_id','int8',False,True,'accounts_accounts'),
]

T['backjob_schedule_confirmations'] = [
    ('confirmationID','int8',True,False,None),
    ('confirmed','bool',False,False,None),
    ('confirmedAt','timestamptz',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('disputeID_id','int8',False,True,'job_disputes'),
    ('assignmentID_id','int8',False,True,'job_worker_assignments'),
    ('confirmedBy_id','int8',False,True,'accounts_accounts'),
]

T['job_reviews'] = [
    ('reviewID','int8',True,False,None),
    ('reviewerType','varchar',False,False,None),
    ('rating','numeric',False,False,None),
    ('comment','text',False,False,None),
    ('status','varchar',False,False,None),
    ('isFlagged','bool',False,False,None),
    ('flagReason','text',False,False,None),
    ('flaggedAt','timestamptz',False,False,None),
    ('helpfulCount','int4',False,False,None),
    ('rating_communication','numeric',False,False,None),
    ('rating_professionalism','numeric',False,False,None),
    ('rating_punctuality','numeric',False,False,None),
    ('rating_quality','numeric',False,False,None),
    ('agency_response','text',False,False,None),
    ('agency_response_at','timestamptz',False,False,None),
    ('backjob_edit_deadline','timestamptz',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('jobID_id','int8',False,True,'jobs'),
    ('reviewerID_id','int8',False,True,'accounts_accounts'),
    ('revieweeID_id','int8',False,True,'accounts_accounts'),
    ('revieweeProfileID_id','int8',False,True,'accounts_profile'),
    ('revieweeAgencyID_id','int8',False,True,'accounts_agency'),
    ('revieweeEmployeeID_id','int8',False,True,'agency_employees'),
    ('flaggedBy_id','int8',False,True,'accounts_accounts'),
]

T['review_skill_tags'] = [
    ('tagID','int8',True,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('reviewID_id','int8',False,True,'job_reviews'),
    ('workerSpecializationID_id','int8',False,True,'accounts_workerspecialization'),
]

T['job_materials'] = [
    ('jobMaterialID','int8',True,False,None),
    ('name','varchar',False,False,None),
    ('description','text',False,False,None),
    ('quantity','int4',False,False,None),
    ('unit','varchar',False,False,None),
    ('source','varchar',False,False,None),
    ('purchase_price','numeric',False,False,None),
    ('receipt_image_url','varchar',False,False,None),
    ('client_approved','bool',False,False,None),
    ('client_approved_at','timestamptz',False,False,None),
    ('client_rejected','bool',False,False,None),
    ('rejection_reason','text',False,False,None),
    ('added_by','varchar',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('jobID_id','int8',False,True,'jobs'),
    ('workerMaterialID_id','int8',False,True,'worker_materials'),
]

T['job_photos'] = [
    ('photoID','int8',True,False,None),
    ('photoURL','varchar',False,False,None),
    ('fileName','varchar',False,False,None),
    ('uploadedAt','timestamptz',False,False,None),
    ('jobID_id','int8',False,True,'jobs'),
]

T['daily_attendance'] = [
    ('attendanceID','int8',True,False,None),
    ('date','date',False,False,None),
    ('time_in','timestamptz',False,False,None),
    ('time_out','timestamptz',False,False,None),
    ('status','varchar',False,False,None),
    ('worker_confirmed','bool',False,False,None),
    ('worker_confirmed_at','timestamptz',False,False,None),
    ('client_confirmed','bool',False,False,None),
    ('client_confirmed_at','timestamptz',False,False,None),
    ('amount_earned','numeric',False,False,None),
    ('payment_processed','bool',False,False,None),
    ('payment_processed_at','timestamptz',False,False,None),
    ('payment_method','varchar',False,False,None),
    ('notes','text',False,False,None),
    ('absent_penalty_amount','numeric',False,False,None),
    ('absent_penalty_applied','bool',False,False,None),
    ('absent_penalty_applied_at','timestamptz',False,False,None),
    ('absent_penalty_percent','numeric',False,False,None),
    ('cash_payment_proof_url','varchar',False,False,None),
    ('cash_payment_verified','bool',False,False,None),
    ('cash_payment_verified_at','timestamptz',False,False,None),
    ('cash_proof_uploaded_at','timestamptz',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('jobID_id','int8',False,True,'jobs'),
    ('workerID_id','int8',False,True,'accounts_workerprofile'),
    ('assignmentID_id','int8',False,True,'job_worker_assignments'),
    ('employeeID_id','int8',False,True,'agency_employees'),
]

T['daily_job_extensions'] = [
    ('extensionID','int8',True,False,None),
    ('additional_days','int4',False,False,None),
    ('additional_escrow','numeric',False,False,None),
    ('reason','text',False,False,None),
    ('status','varchar',False,False,None),
    ('requested_by','varchar',False,False,None),
    ('client_approved','bool',False,False,None),
    ('client_approved_at','timestamptz',False,False,None),
    ('worker_approved','bool',False,False,None),
    ('worker_approved_at','timestamptz',False,False,None),
    ('escrow_collected','bool',False,False,None),
    ('escrow_collected_at','timestamptz',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('jobID_id','int8',False,True,'jobs'),
    ('requestedByUser_id','int8',False,True,'accounts_accounts'),
]

T['daily_rate_changes'] = [
    ('changeID','int8',True,False,None),
    ('old_rate','numeric',False,False,None),
    ('new_rate','numeric',False,False,None),
    ('reason','text',False,False,None),
    ('effective_date','date',False,False,None),
    ('status','varchar',False,False,None),
    ('requested_by','varchar',False,False,None),
    ('client_approved','bool',False,False,None),
    ('client_approved_at','timestamptz',False,False,None),
    ('worker_approved','bool',False,False,None),
    ('worker_approved_at','timestamptz',False,False,None),
    ('escrow_adjusted','bool',False,False,None),
    ('escrow_adjustment_amount','numeric',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('jobID_id','int8',False,True,'jobs'),
    ('requestedByUser_id','int8',False,True,'accounts_accounts'),
]

T['daily_skip_day_requests'] = [
    ('skipRequestID','int8',True,False,None),
    ('request_date','date',False,False,None),
    ('status','varchar',False,False,None),
    ('requested_by','varchar',False,False,None),
    ('requested_account_ids','jsonb',False,False,None),
    ('requested_count','int4',False,False,None),
    ('total_required','int4',False,False,None),
    ('requires_all_team_workers','bool',False,False,None),
    ('all_workers_requested','bool',False,False,None),
    ('target_type','varchar',False,False,None),
    ('reviewedAt','timestamptz',False,False,None),
    ('client_rejection_reason','text',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('jobID_id','int8',False,True,'jobs'),
    ('requestedByUser_id','int8',False,True,'accounts_accounts'),
    ('reviewedByUser_id','int8',False,True,'accounts_accounts'),
    ('target_employee_id','int8',False,True,'agency_employees'),
    ('target_worker_account_id','int8',False,True,'accounts_accounts'),
]

T['conversation'] = [
    ('conversationID','int8',True,False,None),
    ('conversation_type','varchar',False,False,None),
    ('status','varchar',False,False,None),
    ('lastMessageText','text',False,False,None),
    ('lastMessageTime','timestamptz',False,False,None),
    ('unreadCountClient','int4',False,False,None),
    ('unreadCountWorker','int4',False,False,None),
    ('archivedByClient','bool',False,False,None),
    ('archivedByWorker','bool',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('client_id','int8',False,True,'accounts_profile'),
    ('worker_id','int8',False,True,'accounts_profile'),
    ('agency_id','int8',False,True,'accounts_agency'),
    ('relatedJobPosting_id','int8',False,True,'jobs'),
    ('lastMessageSender_id','int8',False,True,'accounts_profile'),
]

T['conversation_participants'] = [
    ('participantID','int8',True,False,None),
    ('participant_type','varchar',False,False,None),
    ('unread_count','int4',False,False,None),
    ('is_archived','bool',False,False,None),
    ('joined_at','timestamptz',False,False,None),
    ('last_read_at','timestamptz',False,False,None),
    ('conversation_id','int8',False,True,'conversation'),
    ('profile_id','int8',False,True,'accounts_profile'),
    ('skill_slot_id','int8',False,True,'job_skill_slots'),
    ('admin_account_id','int8',False,True,'accounts_accounts'),
]

T['message'] = [
    ('messageID','int8',True,False,None),
    ('messageText','text',False,False,None),
    ('messageType','varchar',False,False,None),
    ('locationAddress','varchar',False,False,None),
    ('locationLandmark','varchar',False,False,None),
    ('locationLatitude','numeric',False,False,None),
    ('locationLongitude','numeric',False,False,None),
    ('isRead','bool',False,False,None),
    ('readAt','timestamptz',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('conversationID_id','int8',False,True,'conversation'),
    ('sender_id','int8',False,True,'accounts_profile'),
    ('senderAgency_id','int8',False,True,'accounts_agency'),
    ('sender_admin_id','int8',False,True,'accounts_accounts'),
]

T['message_attachment'] = [
    ('attachmentID','int8',True,False,None),
    ('fileURL','varchar',False,False,None),
    ('fileName','varchar',False,False,None),
    ('fileSize','int4',False,False,None),
    ('fileType','varchar',False,False,None),
    ('uploadedAt','timestamptz',False,False,None),
    ('messageID_id','int8',False,True,'message'),
]

T['agency_employees'] = [
    ('employeeID','int8',True,False,None),
    ('name','varchar',False,False,None),
    ('firstName','varchar',False,False,None),
    ('middleName','varchar',False,False,None),
    ('lastName','varchar',False,False,None),
    ('email','varchar',False,False,None),
    ('role','varchar',False,False,None),
    ('avatar','varchar',False,False,None),
    ('mobile','varchar',False,False,None),
    ('rating','numeric',False,False,None),
    ('specializations','text',False,False,None),
    ('daily_rate','numeric',False,False,None),
    ('hourly_rate','numeric',False,False,None),
    ('is_available_daily_jobs','bool',False,False,None),
    ('isActive','bool',False,False,None),
    ('employeeOfTheMonth','bool',False,False,None),
    ('employeeOfTheMonthDate','timestamptz',False,False,None),
    ('employeeOfTheMonthReason','text',False,False,None),
    ('lastRatingUpdate','timestamptz',False,False,None),
    ('totalEarnings','numeric',False,False,None),
    ('totalJobsCompleted','int4',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('agency_id','int8',False,True,'accounts_accounts'),
]

T['worker_certifications'] = [
    ('certificationID','int8',True,False,None),
    ('name','varchar',False,False,None),
    ('issuing_organization','varchar',False,False,None),
    ('issue_date','date',False,False,None),
    ('expiry_date','date',False,False,None),
    ('certificate_url','varchar',False,False,None),
    ('is_verified','bool',False,False,None),
    ('verified_at','timestamptz',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('workerID_id','int8',False,True,'accounts_workerprofile'),
    ('specializationID_id','int8',False,True,'accounts_workerspecialization'),
    ('verified_by_id','int8',False,True,'accounts_accounts'),
]

T['certification_logs'] = [
    ('certLogID','int8',True,False,None),
    ('certificationID','int8',False,False,None),
    ('action','varchar',False,False,None),
    ('certificationName','varchar',False,False,None),
    ('workerEmail','varchar',False,False,None),
    ('workerAccountID','int8',False,False,None),
    ('reason','text',False,False,None),
    ('reviewedAt','timestamptz',False,False,None),
    ('workerID_id','int8',False,True,'accounts_workerprofile'),
    ('reviewedBy_id','int8',False,True,'accounts_accounts'),
]

T['worker_materials'] = [
    ('materialID','int8',True,False,None),
    ('name','varchar',False,False,None),
    ('description','text',False,False,None),
    ('price','numeric',False,False,None),
    ('unit','varchar',False,False,None),
    ('image_url','varchar',False,False,None),
    ('quantity','numeric',False,False,None),
    ('is_available','bool',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('workerID_id','int8',False,True,'accounts_workerprofile'),
    ('agencyID_id','int8',False,True,'accounts_agency'),
    ('categoryID_id','int8',False,True,'specializations'),
]

T['worker_portfolio'] = [
    ('portfolioID','int8',True,False,None),
    ('image_url','varchar',False,False,None),
    ('caption','text',False,False,None),
    ('display_order','int4',False,False,None),
    ('file_name','varchar',False,False,None),
    ('file_size','int4',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('workerID_id','int8',False,True,'accounts_workerprofile'),
]

T['profiles_workerproduct'] = [
    ('productID','int8',True,False,None),
    ('productName','varchar',False,False,None),
    ('description','text',False,False,None),
    ('price','numeric',False,False,None),
    ('priceUnit','varchar',False,False,None),
    ('inStock','bool',False,False,None),
    ('stockQuantity','int4',False,False,None),
    ('productImage','varchar',False,False,None),
    ('isActive','bool',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('workerID_id','int8',False,True,'accounts_workerprofile'),
    ('categoryID_id','int8',False,True,'specializations'),
]

# ══ COLUMN LAYOUT ════════════════════════════════════════════════════════════
COLUMNS = [
    # Col 0 — Auth & Social
    ['accounts_accounts', 'account_emailaddress', 'account_emailconfirmation',
     'socialaccount_socialaccount', 'socialaccount_socialapp', 'socialaccount_socialtoken'],
    # Col 1 — Profiles
    ['accounts_profile', 'accounts_workerprofile', 'accounts_clientprofile', 'accounts_agency',
     'accounts_barangay', 'accounts_city'],
    # Col 2 — Specializations & Wallet
    ['specializations', 'accounts_workerspecialization', 'accounts_interestedjobs',
     'accounts_wallet', 'accounts_userpaymentmethod', 'accounts_pushtoken',
     'accounts_notificationsettings'],
    # Col 3 — Finance, Notifications & some Admin
    ['accounts_notification', 'accounts_transaction',
     'adminpanel_cannedresponse', 'adminpanel_contentmoderationterm',
     'adminpanel_faq', 'adminpanel_systemroles'],
    # Col 4 — KYC Individual
    ['accounts_kyc', 'accounts_kycfiles', 'kyc_extracted_data'],
    # Col 5 — KYC Agency + KYC Logs + Admin A
    ['agency_agencykyc', 'agency_agencykycfile', 'agency_kyc_extracted_data', 'adminpanel_kyclogs'],
    # Col 6 — Admin Panel B
    ['adminpanel_adminaccount', 'adminpanel_auditlog', 'adminpanel_supportticket',
     'adminpanel_supportticketreply', 'adminpanel_userreport', 'adminpanel_platformsettings'],
    # Col 7 — Jobs
    ['jobs'],
    # Col 8 — Job Sub-tables
    ['job_skill_slots', 'job_applications', 'price_negotiations'],
    # Col 9 — Assignments & Logs
    ['job_worker_assignments', 'job_employee_assignments', 'job_logs', 'saved_jobs'],
    # Col 10 — Disputes & Reviews
    ['job_disputes', 'dispute_evidence', 'backjob_schedule_confirmations',
     'job_reviews', 'review_skill_tags'],
    # Col 11 — Materials, Photos & Daily A
    ['job_materials', 'job_photos', 'daily_attendance', 'daily_job_extensions'],
    # Col 12 — Daily B + Messaging
    ['daily_rate_changes', 'daily_skip_day_requests',
     'conversation', 'conversation_participants', 'message', 'message_attachment'],
    # Col 13 — Workers & Agencies
    ['agency_employees', 'worker_certifications', 'certification_logs',
     'worker_materials', 'worker_portfolio', 'profiles_workerproduct'],
]

# Selected FK relationships to draw (source_table, target_table)
RELS = [
    ('account_emailaddress',         'accounts_accounts'),
    ('account_emailconfirmation',     'account_emailaddress'),
    ('socialaccount_socialaccount',   'accounts_accounts'),
    ('socialaccount_socialtoken',     'socialaccount_socialaccount'),
    ('accounts_profile',              'accounts_accounts'),
    ('accounts_workerprofile',        'accounts_profile'),
    ('accounts_clientprofile',        'accounts_profile'),
    ('accounts_agency',               'accounts_accounts'),
    ('accounts_barangay',             'accounts_city'),
    ('specializations',               'accounts_agency'),
    ('accounts_workerspecialization', 'accounts_workerprofile'),
    ('accounts_workerspecialization', 'specializations'),
    ('accounts_interestedjobs',       'accounts_clientprofile'),
    ('accounts_interestedjobs',       'specializations'),
    ('accounts_wallet',               'accounts_accounts'),
    ('accounts_wallet',               'accounts_userpaymentmethod'),
    ('accounts_userpaymentmethod',    'accounts_accounts'),
    ('accounts_pushtoken',            'accounts_accounts'),
    ('accounts_notificationsettings', 'accounts_accounts'),
    ('accounts_notification',         'accounts_accounts'),
    ('accounts_transaction',          'accounts_wallet'),
    ('accounts_kyc',                  'accounts_accounts'),
    ('accounts_kycfiles',             'accounts_kyc'),
    ('kyc_extracted_data',            'accounts_kyc'),
    ('agency_agencykyc',              'accounts_accounts'),
    ('agency_agencykycfile',          'agency_agencykyc'),
    ('agency_kyc_extracted_data',     'agency_agencykyc'),
    ('adminpanel_kyclogs',            'accounts_accounts'),
    ('adminpanel_adminaccount',       'accounts_accounts'),
    ('adminpanel_auditlog',           'accounts_accounts'),
    ('adminpanel_supportticket',      'accounts_accounts'),
    ('adminpanel_supportticketreply', 'adminpanel_supportticket'),
    ('adminpanel_platformsettings',   'accounts_accounts'),
    ('jobs',                          'accounts_clientprofile'),
    ('jobs',                          'accounts_agency'),
    ('job_skill_slots',               'jobs'),
    ('job_skill_slots',               'specializations'),
    ('job_applications',              'jobs'),
    ('job_applications',              'accounts_workerprofile'),
    ('job_applications',              'job_skill_slots'),
    ('price_negotiations',            'job_applications'),
    ('job_worker_assignments',        'jobs'),
    ('job_worker_assignments',        'job_skill_slots'),
    ('job_worker_assignments',        'accounts_workerprofile'),
    ('job_employee_assignments',      'jobs'),
    ('job_employee_assignments',      'job_skill_slots'),
    ('job_logs',                      'jobs'),
    ('saved_jobs',                    'jobs'),
    ('job_disputes',                  'jobs'),
    ('dispute_evidence',              'job_disputes'),
    ('backjob_schedule_confirmations','job_disputes'),
    ('backjob_schedule_confirmations','job_worker_assignments'),
    ('job_reviews',                   'jobs'),
    ('review_skill_tags',             'job_reviews'),
    ('review_skill_tags',             'accounts_workerspecialization'),
    ('job_materials',                 'jobs'),
    ('job_materials',                 'worker_materials'),
    ('job_photos',                    'jobs'),
    ('daily_attendance',              'jobs'),
    ('daily_attendance',              'job_worker_assignments'),
    ('daily_job_extensions',          'jobs'),
    ('daily_rate_changes',            'jobs'),
    ('daily_skip_day_requests',       'jobs'),
    ('conversation',                  'jobs'),
    ('conversation',                  'accounts_profile'),
    ('conversation_participants',     'conversation'),
    ('message',                       'conversation'),
    ('message_attachment',            'message'),
    ('agency_employees',              'accounts_accounts'),
    ('worker_certifications',         'accounts_workerprofile'),
    ('worker_certifications',         'accounts_workerspecialization'),
    ('certification_logs',            'accounts_workerprofile'),
    ('worker_materials',              'accounts_workerprofile'),
    ('worker_materials',              'accounts_agency'),
    ('worker_portfolio',              'accounts_workerprofile'),
    ('profiles_workerproduct',        'accounts_workerprofile'),
    ('profiles_workerproduct',        'specializations'),
    ('job_employee_assignments',      'agency_employees'),
    ('daily_attendance',              'agency_employees'),
    ('daily_skip_day_requests',       'agency_employees'),
    ('job_reviews',                   'agency_employees'),
    ('accounts_transaction',          'jobs'),
]


def build_positions(columns, top_y, left_x):
    pos = {}
    x = left_x
    for col in columns:
        y = top_y
        for tname in col:
            pos[tname] = (x, y)
            y -= tbl_h(len(T[tname])) + GAP
        x += TW + CGAP
    return pos


def generate_full_canvas():
    TOP_Y  = -0.55
    LEFT_X =  0.30

    positions = build_positions(COLUMNS, TOP_Y, LEFT_X)

    # Compute canvas dimensions
    all_bottoms = [pos[1] - tbl_h(len(T[tn])) for tn, pos in positions.items()]
    fig_bottom  = min(all_bottoms) - 0.50
    num_cols    = len(COLUMNS)
    fig_right   = LEFT_X + num_cols*(TW+CGAP) + 0.30
    fig_top     = 0.50

    fig_w = fig_right
    fig_h = fig_top - fig_bottom

    print(f"Canvas: {fig_w:.1f}\" × {fig_h:.1f}\" → "
          f"{int(fig_w*150)}×{int(fig_h*150)} px @ 150dpi")

    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
    fig.patch.set_facecolor(C['bg'])
    ax.set_facecolor(C['bg'])
    ax.set_xlim(0, fig_w)
    ax.set_ylim(fig_bottom, fig_top)
    ax.axis('off')
    ax.set_aspect('equal')

    # Title
    ax.text(fig_w/2, fig_top-0.16,
            'Platform Database – Complete Entity Relationship Diagram',
            ha='center', va='top', fontsize=11, fontweight='bold',
            color=C['title'])
    ax.text(fig_w/2, fig_top-0.37,
            f'{len(T)} tables  ·  ERD v2  ·  All fields shown',
            ha='center', va='top', fontsize=7, color=C['note'])

    # Draw tables
    all_rc    = {}
    tbl_boxes = {}
    for tname, (x, y_top) in positions.items():
        rc, box = draw_table(ax, x, y_top, tname, T[tname])
        all_rc[tname]    = rc
        tbl_boxes[tname] = box

    # Draw relationships
    for src_t, dst_t in RELS:
        if src_t not in tbl_boxes or dst_t not in tbl_boxes:
            continue
        sx1, sy_top, sw, sh = tbl_boxes[src_t]
        dx1, dy_top, dw, dh = tbl_boxes[dst_t]
        # Use centre of header as connection point
        sx = sx1 + sw/2
        sy = sy_top - sh/2          # centre of source table
        dx = dx1 + dw/2
        dy = dy_top - HDR/2         # top of destination (header centre)
        draw_rel(ax, sx, sy, dx, dy)

    plt.tight_layout(pad=0.05)
    out = '/workspace/erd_v2_complete_canvas.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor=C['bg'])
    plt.close(fig)
    print(f'Saved {out}')


if __name__ == '__main__':
    generate_full_canvas()
