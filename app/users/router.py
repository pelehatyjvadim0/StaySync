from fastapi import APIRouter, status, HTTPException
from app.users.schemas import SUserAuth, SUserRead
from app.users.dao import UserDAO
from app.users.auth import get_password_hash

router = APIRouter(prefix='/user')

@router.get('', response_model=list[SUserRead], status_code=status.HTTP_200_OK)
async def get_all():
    return await UserDAO.find_all()

@router.post('/registration', status_code=status.HTTP_201_CREATED)
async def add(user_data: SUserAuth):
    
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует!'
        )
    
    hashed_password = get_password_hash(user_data.password)
    
    print(f"DEBUG: Length of hash is {len(hashed_password)}")
    
    await UserDAO.add(email=user_data.email, hashed_password = hashed_password)
    
    return {'message': 'Регистрация прошла успешно!'}