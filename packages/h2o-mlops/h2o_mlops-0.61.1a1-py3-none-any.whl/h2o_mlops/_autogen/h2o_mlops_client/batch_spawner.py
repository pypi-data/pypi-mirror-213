from typing import Callable

from _h2o_mlops_client.batch_spawner import api
from _h2o_mlops_client.batch_spawner import api_client
from _h2o_mlops_client.batch_spawner.exceptions import *  # noqa: F403, F401


class ApiClient(api_client.ApiClient):
    """Overrides update_params_for_auth method of the generated ApiClient classes"""

    def __init__(
        self, configuration: api_client.Configuration, token_provider: Callable[[], str]
    ):
        self._token_provider = token_provider
        super().__init__(configuration=configuration)

    def update_params_for_auth(self, headers, querys, auth_settings, request_auth=None):
        token = self._token_provider()
        headers["Authorization"] = f"Bearer {token}"


class Client:
    """The composite client for accessing Batch Spawner services."""

    def __init__(self, host: str, token_provider: Callable[[], str]):
        client = ApiClient(
            configuration=api_client.Configuration(host=host),
            token_provider=token_provider,
        )
        self._spawner = api.SpawnerServiceApi(api_client=client)

    @property
    def spawner(self) -> api.SpawnerServiceApi:
        return self._spawner
