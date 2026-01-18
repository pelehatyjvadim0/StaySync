from datetime import date
from sqlalchemy import select, func, and_, or_, insert
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.dao.base import BaseDAO
from app.core.database import new_session

class BookingDAO(BaseDAO):
    model = Bookings
    
    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date
    ):
        async with new_session() as session:
            occupied_bookings = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == room_id,
                        and_(
                            Bookings.date_from < date_to,
                            Bookings.date_to > date_from
                        )
                    )
                )
                .cte("occupied_bookings")
            )
            
            get_rooms_left = (
                select(
                    (Rooms.quantity - func.count(occupied_bookings.c.id)).label("rooms_left")
                )
                .select_from(Rooms)
                .join(occupied_bookings, occupied_bookings.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, Rooms.id)
            )
            
            result = await session.execute(get_rooms_left)
            
            rooms_left: int = result.scalar()
            
            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price_res = await session.execute(get_price)
                price: int = price_res.scalar()
                
                add_booking = (
                    insert(Bookings)
                    .values(
                        room_id = room_id,
                        user_id = user_id,
                        date_from = date_from,
                        date_to=date_to,
                        price=price,
                        total_cost=(date_to - date_from).days * price,
                        total_days=(date_to - date_from).days
                    )
                .returning(
                    Bookings.id, 
                    Bookings.room_id, 
                    Bookings.user_id, 
                    Bookings.date_from, 
                    Bookings.date_to,
                    Bookings.price,
                    Bookings.total_cost,
                    Bookings.total_days
                )
                )
                

                result = await session.execute(add_booking)
                await session.commit()
                # Возвращаем данные как словарь (Mapping), а не живой объект SQLAlchemy
                return result.mappings().first()
            else:
                return None                    