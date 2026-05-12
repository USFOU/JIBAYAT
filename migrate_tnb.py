"""migrate_tnb.py — Applique les migrations TNB v3 à fiscalite.db"""
import sqlite3, sys, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
DB = 'fiscalite.db'

conn = sqlite3.connect(DB)
c = conn.cursor()

# 1. Table dossiers_tnb
c.execute('''CREATE TABLE IF NOT EXISTS dossiers_tnb (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_dossier INTEGER UNIQUE NOT NULL,
    contribuable_id INTEGER NOT NULL REFERENCES contribuables(id),
    archive INTEGER DEFAULT 0,
    date_creation TEXT DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()
print("OK: dossiers_tnb")

# 2. Table tnb_documents
c.execute('''CREATE TABLE IF NOT EXISTS tnb_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    terrain_id INTEGER NOT NULL REFERENCES terrains(id),
    nom_fichier TEXT,
    chemin TEXT,
    type_doc TEXT DEFAULT "autre",
    taille INTEGER,
    date_upload TEXT DEFAULT CURRENT_TIMESTAMP,
    agent_id INTEGER
)''')
conn.commit()
print("OK: tnb_documents")

# 3. Table terrain_coproprietaires
c.execute('''CREATE TABLE IF NOT EXISTS terrain_coproprietaires (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    terrain_id INTEGER NOT NULL REFERENCES terrains(id),
    contribuable_id INTEGER NOT NULL REFERENCES contribuables(id),
    part_indivision REAL DEFAULT 0,
    date_ajout TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(terrain_id, contribuable_id)
)''')
conn.commit()
print("OK: terrain_coproprietaires")

# 4. Colonnes manquantes sur terrains
for col, typ in [('lotissement', 'TEXT DEFAULT ""'), ('archive', 'INTEGER DEFAULT 0')]:
    try:
        c.execute(f'ALTER TABLE terrains ADD COLUMN {col} {typ}')
        conn.commit()
        print(f"OK: terrains.{col} added")
    except Exception as e:
        print(f"SKIP: terrains.{col} ({e})")

# 5. Colonnes manquantes sur permis
for col, typ in [
    ('date_autorisation', 'TEXT'),
    ('annee_debut_exoneration', 'INTEGER'),
    ('annee_fin_exoneration', 'INTEGER'),
]:
    try:
        c.execute(f'ALTER TABLE permis ADD COLUMN {col} {typ}')
        conn.commit()
        print(f"OK: permis.{col} added")
    except Exception as e:
        print(f"SKIP: permis.{col} ({e})")

# 6. Parametre AMENDE_NON_DECLARATION
c.execute('''INSERT OR IGNORE INTO parametres_calcul
    (module, code, libelle, valeur, unite, description)
    VALUES ("TNB","AMENDE_NON_DECLARATION",
            "Amende non-declaration (%)","15","%",
            "Pourcentage amende pour non-declaration dans les delais")''')
conn.commit()
print("OK: parametres_calcul AMENDE_NON_DECLARATION")

# Verification finale
tables = [r[0] for r in c.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()]
print("\n=== Tables TNB presentes ===")
for t in ['dossiers_tnb', 'tnb_documents', 'terrain_coproprietaires']:
    status = "PRESENT" if t in tables else "MANQUANTE"
    print(f"  {t}: {status}")

print("\n=== Colonnes terrains ===")
cols = [r[1] for r in c.execute('PRAGMA table_info(terrains)').fetchall()]
print("  ", cols)

print("\n=== Colonnes permis ===")
cols = [r[1] for r in c.execute('PRAGMA table_info(permis)').fetchall()]
print("  ", cols)

conn.close()
print("\nMigration terminee avec succes!")
