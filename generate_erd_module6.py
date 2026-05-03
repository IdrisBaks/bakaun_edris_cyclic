#!/usr/bin/env python3
"""ERD Diagram Generator - Module 6: Admin Panel, Messaging, Notifications & Worker Assets"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

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
}

TW   = 3.25
RH   = 0.178
HDR  = 0.270
GAP  = 0.35
CGAP = 0.52

def tbl_h(n): return HDR + n * RH

def draw_table(ax, x, y_top, name, fields):
    n = len(fields)
    h = tbl_h(n)
    ax.add_patch(mpatches.FancyBboxPatch(
        (x+0.05, y_top - h - 0.05), TW, h,
        boxstyle="square,pad=0", linewidth=0,
        facecolor='#D1D9E0', zorder=1))
    ax.add_patch(mpatches.Rectangle(
        (x, y_top - HDR), TW, HDR,
        linewidth=0, facecolor=C['hdr_bg'], zorder=2))
    ax.text(x + TW/2, y_top - HDR/2, name,
            ha='center', va='center', fontsize=6.8, fontweight='bold',
            color=C['hdr_txt'], zorder=5)
    row_centers = {}
    for i, (fname, ftype, is_pk, is_fk, fk_tgt) in enumerate(fields):
        ry_top = y_top - HDR - i * RH
        ry_ctr = ry_top - RH / 2
        ax.add_patch(mpatches.Rectangle(
            (x, ry_top - RH), TW, RH,
            linewidth=0,
            facecolor=C['row_lt'] if i % 2 == 0 else C['row_dk'],
            zorder=2))
        ax.plot([x, x+TW], [ry_top, ry_top],
                color=C['border'], linewidth=0.22, zorder=3)
        row_centers[fname] = (x + TW/2, ry_ctr)
        if is_pk:
            ax.add_patch(mpatches.FancyBboxPatch(
                (x+0.03, ry_top - RH + 0.016), 0.28, RH - 0.032,
                boxstyle="round,pad=0.01",
                linewidth=0, facecolor=C['pk_bg'], zorder=3))
            ax.text(x+0.17, ry_ctr, 'PK',
                    ha='center', va='center', fontsize=4.6,
                    fontweight='bold', color=C['pk_txt'], zorder=5)
            ax.text(x+0.35, ry_ctr, fname,
                    ha='left', va='center', fontsize=5.5,
                    fontweight='bold', color=C['norm_txt'], zorder=5)
            ax.text(x+TW-0.06, ry_ctr, ftype,
                    ha='right', va='center', fontsize=4.4,
                    color=C['type_txt'], zorder=5)
        elif is_fk:
            ax.text(x+0.09, ry_ctr, fname,
                    ha='left', va='center', fontsize=5.4,
                    fontstyle='italic', color=C['fk_txt'], zorder=5)
            if fk_tgt:
                ax.text(x+TW-0.06, ry_ctr, f'→ {fk_tgt}',
                        ha='right', va='center', fontsize=4.2,
                        color=C['fk_txt'], zorder=5)
        else:
            ax.text(x+0.09, ry_ctr, fname,
                    ha='left', va='center', fontsize=5.4,
                    color=C['norm_txt'], zorder=5)
            ax.text(x+TW-0.06, ry_ctr, ftype,
                    ha='right', va='center', fontsize=4.4,
                    color=C['type_txt'], zorder=5)
    ax.add_patch(mpatches.Rectangle(
        (x, y_top - h), TW, h,
        linewidth=0.8, edgecolor=C['border'],
        facecolor='none', zorder=4))
    return row_centers, (x, y_top, TW, h)


def crow_foot_arrow(ax, x1, y1, x2, y2, rad=0.13):
    ax.annotate('',
        xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle='-', color=C['rel_line'],
                        linewidth=0.65,
                        connectionstyle=f'arc3,rad={rad}'),
        zorder=0)
    ang  = np.arctan2(y2 - y1, x2 - x1)
    perp = ang + np.pi/2
    sz   = 0.078
    for off in [-sz*0.65, 0, sz*0.65]:
        ex = x1 + sz*np.cos(ang+np.pi) + off*np.cos(perp)
        ey = y1 + sz*np.sin(ang+np.pi) + off*np.sin(perp)
        ax.plot([x1, ex], [y1, ey], color=C['rel_line'], linewidth=0.65, zorder=0)
    tk = 0.065
    ax.plot([x2 - tk*np.cos(perp+np.pi/2), x2 + tk*np.cos(perp+np.pi/2)],
            [y2 - tk*np.sin(perp+np.pi/2), y2 + tk*np.sin(perp+np.pi/2)],
            color=C['rel_line'], linewidth=0.9, zorder=0)


T = {
# ── Admin panel tables ─────────────────────────────────────────────────────
'adminpanel_adminaccount': [
    ('adminID','int8',True,False,None),
    ('role','varchar',False,False,None),
    ('permissions','jsonb',False,False,None),
    ('isActive','bool',False,False,None),
    ('lastLogin','timestamptz',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('accountFK_id','int8 UNIQUE',False,True,'accounts_accounts'),
],
'adminpanel_auditlog': [
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
],
'adminpanel_supportticket': [
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
],
'adminpanel_supportticketreply': [
    ('replyID','int8',True,False,None),
    ('content','text',False,False,None),
    ('isSystemMessage','bool',False,False,None),
    ('attachmentURL','varchar',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('ticketFK_id','int8',False,True,'adminpanel_supportticket'),
    ('senderFK_id','int8',False,True,'accounts_accounts'),
],
'adminpanel_userreport': [
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
],
'adminpanel_platformsettings': [
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
],
'adminpanel_cannedresponse': [
    ('responseID','int8',True,False,None),
    ('title','varchar',False,False,None),
    ('content','text',False,False,None),
    ('category','varchar',False,False,None),
    ('shortcuts','jsonb',False,False,None),
    ('usageCount','int4',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('createdBy_id','int8',False,True,'accounts_accounts'),
],
'adminpanel_contentmoderationterm': [
    ('termID','int8',True,False,None),
    ('term','varchar',False,False,None),
    ('normalizedTerm','varchar UNIQUE',False,False,None),
    ('isActive','bool',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('createdBy_id','int8',False,True,'accounts_accounts'),
    ('updatedBy_id','int8',False,True,'accounts_accounts'),
],
'adminpanel_faq': [
    ('faqID','int8',True,False,None),
    ('question','varchar',False,False,None),
    ('answer','text',False,False,None),
    ('category','varchar',False,False,None),
    ('sortOrder','int4',False,False,None),
    ('viewCount','int4',False,False,None),
    ('isPublished','bool',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
],
'adminpanel_systemroles': [
    ('systemRoleID','int8',True,False,None),
    ('systemRole','varchar',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('accountID_id','int8',False,True,'accounts_accounts'),
],
# ── Notification ────────────────────────────────────────────────────────────
'accounts_notification': [
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
],
# ── Messaging ───────────────────────────────────────────────────────────────
'conversation': [
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
],
'conversation_participants': [
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
],
'message': [
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
],
'message_attachment': [
    ('attachmentID','int8',True,False,None),
    ('fileURL','varchar',False,False,None),
    ('fileName','varchar',False,False,None),
    ('fileSize','int4',False,False,None),
    ('fileType','varchar',False,False,None),
    ('uploadedAt','timestamptz',False,False,None),
    ('messageID_id','int8',False,True,'message'),
],
# ── Transactions ─────────────────────────────────────────────────────────────
'accounts_transaction': [
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
    ('xenditInvoiceID','varchar UNIQUE',False,False,None),
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
],
# ── Agency & Workers ─────────────────────────────────────────────────────────
'agency_employees': [
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
],
'worker_certifications': [
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
    ('specializationID_id','int8',False,True,'accts_workerspecialization'),
    ('verified_by_id','int8',False,True,'accounts_accounts'),
],
'certification_logs': [
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
],
'worker_materials': [
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
],
'worker_portfolio': [
    ('portfolioID','int8',True,False,None),
    ('image_url','varchar',False,False,None),
    ('caption','text',False,False,None),
    ('display_order','int4',False,False,None),
    ('file_name','varchar',False,False,None),
    ('file_size','int4',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('workerID_id','int8',False,True,'accounts_workerprofile'),
],
'profiles_workerproduct': [
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
],
}

# 6 columns
COLUMNS = [
    ['adminpanel_adminaccount', 'adminpanel_auditlog',
     'adminpanel_platformsettings', 'adminpanel_faq'],
    ['adminpanel_supportticket', 'adminpanel_supportticketreply',
     'adminpanel_userreport', 'adminpanel_systemroles'],
    ['adminpanel_cannedresponse', 'adminpanel_contentmoderationterm',
     'accounts_notification', 'accounts_transaction'],
    ['conversation', 'conversation_participants', 'message', 'message_attachment'],
    ['agency_employees', 'worker_certifications', 'certification_logs'],
    ['worker_materials', 'worker_portfolio', 'profiles_workerproduct'],
]

RELS = [
    ('adminpanel_supportticketreply', 'ticketFK_id',    'adminpanel_supportticket'),
    ('conversation_participants',     'conversation_id', 'conversation'),
    ('message',                       'conversationID_id','conversation'),
    ('message_attachment',            'messageID_id',    'message'),
    ('worker_certifications',         'workerID_id',     'agency_employees'),
    ('certification_logs',            'workerID_id',     'agency_employees'),
    ('profiles_workerproduct',        'workerID_id',     'agency_employees'),
    ('worker_portfolio',              'workerID_id',     'agency_employees'),
    ('worker_materials',              'workerID_id',     'agency_employees'),
]


def build_layout(columns, top_margin, left_margin, col_spacing):
    positions = {}
    for ci, col in enumerate(columns):
        x = left_margin + ci * (TW + col_spacing)
        y = top_margin
        for tname in col:
            positions[tname] = (x, y)
            y -= tbl_h(len(T[tname])) + GAP
    return positions


def generate_module6():
    TOP_MARGIN  = -0.6
    LEFT_MARGIN =  0.3
    COL_SPACING =  CGAP

    positions = build_layout(COLUMNS, TOP_MARGIN, LEFT_MARGIN, COL_SPACING)
    all_bottoms = [pos[1] - tbl_h(len(T[tn])) for tn, pos in positions.items()]
    fig_bottom  = min(all_bottoms) - 0.6
    fig_right   = LEFT_MARGIN + len(COLUMNS) * (TW + COL_SPACING) + 0.3
    fig_top     = 0.5

    fig_w = fig_right
    fig_h = fig_top - fig_bottom

    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=150)
    fig.patch.set_facecolor(C['bg'])
    ax.set_facecolor(C['bg'])
    ax.set_xlim(0, fig_w)
    ax.set_ylim(fig_bottom, fig_top)
    ax.axis('off')
    ax.set_aspect('equal')

    ax.text(fig_w/2, fig_top - 0.18,
            'MODULE 6 – Admin Panel, Messaging, Notifications & Worker Assets',
            ha='center', va='top', fontsize=12.5, fontweight='bold',
            color=C['title'])
    ax.text(fig_w/2, fig_top - 0.40,
            '22 tables  |  ERD v2',
            ha='center', va='top', fontsize=8, color=C['note'])

    all_rc    = {}
    tbl_boxes = {}
    for tname, (x, y_top) in positions.items():
        rc, box = draw_table(ax, x, y_top, tname, T[tname])
        all_rc[tname]    = rc
        tbl_boxes[tname] = box

    for src_t, src_f, dst_t in RELS:
        if src_t not in all_rc or dst_t not in all_rc:
            continue
        if src_f not in all_rc[src_t]:
            continue
        sx, sy = all_rc[src_t][src_f]
        dx, dy = tbl_boxes[dst_t][0] + TW/2, tbl_boxes[dst_t][1] - HDR/2
        crow_foot_arrow(ax, sx, sy, dx, dy)

    plt.tight_layout(pad=0.1)
    out = '/workspace/erd_v2_module6_admin.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor=C['bg'])
    plt.close(fig)
    print(f'Saved {out}')


if __name__ == '__main__':
    generate_module6()
