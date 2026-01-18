from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends
from app.core.database import new_session

# ---- Фабрика сессий ----
async def get_session_db():
    async with new_session() as session:
        yield session
        
SessionDep = Annotated[AsyncSession, Depends(get_session_db)]