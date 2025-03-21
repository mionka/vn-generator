from functools import lru_cache
from os import environ

from app.config.default import DefaultSettings


@lru_cache
def get_settings() -> DefaultSettings:
    """Retrieves settings based on the 'ENV' variable."""
    env = environ.get("ENV", "local")
    if env == "local":
        return DefaultSettings()
    # ...
    # space for other settings
    # ...
    return DefaultSettings()  # fallback to default
