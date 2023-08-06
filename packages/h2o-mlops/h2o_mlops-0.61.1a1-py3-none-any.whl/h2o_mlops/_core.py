from __future__ import annotations

import h2o_authn
import h2o_mlops_autogen

from h2o_mlops import _projects
from h2o_mlops import _runtimes


class MLOpsClient:
    """Connect to and interact with H2O MLOps.

    Args:
        gateway_url: full URL of the MLOps gRPC Gateway to connect to
        token_provider: authentication token to authorize access on H2O AI Cloud

    Examples::

        ### Connect with token

        # 1) set up a token provider with a refresh token from AI Cloud
        token_provider = h2o_authn.TokenProvider(
            refresh_token="eyJhbGciOiJIUzI1N...",
            client_id="python_client",
            token_endpoint_url="https://keycloak-server/auth/realms/..."
        )

        # 2) use the token provider to get authorization to connect to the
        # MLOps API
        mlops = h2o_mlops.MLOpsClient(
            gateway_url="https://mlops-api.my.domain",
            token_provider=token_provider
        )
    """

    def __init__(self, gateway_url: str, token_provider: h2o_authn.TokenProvider):
        self._mlops_backend = h2o_mlops_autogen.Client(
            gateway_url=gateway_url,
            token_provider=token_provider,
        )

    @property
    def projects(self) -> _projects.MLOpsProjects:
        """Interact with Projects in H2O MLOps"""
        return _projects.MLOpsProjects(self)

    @property
    def runtimes(self) -> _runtimes.MLOpsRuntimes:
        """Interact with Scoring Runtimes in H2O MLOps"""
        return _runtimes.MLOpsRuntimes(self)
