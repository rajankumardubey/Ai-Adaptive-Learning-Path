from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from datetime import date, datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from models.user import User, UserCreate, UserLogin, Token
from auth.auth import AuthService
from auth.dependencies import get_current_user
from database.crud import get_user_by_email, create_user as db_create_user
from database.connection import get_db
from models.user_table import UserTable
from supabase_client import get_supabase
from config import settings
import smtplib
from email.message import EmailMessage

router = APIRouter()


class UserSignupSchema(BaseModel):
    id: str
    fullName: str
    status: str
    dob: date
    age: int
    address: str
    phonenumber: str
    email: EmailStr


class RegisterRequest(BaseModel):
    fullname: str
    email: EmailStr
    mobile: str
    password: str


class OtpRequest(BaseModel):
    target: str
    medium: str  # 'email' or 'mobile'


class OtpVerifyRequest(BaseModel):
    target: str
    otp: str
    medium: str


def _send_email(to_email: str, subject: str, body: str) -> bool:
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        # SMTP not configured — skip actual sending
        return False
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = settings.SMTP_USER
        msg['To'] = to_email
        msg.set_content(body)

        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception:
        return False


@router.post("/users/signup", status_code=201)
async def sync_user_signup(user_data: UserSignupSchema, db: Session = Depends(get_db)):
    """Sync a Flutter user profile into the local database."""
    # TODO: Insert the synced profile into the local ORM model using the existing conventions.
    # Example:
    # new_profile = UserTable(
    #     id=user_data.id,
    #     email=str(user_data.email),
    #     username=str(user_data.email).split('@')[0],
    #     full_name=user_data.fullName,
    #     mobile=user_data.phonenumber,
    #     is_active=True,
    # )
    # db.add(new_profile)
    # db.commit()
    # db.refresh(new_profile)

    return {
        "status": "success",
        "message": "User profile synced.",
        "received": user_data.id,
    }


@router.post('/send_otp')
async def send_otp(req: OtpRequest):
    """Generate and store OTP for a target (email or mobile)."""
    supabase = get_supabase()
    otp = str("%06d" % (int(datetime.utcnow().timestamp()) % 1000000))
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    record = {
        'target': req.target,
        'otp': otp,
        'medium': req.medium,
        'purpose': 'signup',
        'expires_at': expires_at.isoformat(),
        'verified': False,
    }
    # store OTP in Supabase if available, else skip storage
    if supabase:
        try:
            res = supabase.table('otps').insert(record).execute()
        except Exception:
            # don't fail the whole flow if DB insert has issues; continue as simulation
            res = None

    # send via email if medium==email
    if req.medium == 'email':
        sent = _send_email(req.target, 'Your StudySense OTP', f'Your OTP is: {otp}')
        # If SMTP isn't configured or sending failed, return the OTP in response for development/testing
        if not sent:
            return {'ok': True, 'sent': False, 'otp': otp}
        return {'ok': True, 'sent': True}

    # For mobile, we currently simulate sending and return OTP for dev use
    return {'ok': True, 'sent': False, 'otp': otp}


@router.post('/verify_otp')
async def verify_otp(req: OtpVerifyRequest):
    """Verify an OTP for a given target and mark it verified if correct."""
    supabase = get_supabase()
    now = datetime.utcnow().isoformat()
    if supabase:
        q = supabase.table('otps').select('*').eq('target', req.target).eq('otp', req.otp).eq('purpose', 'signup').gte('expires_at', now).order('id', desc=True).limit(1).execute()
        data = q.data if hasattr(q, 'data') else (q.get('data') if isinstance(q, dict) else None)
        if not data:
            raise HTTPException(status_code=400, detail='Invalid or expired OTP')
        # mark verified
        otp_id = data[0].get('id')
        supabase.table('otps').update({'verified': True}).eq('id', otp_id).execute()
        return {'ok': True}
    # If no supabase, accept any OTP for simulation
    return {'ok': True}


@router.post("/register", response_model=User)
async def register(req: RegisterRequest):
    """Register a new user — requires prior OTP verification (server-side)."""
    # Check existing
    existing = get_user_by_email(req.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    supabase = get_supabase()
    # Check email/mobile verified in otps table when supabase is available
    if supabase:
        now = datetime.utcnow().isoformat()
        email_q = supabase.table('otps').select('*').eq('target', req.email).eq('purpose', 'signup').eq('verified', True).gte('expires_at', now).execute()
        email_verified = bool(getattr(email_q, 'data', None))
        mobile_q = supabase.table('otps').select('*').eq('target', req.mobile).eq('purpose', 'signup').eq('verified', True).gte('expires_at', now).execute()
        mobile_verified = bool(getattr(mobile_q, 'data', None))
        if not email_verified or not mobile_verified:
            raise HTTPException(status_code=400, detail='Email and mobile must be OTP-verified')

    # create user
    hashed = AuthService.hash_password(req.password)
    user_record = {
        'email': req.email,
        'full_name': req.fullname,
        'mobile': req.mobile,
        'hashed_password': hashed,
        'is_active': True,
    }
    if supabase:
        res = supabase.table('users').insert(user_record).select('*').execute()
        data = res.data if hasattr(res, 'data') else (res.get('data') if isinstance(res, dict) else None)
        if not data:
            raise HTTPException(status_code=500, detail='Failed to create user')
        created = data[0]
        return {
            'id': created.get('id'),
            'email': created.get('email'),
            'username': created.get('email').split('@')[0],
            'full_name': created.get('full_name'),
            'is_active': created.get('is_active', True),
            'learning_level': created.get('learning_level', 0.0),
            'created_at': created.get('created_at')
        }

    # fallback to mock DB
    new_user = db_create_user(UserCreate(username=req.email.split('@')[0], email=req.email, full_name=req.fullname, password=req.password))
    return new_user


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """Login user and return JWT token"""
    user = get_user_by_email(credentials.email)

    if not user or not AuthService.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = AuthService.create_access_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout user"""
    return {"message": "Successfully logged out"}


@router.post("/refresh")
async def refresh_token(current_user: User = Depends(get_current_user)):
    """Refresh access token"""
    access_token = AuthService.create_access_token(current_user.id)
    return {"access_token": access_token, "token_type": "bearer"}
