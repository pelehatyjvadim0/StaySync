from fastapi import APIRouter
from datetime import date, datetime, timezone
from app.dependencies import get_current_user
from app.users.models import User
from fastapi import Depends, HTTPException, status
from app.bookings.dao import BookingDAO

router = APIRouter(prefix='/bookings', tags=['Бронирования'])

@router.post('')
async def booking(room_id: int, date_from: date, date_to: date, user: User = Depends(get_current_user)):
    if date_from >= date_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Дата заезда должна быть раньше даты выезда!'
        )
    
    room = await BookingDAO.add(
        user_id=user.id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to
    )
    
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Упс, свободых номеров нет!'
        )
        
    return room