#!/usr/bin/env python3
"""ERD Diagram Generator - Module 5: KYC Verification (Individual & Agency)"""
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
RH   = 0.183
HDR  = 0.280
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
            ha='center', va='center', fontsize=7.0, fontweight='bold',
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
                (x+0.03, ry_top - RH + 0.018), 0.30, RH - 0.036,
                boxstyle="round,pad=0.01",
                linewidth=0, facecolor=C['pk_bg'], zorder=3))
            ax.text(x+0.18, ry_ctr, 'PK',
                    ha='center', va='center', fontsize=4.8,
                    fontweight='bold', color=C['pk_txt'], zorder=5)
            ax.text(x+0.37, ry_ctr, fname,
                    ha='left', va='center', fontsize=5.8,
                    fontweight='bold', color=C['norm_txt'], zorder=5)
            ax.text(x+TW-0.06, ry_ctr, ftype,
                    ha='right', va='center', fontsize=4.6,
                    color=C['type_txt'], zorder=5)
        elif is_fk:
            ax.text(x+0.09, ry_ctr, fname,
                    ha='left', va='center', fontsize=5.6,
                    fontstyle='italic', color=C['fk_txt'], zorder=5)
            if fk_tgt:
                ax.text(x+TW-0.06, ry_ctr, f'→ {fk_tgt}',
                        ha='right', va='center', fontsize=4.4,
                        color=C['fk_txt'], zorder=5)
        else:
            ax.text(x+0.09, ry_ctr, fname,
                    ha='left', va='center', fontsize=5.6,
                    color=C['norm_txt'], zorder=5)
            ax.text(x+TW-0.06, ry_ctr, ftype,
                    ha='right', va='center', fontsize=4.6,
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
'accounts_kyc': [
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
],
'accounts_kycfiles': [
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
],
'kyc_extracted_data': [
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
],
'agency_agencykyc': [
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
],
'agency_agencykycfile': [
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
],
'agency_kyc_extracted_data': [
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
],
'adminpanel_kyclogs': [
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
],
}

COLUMNS = [
    ['accounts_kyc', 'accounts_kycfiles'],
    ['kyc_extracted_data'],
    ['agency_agencykyc', 'agency_agencykycfile'],
    ['agency_kyc_extracted_data', 'adminpanel_kyclogs'],
]

RELS = [
    ('accounts_kycfiles',      'kycID_id',     'accounts_kyc'),
    ('kyc_extracted_data',     'kycID_id',     'accounts_kyc'),
    ('agency_agencykycfile',   'agencyKyc_id', 'agency_agencykyc'),
    ('agency_kyc_extracted_data','agencyKyc_id','agency_agencykyc'),
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


def generate_module5():
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
            'MODULE 5 – KYC Verification (Individual & Agency)',
            ha='center', va='top', fontsize=13, fontweight='bold',
            color=C['title'])
    ax.text(fig_w/2, fig_top - 0.40,
            '7 tables  |  ERD v2',
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
    out = '/workspace/erd_v2_module5_kyc.png'
    fig.savefig(out, dpi=150, bbox_inches='tight', facecolor=C['bg'])
    plt.close(fig)
    print(f'Saved {out}')


if __name__ == '__main__':
    generate_module5()
