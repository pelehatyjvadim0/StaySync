from fastapi import APIRouter
from app.dependencies import get_current_user
from app.users.models import User
from fastapi import Depends
from app.bookings.schemas import SBookingResponse, SBookingAdd
from app.tasks.tasks import send_email
from app.core.redis import cache_response
from app.bookings.service import BookingService

router = APIRouter(prefix='/bookings', tags=['Бронирования'])

@router.post('add', response_model=SBookingResponse)
async def booking(booking_info: SBookingAdd, user: User = Depends(get_current_user)):
    
    booking = await BookingService.add_booking(user_id=user.id, booking_data=booking_info)
    
    send_email.delay(booking.model_dump(), user.email)
        
    return booking

@router.get('', response_model=list[SBookingResponse])
@cache_response(expire=60, model=SBookingResponse)
async def get_all_bookings(user: User = Depends(get_current_user)):
    return await BookingService.get_all_user_bookings(user_id=user.id)