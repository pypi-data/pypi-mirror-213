"""Define Model Registry Manager."""
from functools import partial
from operator import attrgetter

from ML_management import mlmanagement
from ML_management.registry.exceptions import MetricNotLogged, ModelNotRegistered, NoMetricProvided, UnsupportedCriteria, VersionNotFound
from mlflow.entities.model_registry.model_version import ModelVersion
from mlflow.entities.model_registry.registered_model import RegisteredModel
from mlflow.exceptions import RestException
from mlflow.store.entities import PagedList

# noinspection PyUnresolvedReferences
# TODO maybe make it singleton?


class RegistryManager:
    """Registry Manager to choose necessary version of the model."""

    def __init__(self):
        self.client = mlmanagement.MlflowClient()

    def check_model_registered(self, name: str) -> RegisteredModel:
        """Check if model is registered in mlflow or not."""
        try:
            registered_model = self.client.get_registered_model(name)
        except RestException as err:
            if err.error_code == "RESOURCE_DOES_NOT_EXIST":
                raise ModelNotRegistered(name)
            else:
                raise err
        return registered_model

    def get_latest_version(self, name: str) -> ModelVersion:
        """Get the latest version of a model "name"."""
        latest_version = None
        registered_model = self.check_model_registered(name)

        # if there is only one default stage, there should be only one latest version
        # otherwise something is wrong on backend
        # version is not supposed to have no versions
        latest_version = registered_model.latest_versions[0]

        return latest_version

    def get_best_version(
        self,
        name: str,
        metric: str,
        optimal_min: bool = False,
    ) -> ModelVersion:
        """Get best version of model "name" according to a metric."""
        # optimal_min parameter is to look for minimal value of metric, max by default
        current_best_version, current_best_score = None, None
        self.check_model_registered(name)
        # MlflowClient.search_model_versions always returns all versions in single page with no token
        # as it uses SqlAlchemyStore on mlflow server pod based on helm Values.mlflow.backendUri
        # which starts with "postgres". See mlflow/store/model_registry/sqlalchemy_store.py:732
        model_versions = self.client.search_model_versions(filter_string=f"name = '{name}'")

        for mv in model_versions:
            try:
                metric_value = self.client.get_run(run_id=mv.run_id).data.metrics[metric]
            except KeyError:
                continue  # metric might not be logged for SOME versions, so don't raise straight away

            if current_best_score is None:
                current_best_version, current_best_score = mv, metric_value
            else:
                if optimal_min:
                    if metric_value < current_best_score:
                        current_best_version, current_best_score = mv, metric_value
                else:
                    if metric_value > current_best_score:
                        current_best_version, current_best_score = mv, metric_value
        if current_best_version:
            return current_best_version
        else:
            raise MetricNotLogged(name, metric)

    def get_initial_version(self, name: str) -> ModelVersion:
        """Get initial version of model "name"."""
        # TODO make faster initial version retrieval through Model table at server
        model_versions = self.get_all_versions(name)
        min_version = min(model_versions, key=attrgetter("version"))

        return min_version

    def get_version(self, name: str, version: int) -> ModelVersion:
        """
        Get model version from MLflow Model Registry and return its ModelVersion object.

        https://mlflow.org/docs/latest/python_api/mlflow.entities.html#mlflow.entities.model_registry.ModelVersion

        Parameters:
            name (str): Model name used for model registration.
            version (int): Desired version number.

        Returns:
            ModelVersion: Desired model version

        """
        # first, check that model is registered
        self.check_model_registered(name)
        # now, try to retrieve desired version
        try:
            model_version = self.client.get_model_version(name, str(version))
        except RestException as err:
            if err.error_code == "RESOURCE_DOES_NOT_EXIST":
                # model is registered, but version is not found
                raise VersionNotFound(name, str(version))
            else:
                raise err

        return model_version

    def get_all_versions(
        self,
        name: str,
    ) -> PagedList[ModelVersion]:
        """
        Get all versions of a given model and return PagedList of ModelVersion objects.

        https://mlflow.org/docs/latest/python_api/mlflow.entities.html#mlflow.entities.model_registry.ModelVersion

        Parameters:
            name (str): Model name used for model registration.

        Returns:
            PagedList[ModelVersion]: Available model versions
        """
        self.check_model_registered(name)

        # MlflowClient.search_model_versions always returns all versions in single page with no token
        # as it uses SqlAlchemyStore on mlflow server pod based on helm Values.mlflow.backendUri
        # which starts with "postgres". See mlflow/store/model_registry/sqlalchemy_store.py:732
        model_versions = self.client.search_model_versions(filter_string=f"name = '{name}'")

        return model_versions

    def choose_version(
        self,
        *,
        name: str,
        criteria: str,  # TODO enum?
        metric: str = None,
        optimal_min: bool = False,
    ) -> ModelVersion:
        """
        Choose optimal model version from MLflow Model Registry and return its ModelVersion object.

        https://mlflow.org/docs/latest/python_api/mlflow.entities.html#mlflow.entities.model_registry.ModelVersion

        Choice is made according to specified criteria.

        Parameters:
            name (str): Model name used for model registration.
            criteria (str): Criteria to choose between model versions. Must be one of: "initial", "latest", "best".
            metric (str): Metric to use with "best" criteria. Has no effect otherwise.
            optimal_min (bool): If set to True and "best" criteria is used, then choose version with minimal
                value of "metric" (useful if metric is a loss function). Defaults to False (choose version with maximal
                value of "metric").

        Returns:
            ModelVersion: Optimal model version

        """
        # for now, return single path and no name choosing -- model name must be explicitly passed
        # TODO in the future make name resolvers and return list of paths, one per chosen name
        version_fetcher_map = {
            "initial": self.get_initial_version,
            "latest": self.get_latest_version,
            "best": partial(
                self.get_best_version,
                metric=metric,
                optimal_min=optimal_min,
            ),
        }
        if criteria == "best" and metric is None:
            raise NoMetricProvided(criteria)
        if criteria in version_fetcher_map:
            return version_fetcher_map[criteria](name=name)
        else:
            raise UnsupportedCriteria(criteria, list(version_fetcher_map.keys))
