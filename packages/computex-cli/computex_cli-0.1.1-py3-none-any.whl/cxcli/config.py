import os
from typing import Optional

from pydantic import BaseSettings
from dotenv import load_dotenv


def _credentials_path() -> str:
    home_dir = os.path.expanduser("~")
    cx_dir = os.path.join(home_dir, ".cx")
    if not os.path.exists(cx_dir):
        os.makedirs(cx_dir)
    return os.path.join(cx_dir, "credentials")


class Config(BaseSettings):
    username: Optional[str] = None
    password: Optional[str] = None
    core_api_access_token: Optional[str] = None
    core_api_host: str = "api.computex.co"
    core_api_public_key: Optional[str] = None
    core_api_refresh_token: Optional[str] = None
    core_api_scheme: str = "https"
    credentials_path: str = _credentials_path()

    class Config:
        env_prefix = "COMPUTEX_"


def update_config():
    """Use to update config with external env files."""
    config = Config()
    load_dotenv(config.credentials_path)


update_config()
