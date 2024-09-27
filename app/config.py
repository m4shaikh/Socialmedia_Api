from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_host: str = "localhost"
    database_port: str = "5432"
    database_user: str = "postgres"
    database_pass: str = "301120"
    database_name: str = "Newone"
    secret_key: str = "sdkhkujhesdfkujihiokhjs4566d5csd"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 300

settings = Settings()

# Print settings to verify they are being set correctly
print(f"Host: {settings.database_host}")
print(f"User: {settings.database_user}")
