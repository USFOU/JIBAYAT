"""Diagnostic et correction dossiers_tnb"""
import sqlite3

DB = 'fiscalite.db'
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
c = conn.cursor()

print("=== DIAGNOSTIC dossiers_tnb ===\n")

# 1. Contenu de la table
rows = c.execute('''
    SELECT dt.id, dt.numero_dossier, dt.contribuable_id,
           c.nom, c.prenom, c.raison_sociale, c.cin, c.rc
    FROM dossiers_tnb dt
    JOIN contribuables c ON c.id = dt.contribuable_id
    ORDER BY dt.numero_dossier
''').fetchall()

print(f"Nombre de dossiers_tnb : {len(rows)}")
for r in rows:
    print(f"  Dossier #{r['numero_dossier']} | id={r['id']} | ctb={r['contribuable_id']} | {r['nom']} {r['prenom'] or r['raison_sociale'] or ''} | CIN:{r['cin']} RC:{r['rc']}")

# 2. Verifier les doublons par contribuable_id
print("\n=== DOUBLONS par contribuable_id ===")
dups = c.execute('''
    SELECT contribuable_id, COUNT(*) as n FROM dossiers_tnb
    GROUP BY contribuable_id HAVING n > 1
''').fetchall()
if dups:
    print(f"  PROBLEME: {len(dups)} contribuable(s) avec plusieurs dossiers!")
    for d in dups:
        print(f"  contribuable_id={d['contribuable_id']} a {d['n']} dossiers")
else:
    print("  OK: Pas de doublons")

# 3. Terrains sans dossier
print("\n=== Terrains sans dossier ===")
no_dos = c.execute('''
    SELECT t.id, t.contribuable_id, c.nom
    FROM terrains t
    JOIN contribuables c ON c.id = t.contribuable_id
    WHERE t.actif=1
      AND t.contribuable_id NOT IN (SELECT contribuable_id FROM dossiers_tnb)
''').fetchall()
if no_dos:
    print(f"  {len(no_dos)} terrain(s) sans dossier:")
    for t in no_dos:
        print(f"  terrain id={t['id']} | ctb={t['contribuable_id']} | {t['nom']}")
else:
    print("  OK: Tous les terrains ont un dossier")

# 4. Terrains par contribuable
print("\n=== Terrains par contribuable ===")
ter_ctb = c.execute('''
    SELECT t.contribuable_id, c.nom, COUNT(t.id) as nb,
           dt.id as dossier_id, dt.numero_dossier
    FROM terrains t
    JOIN contribuables c ON c.id = t.contribuable_id
    LEFT JOIN dossiers_tnb dt ON dt.contribuable_id = t.contribuable_id
    WHERE t.actif=1
    GROUP BY t.contribuable_id
    ORDER BY t.contribuable_id
''').fetchall()
for r in ter_ctb:
    print(f"  ctb={r['contribuable_id']} {r['nom']} => {r['nb']} terrain(s) | dossier_id={r['dossier_id']} | dossier_num={r['numero_dossier']}")

# === CORRECTION ===
print("\n=== CORRECTION ===")

# Supprimer les doublons (garder le plus petit id par contribuable_id)
if dups:
    print("Correction des doublons...")
    c.execute('''
        DELETE FROM dossiers_tnb
        WHERE id NOT IN (
            SELECT MIN(id) FROM dossiers_tnb GROUP BY contribuable_id
        )
    ''')
    conn.commit()
    print(f"  OK: doublons supprimes")

# Creer dossiers manquants
for t in no_dos:
    max_n = c.execute('SELECT COALESCE(MAX(numero_dossier),0) FROM dossiers_tnb').fetchone()[0]
    c.execute('INSERT INTO dossiers_tnb (numero_dossier, contribuable_id) VALUES (?,?)',
              (max_n + 1, t['contribuable_id']))
    conn.commit()
    print(f"  Dossier #{max_n+1} cree pour contribuable {t['contribuable_id']}")

# Renumeroter proprement
all_dos = c.execute('SELECT id FROM dossiers_tnb ORDER BY id ASC').fetchall()
for idx, row in enumerate(all_dos, start=1):
    c.execute('UPDATE dossiers_tnb SET numero_dossier=? WHERE id=?', (idx, row['id']))
conn.commit()
print(f"  OK: {len(all_dos)} dossiers renumerotes 1..{len(all_dos)}")

# Verification finale
print("\n=== RESULTAT FINAL ===")
final = c.execute('''
    SELECT dt.numero_dossier, c.nom, c.prenom, c.raison_sociale,
           COUNT(t.id) as nb_terrains
    FROM dossiers_tnb dt
    JOIN contribuables c ON c.id = dt.contribuable_id
    LEFT JOIN terrains t ON t.contribuable_id = dt.contribuable_id AND t.actif=1
    GROUP BY dt.id
    ORDER BY dt.numero_dossier
''').fetchall()
for r in final:
    print(f"  Dossier #{r['numero_dossier']} | {r['nom']} {r['prenom'] or r['raison_sociale'] or ''} | {r['nb_terrains']} terrain(s)")

conn.close()
print("\nTermine!")
