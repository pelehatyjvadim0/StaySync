from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import new_session
from app.users.models import User

class BaseDAO:
    model = None
    
    @classmethod
    async def find_all(cls, **filter_by):
        async with new_session() as session:
            query = select(cls.model).filter_by(**filter_by) #type: ignore
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with new_session() as session:
            query = select(cls.model).filter_by(**filter_by) #type: ignore
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def add(cls, **data) -> User:
        async with new_session() as session:
        
            query = insert(cls.model).values(**data).returning(cls.model) #type: ignore  Pylance не может пробросить тип с БД, ругается из-за неизвестности типа
            
            result = await session.execute(query)
            
            await session.commit()
            
            return result.scalars().first() #type: ignore Мы уверены в логике, затыкаем Pylance чтобы не ругался из-за неизвестности типа и возможности получить None из-за first()