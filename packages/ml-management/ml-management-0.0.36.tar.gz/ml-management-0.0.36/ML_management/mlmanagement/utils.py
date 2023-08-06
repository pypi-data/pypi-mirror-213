"""Common variables."""
import os

server_ml_api = os.environ.get("server_url", "http://localhost:8000") + "/mlflow"
is_server = os.environ.get("is_server", False)

active_run_stack = []
active_experiment_name = None

EXPERIMENT_NAME_FOR_EXECUTOR = "executors"
EXPERIMENT_NAME_FOR_DATASET_LOADER = "dataset_loaders"
