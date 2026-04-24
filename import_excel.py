import sqlite3
import openpyxl
from datetime import datetime
import os

target_file = 'liste_resultats.xlsx'
db_file = 'fiscalite.db'

if not os.path.exists(target_file):
    print(f"Erreur : Le fichier {target_file} n'a pas été trouvé.")
    exit(1)

conn = sqlite3.connect(db_file)
conn.row_factory = sqlite3.Row

print(f"Chargement du fichier {target_file}...")
try:
    wb = openpyxl.load_workbook(target_file)
    ws = wb.active
except Exception as e:
    print("Erreur lors de la lecture du fichier Excel :", e)
    exit(1)

added = 0
skipped = 0

rows = list(ws.rows)
total = len(rows) - 1

print(f"{total} lignes détectées. Début de l'importation...")

for count, row in enumerate(rows[1:], 1):
    nom_ar = row[0].value
    cin_rc = row[1].value
    adresse_ar = row[2].value
    tele = row[3].value
    article = row[4].value
    nom_fr = row[5].value
    adresse_fr = row[6].value
    
    if not nom_fr and not nom_ar:
        continue
        
    nom_ar = str(nom_ar).strip() if nom_ar else ''
    nom_fr = str(nom_fr).strip() if nom_fr else ''
    cin_rc = str(cin_rc).strip() if cin_rc else ''
    adresse_ar = str(adresse_ar).strip() if adresse_ar else ''
    adresse_fr = str(adresse_fr).strip() if adresse_fr else ''
    tele = str(tele).strip() if tele else ''
    
    # Split nom and prenom based on first space to make the UI look nicer if possible
    parts = nom_fr.split(' ', 1)
    nom_part = parts[0]
    prenom_part = parts[1] if len(parts) > 1 else ''

    parts_ar = nom_ar.split(' ', 1)
    nom_ar_part = parts_ar[0]
    prenom_ar_part = parts_ar[1] if len(parts_ar) > 1 else ''

    
    # Anti-doublons basique
    if cin_rc:
        exists = conn.execute("SELECT id FROM contribuables WHERE cin=? OR rc=?", (cin_rc, cin_rc)).fetchone()
    else:
        # Doublon par nom/prenom strict ou nom_ar/prenom_ar strict
        exists = conn.execute("SELECT id FROM contribuables WHERE nom=? AND prenom=?", (nom_part, prenom_part)).fetchone()
        if not exists and nom_ar_part:
            exists = conn.execute("SELECT id FROM contribuables WHERE nom_ar=? AND prenom_ar=?", (nom_ar_part, prenom_ar_part)).fetchone()
            
    if exists:
        skipped += 1
        continue
        
    # Generate ID
    n = conn.execute('SELECT COUNT(*) as c FROM contribuables').fetchone()['c'] + 1
    num = f"CTB{datetime.now().year}{n:06d}"

    conn.execute('''INSERT INTO contribuables
        (numero, type_personne, nom, prenom, nom_ar, prenom_ar, cin, adresse, adresse_ar, telephone, commune_id, date_creation, actif)
        VALUES (?, 'physique', ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, 1)''',
        (num, nom_part, prenom_part, nom_ar_part, prenom_ar_part, cin_rc, adresse_fr, adresse_ar, tele, datetime.now().isoformat())
    )
    added += 1

conn.commit()
conn.close()

print("====================================")
print(f"       IMPORTATION TERMINÉE       ")
print("====================================")
print(f" ✅ Ajoutés : {added}")
print(f" ⏭️ Ignorés (déjà existants / doublons) : {skipped}")
