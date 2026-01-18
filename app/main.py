from fastapi import FastAPI
from app.hotels.router import router as HotelRouter
from app.users.router import router as UserRouter
from contextlib import asynccontextmanager
from app.core.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        
        
        print('База данных готова к работе!')
    
        yield 
    
        print('Выключение сервера!')

app = FastAPI(lifespan=lifespan)

app.include_router(HotelRouter)
app.include_router(UserRouter)