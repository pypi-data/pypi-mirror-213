import logging
from functools import lru_cache
from typing import Mapping

from hvac import Client
from hvac.exceptions import InvalidPath

from vault.exceptions import VaultClientImproperlyConfiguredError
from vault import config

logger = logging.getLogger(__name__)


def get_client(
    auth_method: str,
    host: str,
    token: str | None = None,
    role_id: str | None = None,
    secret_id: str | None = None,
) -> Client | None:
    if auth_method == "token":
        if not token:
            raise NotImplementedError(
                "Missing variable VAULT_TOKEN. "
                "Cannot authenticate with vault using token."
            )
        return Client(url=host, token=token)

    if auth_method == "approle":
        if not role_id or not secret_id:
            raise NotImplementedError(
                "Missing variables VAULT_ROLE_ID and/or VAULT_SECRET_ID. "
                "Cannot authenticate with vault using approle."
            )

        client = Client(url=host)
        client.auth.approle.login(
            role_id=role_id,
            secret_id=secret_id,
        )
        return client


def _vault_config_is_valid(
    auth_method: str,
    token: str | None = None,
    role_id: str | None = None,
    secret_id: str | None = None,
) -> bool:
    if auth_method == "token":
        if not token:
            raise VaultClientImproperlyConfiguredError(
                "Missing variable VAULT_TOKEN. "
                "Cannot authenticate with vault using token."
            )
        return True

    if auth_method == "approle":
        if not role_id or not secret_id:
            raise VaultClientImproperlyConfiguredError(
                "Missing variables VAULT_ROLE_ID and/or VAULT_SECRET_ID. "
                "Cannot authenticate with vault using approle."
            )
        return True
    return False


@lru_cache
def _fetch_variables() -> Mapping[str, str]:
    if not config.VAULT_ENABLED:
        logger.info("Vault credentials not fetched. VAULT_ENABLED is False.")
        return dict()

    try:
        _vault_config_is_valid(
            auth_method=config.VAULT_AUTH_METHOD,
            token=config.VAULT_TOKEN,
            role_id=config.VAULT_ROLE_ID,
            secret_id=config.VAULT_SECRET_ID,
        )
    except VaultClientImproperlyConfiguredError as e:
        logger.exception(e, exc_info=True)
        return dict()

    logger.debug("About to fetch credentials from vault.")
    if not (
        client := get_client(
            auth_method=config.VAULT_AUTH_METHOD,
            host=config.VAULT_HOST,
            token=config.VAULT_TOKEN,
            role_id=config.VAULT_ROLE_ID,
            secret_id=config.VAULT_SECRET_ID,
        )
    ):
        raise ConnectionError("Could not connect to vault.")

    logger.debug(f"Connected to vault with auth method {config.VAULT_AUTH_METHOD}.")
    try:
        response = client.secrets.kv.v2.read_secret(
            mount_point=config.VAULT_MOUNT_POINT,
            path=config.VAULT_PATH,
        )
    except InvalidPath:
        raise Exception(
            f"Your path ({config.VAULT_PATH}) has not been created yet "
            f"or there are no credentials in it."
        )

    secrets = response["data"]["data"]
    logger.info(f"Fetched {len(secrets.keys())} secret(s) from vault.")
    return secrets


_variables = _fetch_variables()
