"""应用配置模块。"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用运行时配置。"""

    app_name: str = Field(default="Docx-Agent-Server")
    app_version: str = Field(default="0.1.0")
    debug: bool = Field(default=False)
    temp_dir: Path = Field(default=Path("tmp"))

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="DOCX_AGENT_",
        case_sensitive=False,
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """获取全局单例配置。"""
    settings = Settings()
    settings.temp_dir.mkdir(parents=True, exist_ok=True)
    return settings
