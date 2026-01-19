from fastapi import APIRouter, status, HTTPException, Depends
from app.users.schemas import SUserAuth, SUserRead, SUserAuthTokenResponse
from app.users.dao import UserDAO
from app.users.service import UserService
from app.users.auth import get_password_hash, verify_password, create_token_jwt
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix='/user', tags=['Пользователи'])

@router.post('/login', status_code=status.HTTP_200_OK, response_model=SUserAuthTokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    tokens = await UserService.auth(username=form_data.username, user_password=form_data.password)
    
    return tokens
    
@router.post('/registration', status_code=status.HTTP_201_CREATED, response_model=SUserRead)
async def add(user_data: SUserAuth):
    return await UserService.registration(user_data=user_data)

@router.get('/me', response_model=SUserRead)
async def get_me(user: User = Depends(get_current_user)):
    return user

@router.get('', response_model=list[SUserRead], status_code=status.HTTP_200_OK)
async def get_all():
    return await UserService.find_all()







