from database.connection import engine, Base
from models.user_table import UserTable
from models.signup_email import SignupEmail


def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("Database tables created (or already exist).")
