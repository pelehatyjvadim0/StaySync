from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.models import Model
from typing import TYPE_CHECKING

# Защита от цикличных импортов
if TYPE_CHECKING:
    from app.bookings.models import Bookings

class User(Model):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init = False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    
    bookings: Mapped[list['Bookings']] = relationship(back_populates='user')