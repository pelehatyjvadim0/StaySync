from app.bookings.dao import BookingDAO
from app.bookings.models import Bookings
from app.bookings.schemas import SBookingResponse, SBookingAdd
from app.bookings.exceptions import RoomCannotBeBookedException

class BookingService:
    @classmethod
    async def get_all_user_bookings(cls, user_id: int) -> list[SBookingResponse]:
        bookings = await BookingDAO.find_all(user_id = user_id)
        
        return [SBookingResponse.model_validate(booking) for booking in bookings]
    
    @classmethod
    async def add_booking(cls, user_id: int, booking_data: SBookingAdd) -> SBookingResponse:
        new_booking = await BookingDAO.add(user_id=user_id,
                                           **booking_data.model_dump())
        
        if new_booking is None:
            raise RoomCannotBeBookedException()
        
        return SBookingResponse.model_validate(new_booking)
            