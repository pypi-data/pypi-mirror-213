import enum
from pathlib import Path
from tempfile import gettempdir

from yarl import URL
from pydantic import BaseSettings as PydanticBaseSettings
from pydantic.env_settings import SettingsSourceCallable
from pydantic.utils import deep_update
from yaml import safe_load

CONF_DIR = Path(Path(__file__).parent, "..", "config").resolve()
TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class BaseSettings(PydanticBaseSettings):
    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    # Variables for the database
    db_file: Path = TEMP_DIR / "db.sqlite3"
    db_echo: bool = False

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="sqlite+aiosqlite",
            path=f"///{self.db_file}",
        )

    class Config:
        env_prefix = 'POLITI_'
        config_files = [
            Path(CONF_DIR, "global.yaml"),
            Path(CONF_DIR, "dev.yaml"),
        ]

        @classmethod
        def customise_sources(
                cls,
                init_settings: SettingsSourceCallable,
                env_settings: SettingsSourceCallable,
                file_secret_settings: SettingsSourceCallable
        ) -> tuple[SettingsSourceCallable, ...]:
            return init_settings, env_settings, config_file_settings


def config_file_settings(settings: PydanticBaseSettings) -> dict[str, any]:
    config: dict[str, any] = {}
    if not isinstance(settings, BaseSettings):
        return config
    for path in settings.Config.config_files:
        if not path.is_file():
            print(f"No file found at `{path.resolve()}`")
            continue
        print(f"Reading config file `{path.resolve()}`")
        if path.suffix in {".yaml", ".yml"}:
            config = deep_update(config, load_yaml(path))
        else:
            print(f"Unknown config file extension `{path.suffix}`")
    return config


def load_yaml(path: Path) -> dict[str, any]:
    with Path(path).open("r") as f:
        config = safe_load(f)
    if not isinstance(config, dict):
        raise TypeError(
            f"Config file has no top-level mapping: {path}"
        )
    return config


settings = BaseSettings()
