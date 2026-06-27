from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(user_id: int, expires_delta: timedelta = None) -> str:
        if expires_delta is None:
            expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        expire = datetime.utcnow() + expires_delta
        to_encode = {"sub": str(user_id), "exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> int:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: int = int(payload.get("sub"))
            return user_id
        except (JWTError, ValueError):
            return None
