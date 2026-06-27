from typing import Optional, List
from types import SimpleNamespace

from sqlalchemy.exc import IntegrityError

from models.user import UserCreate
from auth.auth import AuthService
from database.connection import SessionLocal
from models.user_table import UserTable
from supabase_client import get_supabase


def create_user(user: UserCreate) -> Optional[UserTable]:
    """Create a new user in Postgres and return the ORM object.
    Returns None on conflict or failure.
    """
    supabase = get_supabase()
    # Prefer Supabase if configured
    if supabase:
        hashed = AuthService.hash_password(user.password)
        record = {
            'email': user.email,
            'username': user.username,
            'full_name': user.full_name,
            'hashed_password': hashed,
            'is_active': True,
        }
        try:
            res = supabase.table('users').insert(record).select('*').execute()
            data = res.data if hasattr(res, 'data') else (res.get('data') if isinstance(res, dict) else None)
            if not data:
                return None
            # return a simple object with attribute access to match SQLAlchemy model usage
            return SimpleNamespace(**data[0])
        except Exception:
            return None

    db = SessionLocal()
    try:
        hashed = AuthService.hash_password(user.password)
        db_user = UserTable(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            hashed_password=hashed,
            is_active=True,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        return None
    finally:
        db.close()


def get_user_by_email(email: str) -> Optional[UserTable]:
    supabase = get_supabase()
    if supabase:
        try:
            q = supabase.table('users').select('*').eq('email', email).limit(1).execute()
            data = q.data if hasattr(q, 'data') else (q.get('data') if isinstance(q, dict) else None)
            if not data:
                return None
            return SimpleNamespace(**data[0])
        except Exception:
            # fall through to SQLAlchemy
            pass

    db = SessionLocal()
    try:
        return db.query(UserTable).filter(UserTable.email == email).first()
    finally:
        db.close()


def get_user_by_id(user_id: int) -> Optional[UserTable]:
    db = SessionLocal()
    try:
        return db.query(UserTable).get(user_id)
    finally:
        db.close()


def get_all_courses() -> List[dict]:
    return []


def get_course_by_id(course_id: int) -> Optional[dict]:
    return None


def get_user_progress(user_id: int) -> List[dict]:
    return []


def get_user_assessments(user_id: int) -> List[dict]:
    return []


def update_user_difficulty(user_id: int, difficulty: float):
    pass


def create_progress_record(user_id: int, lesson_id: int, score: float, completion: float):
    pass
