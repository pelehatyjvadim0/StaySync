from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, JSON
from app.core.models import Model
from typing import TYPE_CHECKING

# TYPE_CHECKING для защиты от цикличного импорта
if TYPE_CHECKING:
    from app.hotels.models import Hotel
    from app.bookings.models import Bookings

class Rooms(Model):
    __tablename__ = 'rooms'
    
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column(nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON)
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int] = mapped_column(nullable=False)
    
    hotel: Mapped['Hotel'] = relationship(back_populates='rooms')
    bookings: Mapped['Bookings'] = relationship(back_populates='room')