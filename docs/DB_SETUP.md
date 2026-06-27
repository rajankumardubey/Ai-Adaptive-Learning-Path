# PostgreSQL Setup and Connection for the Adaptive Learning Project

This guide shows how to connect the project to your PostgreSQL database and verify the connection.

1) Prepare environment
- Copy `Backend/.env.example` to `Backend/.env`.
- Edit `Backend/.env` and set `DATABASE_URL` using the format:

  postgresql://<user>:<password>@<host>:<port>/<database>

  Example:
  DATABASE_URL=postgresql://alice:pa55w0rd@db.example.com:5432/adaptive_learning

2) Install dependencies (backend)
- From the repo root, run:

```bash
cd Backend
python -m venv .venv      # optional but recommended
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3) Run DB connection test
- Run the included test script:

```bash
python scripts/test_db_connection.py
```

- Expected output:
  - "Connected to Postgres. version: ..."
  - "SELECT 1 -> 1"

4) Start the backend
- Start the FastAPI app with Uvicorn (make sure `.env` is present):

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

5) Common issues
- psycopg2-binary installation fails: ensure you have build tools installed or use a prebuilt wheel; on Windows prefer `psycopg2-binary` from PyPI.
- Connection refused: check host/port and firewall rules, or if using Docker ensure container networking is correct.

6) Optional: Run database migrations
- If your project uses Alembic or other migration tooling, run migrations after setting `DATABASE_URL`.

7) Automating in CI
- Store `DATABASE_URL` as a secure secret in your CI provider and export it before running tests.

If you'd like, I can:
- Add Alembic config and a simple initial migration.
- Add a health-check endpoint in the backend that verifies DB connectivity.
- Wire a sample user table and CRUD example to validate application flows.

Which would you like next?