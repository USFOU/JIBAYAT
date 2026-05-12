import sqlite3

def fix_db():
    conn = sqlite3.connect('fiscalite.db')
    c = conn.cursor()
    
    # Check app_modules
    c.execute('PRAGMA table_info(app_modules)')
    columns = [col[1] for col in c.fetchall()]
    
    if not columns:
        # Table does not exist, create it
        c.execute('''
        CREATE TABLE app_modules (
            code TEXT PRIMARY KEY,
            nom TEXT,
            description TEXT,
            actif INTEGER DEFAULT 1,
            ordre INTEGER DEFAULT 10
        )''')
    else:
        if 'nom' not in columns:
            c.execute('ALTER TABLE app_modules ADD COLUMN nom TEXT')
        if 'description' not in columns:
            c.execute('ALTER TABLE app_modules ADD COLUMN description TEXT')
        if 'actif' not in columns:
            c.execute('ALTER TABLE app_modules ADD COLUMN actif INTEGER DEFAULT 1')
        if 'ordre' not in columns:
            c.execute('ALTER TABLE app_modules ADD COLUMN ordre INTEGER DEFAULT 10')
            
    # Check role_module_permissions
    c.execute('PRAGMA table_info(role_module_permissions)')
    columns_rmp = [col[1] for col in c.fetchall()]
    if not columns_rmp:
        c.execute('''
        CREATE TABLE role_module_permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
            module_code TEXT REFERENCES app_modules(code) ON DELETE CASCADE,
            peut_voir INTEGER DEFAULT 1,
            peut_ajouter INTEGER DEFAULT 0,
            peut_modifier INTEGER DEFAULT 0,
            peut_supprimer INTEGER DEFAULT 0,
            UNIQUE(role_id, module_code)
        )''')
        
    app_modules_default = [
        ('TNB', 'Taxe sur les Terrains Urbains Non Bâtis', '', 1, 10),
        ('DEBITS_BOISSONS', 'Taxe sur les Débits de Boissons', '', 1, 20),
        ('STATIONNEMENT', 'Taxe de Stationnement / TPV', '', 1, 30),
        ('OCCUPATION_DOMAINE', 'Occupation du Domaine Public', '', 1, 40),
        ('FOURRIERE', 'Droits de Fourrière', '', 1, 50),
        ('LOCATION_LOCAUX', 'Location des Locaux Commerciaux', '', 1, 60),
        ('AFFERMAGE_SOUKS', 'Affermage des Souks', '', 1, 70),
        ('REGIE', 'Régie & État Civil', '', 1, 80)
    ]
    
    for m in app_modules_default:
        c.execute('INSERT OR IGNORE INTO app_modules (code, nom, description, actif, ordre) VALUES (?,?,?,?,?)', m)
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    fix_db()
    print("DB FIXED")
