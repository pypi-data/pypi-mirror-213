import os

from ssapi.defaults import DEFAULT_SSAPI_DATABASE_PATH
from ssapi.db import ShopDatabase
from ssapi.types import provides_singleton


def get_database_path() -> str:
    """Get the current database path based on the environment variable"""
    return os.environ.get("SSAPI_DATABASE_PATH", DEFAULT_SSAPI_DATABASE_PATH)


@provides_singleton
def get_env_database() -> ShopDatabase:
    """Get the singleton database defined by the running environment"""
    try:
        db = get_env_database._singleton
    except AttributeError:
        db = get_env_database._singleton = ShopDatabase(get_database_path())
    return db
