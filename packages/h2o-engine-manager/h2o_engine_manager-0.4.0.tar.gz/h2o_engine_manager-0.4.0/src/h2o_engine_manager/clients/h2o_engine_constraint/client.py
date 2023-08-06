from h2o_engine_manager.clients.connection_config import get_connection
from h2o_engine_manager.clients.h2o_engine_constraint.token_api_client import (
    TokenApiClient,
)
from h2o_engine_manager.gen.h2o_engine_constraint_set_service.api.h2_o_engine_constraint_set_service_api import (
    H2OEngineConstraintSetServiceApi,
)
from h2o_engine_manager.gen.h2o_engine_constraint_set_service.configuration import (
    Configuration,
)
from h2o_engine_manager.gen.h2o_engine_constraint_set_service.model.v1_h2_o_engine_constraint_set import (
    V1H2OEngineConstraintSet,
)


class H2OEngineConstraintSetClient:
    """H2OEngineConstraintSetClient manages H2OEngineConstraintSets."""

    def __init__(
        self,
        url: str,
        platform_token: str,
        platform_oidc_url: str,
        platform_oidc_client_id: str,
    ):
        """Initializes H2OEngineConstraintSetClient.

        Args:
            url (str): URL of AI Engine Manager Gateway.
            platform_token (str): H2O.ai platform token.
            platform_oidc_url (str): Base URL of the platform_token OIDC issuer.
            platform_oidc_client_id (str): OIDC Client ID associated with the platform_token.
        """

        cfg = get_connection(
            aiem_url=url,
            refresh_token=platform_token,
            issuer_url=platform_oidc_url,
            client_id=platform_oidc_client_id,
        )

        engine_cfg = Configuration(host=url)
        with TokenApiClient(
            engine_cfg, cfg.token_provider
        ) as engine_service_api_client:
            self.service_api = H2OEngineConstraintSetServiceApi(
                engine_service_api_client
            )

    def get_constraint_set(self, workspace_id: str) -> V1H2OEngineConstraintSet:
        return self.service_api.h2_o_engine_constraint_set_service_get_h2_o_engine_constraint_set(
            name=f"workspaces/{workspace_id}/h2oEngineConstraintSet"
        ).h2o_engine_constraint_set
