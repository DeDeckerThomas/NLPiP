from typing import List
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    APP_NAME: str = Field(env="APP_NAME")

    SCENARIOS_FILE: str = Field(env="SCENARIOS_FILE")

    WARM_UP_RATE: int = Field(env="WARM_UP_RATE", default=10)
    BENCHMARK_RATE: int = Field(env="BENCHMARK_RATE", default=100)
    DEFAULT_BENCHMARK_BATCH_SIZE: int = Field(
        env="DEFAULT_BENCHMARK_BATCH_SIZE", default=32)
    DEFAULT_BENCHMARK_INPUT_DATA: str = Field(
        env="DEFAULT_BENCHMARK_INPUT_DATA", default="Hello everyone!")

    class Config:
        env_prefix = ""
        case_sentive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


settings: Settings = Settings()
