#!/usr/bin/env python3
"""ERD Diagram Generator - Module 1: Platform Database High-Level Overview
   Styled to match Modules 2-6: dark header, white bg, alternating rows, crow-foot arrows.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Colour palette (identical to Modules 2-6) ─────────────────────────────
C = {
    'hdr_bg':   '#1E2D3D',
    'hdr_txt':  '#FFFFFF',
    'row_lt':   '#FFFFFF',
    'row_dk':   '#EDF2F7',
    'border':   '#CBD5E0',
    'bg':       '#FFFFFF',
    'title':    '#1A202C',
    'note':     '#718096',
    'rel_line': '#2B6CB0',
    'tbl_txt':  '#1A202C',
    'tbl_dim':  '#718096',
}

# ── Sizing ─────────────────────────────────────────────────────────────────
BOX_W  = 3.40   # module box width  (inches)
ROW_H  = 0.200  # row height per table name
HDR_H  = 0.360  # header height
H_GAP  = 0.65   # horizontal gap between columns
V_GAP  = 0.60   # vertical gap between rows

def box_h(n_tables):
    return HDR_H + n_tables * ROW_H

# ── Module definitions  (number, label, colour accent, [tables]) ────────────
MODULES = [
    # (id, label, header_accent_colour, [tables])
    (1,  'Auth & Accounts',    '#1E2D3D',
     ['accounts_accounts', 'account_emailaddress',
      'socialaccount_socialaccount', 'socialaccount_socialapp',
      'socialaccount_socialtoken', 'django_session',
      'accounts_accounts_groups', 'accounts_accounts_user_permissions']),

    (2,  'Profiles & Locations', '#1E2D3D',
     ['accounts_profile', 'accounts_workerprofile',
      'accounts_clientprofile', 'accounts_agency',
      'accounts_workerspecialization', 'specializations',
      'accounts_barangay', 'accounts_city',
      'accounts_interestedjobs']),

    (3,  'KYC Verification',   '#1E2D3D',
     ['accounts_kyc', 'accounts_kycfiles',
      'kyc_extracted_data', 'agency_agencykyc',
      'agency_agencykycfile', 'agency_kyc_extracted_data',
      'adminpanel_kyclogs']),

    (4,  'Jobs & Applications', '#1E2D3D',
     ['jobs', 'job_applications',
      'job_skill_slots', 'job_worker_assignments',
      'job_employee_assignments', 'price_negotiations',
      'saved_jobs']),

    (5,  'Job Operations',     '#1E2D3D',
     ['job_logs', 'job_materials',
      'job_photos', 'job_reviews',
      'job_disputes', 'dispute_evidence',
      'review_skill_tags',
      'backjob_schedule_confirmations']),

    (6,  'Daily Jobs',         '#1E2D3D',
     ['daily_attendance', 'daily_job_extensions',
      'daily_rate_changes', 'daily_skip_day_requests']),

    (7,  'Finance & Payments', '#1E2D3D',
     ['accounts_wallet', 'accounts_transaction',
      'accounts_userpaymentmethod']),

    (8,  'Messaging',          '#1E2D3D',
     ['conversation', 'conversation_participants',
      'message', 'message_attachment']),

    (9,  'Admin Panel',        '#1E2D3D',
     ['adminpanel_adminaccount', 'adminpanel_auditlog',
      'adminpanel_supportticket', 'adminpanel_supportticketreply',
      'adminpanel_userreport', 'adminpanel_platformsettings',
      'adminpanel_cannedresponse', 'adminpanel_contentmoderationterm',
      'adminpanel_faq', 'adminpanel_systemroles']),

    (10, 'Workers & Agencies', '#1E2D3D',
     ['agency_employees', 'worker_certifications',
      'certification_logs', 'worker_materials',
      'worker_portfolio', 'profiles_workerproduct',
      'accounts_notification', 'accounts_notificationsettings',
      'accounts_pushtoken']),
]

# ── Grid layout: (col, row) zero-indexed, row 0 = top ──────────────────────
GRID = {
    1:  (0, 0),
    2:  (1, 0),
    3:  (2, 0),
    4:  (0, 1),
    5:  (1, 1),
    6:  (2, 1),
    7:  (0, 2),
    8:  (1, 2),
    9:  (2, 2),
    10: (3, 1),   # put module 10 at col 3 row 1 (centre-right)
}

# ── Cross-module arrows: (src_mod_id, dst_mod_id, label) ───────────────────
ARROWS = [
    (1, 2,  ''),
    (1, 3,  ''),
    (1, 4,  ''),
    (1, 7,  ''),
    (1, 9,  ''),
    (1, 10, ''),
    (2, 4,  ''),
    (2, 5,  ''),
    (2, 8,  ''),
    (4, 5,  ''),
    (4, 6,  ''),
    (4, 7,  ''),
    (4, 8,  ''),
    (5, 6,  ''),
    (9, 3,  ''),
    (10, 2, ''),
    (10, 4, ''),
]


def draw_module_box(ax, x, y_top, mod_id, label, tables):
    """Draw one module box. Returns (cx, cy) of header centre."""
    n   = len(tables)
    h   = box_h(n)

    # Drop shadow
    ax.add_patch(mpatches.FancyBboxPatch(
        (x + 0.06, y_top - h - 0.06), BOX_W, h,
        boxstyle="square,pad=0", linewidth=0,
        facecolor='#C8D2DC', zorder=1))

    # Header
    ax.add_patch(mpatches.Rectangle(
        (x, y_top - HDR_H), BOX_W, HDR_H,
        linewidth=0, facecolor=C['hdr_bg'], zorder=2))

    # Circle badge with module number
    badge_cx = x + 0.32
    badge_cy = y_top - HDR_H / 2
    ax.add_patch(plt.Circle((badge_cx, badge_cy), 0.14,
                             color='#F6C90E', zorder=4))
    ax.text(badge_cx, badge_cy, str(mod_id),
            ha='center', va='center', fontsize=7.0,
            fontweight='bold', color='#5C4500', zorder=5)

    # Module label
    ax.text(x + 0.55, y_top - HDR_H / 2, label,
            ha='left', va='center', fontsize=8.5,
            fontweight='bold', color=C['hdr_txt'], zorder=5)

    # Table rows
    for i, tname in enumerate(tables):
        ry_top = y_top - HDR_H - i * ROW_H
        ry_ctr = ry_top - ROW_H / 2
        ax.add_patch(mpatches.Rectangle(
            (x, ry_top - ROW_H), BOX_W, ROW_H,
            linewidth=0,
            facecolor=C['row_lt'] if i % 2 == 0 else C['row_dk'],
            zorder=2))
        ax.plot([x, x + BOX_W], [ry_top, ry_top],
                color=C['border'], linewidth=0.25, zorder=3)
        # bullet dot
        ax.plot(x + 0.13, ry_ctr, 'o',
                markersize=2.0, color='#A0AEC0', zorder=4)
        ax.text(x + 0.24, ry_ctr, tname,
                ha='left', va='center', fontsize=6.0,
                color=C['tbl_txt'], fontfamily='monospace', zorder=5)

    # Outer border
    ax.add_patch(mpatches.Rectangle(
        (x, y_top - h), BOX_W, h,
        linewidth=1.0, edgecolor=C['border'],
        facecolor='none', zorder=4))

    return (x + BOX_W / 2, y_top - HDR_H / 2)


def crow_foot(ax, x1, y1, x2, y2, rad=0.15):
    ax.annotate('',
        xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle='-', color=C['rel_line'],
                        linewidth=0.9,
                        connectionstyle=f'arc3,rad={rad}'),
        zorder=0)
    ang  = np.arctan2(y2 - y1, x2 - x1)
    perp = ang + np.pi / 2
    sz   = 0.10
    for off in [-sz * 0.6, 0, sz * 0.6]:
        ex = x1 + sz * np.cos(ang + np.pi) + off * np.cos(perp)
        ey = y1 + sz * np.sin(ang + np.pi) + off * np.sin(perp)
        ax.plot([x1, ex], [y1, ey], color=C['rel_line'], linewidth=0.9, zorder=0)
    tk = 0.08
    ax.plot([x2 - tk * np.cos(perp + np.pi/2), x2 + tk * np.cos(perp + np.pi/2)],
            [y2 - tk * np.sin(perp + np.pi/2), y2 + tk * np.sin(perp + np.pi/2)],
            color=C['rel_line'], linewidth=1.1, zorder=0)


def generate_overview():
    LEFT  = 0.40
    TOP   = -0.55   # y_top of row 0

    mod_lookup = {m[0]: m for m in MODULES}

    # Pre-compute positions for each module
    positions = {}  # mod_id -> (x, y_top)
    for mod_id, (col, row) in GRID.items():
        x     = LEFT + col * (BOX_W + H_GAP)
        # y_top for this row = TOP minus sum of heights of all boxes in same
        # column above plus their gaps
        # Simpler: compute max height per row, stack rows
        y_top = TOP - row * 7.5   # fixed row stride; we'll fix later
        positions[mod_id] = (x, y_top)

    # ── Better row y: compute row heights dynamically ──────────────────────
    # Group modules by row
    row_groups = {}
    for mid, (col, row) in GRID.items():
        row_groups.setdefault(row, []).append(mid)

    row_y_top = {}
    current_y = TOP
    for row_idx in sorted(row_groups.keys()):
        mids  = row_groups[row_idx]
        max_h = max(box_h(len(mod_lookup[m][3])) for m in mids)
        row_y_top[row_idx] = current_y
        current_y -= max_h + V_GAP

    for mod_id, (col, row) in GRID.items():
        x = LEFT + col * (BOX_W + H_GAP)
        positions[mod_id] = (x, row_y_top[row])

    # ── Figure size ────────────────────────────────────────────────────────
    all_bottoms = []
    for mid, (x, y_top) in positions.items():
        all_bottoms.append(y_top - box_h(len(mod_lookup[mid][3])))
    fig_bottom = min(all_bottoms) - 0.55
    max_col    = max(GRID[m][0] for m in GRID)
    fig_right  = LEFT + (max_col + 1) * (BOX_W + H_GAP) + 0.30
    fig_top    = 0.55

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
    ax.text(fig_w / 2, fig_top - 0.16,
            'Platform Database – High-Level ERD Overview',
            ha='center', va='top', fontsize=14, fontweight='bold',
            color=C['title'])
    ax.text(fig_w / 2, fig_top - 0.40,
            '60+ tables  ·  10 domain modules  |  ERD v2',
            ha='center', va='top', fontsize=8.5, color=C['note'])

    # Draw module boxes; collect header centres for arrows
    hdr_centres = {}   # mod_id -> (cx, cy)
    box_bounds  = {}   # mod_id -> (x, y_top, w, h)
    for mod_id, (x, y_top) in positions.items():
        _, label, accent, tables = mod_lookup[mod_id]
        cx, cy = draw_module_box(ax, x, y_top, mod_id, label, tables)
        hdr_centres[mod_id] = (cx, cy)
        box_bounds[mod_id]  = (x, y_top, BOX_W, box_h(len(tables)))

    # Draw arrows between modules
    drawn = set()
    for src, dst, lbl in ARROWS:
        key = (min(src, dst), max(src, dst))
        if key in drawn:
            continue
        drawn.add(key)
        sx, sy = hdr_centres[src]
        dx, dy = hdr_centres[dst]
        # Alternate rad to avoid overlap
        rad = 0.05 if abs(sx - dx) > 2 else 0.12
        crow_foot(ax, sx, sy, dx, dy, rad=rad)

    plt.tight_layout(pad=0.05)
    out = '/workspace/erd_v2_module1_overview.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor=C['bg'])
    plt.close(fig)
    print(f'Saved {out}')


if __name__ == '__main__':
    generate_overview()
