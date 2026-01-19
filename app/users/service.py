from app.users.dao import UserDAO
from app.users.auth import get_password_hash, verify_password, create_token_jwt
from app.users.exceptions import AuthError, UserAlredyExistsError, UserRegistrationError
from app.users.schemas import SUserAuthTokenResponse, SUserAuth, SUserRead
from sqlalchemy.exc import IntegrityError

class UserService:
    @classmethod
    async def auth(cls, username: str, user_password: str):
        user = await UserDAO.find_one_or_none(email=username)
        
        if user is None or not verify_password(plain_password=user_password, hashed_password=user.password):
            raise AuthError()
        
        access_jwt_token = create_token_jwt(data = {'sub': str(user.id)})
        
        return SUserAuthTokenResponse(
            access_token=access_jwt_token,
            token_type='bearer'
        )
        
    @classmethod
    async def registration(cls, user_data: SUserAuth) -> SUserRead:
        hashed_password = get_password_hash(user_data.password)
        try:
            new_user = await UserDAO.add(email=user_data.email, hashed_password = hashed_password)
            return SUserRead.model_validate(new_user)
        except IntegrityError as e:
            if 'already exists' in str(e.orig).lower():
                raise UserAlredyExistsError()  
            print(f'USER REGISTRATION ERROR: {e}')
            raise UserRegistrationError()
        
    @classmethod
    async def find_all(cls) -> list[SUserRead]:
        all_users = await UserDAO.find_all()
        return [SUserRead.model_validate(user) for user in all_users]
            
        