from passlib.context import CryptContext

from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
from app.core.config import settings


# ---- Хеширование паролей ----

pwd_context = CryptContext(schemes='bcrypt', deprecated='auto')

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# ---- JWT Токен ----

def create_token_jwt(data: dict) -> str:
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({'exp': expire})
    
    return jwt.encode(to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)    