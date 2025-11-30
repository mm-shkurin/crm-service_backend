from typing import Optional, ClassVar
from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings
from enum import Enum

class BaseConfig(BaseSettings):
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
        "populate_by_name":True 
    }

class LogLevel(str, Enum):
    DEBUG = "debug"  
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class CompressionType(str, Enum):
    GZIP = "gz"
    BZIP2 = "bz2"
    ZIP = "zip"

class AppSettings(BaseSettings):
    app_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        alias="APP_NAME" 
    )
    app_port: int = Field(
        ...,
        ge=1,
        le=65535,
        alias="APP_PORT" 
    )
    
    app_host: str = Field(default="0.0.0.0")
    app_reload: bool = Field(default=False)
    app_log_level: LogLevel = Field(default=LogLevel.INFO)
    log_format: str = Field(default="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
    log_file: str = Field(default="logs/app.log")
    log_rotation: str = Field(default="1 day")
    log_compression: CompressionType = Field(default=CompressionType.GZIP)
    
    model_config = BaseConfig.model_config
    
class DatabaseSettings(BaseSettings):
    postgres_network_name: str = Field(..., alias="POSTGRES_NETWORK_NAME")
    postgres_user: str = Field(..., min_length=1, alias="POSTGRES_USER")
    postgres_password: str = Field(..., min_length=1, alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(..., min_length=1, alias="POSTGRES_DB")
    postgres_host: str = Field(default="localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(..., ge=1, le=65535, alias="POSTGRES_PORT")
    debug_sql: bool = Field(default=False)

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    model_config = BaseConfig.model_config
    
