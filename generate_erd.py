import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

ROW_H = 0.28
HDR_H = 0.38
TBL_W = 6.2
COL_NAME_W = 3.8
FONT_SIZE = 7.0
HDR_FONT = 8.5
TITLE_FONT = 16

C_HDR = '#2C3E50'
C_HDR_TXT = '#FFFFFF'
C_PK = '#B8860B'
C_PK_BG = '#FFF8DC'
C_FK = '#2471A3'
C_ROW_W = '#FFFFFF'
C_ROW_G = '#F2F4F4'
C_BORDER = '#ABB2B9'
C_LINE = '#5D6D7E'
C_BG = '#FFFFFF'


def table_height(nfields):
    return HDR_H + nfields * ROW_H


def draw_table(ax, x, y, name, fields):
    n = len(fields)
    h = table_height(n)

    shadow = patches.FancyBboxPatch(
        (x + 0.06, y - h - 0.06), TBL_W, h, boxstyle="round,pad=0.03",
        facecolor='#D5D8DC', edgecolor='none', linewidth=0, zorder=1, alpha=0.4)
    ax.add_patch(shadow)

    ax.add_patch(patches.FancyBboxPatch(
        (x, y - h), TBL_W, h, boxstyle="round,pad=0.03",
        facecolor=C_BG, edgecolor=C_BORDER, linewidth=1.2, zorder=2))

    ax.add_patch(patches.Rectangle(
        (x + 0.03, y - HDR_H), TBL_W - 0.06, HDR_H - 0.03,
        facecolor=C_HDR, edgecolor=C_HDR, linewidth=0, zorder=3,
        clip_on=True))
    ax.text(x + TBL_W / 2, y - HDR_H / 2, name,
            ha='center', va='center', fontsize=HDR_FONT,
            fontweight='bold', color=C_HDR_TXT, zorder=4, family='monospace')

    positions = {}
    for i, (fname, dtype, is_pk, fk_target) in enumerate(fields):
        ry = y - HDR_H - i * ROW_H
        bg = C_ROW_W if i % 2 == 0 else C_ROW_G
        if is_pk:
            bg = C_PK_BG
        ax.add_patch(patches.Rectangle(
            (x + 0.03, ry - ROW_H), TBL_W - 0.06, ROW_H,
            facecolor=bg, edgecolor='none', linewidth=0, zorder=2))
        ax.plot([x + 0.03, x + TBL_W - 0.03], [ry - ROW_H, ry - ROW_H],
                color='#E5E8E8', linewidth=0.4, zorder=2)

        name_color = '#2C3E50'
        style = 'normal'
        weight = 'normal'
        prefix = ""

        if is_pk:
            prefix = "[PK] "
            name_color = C_PK
            weight = 'bold'
        if fk_target:
            style = 'italic'
            name_color = C_FK

        label = prefix + fname
        ax.text(x + 0.12, ry - ROW_H / 2, label,
                ha='left', va='center', fontsize=FONT_SIZE,
                color=name_color, fontstyle=style, fontweight=weight,
                zorder=4, family='monospace', clip_on=True)

        type_label = dtype
        if fk_target:
            type_label = dtype + "  -> " + fk_target
        ax.text(x + COL_NAME_W + 0.1, ry - ROW_H / 2, type_label,
                ha='left', va='center', fontsize=FONT_SIZE - 0.5,
                color='#566573' if not fk_target else C_FK,
                fontstyle=style, zorder=4, family='monospace', clip_on=True)

        positions[fname] = (x + TBL_W / 2, ry - ROW_H / 2)

    ax.plot([x + COL_NAME_W, x + COL_NAME_W],
            [y - HDR_H, y - h + 0.03], color='#D5D8DC', linewidth=0.5, zorder=3)

    return positions, (x, y, TBL_W, h)


def connect_tables(ax, src_pos, src_bounds, tgt_pos, tgt_bounds,
                   src_field, tgt_field, is_one_to_one=False):
    if src_field not in src_pos or tgt_field not in tgt_pos:
        return
    sx, sy = src_pos[src_field]
    tx, ty = tgt_pos[tgt_field]

    s_left, s_top, s_w, s_h = src_bounds
    t_left, t_top, t_w, t_h = tgt_bounds

    s_right = s_left + s_w
    t_right = t_left + t_w

    if abs(s_left + s_w / 2 - (t_left + t_w / 2)) < 0.1:
        if sy > ty:
            x1, y1 = s_left + s_w / 2, s_top - s_h
            x2, y2 = t_left + t_w / 2, t_top
        else:
            x1, y1 = s_left + s_w / 2, s_top
            x2, y2 = t_left + t_w / 2, t_top - t_h
    elif s_right + 0.5 <= t_left:
        x1, y1 = s_right, sy
        x2, y2 = t_left, ty
    elif t_right + 0.5 <= s_left:
        x1, y1 = s_left, sy
        x2, y2 = t_right, ty
    elif s_left + s_w / 2 < t_left + t_w / 2:
        x1, y1 = s_right, sy
        x2, y2 = t_left, ty
    else:
        x1, y1 = s_left, sy
        x2, y2 = t_right, ty

    dx = x2 - x1
    dy = y2 - y1
    length = np.sqrt(dx**2 + dy**2)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    sz = 0.10

    ax.plot([x1, x2], [y1, y2], color=C_LINE, linewidth=0.9, zorder=1)

    bx, by = x2 - ux * sz * 2.5, y2 - uy * sz * 2.5
    ax.plot([bx + px * sz, bx - px * sz], [by + py * sz, by - py * sz],
            color=C_LINE, linewidth=0.9, zorder=1)

    if not is_one_to_one:
        ex, ey = x2, y2
        ax.plot([ex, ex - ux * sz * 2 + px * sz * 1.2],
                [ey, ey - uy * sz * 2 + py * sz * 1.2],
                color=C_LINE, linewidth=0.9, zorder=1)
        ax.plot([ex, ex - ux * sz * 2 - px * sz * 1.2],
                [ey, ey - uy * sz * 2 - py * sz * 1.2],
                color=C_LINE, linewidth=0.9, zorder=1)
    else:
        ex2, ey2 = x2 - ux * sz * 1.0, y2 - uy * sz * 1.0
        ax.plot([ex2 + px * sz, ex2 - px * sz], [ey2 + py * sz, ey2 - py * sz],
                color=C_LINE, linewidth=0.9, zorder=1)

    sx2, sy2 = x1 + ux * sz * 2.5, y1 + uy * sz * 2.5
    ax.plot([sx2 + px * sz, sx2 - px * sz], [sy2 + py * sz, sy2 - py * sz],
            color=C_LINE, linewidth=0.9, zorder=1)


def generate_module(module_title, table_count, tables_data, positions,
                    relationships, filename, figw=50, figh=40):
    fig, ax = plt.subplots(1, 1, figsize=(figw, figh), dpi=150)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    all_xs = []
    all_ys = []
    for tname, fields in tables_data.items():
        px, py = positions[tname]
        h = table_height(len(fields))
        all_xs.extend([px, px + TBL_W])
        all_ys.extend([py, py - h])

    margin = 1.5
    xmin = min(all_xs) - margin
    xmax = max(all_xs) + margin
    ymin = min(all_ys) - margin
    ymax = max(all_ys) + margin + 1.5

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.axis('off')
    ax.set_aspect('equal')

    ax.text((xmin + xmax) / 2, ymax - 0.3, module_title,
            ha='center', va='top', fontsize=TITLE_FONT, fontweight='bold',
            color='#1B2631', family='sans-serif')
    ax.text((xmin + xmax) / 2, ymax - 1.0,
            f"{table_count} tables",
            ha='center', va='top', fontsize=10, color='#5D6D7E',
            style='italic', family='sans-serif',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#EBF5FB',
                      edgecolor='#AED6F1', linewidth=0.5))

    all_pos = {}
    all_bounds = {}
    for tname, fields in tables_data.items():
        px, py = positions[tname]
        pos, bounds = draw_table(ax, px, py, tname, fields)
        all_pos[tname] = pos
        all_bounds[tname] = bounds

    for (st, sf, tt, tf, oto) in relationships:
        if st in all_pos and tt in all_pos:
            connect_tables(ax, all_pos[st], all_bounds[st],
                           all_pos[tt], all_bounds[tt], sf, tf, oto)

    plt.tight_layout(pad=0.5)
    os.makedirs('erd_diagrams', exist_ok=True)
    filepath = os.path.join('erd_diagrams', filename)
    fig.savefig(filepath, dpi=150, bbox_inches='tight',
                facecolor=C_BG, edgecolor='none')
    plt.close(fig)
    print(f"Generated {filepath}")
    return filepath


# ============================================================
# MODULE 2
# ============================================================

def gen_module2():
    tables = {}

    tables['accounts_profile'] = [
        ('profileID', 'int8', True, None),
        ('profileImg', 'varchar', False, None),
        ('firstName', 'varchar', False, None),
        ('lastName', 'varchar', False, None),
        ('middleName', 'varchar', False, None),
        ('contactNum', 'varchar', False, None),
        ('birthDate', 'date', False, None),
        ('profileType', 'varchar', False, None),
        ('latitude', 'numeric', False, None),
        ('longitude', 'numeric', False, None),
        ('location_sharing_enabled', 'bool', False, None),
        ('location_updated_at', 'timestamptz', False, None),
        ('accountFK_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['accounts_workerprofile'] = [
        ('id', 'int8', True, None),
        ('description', 'varchar', False, None),
        ('workerRating', 'int4', False, None),
        ('totalEarningGross', 'numeric', False, None),
        ('availability_status', 'varchar', False, None),
        ('bio', 'varchar', False, None),
        ('hourly_rate', 'numeric', False, None),
        ('daily_rate', 'numeric', False, None),
        ('profile_completion_percentage', 'int4', False, None),
        ('soft_skills', 'text', False, None),
        ('is_available_daily_jobs', 'bool', False, None),
        ('profileID_id', 'int8', False, 'accounts_profile'),
    ]

    tables['accounts_clientprofile'] = [
        ('id', 'int8', True, None),
        ('description', 'varchar', False, None),
        ('totalJobsPosted', 'int4', False, None),
        ('clientRating', 'int4', False, None),
        ('activeJobsCount', 'int4', False, None),
        ('profileID_id', 'int8', False, 'accounts_profile'),
    ]

    tables['accounts_agency'] = [
        ('agencyId', 'int8', True, None),
        ('businessName', 'varchar', False, None),
        ('businessDesc', 'varchar', False, None),
        ('contactNumber', 'varchar', False, None),
        ('city', 'varchar', False, None),
        ('country', 'varchar', False, None),
        ('postal_code', 'varchar', False, None),
        ('province', 'varchar', False, None),
        ('street_address', 'varchar', False, None),
        ('barangay', 'varchar', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('accountFK_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['accounts_barangay'] = [
        ('barangayID', 'int4', True, None),
        ('name', 'varchar', False, None),
        ('zipCode', 'varchar', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('city_id', 'int4', False, 'accounts_city'),
    ]

    tables['accounts_city'] = [
        ('cityID', 'int4', True, None),
        ('name', 'varchar', False, None),
        ('province', 'varchar', False, None),
        ('region', 'varchar', False, None),
        ('zipCode', 'varchar', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
    ]

    tables['specializations'] = [
        ('specializationID', 'int8', True, None),
        ('specializationName', 'varchar', False, None),
        ('averageProjectCostMax', 'numeric', False, None),
        ('averageProjectCostMin', 'numeric', False, None),
        ('description', 'text', False, None),
        ('minimumRate', 'numeric', False, None),
        ('rateType', 'varchar', False, None),
        ('skillLevel', 'varchar', False, None),
        ('is_custom', 'bool', False, None),
        ('created_by_agency_id', 'int8', False, 'accounts_agency'),
        ('created_by_worker_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['accounts_workerspecialization'] = [
        ('id', 'int8', True, None),
        ('experienceYears', 'int4', False, None),
        ('certification', 'varchar', False, None),
        ('skillType', 'varchar', False, None),
        ('displayOrder', 'int4', False, None),
        ('workerID_id', 'int8', False, 'accounts_workerprofile'),
        ('specializationID_id', 'int8', False, 'specializations'),
    ]

    tables['accounts_interestedjobs'] = [
        ('id', 'int8', True, None),
        ('clientID_id', 'int8', False, 'accounts_clientprofile'),
        ('specializationID_id', 'int8', False, 'specializations'),
    ]

    tables['accounts_wallet'] = [
        ('walletID', 'int8', True, None),
        ('balance', 'numeric', False, None),
        ('reservedBalance', 'numeric', False, None),
        ('pendingEarnings', 'numeric', False, None),
        ('autoWithdrawEnabled', 'bool', False, None),
        ('lastAutoWithdrawAt', 'timestamptz', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('accountFK_id', 'int8', False, 'accounts_accounts'),
        ('preferredPaymentMethodID_id', 'int8 nullable', False, 'accounts_userpaymentmethod'),
    ]

    tables['accounts_userpaymentmethod'] = [
        ('id', 'int8', True, None),
        ('methodType', 'varchar', False, None),
        ('accountName', 'varchar', False, None),
        ('accountNumber', 'varchar', False, None),
        ('bankName', 'varchar', False, None),
        ('bankCode', 'varchar', False, None),
        ('isPrimary', 'bool', False, None),
        ('isVerified', 'bool', False, None),
        ('paymongoRecipientId', 'varchar', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('accountFK_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['accounts_pushtoken'] = [
        ('tokenID', 'int8', True, None),
        ('pushToken', 'varchar UNIQUE', False, None),
        ('deviceType', 'varchar', False, None),
        ('isActive', 'bool', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('lastUsed', 'timestamptz', False, None),
        ('accountFK_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['accounts_notificationsettings'] = [
        ('settingsID', 'int8', True, None),
        ('pushEnabled', 'bool', False, None),
        ('soundEnabled', 'bool', False, None),
        ('jobUpdates', 'bool', False, None),
        ('messages', 'bool', False, None),
        ('payments', 'bool', False, None),
        ('reviews', 'bool', False, None),
        ('kycUpdates', 'bool', False, None),
        ('doNotDisturbStart', 'time', False, None),
        ('doNotDisturbEnd', 'time', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('accountFK_id', 'int8 UNIQUE', False, 'accounts_accounts'),
    ]

    positions = {
        'accounts_profile':              (0, 0),
        'accounts_workerprofile':        (8, 0),
        'accounts_clientprofile':        (16, 0),
        'accounts_agency':               (24, 0),
        'accounts_barangay':             (32, 0),
        'accounts_city':                 (40, 0),
        'specializations':               (16, -5.5),
        'accounts_workerspecialization':  (8, -5.5),
        'accounts_interestedjobs':       (24, -5.5),
        'accounts_wallet':               (0, -6),
        'accounts_userpaymentmethod':    (0, -10),
        'accounts_pushtoken':            (32, -5.5),
        'accounts_notificationsettings': (40, -5.5),
    }

    relationships = [
        ('accounts_workerprofile', 'profileID_id', 'accounts_profile', 'profileID', True),
        ('accounts_clientprofile', 'profileID_id', 'accounts_profile', 'profileID', True),
        ('accounts_barangay', 'city_id', 'accounts_city', 'cityID', False),
        ('specializations', 'created_by_agency_id', 'accounts_agency', 'agencyId', False),
        ('accounts_workerspecialization', 'workerID_id', 'accounts_workerprofile', 'id', False),
        ('accounts_workerspecialization', 'specializationID_id', 'specializations', 'specializationID', False),
        ('accounts_interestedjobs', 'clientID_id', 'accounts_clientprofile', 'id', False),
        ('accounts_interestedjobs', 'specializationID_id', 'specializations', 'specializationID', False),
        ('accounts_wallet', 'preferredPaymentMethodID_id', 'accounts_userpaymentmethod', 'id', False),
    ]

    generate_module(
        "MODULE 2 \u2014 Profiles, Location, Wallet & Specializations",
        13, tables, positions, relationships,
        'erd_v2_module2_profiles.png', figw=52, figh=18)


# ============================================================
# MODULE 3
# ============================================================

def gen_module3():
    tables = {}

    tables['jobs'] = [
        ('jobID', 'int8', True, None),
        ('title', 'varchar', False, None),
        ('description', 'text', False, None),
        ('budget', 'numeric', False, None),
        ('location', 'varchar', False, None),
        ('expectedDuration', 'varchar', False, None),
        ('urgency', 'varchar', False, None),
        ('preferredStartDate', 'date', False, None),
        ('materialsNeeded', 'jsonb', False, None),
        ('status', 'varchar', False, None),
        ('completedAt', 'timestamptz', False, None),
        ('cancellationReason', 'text', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('clientMarkedComplete', 'bool', False, None),
        ('clientMarkedCompleteAt', 'timestamptz', False, None),
        ('workerMarkedComplete', 'bool', False, None),
        ('workerMarkedCompleteAt', 'timestamptz', False, None),
        ('escrowAmount', 'numeric', False, None),
        ('escrowPaid', 'bool', False, None),
        ('escrowPaidAt', 'timestamptz', False, None),
        ('remainingPayment', 'numeric', False, None),
        ('remainingPaymentPaid', 'bool', False, None),
        ('remainingPaymentPaidAt', 'timestamptz', False, None),
        ('finalPaymentMethod', 'varchar', False, None),
        ('cashPaymentProofUrl', 'varchar', False, None),
        ('paymentMethodSelectedAt', 'timestamptz', False, None),
        ('cashProofUploadedAt', 'timestamptz', False, None),
        ('cashPaymentApproved', 'bool', False, None),
        ('cashPaymentApprovedAt', 'timestamptz', False, None),
        ('jobType', 'varchar', False, None),
        ('inviteRejectionReason', 'text', False, None),
        ('inviteRespondedAt', 'timestamptz', False, None),
        ('inviteStatus', 'varchar', False, None),
        ('clientConfirmedWorkStarted', 'bool', False, None),
        ('clientConfirmedWorkStartedAt', 'timestamptz', False, None),
        ('assignmentNotes', 'text', False, None),
        ('employeeAssignedAt', 'timestamptz', False, None),
        ('is_team_job', 'bool', False, None),
        ('budget_allocation_type', 'varchar', False, None),
        ('team_job_start_threshold', 'numeric', False, None),
        ('paymentReleaseDate', 'timestamptz', False, None),
        ('paymentReleasedToWorker', 'bool', False, None),
        ('paymentReleasedAt', 'timestamptz', False, None),
        ('paymentHeldReason', 'varchar', False, None),
        ('job_scope', 'varchar', False, None),
        ('skill_level_required', 'varchar', False, None),
        ('work_environment', 'varchar', False, None),
        ('payment_model', 'varchar', False, None),
        ('duration_days', 'int4', False, None),
        ('daily_rate_agreed', 'numeric', False, None),
        ('actual_start_date', 'date', False, None),
        ('total_days_worked', 'int4', False, None),
        ('daily_escrow_total', 'numeric', False, None),
        ('materialsCost', 'numeric', False, None),
        ('materials_status', 'varchar', False, None),
        ('scheduled_end_date', 'date', False, None),
        ('qa_day_offset', 'int4', False, None),
        ('workerMarkedOnTheWay', 'bool', False, None),
        ('workerMarkedOnTheWayAt', 'timestamptz', False, None),
        ('workerMarkedJobStarted', 'bool', False, None),
        ('workerMarkedJobStartedAt', 'timestamptz', False, None),
        ('is_early_completed', 'bool', False, None),
        ('early_completed_at', 'timestamptz', False, None),
        ('early_completion_payout', 'numeric', False, None),
        ('shift_type', 'varchar', False, None),
        ('cancelledAt', 'timestamptz', False, None),
        ('cancelledByRole', 'varchar', False, None),
        ('cancellationStage', 'varchar', False, None),
        ('clientRefundAmount', 'numeric', False, None),
        ('workerCompensationAmount', 'numeric', False, None),
        ('agency_flow_mode', 'varchar', False, None),
        ('clientID_id', 'int8', False, 'accounts_clientprofile'),
        ('assignedWorkerID_id', 'int8', False, 'accounts_workerprofile'),
        ('assignedAgencyFK_id', 'int8', False, 'accounts_agency'),
        ('assignedEmployeeID_id', 'int8', False, 'agency_employees'),
        ('categoryID_id', 'int8', False, 'specializations'),
        ('cancelledByAccountID_id', 'int8', False, 'accounts_accounts'),
        ('cashPaymentApprovedBy_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['job_skill_slots'] = [
        ('skillSlotID', 'int8', True, None),
        ('workers_needed', 'int4', False, None),
        ('budget_allocated', 'numeric', False, None),
        ('skill_level_required', 'varchar', False, None),
        ('status', 'varchar', False, None),
        ('notes', 'text', False, None),
        ('agency_invite_status', 'varchar', False, None),
        ('agency_invite_responded_at', 'timestamptz', False, None),
        ('last_rejected_agency_id', 'int8', False, None),
        ('last_rejected_agency_name', 'varchar', False, None),
        ('last_rejected_at', 'timestamptz', False, None),
        ('last_rejection_reason', 'text', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('jobID_id', 'int8', False, 'jobs'),
        ('specializationID_id', 'int8', False, 'specializations'),
        ('invited_agency_id', 'int8', False, 'accounts_agency'),
    ]

    tables['job_applications'] = [
        ('applicationID', 'int8', True, None),
        ('proposalMessage', 'text', False, None),
        ('proposedBudget', 'numeric', False, None),
        ('estimatedDuration', 'varchar', False, None),
        ('budgetOption', 'varchar', False, None),
        ('status', 'varchar', False, None),
        ('selected_materials', 'jsonb', False, None),
        ('proposed_daily_rate', 'numeric', False, None),
        ('proposed_days', 'int4', False, None),
        ('negotiation_count', 'int2', False, None),
        ('applied_shift', 'varchar', False, None),
        ('clientRejectionReason', 'text', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('jobID_id', 'int8', False, 'jobs'),
        ('workerID_id', 'int8', False, 'accounts_workerprofile'),
        ('applied_skill_slot_id', 'int8', False, 'job_skill_slots'),
    ]

    tables['price_negotiations'] = [
        ('negotiationID', 'int8', True, None),
        ('actor', 'varchar', False, None),
        ('round_number', 'int2', False, None),
        ('proposed_budget', 'numeric', False, None),
        ('proposed_daily_rate', 'numeric', False, None),
        ('proposed_days', 'int4', False, None),
        ('message', 'text', False, None),
        ('status', 'varchar', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('application_id', 'int8', False, 'job_applications'),
    ]

    tables['job_worker_assignments'] = [
        ('assignmentID', 'int8', True, None),
        ('slot_position', 'int4', False, None),
        ('assignment_status', 'varchar', False, None),
        ('worker_marked_complete', 'bool', False, None),
        ('worker_marked_complete_at', 'timestamptz', False, None),
        ('completion_notes', 'text', False, None),
        ('individual_rating', 'numeric', False, None),
        ('client_confirmed_arrival', 'bool', False, None),
        ('client_confirmed_arrival_at', 'timestamptz', False, None),
        ('daily_rate_at_assignment', 'numeric', False, None),
        ('days_worked', 'int4', False, None),
        ('total_earned', 'numeric', False, None),
        ('early_completed', 'bool', False, None),
        ('early_completed_at', 'timestamptz', False, None),
        ('early_completion_payout', 'numeric', False, None),
        ('assigned_shift', 'varchar', False, None),
        ('assignedAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('jobID_id', 'int8', False, 'jobs'),
        ('skillSlotID_id', 'int8', False, 'job_skill_slots'),
        ('workerID_id', 'int8', False, 'accounts_workerprofile'),
    ]

    tables['job_employee_assignments'] = [
        ('assignmentID', 'int8', True, None),
        ('notes', 'text', False, None),
        ('isPrimaryContact', 'bool', False, None),
        ('status', 'varchar', False, None),
        ('employeeMarkedComplete', 'bool', False, None),
        ('employeeMarkedCompleteAt', 'timestamptz', False, None),
        ('completionNotes', 'text', False, None),
        ('dispatched', 'bool', False, None),
        ('dispatchedAt', 'timestamptz', False, None),
        ('clientConfirmedArrival', 'bool', False, None),
        ('clientConfirmedArrivalAt', 'timestamptz', False, None),
        ('agencyMarkedComplete', 'bool', False, None),
        ('agencyMarkedCompleteAt', 'timestamptz', False, None),
        ('paymentAmount', 'numeric', False, None),
        ('clientApproved', 'bool', False, None),
        ('clientApprovedAt', 'timestamptz', False, None),
        ('early_completed', 'bool', False, None),
        ('early_completed_at', 'timestamptz', False, None),
        ('early_completion_payout', 'numeric', False, None),
        ('assignedAt', 'timestamptz', False, None),
        ('job_id', 'int8', False, 'jobs'),
        ('employee_id', 'int8', False, 'agency_employees'),
        ('skill_slot_id', 'int8', False, 'job_skill_slots'),
        ('assignedBy_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['job_logs'] = [
        ('logID', 'int8', True, None),
        ('oldStatus', 'varchar', False, None),
        ('newStatus', 'varchar', False, None),
        ('notes', 'text', False, None),
        ('actionType', 'varchar', False, None),
        ('metadata', 'jsonb', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('jobID_id', 'int8', False, 'jobs'),
        ('changedBy_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['saved_jobs'] = [
        ('savedJobID', 'int8', True, None),
        ('savedAt', 'timestamptz', False, None),
        ('jobID_id', 'int8', False, 'jobs'),
        ('workerID_id', 'int8', False, 'accounts_workerprofile'),
    ]

    positions = {
        'jobs':                     (0, 0),
        'job_skill_slots':          (8, 0),
        'job_applications':         (16, 0),
        'price_negotiations':       (24, 0),
        'job_worker_assignments':   (8, -7),
        'job_employee_assignments': (16, -7),
        'job_logs':                 (24, -5),
        'saved_jobs':               (32, 0),
    }

    relationships = [
        ('job_skill_slots', 'jobID_id', 'jobs', 'jobID', False),
        ('job_applications', 'jobID_id', 'jobs', 'jobID', False),
        ('job_applications', 'applied_skill_slot_id', 'job_skill_slots', 'skillSlotID', False),
        ('price_negotiations', 'application_id', 'job_applications', 'applicationID', False),
        ('job_worker_assignments', 'jobID_id', 'jobs', 'jobID', False),
        ('job_worker_assignments', 'skillSlotID_id', 'job_skill_slots', 'skillSlotID', False),
        ('job_employee_assignments', 'job_id', 'jobs', 'jobID', False),
        ('job_employee_assignments', 'skill_slot_id', 'job_skill_slots', 'skillSlotID', False),
        ('job_logs', 'jobID_id', 'jobs', 'jobID', False),
        ('saved_jobs', 'jobID_id', 'jobs', 'jobID', False),
    ]

    generate_module(
        "MODULE 3 \u2014 Jobs, Applications & Assignments",
        8, tables, positions, relationships,
        'erd_v2_module3_jobs.png', figw=44, figh=30)


# ============================================================
# MODULE 4
# ============================================================

def gen_module4():
    tables = {}

    tables['job_disputes'] = [
        ('disputeID', 'int8', True, None),
        ('disputedBy', 'varchar', False, None),
        ('reason', 'varchar', False, None),
        ('description', 'text', False, None),
        ('status', 'varchar', False, None),
        ('priority', 'varchar', False, None),
        ('jobAmount', 'numeric', False, None),
        ('disputedAmount', 'numeric', False, None),
        ('resolution', 'text', False, None),
        ('resolvedDate', 'timestamptz', False, None),
        ('assignedTo', 'varchar', False, None),
        ('openedDate', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('backjobStarted', 'bool', False, None),
        ('backjobStartedAt', 'timestamptz', False, None),
        ('clientConfirmedBackjob', 'bool', False, None),
        ('clientConfirmedBackjobAt', 'timestamptz', False, None),
        ('workerMarkedBackjobComplete', 'bool', False, None),
        ('workerMarkedBackjobCompleteAt', 'timestamptz', False, None),
        ('termsAccepted', 'bool', False, None),
        ('termsVersion', 'varchar', False, None),
        ('termsAcceptedAt', 'timestamptz', False, None),
        ('adminRejectedAt', 'timestamptz', False, None),
        ('adminRejectionReason', 'text', False, None),
        ('in_negotiation_at', 'timestamptz', False, None),
        ('scheduled_date', 'date', False, None),
        ('workerScheduleConfirmed', 'bool', False, None),
        ('workerScheduleConfirmedAt', 'timestamptz', False, None),
        ('jobID_id', 'int8', False, 'jobs'),
    ]

    tables['dispute_evidence'] = [
        ('evidenceID', 'int8', True, None),
        ('imageURL', 'varchar', False, None),
        ('description', 'text', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('disputeID_id', 'int8', False, 'job_disputes'),
        ('uploadedBy_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['backjob_schedule_confirmations'] = [
        ('confirmationID', 'int8', True, None),
        ('confirmed', 'bool', False, None),
        ('confirmedAt', 'timestamptz', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('disputeID_id', 'int8', False, 'job_disputes'),
        ('assignmentID_id', 'int8', False, 'job_worker_assignments'),
        ('confirmedBy_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['job_reviews'] = [
        ('reviewID', 'int8', True, None),
        ('reviewerType', 'varchar', False, None),
        ('rating', 'numeric', False, None),
        ('comment', 'text', False, None),
        ('status', 'varchar', False, None),
        ('isFlagged', 'bool', False, None),
        ('flagReason', 'text', False, None),
        ('flaggedAt', 'timestamptz', False, None),
        ('helpfulCount', 'int4', False, None),
        ('rating_communication', 'numeric', False, None),
        ('rating_professionalism', 'numeric', False, None),
        ('rating_punctuality', 'numeric', False, None),
        ('rating_quality', 'numeric', False, None),
        ('agency_response', 'text', False, None),
        ('agency_response_at', 'timestamptz', False, None),
        ('backjob_edit_deadline', 'timestamptz', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('jobID_id', 'int8', False, 'jobs'),
        ('reviewerID_id', 'int8', False, 'accounts_accounts'),
        ('revieweeID_id', 'int8', False, 'accounts_accounts'),
        ('revieweeProfileID_id', 'int8', False, 'accounts_profile'),
        ('revieweeAgencyID_id', 'int8', False, 'accounts_agency'),
        ('revieweeEmployeeID_id', 'int8', False, 'agency_employees'),
        ('flaggedBy_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['review_skill_tags'] = [
        ('tagID', 'int8', True, None),
        ('createdAt', 'timestamptz', False, None),
        ('reviewID_id', 'int8', False, 'job_reviews'),
        ('workerSpecializationID_id', 'int8', False, 'accounts_workerspecialization'),
    ]

    tables['job_materials'] = [
        ('jobMaterialID', 'int8', True, None),
        ('name', 'varchar', False, None),
        ('description', 'text', False, None),
        ('quantity', 'int4', False, None),
        ('unit', 'varchar', False, None),
        ('source', 'varchar', False, None),
        ('purchase_price', 'numeric', False, None),
        ('receipt_image_url', 'varchar', False, None),
        ('client_approved', 'bool', False, None),
        ('client_approved_at', 'timestamptz', False, None),
        ('client_rejected', 'bool', False, None),
        ('rejection_reason', 'text', False, None),
        ('added_by', 'varchar', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('jobID_id', 'int8', False, 'jobs'),
        ('workerMaterialID_id', 'int8', False, 'worker_materials'),
    ]

    tables['job_photos'] = [
        ('photoID', 'int8', True, None),
        ('photoURL', 'varchar', False, None),
        ('fileName', 'varchar', False, None),
        ('uploadedAt', 'timestamptz', False, None),
        ('jobID_id', 'int8', False, 'jobs'),
    ]

    tables['daily_attendance'] = [
        ('attendanceID', 'int8', True, None),
        ('date', 'date', False, None),
        ('time_in', 'timestamptz', False, None),
        ('time_out', 'timestamptz', False, None),
        ('status', 'varchar', False, None),
        ('worker_confirmed', 'bool', False, None),
        ('worker_confirmed_at', 'timestamptz', False, None),
        ('client_confirmed', 'bool', False, None),
        ('client_confirmed_at', 'timestamptz', False, None),
        ('amount_earned', 'numeric', False, None),
        ('payment_processed', 'bool', False, None),
        ('payment_processed_at', 'timestamptz', False, None),
        ('notes', 'text', False, None),
        ('absent_penalty_amount', 'numeric', False, None),
        ('absent_penalty_applied', 'bool', False, None),
        ('absent_penalty_applied_at', 'timestamptz', False, None),
        ('absent_penalty_percent', 'numeric', False, None),
        ('cash_payment_proof_url', 'varchar', False, None),
        ('cash_payment_verified', 'bool', False, None),
        ('cash_payment_verified_at', 'timestamptz', False, None),
        ('cash_proof_uploaded_at', 'timestamptz', False, None),
        ('payment_method', 'varchar', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('jobID_id', 'int8', False, 'jobs'),
        ('workerID_id', 'int8', False, 'accounts_workerprofile'),
        ('assignmentID_id', 'int8', False, 'job_worker_assignments'),
        ('employeeID_id', 'int8', False, 'agency_employees'),
    ]

    tables['daily_job_extensions'] = [
        ('extensionID', 'int8', True, None),
        ('additional_days', 'int4', False, None),
        ('additional_escrow', 'numeric', False, None),
        ('reason', 'text', False, None),
        ('status', 'varchar', False, None),
        ('requested_by', 'varchar', False, None),
        ('client_approved', 'bool', False, None),
        ('client_approved_at', 'timestamptz', False, None),
        ('worker_approved', 'bool', False, None),
        ('worker_approved_at', 'timestamptz', False, None),
        ('escrow_collected', 'bool', False, None),
        ('escrow_collected_at', 'timestamptz', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('jobID_id', 'int8', False, 'jobs'),
        ('requestedByUser_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['daily_rate_changes'] = [
        ('changeID', 'int8', True, None),
        ('old_rate', 'numeric', False, None),
        ('new_rate', 'numeric', False, None),
        ('reason', 'text', False, None),
        ('effective_date', 'date', False, None),
        ('status', 'varchar', False, None),
        ('requested_by', 'varchar', False, None),
        ('client_approved', 'bool', False, None),
        ('client_approved_at', 'timestamptz', False, None),
        ('worker_approved', 'bool', False, None),
        ('worker_approved_at', 'timestamptz', False, None),
        ('escrow_adjusted', 'bool', False, None),
        ('escrow_adjustment_amount', 'numeric', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('jobID_id', 'int8', False, 'jobs'),
        ('requestedByUser_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['daily_skip_day_requests'] = [
        ('skipRequestID', 'int8', True, None),
        ('request_date', 'date', False, None),
        ('status', 'varchar', False, None),
        ('requested_by', 'varchar', False, None),
        ('requested_account_ids', 'jsonb', False, None),
        ('requested_count', 'int4', False, None),
        ('total_required', 'int4', False, None),
        ('requires_all_team_workers', 'bool', False, None),
        ('all_workers_requested', 'bool', False, None),
        ('reviewedAt', 'timestamptz', False, None),
        ('client_rejection_reason', 'text', False, None),
        ('target_type', 'varchar', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('jobID_id', 'int8', False, 'jobs'),
        ('requestedByUser_id', 'int8', False, 'accounts_accounts'),
        ('reviewedByUser_id', 'int8', False, 'accounts_accounts'),
        ('target_employee_id', 'int8', False, 'agency_employees'),
        ('target_worker_account_id', 'int8', False, 'accounts_accounts'),
    ]

    positions = {
        'job_disputes':                    (0, 0),
        'dispute_evidence':                (8, 0),
        'backjob_schedule_confirmations':  (8, -3),
        'job_reviews':                     (16, 0),
        'review_skill_tags':               (24, 0),
        'job_materials':                   (0, -10),
        'job_photos':                      (8, -6),
        'daily_attendance':                (16, -8.5),
        'daily_job_extensions':            (24, -3),
        'daily_rate_changes':              (32, 0),
        'daily_skip_day_requests':         (32, -6.5),
    }

    relationships = [
        ('dispute_evidence', 'disputeID_id', 'job_disputes', 'disputeID', False),
        ('backjob_schedule_confirmations', 'disputeID_id', 'job_disputes', 'disputeID', False),
        ('review_skill_tags', 'reviewID_id', 'job_reviews', 'reviewID', False),
    ]

    generate_module(
        "MODULE 4 \u2014 Disputes, Reviews, Daily Operations & Attendance",
        11, tables, positions, relationships,
        'erd_v2_module4_disputes.png', figw=44, figh=22)


# ============================================================
# MODULE 5
# ============================================================

def gen_module5():
    tables = {}

    tables['accounts_kyc'] = [
        ('kycID', 'int8', True, None),
        ('kyc_status', 'varchar', False, None),
        ('reviewedAt', 'timestamptz', False, None),
        ('notes', 'text', False, None),
        ('rejectionCategory', 'varchar', False, None),
        ('rejectionReason', 'text', False, None),
        ('resubmissionCount', 'int4', False, None),
        ('maxResubmissions', 'int4', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('accountFK_id', 'int8', False, 'accounts_accounts'),
        ('reviewedBy_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['accounts_kycfiles'] = [
        ('kycFileID', 'int8', True, None),
        ('idType', 'varchar', False, None),
        ('fileURL', 'varchar', False, None),
        ('fileName', 'varchar', False, None),
        ('fileSize', 'int4', False, None),
        ('uploadedAt', 'timestamptz', False, None),
        ('ai_verification_status', 'varchar', False, None),
        ('face_detected', 'bool', False, None),
        ('face_count', 'int4', False, None),
        ('face_confidence', 'float8', False, None),
        ('ocr_text', 'text', False, None),
        ('ocr_confidence', 'float8', False, None),
        ('quality_score', 'float8', False, None),
        ('ai_confidence_score', 'float8', False, None),
        ('ai_rejection_reason', 'varchar', False, None),
        ('ai_rejection_message', 'varchar', False, None),
        ('ai_warnings', 'jsonb', False, None),
        ('ai_details', 'jsonb', False, None),
        ('verified_at', 'timestamptz', False, None),
        ('kycID_id', 'int8', False, 'accounts_kyc'),
    ]

    tables['kyc_extracted_data'] = [
        ('extractedDataID', 'int8', True, None),
        ('extracted_full_name', 'varchar', False, None),
        ('extracted_first_name', 'varchar', False, None),
        ('extracted_middle_name', 'varchar', False, None),
        ('extracted_last_name', 'varchar', False, None),
        ('extracted_birth_date', 'date', False, None),
        ('extracted_address', 'text', False, None),
        ('extracted_id_number', 'varchar', False, None),
        ('extracted_id_type', 'varchar', False, None),
        ('extracted_expiry_date', 'date', False, None),
        ('extracted_nationality', 'varchar', False, None),
        ('extracted_sex', 'varchar', False, None),
        ('extracted_place_of_birth', 'varchar', False, None),
        ('extracted_clearance_number', 'varchar', False, None),
        ('extracted_clearance_type', 'varchar', False, None),
        ('extracted_clearance_issue_date', 'date', False, None),
        ('extracted_clearance_validity_date', 'date', False, None),
        ('confirmed_full_name', 'varchar', False, None),
        ('confirmed_first_name', 'varchar', False, None),
        ('confirmed_middle_name', 'varchar', False, None),
        ('confirmed_last_name', 'varchar', False, None),
        ('confirmed_birth_date', 'date', False, None),
        ('confirmed_address', 'text', False, None),
        ('confirmed_id_number', 'varchar', False, None),
        ('confirmed_nationality', 'varchar', False, None),
        ('confirmed_sex', 'varchar', False, None),
        ('confirmed_place_of_birth', 'varchar', False, None),
        ('confirmed_clearance_number', 'varchar', False, None),
        ('confirmed_clearance_type', 'varchar', False, None),
        ('confirmed_clearance_issue_date', 'date', False, None),
        ('confirmed_clearance_validity_date', 'date', False, None),
        ('confidence_full_name', 'float8', False, None),
        ('confidence_birth_date', 'float8', False, None),
        ('confidence_address', 'float8', False, None),
        ('confidence_id_number', 'float8', False, None),
        ('confidence_place_of_birth', 'float8', False, None),
        ('confidence_clearance_number', 'float8', False, None),
        ('overall_confidence', 'float8', False, None),
        ('extraction_status', 'varchar', False, None),
        ('extraction_source', 'varchar', False, None),
        ('extracted_at', 'timestamptz', False, None),
        ('confirmed_at', 'timestamptz', False, None),
        ('face_match_completed', 'bool', False, None),
        ('face_match_score', 'float8', False, None),
        ('raw_extraction_data', 'jsonb', False, None),
        ('user_edited_fields', 'jsonb', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('kycID_id', 'int8 UNIQUE', False, 'accounts_kyc'),
    ]

    tables['agency_agencykyc'] = [
        ('agencyKycID', 'int8', True, None),
        ('status', 'varchar', False, None),
        ('reviewedAt', 'timestamptz', False, None),
        ('notes', 'varchar', False, None),
        ('rejectionCategory', 'varchar', False, None),
        ('rejectionReason', 'text', False, None),
        ('resubmissionCount', 'int4', False, None),
        ('maxResubmissions', 'int4', False, None),
        ('face_similarity_score', 'float8', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('accountFK_id', 'int8', False, 'accounts_accounts'),
        ('reviewedBy_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['agency_agencykycfile'] = [
        ('fileID', 'int8', True, None),
        ('fileType', 'varchar', False, None),
        ('fileURL', 'varchar', False, None),
        ('fileName', 'varchar', False, None),
        ('fileSize', 'int4', False, None),
        ('uploadedAt', 'timestamptz', False, None),
        ('ai_verification_status', 'varchar', False, None),
        ('face_detected', 'bool', False, None),
        ('face_count', 'int4', False, None),
        ('face_confidence', 'float8', False, None),
        ('ocr_text', 'text', False, None),
        ('ocr_confidence', 'float8', False, None),
        ('quality_score', 'float8', False, None),
        ('ai_confidence_score', 'float8', False, None),
        ('ai_rejection_reason', 'varchar', False, None),
        ('ai_rejection_message', 'varchar', False, None),
        ('ai_warnings', 'jsonb', False, None),
        ('ai_details', 'jsonb', False, None),
        ('verified_at', 'timestamptz', False, None),
        ('agencyKyc_id', 'int8', False, 'agency_agencykyc'),
    ]

    tables['agency_kyc_extracted_data'] = [
        ('extractedDataID', 'int8', True, None),
        ('extracted_business_name', 'varchar', False, None),
        ('extracted_business_type', 'varchar', False, None),
        ('extracted_business_address', 'text', False, None),
        ('extracted_permit_number', 'varchar', False, None),
        ('extracted_permit_issue_date', 'date', False, None),
        ('extracted_permit_expiry_date', 'date', False, None),
        ('extracted_dti_number', 'varchar', False, None),
        ('extracted_sec_number', 'varchar', False, None),
        ('extracted_tin', 'varchar', False, None),
        ('extracted_rep_full_name', 'varchar', False, None),
        ('extracted_rep_id_number', 'varchar', False, None),
        ('extracted_rep_id_type', 'varchar', False, None),
        ('extracted_rep_birth_date', 'date', False, None),
        ('extracted_rep_address', 'text', False, None),
        ('confirmed_business_name', 'varchar', False, None),
        ('confirmed_business_type', 'varchar', False, None),
        ('confirmed_business_address', 'text', False, None),
        ('confirmed_permit_number', 'varchar', False, None),
        ('confirmed_permit_issue_date', 'date', False, None),
        ('confirmed_permit_expiry_date', 'date', False, None),
        ('confirmed_dti_number', 'varchar', False, None),
        ('confirmed_sec_number', 'varchar', False, None),
        ('confirmed_tin', 'varchar', False, None),
        ('confirmed_rep_full_name', 'varchar', False, None),
        ('confirmed_rep_id_number', 'varchar', False, None),
        ('confirmed_rep_birth_date', 'date', False, None),
        ('confirmed_rep_address', 'text', False, None),
        ('confidence_business_name', 'float8', False, None),
        ('confidence_business_address', 'float8', False, None),
        ('confidence_permit_number', 'float8', False, None),
        ('confidence_rep_name', 'float8', False, None),
        ('overall_confidence', 'float8', False, None),
        ('extraction_status', 'varchar', False, None),
        ('extraction_source', 'varchar', False, None),
        ('extracted_at', 'timestamptz', False, None),
        ('confirmed_at', 'timestamptz', False, None),
        ('raw_extraction_data', 'jsonb', False, None),
        ('user_edited_fields', 'jsonb', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('agencyKyc_id', 'int8 UNIQUE', False, 'agency_agencykyc'),
    ]

    tables['adminpanel_kyclogs'] = [
        ('kycLogID', 'int8', True, None),
        ('action', 'varchar', False, None),
        ('reviewedAt', 'timestamptz', False, None),
        ('reason', 'text', False, None),
        ('userEmail', 'varchar', False, None),
        ('userAccountID', 'int8', False, None),
        ('kycID', 'int8', False, None),
        ('kycType', 'varchar', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('accountFK_id', 'int8', False, 'accounts_accounts'),
        ('reviewedBy_id', 'int8', False, 'accounts_accounts'),
    ]

    positions = {
        'accounts_kyc':              (0, 0),
        'accounts_kycfiles':         (8, 0),
        'kyc_extracted_data':        (16, 0),
        'agency_agencykyc':          (0, -6),
        'agency_agencykycfile':      (8, -6),
        'agency_kyc_extracted_data': (16, -6),
        'adminpanel_kyclogs':        (26, 0),
    }

    relationships = [
        ('accounts_kycfiles', 'kycID_id', 'accounts_kyc', 'kycID', False),
        ('kyc_extracted_data', 'kycID_id', 'accounts_kyc', 'kycID', True),
        ('agency_agencykycfile', 'agencyKyc_id', 'agency_agencykyc', 'agencyKycID', False),
        ('agency_kyc_extracted_data', 'agencyKyc_id', 'agency_agencykyc', 'agencyKycID', True),
    ]

    generate_module(
        "MODULE 5 \u2014 KYC Verification (Individual & Agency)",
        7, tables, positions, relationships,
        'erd_v2_module5_kyc.png', figw=38, figh=22)


# ============================================================
# MODULE 6
# ============================================================

def gen_module6():
    tables = {}

    tables['adminpanel_adminaccount'] = [
        ('adminID', 'int8', True, None),
        ('role', 'varchar', False, None),
        ('permissions', 'jsonb', False, None),
        ('isActive', 'bool', False, None),
        ('lastLogin', 'timestamptz', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('accountFK_id', 'int8 UNIQUE', False, 'accounts_accounts'),
    ]

    tables['adminpanel_auditlog'] = [
        ('auditLogID', 'int8', True, None),
        ('adminEmail', 'varchar', False, None),
        ('action', 'varchar', False, None),
        ('entityType', 'varchar', False, None),
        ('entityID', 'varchar', False, None),
        ('details', 'jsonb', False, None),
        ('beforeValue', 'jsonb', False, None),
        ('afterValue', 'jsonb', False, None),
        ('ipAddress', 'inet', False, None),
        ('userAgent', 'text', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('adminFK_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['adminpanel_supportticket'] = [
        ('ticketID', 'int8', True, None),
        ('subject', 'varchar', False, None),
        ('category', 'varchar', False, None),
        ('priority', 'varchar', False, None),
        ('status', 'varchar', False, None),
        ('ticketType', 'varchar', False, None),
        ('platform', 'varchar', False, None),
        ('deviceInfo', 'text', False, None),
        ('appVersion', 'varchar', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('lastReplyAt', 'timestamptz', False, None),
        ('resolvedAt', 'timestamptz', False, None),
        ('userFK_id', 'int8', False, 'accounts_accounts'),
        ('assignedTo_id', 'int8', False, 'accounts_accounts'),
        ('agencyFK_id', 'int8', False, 'accounts_agency'),
    ]

    tables['adminpanel_supportticketreply'] = [
        ('replyID', 'int8', True, None),
        ('content', 'text', False, None),
        ('isSystemMessage', 'bool', False, None),
        ('attachmentURL', 'varchar', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('ticketFK_id', 'int8', False, 'adminpanel_supportticket'),
        ('senderFK_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['adminpanel_userreport'] = [
        ('reportID', 'int8', True, None),
        ('reportType', 'varchar', False, None),
        ('reason', 'varchar', False, None),
        ('description', 'text', False, None),
        ('relatedContentID', 'int8', False, None),
        ('status', 'varchar', False, None),
        ('adminNotes', 'text', False, None),
        ('actionTaken', 'varchar', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('resolvedAt', 'timestamptz', False, None),
        ('reporterFK_id', 'int8', False, 'accounts_accounts'),
        ('reportedUserFK_id', 'int8', False, 'accounts_accounts'),
        ('reviewedBy_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['adminpanel_platformsettings'] = [
        ('settingsID', 'int8', True, None),
        ('platformFeePercentage', 'numeric', False, None),
        ('escrowHoldingDays', 'int4', False, None),
        ('maxJobBudget', 'numeric', False, None),
        ('minJobBudget', 'numeric', False, None),
        ('workerVerificationRequired', 'bool', False, None),
        ('autoApproveKYC', 'bool', False, None),
        ('kycDocumentExpiryDays', 'int4', False, None),
        ('maintenanceMode', 'bool', False, None),
        ('sessionTimeoutMinutes', 'int4', False, None),
        ('maxUploadSizeMB', 'int4', False, None),
        ('kycAutoApproveMinConfidence', 'numeric', False, None),
        ('kycFaceMatchMinSimilarity', 'numeric', False, None),
        ('kycRequireUserConfirmation', 'bool', False, None),
        ('lastUpdated', 'timestamptz', False, None),
        ('updatedBy_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['adminpanel_cannedresponse'] = [
        ('responseID', 'int8', True, None),
        ('title', 'varchar', False, None),
        ('content', 'text', False, None),
        ('category', 'varchar', False, None),
        ('shortcuts', 'jsonb', False, None),
        ('usageCount', 'int4', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('createdBy_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['adminpanel_contentmoderationterm'] = [
        ('termID', 'int8', True, None),
        ('term', 'varchar', False, None),
        ('normalizedTerm', 'varchar UNIQUE', False, None),
        ('isActive', 'bool', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('createdBy_id', 'int8', False, 'accounts_accounts'),
        ('updatedBy_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['adminpanel_faq'] = [
        ('faqID', 'int8', True, None),
        ('question', 'varchar', False, None),
        ('answer', 'text', False, None),
        ('category', 'varchar', False, None),
        ('sortOrder', 'int4', False, None),
        ('viewCount', 'int4', False, None),
        ('isPublished', 'bool', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
    ]

    tables['adminpanel_systemroles'] = [
        ('systemRoleID', 'int8', True, None),
        ('systemRole', 'varchar', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('accountID_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['accounts_notification'] = [
        ('notificationID', 'int8', True, None),
        ('notificationType', 'varchar', False, None),
        ('title', 'varchar', False, None),
        ('message', 'text', False, None),
        ('isRead', 'bool', False, None),
        ('relatedKYCLogID', 'int8', False, None),
        ('relatedJobID', 'int8', False, None),
        ('relatedApplicationID', 'int8', False, None),
        ('profile_type', 'varchar', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('readAt', 'timestamptz', False, None),
        ('accountFK_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['conversation'] = [
        ('conversationID', 'int8', True, None),
        ('lastMessageText', 'text', False, None),
        ('lastMessageTime', 'timestamptz', False, None),
        ('unreadCountClient', 'int4', False, None),
        ('unreadCountWorker', 'int4', False, None),
        ('status', 'varchar', False, None),
        ('archivedByClient', 'bool', False, None),
        ('archivedByWorker', 'bool', False, None),
        ('conversation_type', 'varchar', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('client_id', 'int8', False, 'accounts_profile'),
        ('worker_id', 'int8', False, 'accounts_profile'),
        ('agency_id', 'int8', False, 'accounts_agency'),
        ('relatedJobPosting_id', 'int8', False, 'jobs'),
        ('lastMessageSender_id', 'int8', False, 'accounts_profile'),
    ]

    tables['conversation_participants'] = [
        ('participantID', 'int8', True, None),
        ('participant_type', 'varchar', False, None),
        ('unread_count', 'int4', False, None),
        ('is_archived', 'bool', False, None),
        ('joined_at', 'timestamptz', False, None),
        ('last_read_at', 'timestamptz', False, None),
        ('conversation_id', 'int8', False, 'conversation'),
        ('profile_id', 'int8', False, 'accounts_profile'),
        ('skill_slot_id', 'int8', False, 'job_skill_slots'),
        ('admin_account_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['message'] = [
        ('messageID', 'int8', True, None),
        ('messageText', 'text', False, None),
        ('messageType', 'varchar', False, None),
        ('locationAddress', 'varchar', False, None),
        ('locationLandmark', 'varchar', False, None),
        ('locationLatitude', 'numeric', False, None),
        ('locationLongitude', 'numeric', False, None),
        ('isRead', 'bool', False, None),
        ('readAt', 'timestamptz', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('conversationID_id', 'int8', False, 'conversation'),
        ('sender_id', 'int8', False, 'accounts_profile'),
        ('senderAgency_id', 'int8', False, 'accounts_agency'),
        ('sender_admin_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['message_attachment'] = [
        ('attachmentID', 'int8', True, None),
        ('fileURL', 'varchar', False, None),
        ('fileName', 'varchar', False, None),
        ('fileSize', 'int4', False, None),
        ('fileType', 'varchar', False, None),
        ('uploadedAt', 'timestamptz', False, None),
        ('messageID_id', 'int8', False, 'message'),
    ]

    tables['accounts_transaction'] = [
        ('transactionID', 'int8', True, None),
        ('transactionType', 'varchar', False, None),
        ('amount', 'numeric', False, None),
        ('balanceAfter', 'numeric', False, None),
        ('status', 'varchar', False, None),
        ('description', 'varchar', False, None),
        ('referenceNumber', 'varchar', False, None),
        ('paymentMethod', 'varchar', False, None),
        ('invoiceURL', 'varchar', False, None),
        ('xenditExternalID', 'varchar', False, None),
        ('xenditInvoiceID', 'varchar', False, None),
        ('xenditPaymentChannel', 'varchar', False, None),
        ('xenditPaymentID', 'varchar', False, None),
        ('xenditPaymentMethod', 'varchar', False, None),
        ('adminReferenceNumber', 'varchar', False, None),
        ('paymongoPaymentId', 'varchar', False, None),
        ('paymongoTransferId', 'varchar', False, None),
        ('paymongoTransferStatus', 'varchar', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('completedAt', 'timestamptz', False, None),
        ('processedAt', 'timestamptz', False, None),
        ('walletID_id', 'int8', False, 'accounts_wallet'),
        ('relatedJobPosting_id', 'int8', False, 'jobs'),
        ('processedByAdmin_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['agency_employees'] = [
        ('employeeID', 'int8', True, None),
        ('name', 'varchar', False, None),
        ('firstName', 'varchar', False, None),
        ('middleName', 'varchar', False, None),
        ('lastName', 'varchar', False, None),
        ('email', 'varchar', False, None),
        ('mobile', 'varchar', False, None),
        ('role', 'varchar', False, None),
        ('avatar', 'varchar', False, None),
        ('rating', 'numeric', False, None),
        ('specializations', 'text', False, None),
        ('hourly_rate', 'numeric', False, None),
        ('daily_rate', 'numeric', False, None),
        ('is_available_daily_jobs', 'bool', False, None),
        ('employeeOfTheMonth', 'bool', False, None),
        ('employeeOfTheMonthDate', 'timestamptz', False, None),
        ('employeeOfTheMonthReason', 'text', False, None),
        ('isActive', 'bool', False, None),
        ('lastRatingUpdate', 'timestamptz', False, None),
        ('totalEarnings', 'numeric', False, None),
        ('totalJobsCompleted', 'int4', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('agency_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['worker_certifications'] = [
        ('certificationID', 'int8', True, None),
        ('name', 'varchar', False, None),
        ('issuing_organization', 'varchar', False, None),
        ('issue_date', 'date', False, None),
        ('expiry_date', 'date', False, None),
        ('certificate_url', 'varchar', False, None),
        ('is_verified', 'bool', False, None),
        ('verified_at', 'timestamptz', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('workerID_id', 'int8', False, 'accounts_workerprofile'),
        ('specializationID_id', 'int8', False, 'accounts_workerspecialization'),
        ('verified_by_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['certification_logs'] = [
        ('certLogID', 'int8', True, None),
        ('certificationID', 'int8', False, None),
        ('action', 'varchar', False, None),
        ('reviewedAt', 'timestamptz', False, None),
        ('reason', 'text', False, None),
        ('workerEmail', 'varchar', False, None),
        ('workerAccountID', 'int8', False, None),
        ('certificationName', 'varchar', False, None),
        ('workerID_id', 'int8', False, 'accounts_workerprofile'),
        ('reviewedBy_id', 'int8', False, 'accounts_accounts'),
    ]

    tables['worker_materials'] = [
        ('materialID', 'int8', True, None),
        ('name', 'varchar', False, None),
        ('description', 'text', False, None),
        ('price', 'numeric', False, None),
        ('unit', 'varchar', False, None),
        ('image_url', 'varchar', False, None),
        ('is_available', 'bool', False, None),
        ('quantity', 'numeric', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('workerID_id', 'int8', False, 'accounts_workerprofile'),
        ('agencyID_id', 'int8', False, 'accounts_agency'),
        ('categoryID_id', 'int8', False, 'specializations'),
    ]

    tables['worker_portfolio'] = [
        ('portfolioID', 'int8', True, None),
        ('image_url', 'varchar', False, None),
        ('caption', 'text', False, None),
        ('display_order', 'int4', False, None),
        ('file_name', 'varchar', False, None),
        ('file_size', 'int4', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('workerID_id', 'int8', False, 'accounts_workerprofile'),
    ]

    tables['profiles_workerproduct'] = [
        ('productID', 'int8', True, None),
        ('productName', 'varchar', False, None),
        ('description', 'text', False, None),
        ('price', 'numeric', False, None),
        ('priceUnit', 'varchar', False, None),
        ('inStock', 'bool', False, None),
        ('stockQuantity', 'int4', False, None),
        ('productImage', 'varchar', False, None),
        ('isActive', 'bool', False, None),
        ('createdAt', 'timestamptz', False, None),
        ('updatedAt', 'timestamptz', False, None),
        ('workerID_id', 'int8', False, 'accounts_workerprofile'),
        ('categoryID_id', 'int8', False, 'specializations'),
    ]

    positions = {
        'adminpanel_adminaccount':          (0, 0),
        'adminpanel_auditlog':              (8, 0),
        'adminpanel_supportticket':         (16, 0),
        'adminpanel_supportticketreply':    (24, 0),
        'adminpanel_userreport':            (32, 0),
        'adminpanel_platformsettings':      (40, 0),
        'adminpanel_cannedresponse':        (48, 0),
        'adminpanel_contentmoderationterm': (56, 0),
        'adminpanel_faq':                   (0, -5),
        'adminpanel_systemroles':           (8, -5),
        'accounts_notification':            (16, -5.5),
        'conversation':                     (24, -6),
        'conversation_participants':        (32, -6),
        'message':                          (40, -6),
        'message_attachment':               (48, -6),
        'accounts_transaction':             (56, -6),
        'agency_employees':                 (0, -9),
        'worker_certifications':            (8, -9),
        'certification_logs':               (16, -10),
        'worker_materials':                 (24, -11),
        'worker_portfolio':                 (32, -11),
        'profiles_workerproduct':           (40, -11),
    }

    relationships = [
        ('adminpanel_supportticketreply', 'ticketFK_id', 'adminpanel_supportticket', 'ticketID', False),
        ('conversation_participants', 'conversation_id', 'conversation', 'conversationID', False),
        ('message', 'conversationID_id', 'conversation', 'conversationID', False),
        ('message_attachment', 'messageID_id', 'message', 'messageID', False),
    ]

    generate_module(
        "MODULE 6 \u2014 Admin Panel, Messaging, Notifications & Worker Assets",
        22, tables, positions, relationships,
        'erd_v2_module6_admin.png', figw=70, figh=22)


if __name__ == '__main__':
    print("Generating Module 2...")
    gen_module2()
    print("Generating Module 3...")
    gen_module3()
    print("Generating Module 4...")
    gen_module4()
    print("Generating Module 5...")
    gen_module5()
    print("Generating Module 6...")
    gen_module6()
    print("All modules generated!")
