# Notes App — React (Vercel) + FastAPI (Render)

A minimal, production-ready example with CRUD and shareable public links.

## Monorepo layout

```
notes-app-fastapi-react/
├─ backend/    # FastAPI API (Render/Railway/Fly/Heroku)
└─ frontend/   # React (Vite) UI (Vercel)
```

## Quickstart (local)

1) **Backend**

```bash
cd backend
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs

2) **Frontend**

```bash
cd frontend
npm install
# Point frontend at local API (already defaulted in .env.example)
npm run dev
```

Visit the dev server URL shown (usually http://localhost:5173).

## Deploying

### 1) Deploy API on Render (recommended for SQLite persistence)

- Create a new Web Service from your GitHub repo, set **Root Directory** = `backend`.
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Add Env Var `ALLOWED_ORIGINS` with your Vercel domain (comma-separated for multiple).
- (Optional) Add a Persistent **Disk** and set `DB_PATH` to its mount path (e.g., `/opt/render/project/src/backend/data/notes.db`).

When deployed, note your backend URL, e.g. `https://<service>.onrender.com`.

### 2) Deploy frontend on Vercel

- Import the same repo.
- Set **Root Directory** = `frontend`.
- Add Env Var **VITE_API_URL** = your Render backend URL.
- Deploy.

### 3) Test

- Create notes, edit, delete.
- Use the 🔗 **Share** button to generate and copy a public link.
- Open the link in an incognito window to verify public access.

## API surface

- `GET /notes` – list notes
- `POST /notes` – create note `{ title, content }`
- `GET /notes/{id}` – fetch single note
- `PUT /notes/{id}` – update note `{ title?, content? }`
- `DELETE /notes/{id}` – delete
- `POST /notes/{id}/share` – generate/return share link
- `GET /share/{share_id}` – fetch public note (no auth)

## Security & Hardening (quick tips)

- Add simple API key or auth before allowing internet write access.
- Rate-limit by IP on POST/PUT/DELETE if exposing publicly.
- Move to Postgres for multi-instance robustness (`DATABASE_URL` env).

---

Happy shipping! 🚀