from fastapi import APIRouter
from fastapi import status
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel

router = APIRouter(prefix='/hotels')

@router.get('/find_all', status_code=status.HTTP_200_OK, response_model=list[SHotel])
async def find_all():
    return await HotelDAO.find_all()