from fastapi import FastAPI
from app.hotels.router import router as HotelRouter
from app.users.router import router as UserRouter
from app.bookings.router import router as BookingRouter
from contextlib import asynccontextmanager
from app.core.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        
        
        print('База данных готова к работе!')
    
        yield 
    
        print('Выключение сервера!')

app = FastAPI(lifespan=lifespan,
              title='StaySync',
              version='1.0',
              description='Сервис бронирования номеров')

app.include_router(HotelRouter)
app.include_router(UserRouter)
app.include_router(BookingRouter)