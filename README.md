# 🏛️ JIBAYAT — Système de Gestion Fiscale Communale

<div align="center">

![Version](https://img.shields.io/badge/version-1.4.9-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-green?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.3-black?style=for-the-badge&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?style=for-the-badge&logo=sqlite)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)
![License](https://img.shields.io/badge/Licence-Propriétaire-red?style=for-the-badge)

**Application web complète pour la gestion fiscale et financière des communes marocaines.**

[Fonctionnalités](#-fonctionnalités) • [Installation](#-installation) • [Déploiement Docker](#-déploiement-docker) • [Modules](#-modules) • [Configuration](#-configuration)

</div>

---

## 📋 Présentation

**JIBAYAT** est un système de gestion fiscale communale développé en Python/Flask, conçu spécifiquement pour les besoins des communes marocaines. Il centralise la gestion de l'ensemble des taxes et redevances locales, du suivi des contribuables jusqu'à l'émission des bulletins de versement.

### Pourquoi JIBAYAT ?

- 🎯 **Complet** : Couvre tous les types de taxes communales en un seul outil
- 🔒 **Sécurisé** : Authentification, CSRF, gestion fine des droits utilisateurs
- 📊 **Analytique** : Tableaux de bord avec graphiques de recouvrement
- 🐳 **Déployable** : Conteneurisé avec Docker, prêt pour Dokploy/Traefik
- 📄 **Documenté** : Génération automatique de PDF (avis, quittances, lettres)

---

## ✨ Fonctionnalités

### 🏠 Tableau de bord principal
- KPIs globaux : contribuables actifs, bulletins en attente, avis émis
- Graphiques interactifs (Chart.js) : recouvrement mensuel, répartition par module
- Accès rapide aux déclarations récentes

### 📑 Gestion des déclarations
- Création de déclarations multi-modules avec calcul automatique
- Calcul des **pénalités de retard** (5% + 0,5% par mois)
- Calcul des **amendes de non-déclaration** (10% min. 500 DH)
- Statuts : `émis` → `en attente` → `payé` / `rejeté` / `annulé`

### 💳 Bulletins de versement
- Workflow : Agent crée → Régisseur valide/rejette
- Validation en masse avec numéro de quittance unique
- Impression PDF des quittances

### 📬 Avis & Recouvrement
- Génération d'avis de non-paiement en lot ou individuel
- Historique des lettres de notification
- Filtres avancés (module, statut, année)

### 👥 Gestion des contribuables
- Fiche complète (CIN, ICE, coordonnées)
- Historique de toutes les déclarations et paiements
- Import depuis fichiers Excel/CSV

### ⚙️ Administration
- Gestion des utilisateurs et des droits
- Configuration des paramètres par module (taux, tarifs)
- Mise à jour automatique depuis GitHub
- Import de données depuis fichiers Excel

---

## 📦 Modules

| Module | Taxe | Description |
|--------|------|-------------|
| 🏗️ **TNB** | Taxe sur les Terrains Non Bâtis | Gestion des terrains et calcul de la TNB |
| 🍺 **TDB** | Taxe sur les Débits de Boissons | Établissements avec licence de débit |
| 🚗 **Stationnement** | TPV Stationnement | Vignettes et droits de stationnement |
| 🔑 **Fourrière** | Frais de Fourrière | Gestion des véhicules mis en fourrière |
| 🏪 **ODP** | Occupation Domaine Public | Terrasses, étalages, kiosques |
| 🏢 **Location** | Location Locaux Commerciaux | Locaux propriété de la commune |
| 🛒 **Souks** | Affermage des Souks | Droits de place marchés communaux |
| 📋 **Émission** | Émission en Masse | Génération groupée de déclarations |
| 📖 **Registre** | Registre Officiel | Registre chronologique des recettes |
| 💼 **Régie** | Gestion de la Régie | Suivi du régisseur et caisse |

---

## 🚀 Installation

### Prérequis

- Python 3.11+
- pip

### Installation locale

```bash
# 1. Cloner le dépôt
git clone https://github.com/Yomix90/JIBAYAT.git
cd JIBAYAT

# 2. Créer un environnement virtuel
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Initialiser la base de données
python -c "from database import init_db; init_db()"

# 5. Lancer l'application
python app.py
```

L'application sera accessible sur **http://localhost:5000**

### Lancement rapide (Windows)

Double-cliquer sur `LANCER.bat`

---

## 🐳 Déploiement Docker

### Avec Docker Compose

```bash
# Construire et démarrer
docker compose up -d --build

# Voir les logs
docker compose logs -f

# Arrêter
docker compose down
```

### Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `JIBAYAT_SECRET_KEY` | Clé secrète Flask | `super_secret_key_jibayat` |
| `FLASK_ENV` | Environnement Flask | `production` |

### Volumes persistants

| Volume | Chemin dans le conteneur | Contenu |
|--------|--------------------------|---------|
| `jibayat_db` | `/app/data` | Base de données SQLite |
| `jibayat_uploads` | `/app/uploads` | Fichiers uploadés |
| `jibayat_exports` | `/app/static/exports` | PDF générés |

### Déploiement sur Dokploy

Le fichier `docker-compose.yml` est préconfiguré pour Dokploy avec le réseau Traefik `dokploy-network`.

---

## ⚙️ Configuration

Le fichier `config.json` (non versionné) permet de personnaliser l'application :

```json
{
  "secret_key": "votre_cle_secrete",
  "github_token": "ghp_votre_token_pour_mises_a_jour"
}
```

> ⚠️ **Ne jamais committer `config.json`** — il est listé dans `.gitignore`

### Mise à jour automatique

JIBAYAT vérifie automatiquement les nouvelles versions sur GitHub au démarrage. Si un token GitHub est configuré, les dépôts privés sont également supportés.

Pour mettre à jour manuellement, utiliser le script `git_pull.bat` ou `GIT_PULL_GITHUB.bat`.

---

## 🗄️ Architecture

```
JIBAYAT/
├── app.py                  # Orchestrateur principal Flask
├── database.py             # Connexion & initialisation SQLite
├── my_schema.sql           # Schéma complet de la base de données
├── requirements.txt        # Dépendances Python
├── Dockerfile              # Image Docker
├── docker-compose.yml      # Composition des services
│
├── modules/                # Blueprints Flask par module
│   ├── config.py           # Configuration & paramètres
│   ├── contribuables.py    # Gestion des contribuables
│   ├── tnb.py              # Module TNB
│   ├── tdb.py              # Module Débits de Boissons
│   ├── stationnement.py    # Module Stationnement
│   ├── fourriere.py        # Module Fourrière
│   ├── occupation.py       # Module ODP
│   ├── location.py         # Module Location
│   ├── souks.py            # Module Souks
│   ├── regie.py            # Module Régie
│   ├── emission/           # Module Émission en masse
│   ├── registre.py         # Registre officiel
│   ├── helpers.py          # Fonctions utilitaires partagées
│   └── tgr_parser.py       # Parseur fichiers TGR
│
├── templates/              # Templates Jinja2
├── static/                 # CSS, JS, images
└── uploads/                # Fichiers uploadés (non versionné)
```

---

## 🔐 Sécurité

- **Authentification** : Hashage SHA-256 des mots de passe
- **CSRF** : Protection anti-CSRF sur toutes les routes POST
- **Sessions** : Sessions chiffrées avec durée de 7 jours
- **Droits granulaires** : Chaque utilisateur a des permissions spécifiques par module
  - `peut_creer_bulletin` — Création de bulletins de versement
  - `peut_valider_paiement` — Validation réservée au Régisseur

---

## 📚 Technologies utilisées

| Technologie | Version | Usage |
|-------------|---------|-------|
| Python | 3.11 | Langage principal |
| Flask | 3.0.3 | Framework web |
| SQLite | — | Base de données |
| Pandas | 2.2.2 | Import/export données |
| ReportLab | 4.2.0 | Génération PDF |
| Gunicorn | 22.0.0 | Serveur WSGI production |
| OpenPyXL | 3.1.2 | Lecture fichiers Excel |
| Chart.js | — | Graphiques interactifs |
| Bootstrap | — | Interface responsive |

---

## 📝 Changelog

### v1.4.9 (Mai 2026)
- ✅ Module TDB : calcul des pénalités de retard (5% + 0,5%/mois)
- ✅ Module TDB : amende de non-déclaration Q4 (10%, min 500 DH)
- ✅ Dashboards par module avec graphiques interactifs
- ✅ Import Excel amélioré sur Dokploy
- ✅ Synchronisation Google Sheets

### v1.4.x
- Module Émission en masse
- Registre officiel des recettes
- Module Régie complet

---

## 👤 Auteur

**Yomix90** — Développeur principal

📧 GitHub : [https://github.com/Yomix90](https://github.com/Yomix90)

---

## 📄 Licence

Ce projet est un logiciel propriétaire. Tous droits réservés.  
Usage réservé aux communes marocaines autorisées.

---

<div align="center">
  <strong>JIBAYAT</strong> — Gestion fiscale moderne pour les communes marocaines 🇲🇦
</div>
