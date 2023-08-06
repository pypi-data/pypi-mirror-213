"""Dataset loader template for custom dataset loader."""
from abc import ABC, abstractmethod

from ML_management.mlmanagement import mlmanagement, utils
from ML_management.mlmanagement.utils import EXPERIMENT_NAME_FOR_DATASET_LOADER
from mlflow.pyfunc import PythonModel


class DatasetLoaderPattern(PythonModel, ABC):
    """Define dataset loader."""

    def __init__(self, dataset_loader_name: str):
        """
        Init dataset loader class.

        :param dataset_loader_name: The name of the dataset loader
        """
        self.dataset_loader_name = dataset_loader_name

        # That parameters will be set automatically in job before the 'get_dataset' func would be executed.
        self.data_path = None

    @abstractmethod
    def get_dataset(self, **dataset_params):
        """
        Return dataset.

        To get data_path use self.data_path parameter, which also will be set in the job.
        'dataset_params' are dataset_loader parameters. One has to define it as ordinary kwargs
        with type annotation.
        """
        raise NotImplementedError

    def upload_dataset_loader(self, pip_requirements=None, extra_pip_requirements=None, conda_env=None):
        """
        Upload wrapper to MLmanagement server.

        :param pip_requirements: {{ pip_requirements }}
        :param extra_pip_requirements: {{ extra_pip_requirements }}
        `pip_requirements` and 'extra_pip_requirements' must be either a string path to a pip requirements file on the
            local filesystem or an iterable of pip requirement strings.
        :param conda_env: {{ conda_env }}
        'conda_env' must be a dict specifying the conda environment for this model.
        """
        old_experiment_name = utils.active_experiment_name
        mlmanagement.set_experiment(EXPERIMENT_NAME_FOR_DATASET_LOADER)
        try:
            with mlmanagement.start_run(nested=True):
                mlmanagement.log_model(
                    artifact_path="",
                    python_model=self,
                    registered_model_name=self.dataset_loader_name,
                    pip_requirements=pip_requirements,
                    extra_pip_requirements=extra_pip_requirements,
                    conda_env=conda_env,
                )
        except Exception as err:
            raise err
        finally:
            utils.active_experiment_name = old_experiment_name
