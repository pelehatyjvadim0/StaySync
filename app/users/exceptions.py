from app.core.exceptions import StaySyncException
from fastapi import status

class AuthError(StaySyncException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = 'Неверный логин или пароль!'
    
class UserRegistrationError(StaySyncException):
    status_code = status.HTTP_409_CONFLICT
    message = 'Ошибка регистрации нового пользователя!'
    
class UserAlredyExistsError(StaySyncException):
    status_code = status.HTTP_409_CONFLICT
    message = 'Имя пользователя занято!'