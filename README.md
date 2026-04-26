# Cloud-ready Quiz App

This project is split for cloud deployment:

- **Frontend (`/frontend`)**: React + Vite, deploy to **Vercel**.
- **Backend (`/backend`)**: Express API + Prisma, deploy to **Render** with hosted Postgres.

## Why this layout

- No backend logic is embedded in the frontend bundle.
- Backend uses lightweight HTTP handling only (`express` + `fetch` from browser).
- No browser automation tooling (Puppeteer/Playwright) is used.
- Prisma is configured for hosted PostgreSQL.

## Local setup

### 1) Backend

```bash
cd backend
cp .env.example .env
npm install
npx prisma generate
npm start
```

### 2) Frontend

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Set `VITE_API_BASE_URL` to your backend URL.

## Deployment

### Vercel (frontend)

- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`
- Environment variable: `VITE_API_BASE_URL=https://<your-render-service>.onrender.com`

### Render (backend)

Use `render.yaml` or set service manually:
- Root directory: `backend`
- Build command: `npm install && npx prisma generate && npx prisma migrate deploy`
- Start command: `npm start`
- Environment variables: `DATABASE_URL`, `CORS_ORIGIN`
