from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    GEMINI_API_KEY: str
    GEMINI_MODEL: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

Config = Settings()

broker_url = Config.CELERY_BROKER_URL
result_backend = Config.CELERY_RESULT_BACKEND
broker_connection_retry_on_startup = True