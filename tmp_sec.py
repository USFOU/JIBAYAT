lines = open('modules/location.py', encoding='utf-8').readlines()

# Trouver la ligne 777 (index 776) - debut du bloc boutiques_non_exploitees
# Jusqu'a la ligne conn.close() + return render_template
start_idx = 776  # L777

# Trouver la fin du bloc (conn.close() + return render_template)
end_idx = None
for i in range(start_idx, min(start_idx + 30, len(lines))):
    if 'return render_template' in lines[i] and 'loc_secteurs' in lines[i]:
        end_idx = i + 1  # inclure la ligne return
        break

print(f'Block: L{start_idx+1} to L{end_idx}')
for i in range(start_idx, end_idx):
    print(f'L{i+1}: {repr(lines[i][:70])}')

NEW_BLOCK = '''    # Boutiques non exploit\u00e9es
    boutiques_non_exploitees = conn.execute(\'\'\'
        SELECT bo.*, lt.libelle as tarif_libelle, lt.valeur as tarif_valeur, lt.type_tarif,
               s.libelle as secteur_libelle, s.code as secteur_code
        FROM loc_boutiques bo
        JOIN loc_tarifs lt ON lt.id=bo.tarif_id
        JOIN loc_secteurs s ON s.id=lt.secteur_id
        WHERE bo.statut=\'disponible\'
        ORDER BY s.code, bo.numero
    \'\'\').fetchall()

    # Arr\u00eat\u00e9 fiscal actif
    arrete_actif = conn.execute(
        "SELECT * FROM arretes_fiscaux WHERE statut=\'actif\' ORDER BY id DESC LIMIT 1"
    ).fetchone()

    # Enrichir les tarifs avec infos de synchro avec l\'arrete
    for d in data:
        for td in d[\'tarifs\']:
            lt = td[\'tarif\']
            if lt.get(\'tarif_fiscal_id\'):
                tf = conn.execute(
                    \'SELECT valeur, date_debut, date_fin, actif FROM tarifs WHERE id=?\',
                    (lt[\'tarif_fiscal_id\'],)
                ).fetchone()
                if tf:
                    valeur_arrete = float(tf[\'valeur\'])
                    valeur_loc    = float(lt[\'valeur\'])
                    td[\'tarif\'][\'valeur_arrete\']       = valeur_arrete
                    td[\'tarif\'][\'date_arrete\']         = tf[\'date_debut\']
                    td[\'tarif\'][\'synchro_ok\']          = (abs(valeur_arrete - valeur_loc) < 0.01)
                    td[\'tarif\'][\'tarif_actif_arrete\']  = bool(tf[\'actif\'])
                else:
                    td[\'tarif\'][\'synchro_ok\'] = False
                    td[\'tarif\'][\'valeur_arrete\'] = None
            else:
                td[\'tarif\'][\'synchro_ok\'] = False
                td[\'tarif\'][\'valeur_arrete\'] = None

    conn.close()
    return render_template(\'location/loc_secteurs.html\', user=user, data=data,
                           boutiques_non_exploitees=boutiques_non_exploitees,
                           arrete_actif=arrete_actif)
'''

lines[start_idx:end_idx] = [NEW_BLOCK]
open('modules/location.py', 'w', encoding='utf-8').writelines(lines)
print(f'OK - rewritten')

import py_compile
py_compile.compile('modules/location.py', doraise=True)
print('Syntaxe OK')
