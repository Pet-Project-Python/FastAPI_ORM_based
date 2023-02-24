import logging

from app.core.settings.configurations import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True

    title: str = "Dev Service Layout"

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env"
