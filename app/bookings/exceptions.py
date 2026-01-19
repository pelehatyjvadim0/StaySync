from app.core.exceptions import StaySyncException
from fastapi import status

# Номер нельзя забронировать
class RoomCannotBeBookedException(StaySyncException):
    status_code=status.HTTP_409_CONFLICT