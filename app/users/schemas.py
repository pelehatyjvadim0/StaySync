from pydantic import BaseModel, ConfigDict, Field, EmailStr

class SUserAuth(BaseModel):
    email: EmailStr
    password: str = Field(min_length=5)
    
    model_config = ConfigDict(from_attributes=True)
    
class SUserRead(BaseModel):
    id: int
    email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)