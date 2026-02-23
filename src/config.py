from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # These MUST match the names inside your .env file exactly
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    Redis_HOST: str = "localhost"
    Redis_PORT: int = 6379
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_FROM: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool= True
    MAIL_SSL_TLS: bool= False
    USE_CREDENTIALS: bool= True
    VALIDATE_CERTS: bool= True
    DOMAIN: str

    # This creates the "Universal Connection String" for your tutor's asyncpg
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # THE MAGIC LINE: This tells Pydantic to load your .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Initialize the settings
Config = Settings()
