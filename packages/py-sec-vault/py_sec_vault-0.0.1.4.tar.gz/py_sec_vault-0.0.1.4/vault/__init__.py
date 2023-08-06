import os

from .main import _variables


def from_env_or_vault(env_name: str, default: str | None = None) -> str | None:
    return os.environ.get(env_name, _variables.get(env_name, default))


def from_vault(key: str) -> str | None:
    return _variables[key]
