"""Verifier le contenu HTML de la page TNB - combien de dossier-cards ?"""
import sys, os
sys.path.insert(0, 'c:/Users/USF/Desktop/JIBAYAT')
os.chdir('c:/Users/USF/Desktop/JIBAYAT')

from app import app
app.config['TESTING'] = True

with app.test_client() as client:
    client.post('/login', data={'email': 'admin@commune.ma', 'password': 'admin123'}, follow_redirects=True)
    r = client.get('/tnb', follow_redirects=True)
    content = r.data.decode('utf-8', errors='ignore')

    import re
    # Compter les dossier-cards
    cards = re.findall(r'class="dossier-card', content)
    print(f"Nombre de dossier-cards dans le HTML: {len(cards)}")

    # Trouver les noms et numeros de dossier affichés
    # Chercher les numero_dossier dans les headers
    nums = re.findall(r'Dossier\s*#?(\d+)', content)
    noms = re.findall(r'dossier-nom[^>]*>.*?👤\s*([^<]+)<', content, re.DOTALL)
    print(f"Numeros de dossier trouves: {nums[:20]}")

    # Verifier OUHCHOUCH - combien de fois apparait-il ?
    ouhchouch_count = content.lower().count('ouhchouch')
    print(f"OUHCHOUCH apparait {ouhchouch_count} fois dans la page")

    # Verifier si c'est bien 5 dossiers (1 par personne)
    if len(cards) == 5:
        print("CORRECT: 5 dossiers (1 par personne)")
    elif len(cards) == 6:
        print("PROBLEME: 6 cards - un terrain de OUHCHOUCH est peut-etre separe")
    else:
        print(f"PROBLEME: {len(cards)} cards attendu 5")

    # Chercher les lignes de terrains dans OUHCHOUCH
    ouhchouch_idx = content.find('OUHCHOUCH')
    if ouhchouch_idx > 0:
        bloc = content[ouhchouch_idx:ouhchouch_idx+3000]
        terrain_rows = bloc.count('terrains-table')
        print(f"Tables de terrains dans le bloc OUHCHOUCH: {terrain_rows}")
