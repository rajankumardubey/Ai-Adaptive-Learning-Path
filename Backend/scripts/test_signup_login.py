"""
Lightweight test script to verify signup/login persistence.

Run from repository root:

    python Backend/scripts/test_signup_login.py

The script will attempt to create a user using the project's CRUD layer.
It prefers Supabase if configured; otherwise it uses local Postgres via SQLAlchemy.
"""

import time
import sys
import os

# Ensure Backend package root is on sys.path so imports like `models` resolve
THIS_DIR = os.path.dirname(__file__)
BACKEND_ROOT = os.path.abspath(os.path.join(THIS_DIR, '..'))
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from models.user import UserCreate
from database import crud
from auth.auth import AuthService


def main():
    ts = int(time.time())
    email = f"testuser{ts}@example.com"
    username = f"testuser{ts}"
    password = "TestPass123!"

    print("Creating user:", email)
    user_create = UserCreate(email=email, username=username, full_name="Test User", password=password)
    created = crud.create_user(user_create)

    if not created:
        print("User creation returned None — possibly conflict or DB error.")
        sys.exit(1)

    # created may be a SQLAlchemy model or a SimpleNamespace from Supabase
    user_id = getattr(created, "id", None)
    created_email = getattr(created, "email", None)
    print("Created user id:", user_id, "email:", created_email)

    print("Fetching user by email:", email)
    fetched = crud.get_user_by_email(email)
    if not fetched:
        print("Failed to fetch user after creation.")
        sys.exit(1)

    print("Fetched user:", getattr(fetched, "email", None), "id:", getattr(fetched, "id", None))

    hashed = getattr(fetched, "hashed_password", None)
    if not hashed:
        print("No hashed_password found on fetched user — check DB schema/mapping.")
        sys.exit(1)

    ok = AuthService.verify_password(password, hashed)
    print("Password verification result:", ok)

    if ok:
        print("Signup/login persistence appears to be working.")
    else:
        print("Password verification failed — investigate hashing/storage.")


if __name__ == "__main__":
    main()
