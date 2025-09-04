# Notes API — FastAPI

Simple CRUD + shareable public links using FastAPI + SQLite.

## Run locally

```bash
cd backend
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API will run at http://127.0.0.1:8000 . Interactive docs: http://127.0.0.1:8000/docs

## Environment

- `ALLOWED_ORIGINS`: Comma-separated list of origins for CORS (e.g., `http://localhost:5173,https://your-frontend.vercel.app`).
- `BASE_URL`: Optional; used to generate absolute share URLs. If unset, backend will infer from request.

## Render deploy (quick)
1. Push this repo to GitHub.
2. On Render: **New +** → **Web Service** → connect repo → select `backend` as root.
3. Runtime: Python 3.11+
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variable `ALLOWED_ORIGINS` with your Vercel domain.
7. (Optional) Add a **Disk** (>=1GB) mounted at `/opt/render/project/src/backend/data` and set env `DB_PATH` to that path for persistence.

## Railway/Fly/Heroku
Use the same start command. For persistence, prefer a managed Postgres. Set `DATABASE_URL` like `postgresql+psycopg://user:pass@host:5432/db`.