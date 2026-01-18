from fastapi import APIRouter, status, HTTPException, Depends
from app.users.schemas import SUserAuth, SUserRead
from app.users.dao import UserDAO
from app.users.auth import get_password_hash, verify_password, create_token_jwt
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix='/user', tags=['Пользователи'])

@router.post('/login', status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserDAO.find_one_or_none(email=form_data.username)
    
    if user is None or not verify_password(plain_password=form_data.password, hashed_password=user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный логин или пароль!'
        )
    
    access_jwt_token = create_token_jwt(data = {'sub': str(user.id)})
    
    return {
        'access_token': access_jwt_token,
        'token_type': 'bearer'
    }
    
@router.post('/registration', status_code=status.HTTP_201_CREATED)
async def add(user_data: SUserAuth):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует!'
        )
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password = hashed_password)
    return {'message': 'Регистрация прошла успешно!'}

@router.get('/me', response_model=SUserRead)
async def get_me(user: User = Depends(get_current_user)):
    return user

@router.get('', response_model=list[SUserRead], status_code=status.HTTP_200_OK)
async def get_all():
    return await UserDAO.find_all()







