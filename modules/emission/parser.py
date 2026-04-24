import pandas as pd
import re
import os

def parse_bordereau_versement(filepath: str) -> dict:
    """
    Retourne:
    {
        "mois": 1,
        "annee": 2026,
        "total_general": 1000028.01,
        "lignes": [
            {"code_budgetaire": "1140201016", "nature_recette": "Taxe sur le transport...", "montant": 4478.4},
            ...
        ]
    }
    """
    result = {
        "mois": None,
        "annee": None,
        "total_general": 0.0,
        "lignes": []
    }
    
    engine = 'openpyxl' if filepath.endswith('.xlsx') else 'xlrd'
    try:
        df = pd.read_excel(filepath, header=None, engine=engine)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return result

    start_row = -1
    
    # 1. Chercher Mois / Année
    for i in range(min(20, len(df))):
        row = df.iloc[i]
        row_str = " ".join([str(x) for x in row if pd.notna(x)]).upper()
        
        # This is a bit robust for various formats
        m_mois = re.search(r'MOIS\s*[:\s]\s*(\d+)', row_str)
        m_annee = re.search(r'ANN[EÉ]E\s*[:\s]\s*(\d{4})', row_str)
        
        if m_mois and not result["mois"]:
            result["mois"] = int(m_mois.group(1))
        if m_annee and not result["annee"]:
            result["annee"] = int(m_annee.group(1))
                    
    # 2. Chercher "CODE BUDGETAIRE"
    for i in range(len(df)):
        row = df.iloc[i]
        for val in row:
            if 'CODE BUDGETAIRE' in str(val).strip().upper() or 'CODE BUDGÉTAIRE' in str(val).upper() or 'BUDGETAIRE' in str(val).upper():
                start_row = i + 1
                break
        if start_row != -1:
            break
            
    if start_row == -1:
        return result
        
    # 3. Extraire les lignes
    for i in range(start_row, len(df)):
        row = df.iloc[i]
        first_cell = str(row.iloc[0]).strip().upper()
        
        if 'TOTAL GENERAL' in first_cell or 'TOTAL GÉNÉRAL' in first_cell or 'TOTAL' in first_cell:
            for val in reversed(row):
                if pd.notna(val):
                    try:
                        v = str(val).replace(' ', '').replace(',', '.')
                        result["total_general"] = float(v)
                        break
                    except:
                        pass
            break
            
        code = str(row.iloc[0]).strip()
        if not code or code.lower() == 'nan':
            for j in range(len(row)):
                 c = str(row.iloc[j]).strip()
                 if c.replace('.0', '').isdigit() and len(c) > 6:
                     code = c.replace('.0', '')
                     break
                     
        if not code or code.lower() == 'nan' or not code.isdigit():
            continue
            
        nature = ""
        montant = 0.0
        
        for j in range(1, len(row)):
            val = str(row.iloc[j]).strip()
            if val and val.lower() != 'nan' and not any(char.isdigit() for char in val):
                nature = val
                break
                
        for val in reversed(row):
            if pd.notna(val):
                try:
                    v = str(val).replace(' ', '').replace(',', '.')
                    if '.' in v or v.isdigit():
                         montant = float(v)
                         if montant > 0:
                             break
                except:
                     pass
                     
        if code and montant > 0:
            result["lignes"].append({
                "code_budgetaire": code,
                "nature_recette": nature,
                "montant": montant
            })
            
    if result["total_general"] == 0.0:
        result["total_general"] = sum(l["montant"] for l in result["lignes"])
        
    return result
