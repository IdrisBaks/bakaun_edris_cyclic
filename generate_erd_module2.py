#!/usr/bin/env python3
"""ERD Diagram Generator - Module 2: Profiles, Location, Wallet & Specializations"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Color palette ─────────────────────────────────────────────────────────────
C = {
    'hdr_bg':    '#1E2D3D',
    'hdr_txt':   '#FFFFFF',
    'pk_bg':     '#F6C90E',
    'pk_txt':    '#5C4500',
    'fk_txt':    '#1565C0',
    'norm_txt':  '#1A202C',
    'type_txt':  '#718096',
    'row_lt':    '#FFFFFF',
    'row_dk':    '#EDF2F7',
    'border':    '#CBD5E0',
    'bg':        '#FFFFFF',
    'title':     '#1A202C',
    'note':      '#718096',
    'rel_line':  '#2B6CB0',
}

TW   = 3.30   # table width  (inches)
RH   = 0.195  # row height   (inches)
HDR  = 0.295  # header height(inches)
GAP  = 0.40   # vertical gap between tables (inches)
CGAP = 0.55   # horizontal gap between columns (inches)

def tbl_h(n): return HDR + n * RH

def draw_table(ax, x, y_top, name, fields):
    """Draw one ERD table. fields = [(fname, ftype, is_pk, is_fk, fk_target), ...]
    Returns dict {fname: (row_center_x, row_center_y)} and bounding box."""
    n = len(fields)
    h = tbl_h(n)

    # Light drop shadow
    ax.add_patch(mpatches.FancyBboxPatch(
        (x+0.05, y_top - h - 0.05), TW, h,
        boxstyle="square,pad=0", linewidth=0,
        facecolor='#D1D9E0', zorder=1))

    # Header
    ax.add_patch(mpatches.Rectangle(
        (x, y_top - HDR), TW, HDR,
        linewidth=0, facecolor=C['hdr_bg'], zorder=2))
    ax.text(x + TW/2, y_top - HDR/2, name,
            ha='center', va='center', fontsize=7.8, fontweight='bold',
            color=C['hdr_txt'], zorder=5)

    row_centers = {}
    for i, (fname, ftype, is_pk, is_fk, fk_tgt) in enumerate(fields):
        ry_top = y_top - HDR - i * RH
        ry_ctr = ry_top - RH / 2

        # Row background
        ax.add_patch(mpatches.Rectangle(
            (x, ry_top - RH), TW, RH,
            linewidth=0,
            facecolor=C['row_lt'] if i % 2 == 0 else C['row_dk'],
            zorder=2))
        # Row divider
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
                    ha='left', va='center', fontsize=6.4,
                    fontweight='bold', color=C['norm_txt'], zorder=5)
            ax.text(x+TW-0.06, ry_ctr, ftype,
                    ha='right', va='center', fontsize=5.2,
                    color=C['type_txt'], zorder=5)
        elif is_fk:
            ax.text(x+0.09, ry_ctr, fname,
                    ha='left', va='center', fontsize=6.2,
                    fontstyle='italic', color=C['fk_txt'], zorder=5)
            if fk_tgt:
                ax.text(x+TW-0.06, ry_ctr, f'→ {fk_tgt}',
                        ha='right', va='center', fontsize=4.9,
                        color=C['fk_txt'], zorder=5)
        else:
            ax.text(x+0.09, ry_ctr, fname,
                    ha='left', va='center', fontsize=6.2,
                    color=C['norm_txt'], zorder=5)
            ax.text(x+TW-0.06, ry_ctr, ftype,
                    ha='right', va='center', fontsize=5.2,
                    color=C['type_txt'], zorder=5)

    # Outer border
    ax.add_patch(mpatches.Rectangle(
        (x, y_top - h), TW, h,
        linewidth=0.8, edgecolor=C['border'],
        facecolor='none', zorder=4))

    return row_centers, (x, y_top, TW, h)


def crow_foot_arrow(ax, x1, y1, x2, y2):
    """Draw a crow-foot (many) → tick (one) connector."""
    ax.annotate('',
        xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle='-',
            color=C['rel_line'],
            linewidth=0.75,
            connectionstyle='arc3,rad=0.18'),
        zorder=0)
    # crow-foot at source (many)
    ang = np.arctan2(y2 - y1, x2 - x1)
    perp = ang + np.pi/2
    sz = 0.085
    for off in [-sz*0.65, 0, sz*0.65]:
        ex = x1 + sz*np.cos(ang+np.pi) + off*np.cos(perp)
        ey = y1 + sz*np.sin(ang+np.pi) + off*np.sin(perp)
        ax.plot([x1, ex], [y1, ey],
                color=C['rel_line'], linewidth=0.75, zorder=0)
    # tick at destination (one)
    tk = 0.07
    ax.plot([x2 - tk*np.cos(perp+np.pi/2),
             x2 + tk*np.cos(perp+np.pi/2)],
            [y2 - tk*np.sin(perp+np.pi/2),
             y2 + tk*np.sin(perp+np.pi/2)],
            color=C['rel_line'], linewidth=1.0, zorder=0)


# ══════════════════════════════════════════════════════════════════════════════
# TABLE DEFINITIONS  (name, dtype, is_pk, is_fk, fk_target)
# ══════════════════════════════════════════════════════════════════════════════
T = {
'accounts_profile': [
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
],
'accounts_workerprofile': [
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
],
'accounts_clientprofile': [
    ('id','int8',True,False,None),
    ('description','varchar',False,False,None),
    ('totalJobsPosted','int4',False,False,None),
    ('clientRating','int4',False,False,None),
    ('activeJobsCount','int4',False,False,None),
    ('profileID_id','int8',False,True,'accounts_profile'),
],
'accounts_agency': [
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
],
'accounts_barangay': [
    ('barangayID','int4',True,False,None),
    ('name','varchar',False,False,None),
    ('zipCode','varchar',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('city_id','int4',False,True,'accounts_city'),
],
'accounts_city': [
    ('cityID','int4',True,False,None),
    ('name','varchar',False,False,None),
    ('province','varchar',False,False,None),
    ('region','varchar',False,False,None),
    ('zipCode','varchar',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
],
'specializations': [
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
],
'accounts_workerspecialization': [
    ('id','int8',True,False,None),
    ('experienceYears','int4',False,False,None),
    ('certification','varchar',False,False,None),
    ('skillType','varchar',False,False,None),
    ('displayOrder','int4',False,False,None),
    ('workerID_id','int8',False,True,'accounts_workerprofile'),
    ('specializationID_id','int8',False,True,'specializations'),
],
'accounts_interestedjobs': [
    ('id','int8',True,False,None),
    ('clientID_id','int8',False,True,'accounts_clientprofile'),
    ('specializationID_id','int8',False,True,'specializations'),
],
'accounts_wallet': [
    ('walletID','int8',True,False,None),
    ('balance','numeric',False,False,None),
    ('reservedBalance','numeric',False,False,None),
    ('pendingEarnings','numeric',False,False,None),
    ('autoWithdrawEnabled','bool',False,False,None),
    ('lastAutoWithdrawAt','timestamptz',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('accountFK_id','int8',False,True,'accounts_accounts'),
    ('preferredPaymentMethodID_id','int8',False,True,'accts_userpaymentmethod'),
],
'accounts_userpaymentmethod': [
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
],
'accounts_pushtoken': [
    ('tokenID','int8',True,False,None),
    ('pushToken','varchar UNIQUE',False,False,None),
    ('deviceType','varchar',False,False,None),
    ('isActive','bool',False,False,None),
    ('createdAt','timestamptz',False,False,None),
    ('updatedAt','timestamptz',False,False,None),
    ('lastUsed','timestamptz',False,False,None),
    ('accountFK_id','int8',False,True,'accounts_accounts'),
],
'accounts_notificationsettings': [
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
    ('accountFK_id','int8 UNIQUE',False,True,'accounts_accounts'),
],
}

# ══ Column layout  (col_idx: [ table_name, ... ]) ════════════════════════════
# 4 columns, tables stacked top-to-bottom within each column
COLUMNS = [
    ['accounts_city', 'accounts_barangay', 'accounts_interestedjobs'],
    ['accounts_profile', 'accounts_wallet'],
    ['accounts_workerprofile', 'accounts_clientprofile',
     'accounts_notificationsettings'],
    ['accounts_agency', 'specializations', 'accounts_workerspecialization'],
    ['accounts_userpaymentmethod', 'accounts_pushtoken'],
]

# Key relationships to visualise: (src_table, src_field, dst_table)
RELS = [
    ('accounts_profile',           'accountFK_id',           'accounts_city'),
    ('accounts_workerprofile',     'profileID_id',           'accounts_profile'),
    ('accounts_clientprofile',     'profileID_id',           'accounts_profile'),
    ('accounts_barangay',          'city_id',                'accounts_city'),
    ('accounts_agency',            'accountFK_id',           'accounts_profile'),
    ('accounts_wallet',            'accountFK_id',           'accounts_profile'),
    ('accounts_wallet',            'preferredPaymentMethodID_id', 'accounts_userpaymentmethod'),
    ('accounts_userpaymentmethod', 'accountFK_id',           'accounts_profile'),
    ('accounts_pushtoken',         'accountFK_id',           'accounts_profile'),
    ('accounts_notificationsettings','accountFK_id',         'accounts_profile'),
    ('specializations',            'created_by_agency_id',   'accounts_agency'),
    ('accounts_workerspecialization','workerID_id',          'accounts_workerprofile'),
    ('accounts_workerspecialization','specializationID_id',  'specializations'),
    ('accounts_interestedjobs',    'clientID_id',            'accounts_clientprofile'),
    ('accounts_interestedjobs',    'specializationID_id',    'specializations'),
]


def build_layout(columns, top_margin, left_margin, col_spacing):
    """Return {table_name: (x, y_top)} positions."""
    positions = {}
    for ci, col in enumerate(columns):
        x = left_margin + ci * (TW + col_spacing)
        y = top_margin
        for tname in col:
            positions[tname] = (x, y)
            y -= tbl_h(len(T[tname])) + GAP
    return positions


def generate_module2():
    TOP_MARGIN  = -0.6   # y_top of first row (below title area)
    LEFT_MARGIN =  0.3
    COL_SPACING =  CGAP

    positions = build_layout(COLUMNS, TOP_MARGIN, LEFT_MARGIN, COL_SPACING)

    # ── Figure size ──────────────────────────────────────────────────────────
    all_bottoms = []
    for tname, (x, y_top) in positions.items():
        all_bottoms.append(y_top - tbl_h(len(T[tname])))
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

    # Title
    ax.text(fig_w/2, fig_top - 0.18,
            'MODULE 2 – Profiles, Location, Wallet & Specializations',
            ha='center', va='top', fontsize=13, fontweight='bold',
            color=C['title'])
    ax.text(fig_w/2, fig_top - 0.40,
            f'13 tables  |  ERD v2',
            ha='center', va='top', fontsize=8, color=C['note'])

    # Draw tables and collect row centres
    all_rc = {}   # table_name -> {field_name -> (cx, cy)}
    tbl_boxes = {}  # table_name -> (x, y_top, w, h)

    for tname, (x, y_top) in positions.items():
        rc, box = draw_table(ax, x, y_top, tname, T[tname])
        all_rc[tname]   = rc
        tbl_boxes[tname] = box

    # Draw relationships
    for src_t, src_f, dst_t in RELS:
        if src_t not in all_rc or dst_t not in all_rc:
            continue
        if src_f not in all_rc[src_t]:
            continue
        sx, sy = all_rc[src_t][src_f]
        dx, dy = tbl_boxes[dst_t][0] + TW/2, tbl_boxes[dst_t][1] - HDR/2
        crow_foot_arrow(ax, sx, sy, dx, dy)

    plt.tight_layout(pad=0.1)
    out = '/workspace/erd_v2_module2_profiles.png'
    fig.savefig(out, dpi=150, bbox_inches='tight',
                facecolor=C['bg'])
    plt.close(fig)
    print(f'Saved {out}')


if __name__ == '__main__':
    generate_module2()
