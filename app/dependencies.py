from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends
from app.core.database import new_session

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings
from app.users.dao import UserDAO

# ---- Фабрика сессий ----
async def get_session_db():
    async with new_session() as session:
        yield session
        
SessionDep = Annotated[AsyncSession, Depends(get_session_db)]

# ---- Авторизация ----

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user/login')

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        user_id = payload.get('sub')
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Ошибка получения ID пользователя'
            )
            
        user = await UserDAO.find_one_or_none(id=int(user_id))
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Пользователь не существует'
            )
            
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен невалиден или истёк'
        )