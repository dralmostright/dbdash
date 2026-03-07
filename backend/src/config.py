from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL : str
    JWT_SECRET : str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRY : int
    REFRESH_TOKEN_EXPIRY : int
    #FILE_DIRECTORY : str
    #FILE_DIRECTORY_DP : str
    #FILE_DIRECTORY_DP_EXPOSE : str
    
    model_config = SettingsConfigDict (
        env_file=".env",
        extra="ignore"
    )
    
Config = Settings()