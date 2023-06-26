from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    token_secret_key: str
    token_algorithm: str
    token_expire_time: int

    class Config:
        env_file = '.env'


settings = Settings()
