from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM_NAME: str
    
    class Config:
        # Aquí le decimos qué archivo debe leer
        env_file = ".env"

# Esta línea es la que usaremos en otros archivos
settings = Settings()