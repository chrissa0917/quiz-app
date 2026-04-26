# Quiz App Monorepo (Flask + React + Express)

This repo keeps the latest working deployment structure in one place:

- `app.py` (root Flask entrypoint for hosts expecting Flask autodetection)
- `frontend/` (Vite + React app)
- `backend/` (Express API + Prisma)

## Repository layout

```text
.
├── app.py
├── Procfile
├── requirements.txt
├── templates/
├── frontend/
└── backend/
```

## Deployment targets

### Flask entrypoint (root)

- Entrypoint file: `app.py`
- App object: `app`
- Start command (Procfile): `gunicorn app:app`

### Frontend (Vercel)

- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`
- Env var: `VITE_API_BASE_URL=https://<your-render-api>.onrender.com`

### Backend (Render)

- Root directory: `backend`
- Build command: `npm install && npx prisma generate && npx prisma migrate deploy`
- Start command: `npm start`
- Env vars: `DATABASE_URL`, `CORS_ORIGIN`

## Dependency notes

- Python dependencies are isolated in `requirements.txt` for Flask deployment.
- Node dependencies are isolated per app in:
  - `frontend/package.json`
  - `backend/package.json`

## Quick checks

```bash
python -m py_compile app.py
node --check backend/src/server.js
node --check backend/src/questions.js
node --check frontend/vite.config.js
```

## Conflict-resolution status

- Only one `app.py` exists at repo root.
- Flask entrypoint + Procfile + requirements are present.
- Frontend and backend folders are both present and separate.
- No merge conflict markers remain.

## Branching for PRs

Recommended flow for a clean PR branch:

```bash
git checkout -b feature/<name>
git fetch origin
git rebase origin/main
```

Resolve conflicts (if any), then push the feature branch.
