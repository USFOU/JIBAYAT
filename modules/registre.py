from flask import Blueprint, render_template, request
from database import get_db
from modules.helpers import login_required, get_current_user

bp = Blueprint('registre', __name__, url_prefix='/registre')

MODULES_REGISTRE = {
    'TNB': 'Taxe sur les Terrains Non Bâtis',
    'DEBITS_BOISSONS': 'Taxe sur les Débits de Boissons',
    'OCCUPATION_DOMAINE': 'Occupation du Domaine Public',
    'LOCATION_LOCAUX': 'Location Locaux Commerciaux'
}

@bp.route('/')
@login_required
def index():
    user = get_current_user()
    return render_template('registre/index.html', user=user, modules=MODULES_REGISTRE)

@bp.route('/paiements/<module_key>')
@login_required
def paiements(module_key):
    user = get_current_user()
    if module_key not in MODULES_REGISTRE:
        return "Module invalide", 400
        
    import datetime
    annee_selected = request.args.get('annee', type=int, default=datetime.datetime.now().year)
    
    conn = get_db()
    # 1. Récupérer tous les contribuables pour ce module
    contribuables = conn.execute('''
        SELECT DISTINCT c.id, c.nom, c.prenom, c.cin, c.ice, c.adresse, c.telephone, c.raison_sociale
        FROM contribuables c
        JOIN declarations d ON c.id = d.contribuable_id
        WHERE d.module = ?
        ORDER BY c.nom, c.prenom
    ''', (module_key,)).fetchall()
    
    # 2. Récupérer toutes les opérations validées ou émises pour ce module
    operations_all = conn.execute('''
        SELECT d.id as decl_id, d.contribuable_id, d.annee, d.trimestre, d.montant_total as montant_declare,
               b.numero_quittance, b.date_quittance, b.montant as montant_paye, d.notes, d.statut
        FROM declarations d
        LEFT JOIN bulletins b ON d.id = b.declaration_id AND b.statut = 'paye'
        WHERE d.module = ? AND d.montant_total > 0
        ORDER BY d.annee DESC, d.trimestre DESC
    ''', (module_key,)).fetchall()
    conn.close()
    
    # 3. Construire le tableau de données
    lignes_registre = []
    
    for ctb in contribuables:
        ops_ctb = [op for op in operations_all if op['contribuable_id'] == ctb['id']]
        
        # Chercher les opérations de l'année sélectionnée
        ops_annee = [op for op in ops_ctb if op['annee'] == annee_selected]
        
        if ops_annee:
            # S'il y a des opérations pour cette année, on les ajoute toutes (par ex: 4 trimestres)
            for op in ops_annee:
                lignes_registre.append({
                    'contribuable': dict(ctb),
                    'operation': dict(op),
                    'is_last_fallback': False
                })
        else:
            # S'il n'y a pas d'opération pour l'année demandée, on cherche la dernière opération connue
            if ops_ctb:
                # ops_ctb est déjà trié par année DESC, trimestre DESC
                last_op = ops_ctb[0]
                lignes_registre.append({
                    'contribuable': dict(ctb),
                    'operation': dict(last_op),
                    'is_last_fallback': True
                })
            else:
                # Aucun historique valide ? Normalement impossible vu le SELECT DISTINCT initial
                pass
                
    # Pour afficher les années disponibles dans le filtre
    annees_dispo = sorted(list(set([op['annee'] for op in operations_all])), reverse=True)
    if not annees_dispo:
        annees_dispo = [annee_selected]
        
    template_name = f'registre/paiements_{module_key}.html'
    import os
    from flask import current_app
    # Si le template spécifique n'existe pas encore, on se rabat sur un template générique
    if not os.path.exists(os.path.join(current_app.template_folder, 'registre', f'paiements_{module_key}.html')):
        template_name = 'registre/paiements_global.html'
        
    return render_template(template_name, 
                           user=user, 
                           module_key=module_key, 
                           module_name=MODULES_REGISTRE[module_key],
                           lignes_registre=lignes_registre,
                           annee_selected=annee_selected,
                           annees_dispo=annees_dispo)

@bp.route('/declarations/<module_key>')
@login_required
def declarations(module_key):
    user = get_current_user()
    if module_key not in ['TNB', 'DEBITS_BOISSONS']:
        return "Module invalide", 400
        
    conn = get_db()
    declarations_list = conn.execute('''
        SELECT d.*, c.nom, c.prenom, c.cin, c.raison_sociale, c.ice
        FROM declarations d
        JOIN contribuables c ON d.contribuable_id = c.id
        WHERE d.module = ?
        ORDER BY d.annee DESC, d.trimestre DESC, d.date_declaration DESC
    ''', (module_key,)).fetchall()
    conn.close()
    
    return render_template('registre/declarations.html',
                           user=user,
                           module_key=module_key,
                           module_name=MODULES_REGISTRE[module_key],
                           declarations=declarations_list)
