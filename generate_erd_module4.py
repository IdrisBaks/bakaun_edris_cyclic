#!/usr/bin/env python3
"""ERD Diagram Generator - Module 4: Disputes, Reviews, Daily Operations & Attendance"""
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

TW   = 3.30
RH   = 0.188
HDR  = 0.285
GAP  = 0.38
CGAP = 0.55

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
            ha='center', va='center', fontsize=7.3, fontweight='bold',
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
                color=C['border'], linewidth=0.25, zorder=3)
        row_centers[fname] = (x + TW/2, ry_ctr)
        if is_pk:
            ax.add_patch(mpatches.FancyBboxPatch(
                (x+0.03, ry_top - RH + 0.02), 0.30, RH - 0.04,
                boxstyle="round,pad=0.01",
                linewidth=0, facecolor=C['pk_bg'], zorder=3))
            ax.text(x+0.18, ry_ctr, 'PK',
                    ha='center', va='center', fontsize=5.0,
                    fontweight='bold', color=C['pk_txt'], zorder=5)
            ax.text(x+0.37, ry_ctr, fname,
                    ha='left', va='center', fontsize=6.0,
                    fontweight='bold', color=C['norm_txt'], zorder=5)
            ax.text(x+TW-0.06, ry_ctr, ftype,
                    ha='right', va='center', fontsize=4.8,
                    color=C['type_txt'], zorder=5)
        elif is_fk:
            ax.text(x+0.09, ry_ctr, fname,
                    ha='left', va='center', fontsize=5.8,
                    fontstyle='italic', color=C['fk_txt'], zorder=5)
            if fk_tgt:
                ax.text(x+TW-0.06, ry_ctr, f'→ {fk_tgt}',
                        ha='right', va='center', fontsize=4.5,
                        color=C['fk_txt'], zorder=5)
        else:
            ax.text(x+0.09, ry_ctr, fname,
                    ha='left', va='center', fontsize=5.8,
                    color=C['norm_txt'], zorder=5)
            ax.text(x+TW-0.06, ry_ctr, ftype,
                    ha='right', va='center', fontsize=4.8,
                    color=C['type_txt'], zorder=5)
    ax.add_patch(mpatches.Rectangle(
        (x, y_top - h), TW, h,
        linewidth=0.8, edgecolor=C['border'],
        facecolor='none', zorder=4))
    return row_centers, (x, y_top, TW, h)


def crow_foot_arrow(ax, x1, y1, x2, y2, rad=0.15):
    ax.annotate('',
        xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle='-', color=C['rel_line'],
                        linewidth=0.75,
                        connectionstyle=f'arc3,rad={rad}'),
        zorder=0)
    ang  = np.arctan2(y2 - y1, x2 - x1)
    perp = ang + np.pi/2
    sz   = 0.085
    for off in [-sz*0.65, 0, sz*0.65]:
        ex = x1 + sz*np.cos(ang+np.pi) + off*np.cos(perp)
        ey = y1 + sz*np.sin(ang+np.pi) + off*np.sin(perp)
        ax.plot([x1, ex], [y1, ey], color=C['rel_line'], linewidth=0.75, zorder=0)
    tk = 0.07
    ax.plot([x2 - tk*np.cos(perp+np.pi/2), x2 + tk*np.cos(perp+np.pi/2)],
            [y2 - tk*np.sin(perp+np.pi/2), y2 + tk*np.sin(perp+np.pi/2)],
            color=C['rel_line'], linewidth=1.0, zorder=0)


T = {
'job_disputes': [
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
],
'dispute_evidence': [
    ('evidenceID','int8',True,False,None),
    ('imageURL','varchar',False,False,None),
    ('description','text',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('disputeID_id','int8',False,True,'job_disputes'),
    ('uploadedBy_id','int8',False,True,'accounts_accounts'),
],
'backjob_schedule_confirmations': [
    ('confirmationID','int8',True,False,None),
    ('confirmed','bool',False,False,None),
    ('confirmedAt','timestamptz',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('disputeID_id','int8',False,True,'job_disputes'),
    ('assignmentID_id','int8',False,True,'job_worker_assignments'),
    ('confirmedBy_id','int8',False,True,'accounts_accounts'),
],
'job_reviews': [
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
],
'review_skill_tags': [
    ('tagID','int8',True,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('reviewID_id','int8',False,True,'job_reviews'),
    ('workerSpecializationID_id','int8',False,True,'accts_workerspecialization'),
],
'job_materials': [
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
],
'job_photos': [
    ('photoID','int8',True,False,None),
    ('photoURL','varchar',False,False,None),
    ('fileName','varchar',False,False,None),
    ('uploadedAt','timestamptz',False,False,None),
    ('jobID_id','int8',False,True,'jobs'),
],
'daily_attendance': [
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
],
'daily_job_extensions': [
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
],
'daily_rate_changes': [
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
],
'daily_skip_day_requests': [
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
],
}

COLUMNS = [
    ['job_disputes', 'dispute_evidence', 'backjob_schedule_confirmations'],
    ['job_reviews', 'review_skill_tags', 'job_materials', 'job_photos'],
    ['daily_attendance', 'daily_job_extensions'],
    ['daily_rate_changes', 'daily_skip_day_requests'],
]

RELS = [
    ('dispute_evidence',              'disputeID_id',             'job_disputes'),
    ('backjob_schedule_confirmations','disputeID_id',             'job_disputes'),
    ('backjob_schedule_confirmations','assignmentID_id',          'job_disputes'),
    ('job_reviews',                   'jobID_id',                 'job_disputes'),
    ('review_skill_tags',             'reviewID_id',              'job_reviews'),
    ('job_materials',                 'jobID_id',                 'job_disputes'),
    ('job_photos',                    'jobID_id',                 'job_disputes'),
    ('daily_attendance',              'jobID_id',                 'job_disputes'),
    ('daily_job_extensions',          'jobID_id',                 'job_disputes'),
    ('daily_rate_changes',            'jobID_id',                 'job_disputes'),
    ('daily_skip_day_requests',       'jobID_id',                 'job_disputes'),
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


def generate_module4():
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
            'MODULE 4 – Disputes, Reviews, Daily Operations & Attendance',
            ha='center', va='top', fontsize=13, fontweight='bold',
            color=C['title'])
    ax.text(fig_w/2, fig_top - 0.40,
            '11 tables  |  ERD v2',
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
    out = '/workspace/erd_v2_module4_disputes.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor=C['bg'])
    plt.close(fig)
    print(f'Saved {out}')


if __name__ == '__main__':
    generate_module4()
