# 🏛️ JIBAYAT — Système de Gestion Fiscale Communale / Municipal Tax Management System

<div align="center">

![Version](https://img.shields.io/badge/version-1.4.9-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11-green?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.3-black?style=for-the-badge&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?style=for-the-badge&logo=sqlite)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)
![License](https://img.shields.io/badge/Licence-MIT-brightgreen?style=for-the-badge)

**🇫🇷 Application web complète pour la gestion fiscale et financière des communes marocaines.**

**🇬🇧 Full-featured web application for tax and financial management of Moroccan municipalities.**

[Fonctionnalités / Features](#-fonctionnalités--features) • [Installation](#-installation) • [Docker](#-déploiement-docker--docker-deployment) • [Modules](#-modules) • [Configuration](#-configuration)

</div>

---

## 🇫🇷 Présentation / 🇬🇧 Overview

### 🇫🇷 Français

**JIBAYAT** est un système de gestion fiscale communale développé en Python/Flask, conçu spécifiquement pour les besoins des communes marocaines. Il centralise la gestion de l'ensemble des taxes et redevances locales, du suivi des contribuables jusqu'à l'émission des bulletins de versement.

**Pourquoi JIBAYAT ?**

- 🎯 **Complet** : Couvre tous les types de taxes communales en un seul outil
- 🔒 **Sécurisé** : Authentification, CSRF, gestion fine des droits utilisateurs
- 📊 **Analytique** : Tableaux de bord avec graphiques de recouvrement
- 🐳 **Déployable** : Conteneurisé avec Docker, prêt pour Dokploy/Traefik
- 📄 **Documenté** : Génération automatique de PDF (avis, quittances, lettres)

---

### 🇬🇧 English

**JIBAYAT** is a municipal tax management system built with Python/Flask, designed specifically for Moroccan municipalities. It centralizes the management of all local taxes and fees, from taxpayer tracking to payment bulletin issuance.

**Why JIBAYAT?**

- 🎯 **Complete** : Covers all municipal tax types in a single tool
- 🔒 **Secure** : Authentication, CSRF protection, granular user permissions
- 📊 **Analytics** : Dashboards with revenue recovery charts
- 🐳 **Deployable** : Dockerized, ready for Dokploy/Traefik
- 📄 **Documented** : Automatic PDF generation (notices, receipts, letters)

---

## ✨ Fonctionnalités / Features

### 🏠 Tableau de bord / Dashboard
- 🇫🇷 KPIs globaux : contribuables actifs, bulletins en attente, avis émis. Graphiques interactifs (Chart.js).
- 🇬🇧 Global KPIs: active taxpayers, pending bulletins, issued notices. Interactive charts (Chart.js).

### 📑 Gestion des déclarations / Declaration Management
- 🇫🇷 Création multi-modules, calcul automatique des **pénalités** (5% + 0,5%/mois) et **amendes** (10%, min. 500 DH).
- 🇬🇧 Multi-module creation, automatic calculation of **penalties** (5% + 0.5%/month) and **fines** (10%, min. 500 MAD).

### 💳 Bulletins de versement / Payment Bulletins
- 🇫🇷 Workflow Agent → Régisseur, validation en masse, impression PDF des quittances.
- 🇬🇧 Agent → Treasurer workflow, bulk validation, PDF receipt printing.

### 📬 Avis & Recouvrement / Notices & Recovery
- 🇫🇷 Génération d'avis de non-paiement en lot ou individuel, historique des notifications.
- 🇬🇧 Batch or individual non-payment notice generation, notification history.

### 👥 Gestion des contribuables / Taxpayer Management
- 🇫🇷 Fiche complète (CIN, ICE, coordonnées), historique, import Excel/CSV.
- 🇬🇧 Full profile (national ID, tax ID, contact info), history, Excel/CSV import.

### ⚙️ Administration
- 🇫🇷 Gestion des utilisateurs, configuration des taux par module, mise à jour automatique depuis GitHub.
- 🇬🇧 User management, per-module rate configuration, automatic update from GitHub.

---

## 📦 Modules

| Module | Taxe / Tax | 🇫🇷 Description | 🇬🇧 Description |
|--------|-----------|----------------|----------------|
| 🏗️ **TNB** | Taxe sur les Terrains Non Bâtis | Gestion des terrains | Undeveloped land tax management |
| 🍺 **TDB** | Taxe sur les Débits de Boissons | Établissements avec licence | Licensed beverage outlets |
| 🚗 **Stationnement** | TPV Stationnement | Vignettes et droits | Parking stickers and fees |
| 🔑 **Fourrière** | Frais de Fourrière | Véhicules mis en fourrière | Vehicle impoundment fees |
| 🏪 **ODP** | Occupation Domaine Public | Terrasses, étalages, kiosques | Terraces, stalls, kiosks |
| 🏢 **Location** | Location Locaux Commerciaux | Locaux communaux | Municipal commercial premises |
| 🛒 **Souks** | Affermage des Souks | Droits de place marchés | Municipal market stall rights |
| 📋 **Émission** | Émission en Masse | Génération groupée | Bulk declaration generation |
| 📖 **Registre** | Registre Officiel | Registre des recettes | Official revenue register |
| 💼 **Régie** | Gestion de la Régie | Suivi du régisseur | Treasurer tracking |

---

## 🚀 Installation

### Prérequis / Prerequisites

- Python 3.11+
- pip

### 🇫🇷 Installation locale / 🇬🇧 Local Installation

```bash
# 1. Cloner le dépôt / Clone the repository
git clone https://github.com/USFOU/JIBAYAT.git
cd JIBAYAT

# 2. Créer un environnement virtuel / Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

# 3. Installer les dépendances / Install dependencies
pip install -r requirements.txt

# 4. Initialiser la base de données / Initialize the database
python -c "from database import init_db; init_db()"

# 5. Lancer l'application / Start the application
python app.py
```

🇫🇷 L'application sera accessible sur **http://localhost:5000**

🇬🇧 The application will be available at **http://localhost:5000**

### 🇫🇷 Lancement rapide (Windows) / 🇬🇧 Quick Start (Windows)

Double-cliquer sur / Double-click `LANCER.bat`

---

## 🐳 Déploiement Docker / Docker Deployment

```bash
# 🇫🇷 Construire et démarrer / 🇬🇧 Build and start
docker compose up -d --build

# 🇫🇷 Voir les logs / 🇬🇧 View logs
docker compose logs -f

# 🇫🇷 Arrêter / 🇬🇧 Stop
docker compose down
```

### Variables d'environnement / Environment Variables

| Variable | 🇫🇷 Description | 🇬🇧 Description | Défaut / Default |
|----------|----------------|----------------|-----------------|
| `JIBAYAT_SECRET_KEY` | Clé secrète Flask | Flask secret key | `super_secret_key_jibayat` |
| `FLASK_ENV` | Environnement Flask | Flask environment | `production` |

### Volumes persistants / Persistent Volumes

| Volume | Chemin / Path | 🇫🇷 Contenu | 🇬🇧 Content |
|--------|--------------|------------|------------|
| `jibayat_db` | `/app/data` | Base de données SQLite | SQLite database |
| `jibayat_uploads` | `/app/uploads` | Fichiers uploadés | Uploaded files |
| `jibayat_exports` | `/app/static/exports` | PDF générés | Generated PDFs |

---

## ⚙️ Configuration

```json
{
  "secret_key": "votre_cle_secrete / your_secret_key",
  "github_token": "ghp_votre_token_pour_mises_a_jour / ghp_your_update_token"
}
```

> ⚠️ 🇫🇷 **Ne jamais committer `config.json`** — il est listé dans `.gitignore`
>
> ⚠️ 🇬🇧 **Never commit `config.json`** — it is listed in `.gitignore`

---

## 🗄️ Architecture

```
JIBAYAT/
├── app.py                  # Orchestrateur principal Flask / Main Flask orchestrator
├── database.py             # Connexion & initialisation SQLite / SQLite connection & init
├── my_schema.sql           # Schéma complet BDD / Full database schema
├── requirements.txt        # Dépendances Python / Python dependencies
├── Dockerfile              # Image Docker
├── docker-compose.yml      # Composition des services / Service composition
│
├── modules/                # Blueprints Flask par module / Flask blueprints by module
│   ├── config.py
│   ├── contribuables.py
│   ├── tnb.py
│   ├── tdb.py
│   ├── stationnement.py
│   ├── fourriere.py
│   ├── occupation.py
│   ├── location.py
│   ├── souks.py
│   ├── regie.py
│   ├── emission/
│   ├── registre.py
│   ├── helpers.py
│   └── tgr_parser.py
│
├── templates/              # Templates Jinja2
├── static/                 # CSS, JS, images
└── uploads/                # Fichiers uploadés / Uploaded files (non versionné / not versioned)
```

---

## 🔐 Sécurité / Security

| 🇫🇷 | 🇬🇧 |
|-----|-----|
| Hashage SHA-256 des mots de passe | SHA-256 password hashing |
| Protection anti-CSRF sur toutes les routes POST | CSRF protection on all POST routes |
| Sessions chiffrées (durée 7 jours) | Encrypted sessions (7-day duration) |
| Droits granulaires par module | Granular permissions per module |

---

## 📚 Technologies

| Technologie | Version | Usage |
|-------------|---------|-------|
| Python | 3.11 | 🇫🇷 Langage principal / 🇬🇧 Main language |
| Flask | 3.0.3 | 🇫🇷 Framework web / 🇬🇧 Web framework |
| SQLite | — | 🇫🇷 Base de données / 🇬🇧 Database |
| Pandas | 2.2.2 | 🇫🇷 Import/export données / 🇬🇧 Data import/export |
| ReportLab | 4.2.0 | 🇫🇷 Génération PDF / 🇬🇧 PDF generation |
| Gunicorn | 22.0.0 | 🇫🇷 Serveur WSGI production / 🇬🇧 Production WSGI server |
| OpenPyXL | 3.1.2 | 🇫🇷 Lecture fichiers Excel / 🇬🇧 Excel file reading |
| Chart.js | — | 🇫🇷 Graphiques interactifs / 🇬🇧 Interactive charts |
| Bootstrap | — | 🇫🇷 Interface responsive / 🇬🇧 Responsive UI |

---

## 📝 Changelog

### v1.4.9 (Mai / May 2026)
- ✅ Module TDB : calcul des pénalités de retard (5% + 0,5%/mois) / late penalty calculation
- ✅ Module TDB : amende de non-déclaration Q4 (10%, min 500 DH) / non-declaration fine
- ✅ Dashboards par module avec graphiques / per-module dashboards with charts
- ✅ Import Excel amélioré sur Dokploy / improved Excel import on Dokploy
- ✅ Synchronisation Google Sheets / Google Sheets sync

---

## 👤 Auteur / Author

**Yomix90** — Développeur principal / Lead Developer

📧 GitHub : [https://github.com/USFOU](https://github.com/USFOU)

---

## 📄 Licence / License

🇫🇷 Ce projet est distribué sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

🇬🇧 This project is distributed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <strong>JIBAYAT</strong> — 🇫🇷 Gestion fiscale moderne pour les communes marocaines 🇲🇦 / 🇬🇧 Modern tax management for Moroccan municipalities 🇲🇦
</div>
