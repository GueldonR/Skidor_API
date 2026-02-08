from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


    @property
    def api_keys(self) -> list[str]:
        """Get API keys from environment variable."""
        return [key.strip() for key in self.API_KEYS.split(",") if key.strip()]

settings = Settings()