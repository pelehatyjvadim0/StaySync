from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from datetime import date

class SBookingResponse(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    model_config = ConfigDict(from_attributes=True)
    
class SBookingAdd(BaseModel):
    room_id: int
    date_from: date
    date_to: date
    
    @field_validator('date_from')
    @classmethod
    def check_date_from(cls, v: date):
        if v < date.today():
            raise ValueError('Дата заезда не может быть в прошлом!')
        return v
        
    @model_validator(mode='after')
    def check_date_to(self):
        if self.date_to < self.date_from:
            raise ValueError('Дата выезда не может быть раньше даты заезда!')
        return self
    
    model_config = ConfigDict(from_attributes=True)