from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus

class Settings(BaseSettings):
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = '1234'
    DB_HOST: str = 'postgres-db'
    DB_PORT: int = 5432
    DB_NAME: str = 'postgres'
    
    @property
    def DATABASE_URL(self):
        NEW_PASS = quote_plus(str(self.DB_PASSWORD))
        return f'postgresql+asyncpg://{self.DB_USER}:{NEW_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    REDIS_HOST: str
    REDIS_PORT: int
    
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )
    
settings = Settings() # type: ignore