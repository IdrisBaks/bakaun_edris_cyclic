#!/usr/bin/env python3
"""ERD Diagram Generator - Module 3: Jobs, Applications & Assignments"""
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
RH   = 0.190
HDR  = 0.295
GAP  = 0.40
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
            ha='center', va='center', fontsize=7.5, fontweight='bold',
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
                    ha='center', va='center', fontsize=5.2,
                    fontweight='bold', color=C['pk_txt'], zorder=5)
            ax.text(x+0.37, ry_ctr, fname,
                    ha='left', va='center', fontsize=6.2,
                    fontweight='bold', color=C['norm_txt'], zorder=5)
            ax.text(x+TW-0.06, ry_ctr, ftype,
                    ha='right', va='center', fontsize=5.0,
                    color=C['type_txt'], zorder=5)
        elif is_fk:
            ax.text(x+0.09, ry_ctr, fname,
                    ha='left', va='center', fontsize=6.0,
                    fontstyle='italic', color=C['fk_txt'], zorder=5)
            if fk_tgt:
                ax.text(x+TW-0.06, ry_ctr, f'→ {fk_tgt}',
                        ha='right', va='center', fontsize=4.7,
                        color=C['fk_txt'], zorder=5)
        else:
            ax.text(x+0.09, ry_ctr, fname,
                    ha='left', va='center', fontsize=6.0,
                    color=C['norm_txt'], zorder=5)
            ax.text(x+TW-0.06, ry_ctr, ftype,
                    ha='right', va='center', fontsize=5.0,
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


# ══ TABLE DEFINITIONS ════════════════════════════════════════════════════════
T = {
'jobs': [
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
    ('completedAt','timestamptz',False,False,None),
    ('cancellationReason','text',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
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
    ('clientRefundAmount','numeric',False,False,None),
    ('workerCompensationAmount','numeric',False,False,None),
    ('agency_flow_mode','varchar',False,False,None),
    ('clientID_id','int8',False,True,'accounts_clientprofile'),
    ('assignedWorkerID_id','int8',False,True,'accounts_workerprofile'),
    ('assignedAgencyFK_id','int8',False,True,'accounts_agency'),
    ('assignedEmployeeID_id','int8',False,True,'agency_employees'),
    ('categoryID_id','int8',False,True,'specializations'),
    ('cancelledByAccountID_id','int8',False,True,'accounts_accounts'),
    ('cashPaymentApprovedBy_id','int8',False,True,'accounts_accounts'),
],
'job_skill_slots': [
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
],
'job_applications': [
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
],
'price_negotiations': [
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
],
'job_worker_assignments': [
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
],
'job_employee_assignments': [
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
],
'job_logs': [
    ('logID','int8',True,False,None),
    ('actionType','varchar',False,False,None),
    ('oldStatus','varchar',False,False,None),
    ('newStatus','varchar',False,False,None),
    ('notes','text',False,False,None),
    ('metadata','jsonb',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('jobID_id','int8',False,True,'jobs'),
    ('changedBy_id','int8',False,True,'accounts_accounts'),
],
'saved_jobs': [
    ('savedJobID','int8',True,False,None),
    ('savedAt','timestamptz',False,False,None),
    ('jobID_id','int8',False,True,'jobs'),
    ('workerID_id','int8',False,True,'accounts_workerprofile'),
],
}

COLUMNS = [
    ['jobs'],
    ['job_skill_slots', 'job_applications', 'price_negotiations'],
    ['job_worker_assignments', 'job_employee_assignments'],
    ['job_logs', 'saved_jobs'],
]

RELS = [
    ('job_skill_slots',          'jobID_id',            'jobs'),
    ('job_skill_slots',          'specializationID_id', 'jobs'),   # simplified pointer
    ('job_applications',         'jobID_id',            'jobs'),
    ('job_applications',         'workerID_id',         'jobs'),
    ('job_applications',         'applied_skill_slot_id','job_skill_slots'),
    ('price_negotiations',       'application_id',      'job_applications'),
    ('job_worker_assignments',   'jobID_id',            'jobs'),
    ('job_worker_assignments',   'skillSlotID_id',      'job_skill_slots'),
    ('job_worker_assignments',   'workerID_id',         'jobs'),
    ('job_employee_assignments', 'job_id',              'jobs'),
    ('job_employee_assignments', 'skill_slot_id',       'job_skill_slots'),
    ('job_employee_assignments', 'employee_id',         'jobs'),
    ('job_logs',                 'jobID_id',            'jobs'),
    ('saved_jobs',               'jobID_id',            'jobs'),
    ('saved_jobs',               'workerID_id',         'jobs'),
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


def generate_module3():
    TOP_MARGIN  = -0.6
    LEFT_MARGIN =  0.3
    COL_SPACING =  CGAP

    positions = build_layout(COLUMNS, TOP_MARGIN, LEFT_MARGIN, COL_SPACING)

    all_bottoms = [pos[1] - tbl_h(len(T[tn])) for tn, pos in positions.items()]
    fig_bottom = min(all_bottoms) - 0.6
    num_cols   = len(COLUMNS)
    fig_right  = LEFT_MARGIN + num_cols * (TW + COL_SPACING) + 0.3
    fig_top    = 0.5

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
            'MODULE 3 – Jobs, Applications & Assignments',
            ha='center', va='top', fontsize=13, fontweight='bold',
            color=C['title'])
    ax.text(fig_w/2, fig_top - 0.40,
            '8 tables  |  ERD v2',
            ha='center', va='top', fontsize=8, color=C['note'])

    all_rc = {}
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
    out = '/workspace/erd_v2_module3_jobs.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor=C['bg'])
    plt.close(fig)
    print(f'Saved {out}')


if __name__ == '__main__':
    generate_module3()
