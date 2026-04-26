# Cloud-ready Quiz App (Vercel + Render)

This repo is intentionally split so the frontend and backend deploy independently and stay small:

- **Frontend (`/frontend`)**: React + Vite on **Vercel**.
- **Backend (`/backend`)**: Express + Prisma on **Render**.

## Architecture constraints

- Frontend is React-only and calls backend via `VITE_API_BASE_URL`.
- No backend logic is bundled into the frontend build.
- Backend exposes JSON endpoints only (`/health`, `/api/questions`, `/api/submit`).
- No browser automation packages (Puppeteer/Playwright) are used.
- Prisma is configured for hosted PostgreSQL.

## Environment variables

### Frontend (`frontend/.env`)

```bash
VITE_API_BASE_URL="https://your-render-service.onrender.com"
```

### Backend (`backend/.env`)

```bash
DATABASE_URL="postgresql://USER:PASSWORD@HOST:5432/DB?schema=public"
PORT=8080
CORS_ORIGIN="https://your-vercel-app.vercel.app"
```

> `CORS_ORIGIN` supports comma-separated origins if needed.

## Local development

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

## Deploy to Vercel (frontend)

1. Import this repository in Vercel.
2. Set **Root Directory** to `frontend`.
3. Set build/output settings:
   - Build command: `npm run build`
   - Output directory: `dist`
4. Add env var:
   - `VITE_API_BASE_URL=https://<your-render-service>.onrender.com`
5. Deploy.

This keeps Vercel deployment limited to the frontend app and avoids packaging backend artifacts.

## Deploy to Render (backend)

1. Create a new **Web Service** in Render from this repository.
2. Set **Root Directory** to `backend`.
3. Configure:
   - Build command: `npm install && npx prisma generate && npx prisma migrate deploy`
   - Start command: `npm start`
4. Add env vars:
   - `DATABASE_URL`
   - `CORS_ORIGIN` (your Vercel URL)
5. Deploy.

A starter `render.yaml` is included.

## Keeping the production bundle small

- Keep frontend root on `frontend` in Vercel.
- Keep backend root on `backend` in Render.
- Do not commit `node_modules`, `dist`, `build`, or `.next`.
- Use `.gitignore` in this repo to prevent large artifact commits.
