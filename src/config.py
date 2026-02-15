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

    # This creates the "Universal Connection String" for your tutor's asyncpg
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # THE MAGIC LINE: This tells Pydantic to load your .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Initialize the settings
Config = Settings()
