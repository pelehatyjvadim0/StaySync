from sqlalchemy import select
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