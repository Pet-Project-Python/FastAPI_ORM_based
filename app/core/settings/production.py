from app.core.settings.configurations import AppSettings


class ProdAppSettings(AppSettings):
    class Config(AppSettings.Config):
        env_file = ".env"
