from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings
from typing import Annotated
from fastapi import Depends

engine = create_async_engine(url=settings.DATABASE_URL)

new_session = async_sessionmaker(bind=engine, expire_on_commit=False)