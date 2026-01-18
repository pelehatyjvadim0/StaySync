from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Date
from app.core.models import Model
from typing import TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from app.hotels.rooms.models import Rooms
    from app.users.models import User

class Bookings(Model):
    __tablename__ = 'bookings'
    
    id: Mapped[int] = mapped_column(primary_key=True, init = False)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    date_from: Mapped[date] = mapped_column(Date, nullable=False)
    date_to: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    total_cost: Mapped[int] = mapped_column(nullable=False)
    total_days: Mapped[int] = mapped_column(nullable=False)
    
    user: Mapped['User'] = relationship(back_populates='bookings')
    room: Mapped['Rooms'] = relationship(back_populates='bookings')