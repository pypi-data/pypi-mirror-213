from mlflow.utils import databricks_utils

from databricks.feature_store.entities._feature_store_object import _FeatureStoreObject

FEATURE_SERVING_ENDPOINT_PREFIX = "serving-endpoints"


class FeatureServingEndpoint(_FeatureStoreObject):
    def __init__(
        self,
        name: str,
        creator: str,
        creation_time_millis: int,
        state: str,
    ):
        self._name = name
        self._creator = creator
        self._creation_time_millis = creation_time_millis
        self._state = state

    @property
    def name(self) -> str:
        return self._name

    @property
    def creator(self) -> str:
        return self._creator

    @property
    def creation_time_millis(self) -> int:
        return self._creation_time_millis

    @property
    def state(self) -> str:
        """The state of the endpoint. Value could be READY, FAILED or IN_PROGRESS."""
        return self._state

    @property
    def url(self) -> str:
        return "/".join(
            [self._get_workspace_host(), FEATURE_SERVING_ENDPOINT_PREFIX, self.name]
        )

    def _get_workspace_host(self):
        local_host, _ = databricks_utils.get_workspace_info_from_dbutils()
        return local_host
