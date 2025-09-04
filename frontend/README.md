# Notes Frontend — React (Vite) + Vercel

Set `VITE_API_URL` to your FastAPI base URL (e.g., `https://your-notes-api.onrender.com`).

## Run locally

```bash
cd frontend
npm install
npm run dev
```

## Build

```bash
npm run build
npm run preview
```

## Vercel

- Import the repo in Vercel, set **Root Directory** to `frontend`.
- Add env var **VITE_API_URL** with your backend URL.
- Framework Preset: `Vite` (or Auto-detect).