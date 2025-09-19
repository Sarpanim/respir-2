# Respir – Backend & Frontend

Ce dépôt contient un exemple complet pour la plateforme Respir :

- un backend FastAPI avec persistance SQLModel pour gérer les contenus et la progression,
- une application frontend Next.js/TypeScript orientée mobile-first, intégrant l'authentification Supabase par lien magique.

## Structure

```
backend/
├── app/
│   ├── config.py          # Configuration via variables d'environnement
│   ├── database.py        # Initialisation du moteur SQLModel
│   ├── dependencies.py    # Dépendances communes (authentification, sessions)
│   ├── main.py            # Point d'entrée FastAPI
│   ├── models/            # Modèles SQLModel pour PostgreSQL
│   ├── routers/           # Routes REST (cours, catégories, progression, ...)
│   ├── schemas/           # Schémas Pydantic pour les réponses/entrées
│   └── seeds.py           # Données de démonstration
└── requirements.txt       # Dépendances Python

app/                        # Application Next.js (App Router)
├── page.tsx               # Page d'accueil
├── login/                 # Formulaire de connexion (magic link)
├── dashboard/             # Tableau de bord protégé
├── auth/callback/         # Callback Supabase
└── logout/                # Déconnexion et nettoyage des cookies
lib/supabase/              # Clients Supabase (navigateur & serveur)
tailwind.config.ts         # Configuration Tailwind CSS
postcss.config.mjs         # Configuration PostCSS
.eslintrc.cjs / .prettierrc # Qualité de code (ESLint + Prettier)
```

## Installation

1. Créez et activez un environnement virtuel compatible Python 3.11.
2. Installez les dépendances :

   ```bash
   pip install -r backend/requirements.txt
   ```

3. Définissez les variables d'environnement nécessaires (voir ci-dessous). Vous pouvez créer un fichier `.env` à la racine du projet.

## Configuration

| Variable            | Description                                                                                     | Valeur par défaut                                                   |
|---------------------|-------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| `DATABASE_URL`      | Chaîne de connexion SQLAlchemy (recommandé : PostgreSQL).                                       | `postgresql+psycopg2://postgres:postgres@localhost:5432/respir`     |
| `ADMIN_API_KEY`     | Jeton statique requis dans l'en-tête `X-Admin-Token` pour les opérations d'administration.      | `change-me`                                                         |
| `AUTO_SEED`         | Active le chargement automatique des données de démonstration au démarrage (`true`/`false`).     | `false`                                                             |

## Lancement du backend

```bash
uvicorn backend.app.main:app --reload
```

L'API est documentée automatiquement via Swagger UI sur `http://localhost:8000/docs` et via Redoc sur `http://localhost:8000/redoc`.

## Sécurité et en-têtes

- Les opérations d'administration (création/modification/suppression de cours, catégories, niveaux et ambiances) sont protégées par un en-tête `X-Admin-Token`. Renseignez la même valeur que `ADMIN_API_KEY`.
- Les endpoints de progression utilisateur attendent les en-têtes `X-User-Email` (obligatoire) et `X-User-Name` (optionnel). Un utilisateur est créé automatiquement s'il n'existe pas.

## Progression utilisateur

Les endpoints `/progress` permettent :

- `POST /progress/start` : démarrer ou reprendre un cours.
- `POST /progress/{id}/log` : ajouter une durée d'écoute en secondes.
- `POST /progress/{id}/complete` : marquer un cours comme terminé.
- `GET /progress/me` : récupérer la progression de l'utilisateur courant.

Chaque évènement met à jour la durée totale d'écoute, les dates de démarrage/achèvement et le statut.

## Frontend Next.js

### Installation

1. Assurez-vous d'avoir Node.js ≥ 18.
2. Installez les dépendances NPM :

   ```bash
   npm install
   ```

3. Copiez le fichier `.env.example` en `.env.local` et complétez les valeurs Supabase :

   ```env
   NEXT_PUBLIC_SUPABASE_URL=https://djndymuaxwhhdflouljz.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqbmR5bXVheHdoaGRmbG91bGp6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc2MTEzMjksImV4cCI6MjA3MzE4NzMyOX0.BBW4ubsG6c6etU_4pdv0Qh0tNq4DBR_Tt7pY2A8STvI
   SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqbmR5bXVheHdoaGRmbG91bGp6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NzYxMTMyOSwiZXhwIjoyMDczMTg3MzI5fQ.f4o1jQc-6XUmQBNft_dlp01pLBFBVDUy9rxHByF1sNg
   ```

### Commandes utiles

```bash
npm run dev     # Démarre le serveur Next.js en développement
npm run build   # Build de production
npm run start   # Serveur Next.js en mode production
npm run lint    # Analyse ESLint
npm run format  # Vérification du formatage Prettier
```

### Authentification Supabase

- La page `/login` envoie un lien magique à l'email saisi via Supabase.
- Le callback `/auth/callback` échange le code Supabase, crée une session et stocke les tokens dans des cookies HTTP-only.
- Le tableau de bord `/dashboard` vérifie la présence de la session (redirection vers `/login` si nécessaire).
- Une route `/logout` supprime les cookies et redirige l'utilisateur vers la connexion.

## Données de démonstration

Pour insérer les données d'exemple sans activer `AUTO_SEED`, exécutez :

```bash
python -m backend.app.seeds
```

Cela crée des catégories, niveaux, ambiances et cours (avec leurs sessions) prêts à l'emploi.

## Exemple de requête

```bash
curl -X POST http://localhost:8000/courses \
  -H "Content-Type: application/json" \
  -H "X-Admin-Token: <votre_token_admin>" \
  -d '{
        "title": "Nouveau cours",
        "description": "Séance avancée",
        "duration_minutes": 25,
        "category_id": 1,
        "level_id": 2,
        "ambience_id": 1
      }'
```

L'API renverra l'objet créé et l'OpenAPI mettra automatiquement à jour la documentation.
