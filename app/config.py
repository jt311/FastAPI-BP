from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_NAME: str
    DB_USERNAME: str
    DB_HOSTNAME: str
    DB_PORT: str
    DB_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()