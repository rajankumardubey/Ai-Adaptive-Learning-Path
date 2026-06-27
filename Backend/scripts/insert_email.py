"""Simple script to insert an email into the `signup_emails` Postgres table.

Usage:
  python insert_email.py someone@example.com

Ensure `DATABASE_URL` is set (or configured in Backend/.env) and Postgres is reachable.
"""
import sys
from database.connection import SessionLocal
from models.signup_email import SignupEmail


def insert_email(email: str):
    db = SessionLocal()
    try:
        existing = db.query(SignupEmail).filter(SignupEmail.email == email).first()
        if existing:
            print(f"Email {email} already exists (id={existing.id})")
            return
        new = SignupEmail(email=email)
        db.add(new)
        db.commit()
        db.refresh(new)
        print(f"Inserted email id={new.id} email={new.email}")
    except Exception as e:
        print("Error inserting email:", e)
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python insert_email.py someone@example.com")
        sys.exit(1)
    insert_email(sys.argv[1])
