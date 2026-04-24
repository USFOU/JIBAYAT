import os
from datetime import datetime
from database import get_db
from .config import CODE_TO_RUBRIQUE, RUBRIQUE_DEFAULT
from .pdf_exporter import export_bordereau_pdf

def get_report_anterieurs(conn, rubrique: str, annee: int, mois: int) -> float:
    if mois <= 1:
        return 0.0
        
    row = conn.execute('''
        SELECT SUM(be.montant_present) as total
        FROM bordereaux_emission be
        JOIN bordereaux_versement bv ON be.bordereau_id = bv.id
        WHERE bv.annee = ? AND bv.mois < ? AND be.rubrique = ?
    ''', (annee, mois, rubrique)).fetchone()
    
    return float(row['total'] or 0.0)

def get_report_anterieurs_global(conn, annee: int, mois: int) -> float:
    if mois <= 1:
        return 0.0
        
    row = conn.execute('''
        SELECT SUM(be.montant_present) as total
        FROM bordereaux_emission be
        JOIN bordereaux_versement bv ON be.bordereau_id = bv.id
        WHERE bv.annee = ? AND bv.mois < ?
    ''', (annee, mois)).fetchone()
    
    return float(row['total'] or 0.0)

def generer_tous_bordereaux(bordereau_id: int, output_dir: str) -> list:
    conn = get_db()
    bv = conn.execute('SELECT * FROM bordereaux_versement WHERE id = ?', (bordereau_id,)).fetchone()
    if not bv:
        conn.close()
        return []
        
    lignes = conn.execute('SELECT * FROM lignes_recettes WHERE bordereau_id = ?', (bordereau_id,)).fetchall()
    
    generated = []
    
    conn.execute('DELETE FROM bordereaux_emission WHERE bordereau_id = ?', (bordereau_id,))
    
    max_num_row = conn.execute('''
        SELECT MAX(be.numero_bordereau) as max_n
        FROM bordereaux_emission be
        JOIN bordereaux_versement bv ON be.bordereau_id = bv.id
        WHERE bv.annee = ?
    ''', (bv['annee'],)).fetchone()
    num_bordereau = (max_num_row['max_n'] or 0) if max_num_row else 0
    
    report_global = get_report_anterieurs_global(conn, bv['annee'], bv['mois'])
    total_present_global = bv['total_general']
    
    for ligne in lignes:
        code = ligne['code_budgetaire']
        rubrique_info = CODE_TO_RUBRIQUE.get(code, RUBRIQUE_DEFAULT)
        rubrique_nom = rubrique_info[0]
        intitule = rubrique_info[1]
        
        montant = ligne['montant']
        report = get_report_anterieurs(conn, rubrique_nom, bv['annee'], bv['mois'])
        total = montant + report
        
        num_bordereau += 1
        
        pdf_filename = f"BE_{bv['annee']}_{bv['mois']:02d}_{code}.pdf"
        pdf_path = os.path.join(output_dir, pdf_filename)
        
        be_data = {
            'numero_bordereau': num_bordereau,
            'annee': bv['annee'],
            'rubrique': rubrique_nom,
            'code_budgetaire': code,
            'intitule': intitule,
            'montant_present': montant,
            'report_anterieurs': report,
            'total': total,
            'total_present_global': total_present_global,
            'report_global': report_global
        }
        
        export_bordereau_pdf(be_data, datetime.now().strftime('%d/%m/%Y'), pdf_path)
        
        conn.execute('''
            INSERT INTO bordereaux_emission 
            (bordereau_id, numero_bordereau, rubrique, code_budgetaire, intitule, montant_present, report_anterieurs, total, chemin_pdf)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (bordereau_id, num_bordereau, rubrique_nom, code, intitule, montant, report, total, pdf_path))
        
        generated.append(be_data)
        
    conn.commit()
    conn.close()
    
    return generated
