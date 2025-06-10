import os
from logging import config as logging_config
from core.logger import LOGGING
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, computed_field
from pathlib import Path
from datetime import date


# Общая конфигурация
class GeneralConfig(BaseSettings):
    REDIS_HOST: str = Field(..., env="REDIS_HOST")
    REDIS_PORT: int = Field(..., env="REDIS_PORT")

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        10, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    AUTHJWT_SECRET_KEY: str = Field(..., env="AUTHJWT_SECRET_KEY")

    PROJECT_NAME: str = Field(..., env="PROJECT_NAME")

    LIMIT_REQUESTS_ONE_IP: int = Field(100, env="LIMIT_REQUESTS_ONE_IP")
    WINDOW_SIZE_LIMIT_REQUESTS: int = Field(60, env="WINDOW_SIZE_LIMIT_REQUESTS")

    TOPIC_KAFKA: str = Field(..., env="TOPIC_KAFKA")
    KAFKA_BOOTSTRAP_SERVERS: list[str] = Field(..., env="KAFKA_BOOTSTRAP_SERVERS")

    CLICKHOUSE_HOST: str = Field(..., env="CLICKHOUSE_HOST")
    CLICKHOUSE_DATABASE: str = Field(..., env="CLICKHOUSE_DATABASE")
    CLICKHOUSE_USER: str = Field(..., env="CLICKHOUSE_USER")
    CLICKHOUSE_PASSWORD: str = Field(..., env="CLICKHOUSE_PASSWORD")

    BATCH_SIZE: int = Field(150, env="BATCH_SIZE")

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent / ".env"),
        env_file_encoding="utf-8",
        extra="allow",
    )

    @computed_field
    def BASE_DIR(self) -> str:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self, **values):
        # Применяем настройки логирования
        logging_config.dictConfig(LOGGING)
        super().__init__(values)


class SwaggerParam:
    swagger_template = {
        "openapi": "3.0.2",
        "swagger": None,
        "info": {"title": "UGC API", "version": "1.0.0"},
        "host": "localhost:9001",
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
        },
        "security": [{"bearerAuth": []}],
    }

    swagger_config = {
        "headers": [],
        "swagger_ui": True,
        "specs_route": "/apidocs",
        "static_url_path": "/flasgger_static",
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/apispec_1.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
    }
