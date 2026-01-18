from sqlalchemy.orm import Mapped, mapped_column
from app.core.models import Model
from sqlalchemy import JSON

class Hotel(Model):
    __tablename__ = 'hotels'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON)
    rooms_quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]