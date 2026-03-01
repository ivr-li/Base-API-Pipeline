from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Initialize the configuration settings"""

    API_KEY: str = ""
    DB: str = ""
    REQUEST_INTERVAL: int = 60

    model_config = {"env_file": ".env"}


config = Config()
