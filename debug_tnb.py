"""Debug complet - teste la route TNB avec Flask test client"""
import sys, os, traceback
sys.path.insert(0, 'c:/Users/USF/Desktop/JIBAYAT')
os.chdir('c:/Users/USF/Desktop/JIBAYAT')

# Importer l'app
try:
    from app import app
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        # Login
        r = client.post('/login', data={
            'email': 'admin@commune.ma',
            'password': 'admin123'
        }, follow_redirects=True)
        print('Login status:', r.status_code)

        # Test /tnb
        try:
            r2 = client.get('/tnb', follow_redirects=True)
            content = r2.data.decode('utf-8', errors='ignore')
            print('TNB status:', r2.status_code)
            if r2.status_code == 500:
                # Find error details
                import re
                # Look for Python traceback in HTML
                m = re.search(r'OperationalError|AttributeError|TypeError|NameError|KeyError.*?(?=<)', content)
                if m:
                    print('Error type:', m.group(0)[:500])
                # Print the first 2000 chars
                print('Content start:', content[:3000])
            elif r2.status_code == 200:
                if 'N\u00b0 Dossier' in content or 'Dossier' in content:
                    print('OK: Dossier column found')
                if 'Lotissement' in content:
                    print('OK: Lotissement found')
                print('TNB page rendered successfully!')
        except Exception as e:
            print('Route error:')
            traceback.print_exc()
except Exception as e:
    print('App import error:')
    traceback.print_exc()
