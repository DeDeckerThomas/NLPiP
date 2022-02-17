from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    APP_NAME: str = Field(env="APP_NAME")

    API_TASK: str = Field(env="API_TASK")
    API_TASK_MODEL: str = Field(env="API_TASK_MODEL")

    TWEET_LIMIT: int = Field(env="TWEET_LIMIT", default=1000)

    class Config:
        env_prefix: str = ""
        case_sentive: bool = False
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


settings: Settings = Settings()
