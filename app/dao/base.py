from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import new_session

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
    async def add(cls, **data):
        async with new_session() as session:
            query = insert(cls.model).values(**data) #type: ignore
            
            await session.execute(query)
            
            await session.commit()