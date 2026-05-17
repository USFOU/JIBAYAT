import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .config import COMMUNE_CONFIG

# Try to register an Arabic-capable font; fall back if unavailable
_AR_FONT = 'Helvetica'
for _path, _name in [
    ('C:\\Windows\\Fonts\\arial.ttf', 'Arial'),
    ('C:\\Windows\\Fonts\\times.ttf', 'TimesNewRoman'),
]:
    if os.path.exists(_path):
        try:
            pdfmetrics.registerFont(TTFont(_name, _path))
            _AR_FONT = _name
        except Exception:
            pass

def format_dh(val):
    return f"{val:,.2f}".replace(",", " ")

def export_bordereau_pdf(be: dict, date_str: str, output_path: str):
    doc = SimpleDocTemplate(
        output_path, 
        pagesize=A4,
        rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    style_center = ParagraphStyle('Center', parent=styles['Normal'], alignment=TA_CENTER, fontName='Helvetica', fontSize=10)
    style_center_bold = ParagraphStyle('CenterB', parent=style_center, fontName='Helvetica-Bold')
    style_left = ParagraphStyle('Left', parent=styles['Normal'], alignment=TA_LEFT, fontName='Helvetica', fontSize=10)
    style_left_bold = ParagraphStyle('LeftB', parent=style_left, fontName='Helvetica-Bold')
    style_left_ar = ParagraphStyle('LeftAr', parent=style_left, fontName=_AR_FONT, fontSize=10)
    style_left_bold_ar = ParagraphStyle('LeftBAr', parent=style_left, fontName=_AR_FONT, fontSize=10)
    
    # Header (French)
    elements.append(Paragraph(COMMUNE_CONFIG["pays"], style_left_bold))
    elements.append(Paragraph(COMMUNE_CONFIG["ministere"], style_left_bold))
    elements.append(Paragraph("-----------------", style_left_bold))
    elements.append(Paragraph(f"{COMMUNE_CONFIG.get('prefecture', 'Préfecture de')} {COMMUNE_CONFIG['province']}", style_left))
    elements.append(Paragraph(COMMUNE_CONFIG["nom"], style_left))
    
    elements.append(Spacer(1, 15))
    
    elements.append(Paragraph(f"BORDEREAU D'EMISSION N° {be['numero_bordereau']}", ParagraphStyle('Title', parent=style_center_bold, fontSize=14)))
    
    elements.append(Spacer(1, 10))
    
    elements.append(Paragraph("Ordres de Recettes (1)", ParagraphStyle('SubT', parent=style_center, fontSize=11)))
    elements.append(Paragraph("Titres D'Annulation (1)", ParagraphStyle('SubT', parent=style_center, fontSize=11)))
    
    elements.append(Spacer(1, 20))
    
    # Rubrique info
    elements.append(Paragraph("RUBRIQUE BUDGETAIRE", style_left_bold))
    elements.append(Spacer(1, 10))
    
    code = be.get('code_budgetaire', '')
    chap = code[:2] if len(code) >= 2 else ''
    art = code[2:4] if len(code) >= 4 else ''
    par = code[4:] if len(code) >= 5 else ''
    
    data_rubrique = [
        ['1', 'Partie section', f'Chap:      {chap}', f'Article      {art}', par]
    ]
    t_rubrique = Table(data_rubrique, colWidths=[30, 100, 100, 100, 100])
    t_rubrique.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ]))
    elements.append(t_rubrique)
    
    elements.append(Spacer(1, 10))
    
    t_intitule = Table([['Intitulé:', be['intitule']]], colWidths=[100, 350])
    t_intitule.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ]))
    elements.append(t_intitule)
    
    elements.append(Spacer(1, 15))
    
    elements.append(Paragraph("(1) Ordres De Recettes N°", style_left))
    elements.append(Paragraph("(1) Titre D'annulation N°", style_left))
    
    elements.append(Spacer(1, 15))
    
    # ── FIRST TABLE ──
    # Columns: Empty | Montant Rubrique | 1ere Partie | 2eme Partie
    col_widths = [180, 110, 110, 110]
    
    t1_data = [
        ['', 'Montant De La', 'Montant Total Des Emissions De La Collective', ''],
        ['', 'Rebruque sus indiquée', '1ere Partie', '2eme Partie'],
        ['Report Des Antérieurs', format_dh(be['report_anterieurs']), format_dh(be['report_global']), ''],
        ['Montant De Présent Bordereau', format_dh(be['montant_present']), format_dh(be['total_present_global']), ''],
        ['TOTAL', format_dh(be['total']), format_dh(be['report_global'] + be['total_present_global']), '']
    ]
    
    t1 = Table(t1_data, colWidths=col_widths)
    t1.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        
        ('SPAN', (2,0), (3,0)), # Span "Montant Total..."
        ('SPAN', (0,0), (0,1)), # Span Empty top left
        
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('LINEABOVE', (0,4), (-1,4), 1, colors.black), # TOTAL line
    ]))
    elements.append(t1)
    
    elements.append(Spacer(1, 5))
    
    # ── SECOND TABLE ──
    t2_data = [
        ['Montant Brut Du Présent Bordereau', format_dh(be['total']), 'xxxxxxxxxxxx', 'xxxxxxxxxxxx'],
        ['Montant Net Des Antérieurs', 'xxxxxxxxxxxx', format_dh(be['report_global']), ''],
        ['TITRE REJETS', '........................', '', ''],
        ['N° ....................................', '........................', '', ''],
        ['N° ....................................', '........................', '', ''],
        ['N° ....................................', '........................', '', ''],
        ['N° ....................................', '........................', '', ''],
        ['N° ....................................', '........................', '', ''],
        ['Total Rejeté', '........................', '', ''],
        ['Montant Net Admis', format_dh(be['total']), format_dh(be['total_present_global']), ''],
        ['Total Général Admis', 'xxxxxxxxxxxx', format_dh(be['report_global'] + be['total_present_global']), ''],
        ['Total Général Admis', 'xxxxxxxxxxxx', format_dh(be['report_global'] + be['total_present_global']), '']
    ]
    
    t2 = Table(t2_data, colWidths=col_widths)
    t2.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(t2)
    
    # ── SIGNATURE ──
    elements.append(Spacer(1, 5))
    
    # Signature Box
    sig_data = [
        [f"A {COMMUNE_CONFIG['nom'].replace('Commune ', '').upper()} LE", "", "Vu Pour Confirmation De La Prise En Charge"],
        ["", "", "(1) Receveur Des Finances"]
    ]
    t_sig = Table(sig_data, colWidths=[180, 110, 220])
    t_sig.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('BOX', (2,0), (2,1), 1, colors.black),
        ('LINEBELOW', (2,0), (2,0), 1, colors.black),
    ]))
    elements.append(t_sig)
    
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("(1) Barrer La Mention Inutile", style_left))
    
    doc.build(elements)
