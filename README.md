# Judo Club Hem - Plateforme de Gestion

Bienvenue sur le dépôt officiel de l'application de gestion du Judo Club Hem.
Ce projet a été développé pour moderniser et simplifier la gestion administrative du club, des inscriptions aux paiements, en passant par le suivi des adhérents.

## 📋 Fonctionnalités

L'application est divisée en deux portails principaux :

### Pour l'Administration
- **Tableau de bord global** : Statistiques en temps réel (inscriptions, chiffre d'affaires, parité).
- **Gestion des Adhérents** : Fiches complètes, suivi des ceintures, certificats médicaux.
- **Inscriptions 100% en ligne** : Processus dématérialisé avec calcul automatique du tarif (réductions familiales, aides mairie, pass sport).
- **Finances** : Suivi des paiements, facturation automatique, exports comptables.
- **Événements** : Gestion des compétitions et convocations.

### Pour les Familles (Espace Parent)
- **Inscription simplifiée** : Inscrire plusieurs enfants en quelques clics.
- **Suivi administratif** : Accès aux factures, convocations et informations des enfants.
- **Paiement sécurisé** : Intégration pour le règlement des cotisations.

## 🛠 Stack Technique

Ce projet utilise une architecture moderne et conteneurisée :

- **Frontend** : Vue.js 3, Vite, TailwindCSS (Interface moderne et responsive).
- **Backend** : Django 5, Django REST Framework (API robuste et sécurisée).
- **Base de données** : PostgreSQL.
- **Cache & Files d'attente** : Redis, Celery (pour les tâches asynchrones comme l'envoi d'emails).
- **Infrastructure** : Docker & Docker Compose.

## 🚀 Installation et Démarrage

### Prérequis
- Docker et Docker Compose installés sur votre machine.
- Git.

### 1. Cloner le projet
```bash
git clone https://github.com/saidzaier10/JCH.git
cd JCH
```

### 2. Configuration
Créez un fichier `.env` à la racine du projet (basé sur `.env.example` si disponible) avec vos variables d'environnement (Base de données, Clés secrètes, etc.).

### 3. Démarrage
Lancez l'ensemble de la stack technique avec Docker Compose :

```bash
docker-compose up --build -d
```

L'application sera accessible aux adresses suivantes :
- **Frontend** : `http://localhost:5173`
- **Backend API** : `http://localhost:8000`
- **Interface Admin Django** : `http://localhost:8000/admin`

## 📦 Scripts de Maintenance

Des scripts sont disponibles via `manage.py` pour initialiser les données ou effectuer des migrations. Les dépendances sont gérées automatiquement au démarrage des conteneurs.

---

**© 2024-2025 Said Zaier.** Tous droits réservés.
Ce code est la propriété exclusive de Said Zaier. Toute reproduction ou distribution non autorisée est interdite.
