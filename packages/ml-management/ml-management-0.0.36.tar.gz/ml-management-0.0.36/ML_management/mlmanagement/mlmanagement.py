"""
Mlflow server inside ML_management.

ML_manager sends request to our server on /mlflow endpoint
Server calls original mlflow function accordingly
"""
import atexit
import inspect
import io
import os
import tempfile
import zipfile
from typing import Any, Dict, List, Optional, Union

import pandas
from ML_management.executor_template.upload_model_mode import UploadModelMode
from ML_management.mlmanagement import utils
from ML_management.mlmanagement.mlmanager import request_for_function
from ML_management.mlmanagement.utils import active_run_stack, is_server
from mlflow.entities import Experiment, Run, RunStatus, ViewType
from mlflow.entities.model_registry import ModelVersion, RegisteredModel
from mlflow.models import ModelInputExample, ModelSignature
from mlflow.pyfunc import PyFuncModel
from mlflow.store.entities import PagedList
from mlflow.tracking._model_registry import DEFAULT_AWAIT_MAX_SLEEP_SECONDS
from mlflow.tracking.fluent import _RUN_ID_ENV_VAR, SEARCH_MAX_RESULTS_PANDAS
from mlflow.utils import env

import mlflow
from mlflow import ActiveRun


def monkey_patching_exit(self, exc_type, exc_val, exc_tb):
    """Redefine __exit__ function of class ActiveRun."""
    status = RunStatus.FINISHED if exc_type is None else RunStatus.FAILED
    end_run(RunStatus.to_string(status))
    return exc_type is None


# Rewrite __exit__ method to enable using Python ``with`` syntax of ActiveRun class.
ActiveRun.__exit__ = monkey_patching_exit


def start_run_if_not_exist():
    """If run doesn't exist call start_run() function."""
    if len(active_run_stack) == 0:
        start_run()


def set_experiment(experiment_name: str) -> None:
    """
    Set the given experiment as the active experiment.

    The experiment must either be specified by name via
    experiment_name or by ID via experiment_id. The experiment name and ID cannot both be specified.
    Set global variable active_experiment_name to that experiment_name.
    """
    request_for_function(inspect.currentframe())
    utils.active_experiment_name = experiment_name


def get_experiment_by_name(name: str) -> Optional[Experiment]:
    """Retrieve an experiment by experiment name from the backend store."""
    return request_for_function(inspect.currentframe())


def search_runs(
    experiment_ids: Optional[List[str]] = None,
    filter_string: str = "",
    run_view_type: int = ViewType.ACTIVE_ONLY,
    max_results: int = SEARCH_MAX_RESULTS_PANDAS,
    order_by: Optional[List[str]] = None,
    output_format: str = "pandas",
) -> Union[List[Run], "pandas.DataFrame"]:
    """Search experiments that fit the search criteria."""
    return request_for_function(inspect.currentframe())


def start_run(
    run_id: str = None,
    experiment_id: Optional[str] = None,
    run_name: Optional[str] = None,
    nested: bool = False,
    tags: Optional[Dict[str, Any]] = None,
) -> ActiveRun:
    """
    Start a new MLflow run, setting it as the active run under which metrics and parameters will be logged.

    The return value can be used as a context manager within a with block; otherwise, you must call end_run() to
    terminate the current run.
    If you pass a run_id or the MLFLOW_RUN_ID environment variable is set, start_run attempts to resume a run with
    the specified run ID and other parameters are ignored. run_id takes precedence over MLFLOW_RUN_ID.
    If resuming an existing run, the run status is set to RunStatus.RUNNING.
    Add that created run to active_run_stack.
    """
    if len(active_run_stack) > 0 and not nested:
        raise Exception(
            (
                "Run with UUID {} is already active. To start a new run, first end the "
                + "current run with mlmanagement.end_run(). To start a nested "
                + "run, call start_run with nested=True"
            ).format(active_run_stack[0].info.run_id)
        )
    _active_run = request_for_function(inspect.currentframe())
    active_run_stack.append(_active_run)
    return _active_run


def _add_job_registration_metainfo(
    registration_timestamp,
    init_model_version_run_id,
    name,
    job_executor_name,
    job_executor_version,
    dataset_loader_name,
    dataset_loader_version,
    model_name,
    model_version,
    new_model_name,
    experiment_name,
    periodic_type,
    cron_expression,
    metric_name,
    optimal_min,
    choice_criteria,
    executor_model_params_json,
    data_params_json,
    collector_name,
):
    """Add job metainfo on job registration. For internal use only."""
    return request_for_function(inspect.currentframe())


def _add_job_start_metainfo(
    job_name,
    start_timestamp,
):
    """Add job metainfo on execution start. For internal use only."""
    return request_for_function(inspect.currentframe())


def _add_job_end_metainfo(
    job_name,
    end_timestamp,
):
    """Add job metainfo on execution end. For internal use only."""
    return request_for_function(inspect.currentframe())


def _add_job_fail_metainfo(
    job_name,
    end_timestamp,
):
    """Add job metainfo on execution fail. For internal use only."""
    return request_for_function(inspect.currentframe())


def log_model(
    artifact_path,
    upload_model_mode: Optional[UploadModelMode] = None,
    loader_module=None,
    data_path=None,
    code_path=None,
    conda_env=None,
    python_model=None,
    artifacts=None,
    registered_model_name="default_name",  # TODO maybe raise if no name?
    signature: ModelSignature = None,
    input_example: ModelInputExample = None,
    await_registration_for=DEFAULT_AWAIT_MAX_SLEEP_SECONDS,
    pip_requirements=None,
    extra_pip_requirements=None,
    source_model_name=None,
    source_model_version=None,
):
    """
    Log a Pyfunc model with custom inference logic and optional data dependencies as an MLflow artifact.

    Current run is using.
    You cannot specify the parameters: loader_module, data_path and the parameters: python_model, artifacts together.
    """
    start_run_if_not_exist()
    return request_for_function(inspect.currentframe(), ["pyfunc"])


def log_metric(key: str, value: float, step: Optional[int] = None) -> None:
    """Log a metric under the current run. If no run is active, this method will create a new active run."""
    start_run_if_not_exist()
    return request_for_function(inspect.currentframe())


def log_artifact(local_path: str, artifact_path: Optional[str] = None) -> None:
    """
    Log a local file or directory as an artifact of the currently active run.

    If no run is active, this method will create a new active run.
    """
    start_run_if_not_exist()
    return request_for_function(inspect.currentframe())


def log_artifacts(local_dir: str, artifact_path: Optional[str] = None) -> None:
    """
    Log all the contents of a local directory as artifacts of the run.

    If no run is active, this method will create a new active run.
    """
    start_run_if_not_exist()
    return request_for_function(inspect.currentframe())


def set_tag(key: str, value: Any) -> None:
    """Set a tag under the current run. If no run is active, this method will create a new active run."""
    start_run_if_not_exist()
    return request_for_function(inspect.currentframe())


def autolog(
    log_every_n_epoch=1,
    log_models=True,
    disable=False,
    exclusive=False,
    disable_for_unsupported_versions=False,
    silent=False,
) -> None:
    """
    Enable (or disable) and configure autologging for all supported integrations.

    The parameters are passed to any autologging integrations that support them.
    """
    start_run_if_not_exist()
    return request_for_function(inspect.currentframe(), ["pytorch"])


def load_model(model_uri: str, suppress_warnings: bool = True) -> PyFuncModel:
    """Load a model stored in Python function format."""
    return request_for_function(inspect.currentframe(), ["pyfunc"])


def save_model(
    path,
    loader_module=None,
    data_path=None,
    code_path=None,
    conda_env=None,
    mlflow_model=None,
    python_model=None,
    artifacts=None,
    signature: ModelSignature = None,
    input_example: ModelInputExample = None,
    pip_requirements=None,
    extra_pip_requirements=None,
):
    """
    Save a Pyfunc model with custom inference logic and optional data dependencies to a path on the local filesystem.

    You cannot specify the parameters: loader_module, data_path and the parameters: python_model, artifacts together.
    """
    return request_for_function(inspect.currentframe(), ["pyfunc"])


def active_run() -> Optional[ActiveRun]:
    """Get the currently active Run, or None if no such run exists."""
    return active_run_stack[-1] if len(active_run_stack) > 0 else None


def get_run(run_id: str) -> Run:
    """
    Fetch the run from backend store.

    The resulting Run contains a collection of run metadata – RunInfo, as well as a collection of run parameters,
    tags, and metrics – RunData.
    In the case where multiple metrics with the same key are logged for the run, the RunData contains the most recently
    logged value at the largest step for each metric.
    """
    return request_for_function(inspect.currentframe())


finished_run_status = RunStatus.to_string(RunStatus.FINISHED)


def end_run(status: str = finished_run_status) -> None:
    """End an active MLflow run (if there is one)."""
    if is_server:
        mlflow.end_run()
        if len(active_run_stack) > 0:
            active_run_stack.pop()
    elif len(active_run_stack) > 0:
        # Clear out the global existing run environment variable as well.
        env.unset_variable(_RUN_ID_ENV_VAR)
        run = active_run_stack[-1]
        MlflowClient().set_terminated(run.info.run_id, status)
        active_run_stack.pop()


if is_server:
    atexit.unregister(mlflow.end_run)
else:
    atexit.register(end_run)


class MlflowClient(object):
    """Initialize an MLflow Client."""

    def __init__(self, registry_uri: Optional[str] = None):
        self.extra_attrs = ["tracking"]
        self.for_class = {
            "class_name": self.__class__.__name__,
            "class_kwargs": {"registry_uri": registry_uri},
        }

    def set_model_version_tag(self, name: str, version: str, key: str, value: Any) -> None:
        """Set model version tag."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    def get_run(self, run_id: str) -> Run:
        """Get run by id."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    def get_registered_model(self, name: str) -> RegisteredModel:
        """Get registered model by name."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    # MlflowClient.search_model_versions always returns all versions in single page with no token
    # as it uses SqlAlchemyStore on mlflow server pod based on helm Values.mlflow.backendUri
    # which starts with "postgres". See mlflow/store/model_registry/sqlalchemy_store.py:732
    def search_model_versions(self, filter_string: str) -> PagedList[ModelVersion]:
        """Search for model versions in backend that satisfy the filter criteria."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    def set_terminated(self, run_id: str, status: Optional[str] = None, end_time: Optional[int] = None) -> None:
        """Set a run’s status to terminated."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    def get_model_version(self, name: str, version: str) -> ModelVersion:
        """Get model version by model name and version number."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    def download_artifacts(self, run_id: str, path: str, dst_path: Optional[str] = None) -> str:
        """Download an artifact file or directory from a run to a local directory, and return a local path for it."""
        file = request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )
        if is_server:
            return file
        # save artifacts to local store
        if dst_path is None:
            dst_path = tempfile.mkdtemp()
        dst_path = os.path.abspath(os.path.normpath(dst_path))
        local_path = os.path.join(dst_path, os.path.normpath(path))
        if zipfile.is_zipfile(io.BytesIO(file)):
            zip_model = zipfile.ZipFile(io.BytesIO(file))
            try:
                os.makedirs(local_path)
            except OSError as ex:
                if ex.errno == 2:
                    ex.filename = dst_path
                raise ex
            zip_model.extractall(local_path)
        else:
            dirs = os.path.dirname(local_path)
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            with open(local_path, "wb") as f:
                f.write(file)
        return local_path
