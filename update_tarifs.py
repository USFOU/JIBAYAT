from database import get_db

conn = get_db()
c = conn.cursor()

rub_id = c.execute("SELECT id FROM rubriques WHERE module='TNB'").fetchone()[0]
c.execute("UPDATE tarifs SET actif=0 WHERE rubrique_id=?", (rub_id,))

tarifs_to_insert = [
    ("TNB-ZA-22", "Zone A (2022)", 10.0, 'DH/m²', '2022-01-01', '2022-12-31', 0, None),
    ("TNB-ZB-22", "Zone B (2022)", 10.0, 'DH/m²', '2022-01-01', '2022-12-31', 0, None),
    ("TNB-ZC-22", "Zone C (2022)", 10.0, 'DH/m²', '2022-01-01', '2022-12-31', 0, None),
    
    ("TNB-ZA-25-1", "Zone A (<=200m²)", 10.0, 'DH/m²', '2023-01-01', '2025-12-31', 0, 200),
    ("TNB-ZB-25-1", "Zone B (<=200m²)", 10.0, 'DH/m²', '2023-01-01', '2025-12-31', 0, 200),
    ("TNB-ZC-25-1", "Zone C (<=200m²)", 10.0, 'DH/m²', '2023-01-01', '2025-12-31', 0, 200),
    
    ("TNB-ZA-25-2", "Zone A (201-1000m²)", 5.0, 'DH/m²', '2023-01-01', '2025-12-31', 200.01, 1000),
    ("TNB-ZB-25-2", "Zone B (201-1000m²)", 5.0, 'DH/m²', '2023-01-01', '2025-12-31', 200.01, 1000),
    ("TNB-ZC-25-2", "Zone C (201-1000m²)", 5.0, 'DH/m²', '2023-01-01', '2025-12-31', 200.01, 1000),
    
    ("TNB-ZA-25-3", "Zone A (>1000m²)", 2.0, 'DH/m²', '2023-01-01', '2025-12-31', 1000.01, None),
    ("TNB-ZB-25-3", "Zone B (>1000m²)", 2.0, 'DH/m²', '2023-01-01', '2025-12-31', 1000.01, None),
    ("TNB-ZC-25-3", "Zone C (>1000m²)",  2.0, 'DH/m²', '2023-01-01', '2025-12-31', 1000.01, None),

    ("TNB-ZA-26", "Zone A", 15.0, 'DH/m²', '2026-01-01', None, 0, None),
    ("TNB-ZB-26", "Zone B", 5.0, 'DH/m²', '2026-01-01', None, 0, None),
    ("TNB-ZC-26", "Zone C", 5.0, 'DH/m²', '2026-01-01', None, 0, None)
]

arrete_id = c.execute("SELECT id FROM arretes_fiscaux ORDER BY date_effet DESC LIMIT 1").fetchone()[0]

for t in tarifs_to_insert:
    actif = 1 if t[5] is None else 0
    c.execute('''INSERT INTO tarifs
        (rubrique_id, arrete_id, code_tarif, libelle, valeur, unite, date_debut, date_fin, surface_min, surface_max, actif)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (rub_id, arrete_id, t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], actif))

conn.commit()
conn.close()
print("Done")
