"""Simple DB connection test for the Adaptive Learning backend.

Run this after you set `DATABASE_URL` in `Backend/.env` (or environment).
It will attempt to connect using SQLAlchemy engine from
`Backend/database/connection.py` and run a quick SELECT.

Usage:
    cd Backend
    python -m venv .venv          # optional
    .\.venv\Scripts\activate    # Windows PowerShell
    pip install -r requirements.txt
    python scripts/test_db_connection.py

"""
from database.connection import engine

def test_connection():
    try:
        with engine.connect() as conn:
            # quick test
            resp = conn.execute("SELECT version();")
            ver = resp.fetchone()
            print('Connected to Postgres. version:', ver[0] if ver else 'unknown')
            resp2 = conn.execute("SELECT 1;")
            print('SELECT 1 ->', resp2.scalar())
            return True
    except Exception as e:
        print('Database connection failed:', e)
        return False

if __name__ == '__main__':
    ok = test_connection()
    if not ok:
        raise SystemExit(1)
