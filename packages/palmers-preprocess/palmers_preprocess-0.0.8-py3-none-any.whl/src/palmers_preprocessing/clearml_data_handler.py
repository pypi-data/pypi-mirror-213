import pickle

import pandas as pd
from clearml import Dataset, Task


class DatasetLoader:
    def __init__(self, dataset_path=None):
        self.dataset_path = dataset_path

    @classmethod
    def _validate_dataset_identifier(cls, dataset_id, dataset_name, dataset_project):
        if dataset_id is None and (dataset_name is None or dataset_project is None):
            raise ValueError('dataset id cannot be None')

    def download(self, dataset_id=None, dataset_name=None, dataset_project=None, dataset_version=None, tags=None, cache=False):
        self._validate_dataset_identifier(dataset_id, dataset_name, dataset_project)
        if (not cache) or self.dataset_path is None:
            self.dataset_path = Dataset.get(dataset_id=dataset_id,
                                         dataset_name=dataset_name,
                                         dataset_project=dataset_project,
                                         dataset_version=dataset_version,
                                         dataset_tags=tags

                                         ).get_local_copy()
        return self.dataset_path


    def load_dfs_from_dataset(self, dataset_id=None, dataset_name=None, dataset_project=None, dataset_path=None,
                              dataset_file_names=None, dataset_version=None, dataset_tags=None, cache=False):
        if dataset_path is not None:
            self.dataset_path = dataset_path

        if self.dataset_path is None or (not cache):
            self.dataset_path = self.download(dataset_id=dataset_id,
                                                  dataset_project=dataset_project,
                                                  dataset_name=dataset_name,
                                                  dataset_version=dataset_version,
                                                  tags=dataset_tags, cache=cache)

        dfs = {}
        for file_name in dataset_file_names:
            if file_name:
                dataset_file_path = self.dataset_path + '/' + file_name
                df = pd.read_csv(dataset_file_path, dtype=str)
                dfs[file_name] = df
        return dfs


class TaskLoader:
    @classmethod
    def _validate_task_identifier(cls, task_id, project_name, task_name):
        if task_id is None and (project_name is None or task_name is None):
            raise ValueError('task_id cannot be None')

    @classmethod
    def get_task(cls, task_id=None, project_name=None, task_name=None, tags=None):
        cls._validate_task_identifier(task_id=task_id, project_name=project_name, task_name=task_name)
        task = Task.get_task(task_id=task_id, project_name=project_name, task_name=task_name,
                             tags=tags)
        return task


class ArtifactLoader:
    def __init__(self):
        self.artifact_local_path = None

    @classmethod
    def load_artifacts(cls, project_name=None, task_name=None, task_id=None, tags=None):
        task = TaskLoader().get_task(task_id=task_id, project_name=project_name, task_name=task_name, tags=tags)
        return task.artifacts


    def download(self, artifact_name, task_id=None, project_name=None, task_name=None, tags=None, cache=False):
        if self.artifact_local_path is None or (not cache):
            artifacts = self.load_artifacts(project_name=project_name, task_name=task_name, task_id=task_id, tags=tags)
            if artifact_name in artifacts:
                self.artifact_local_path = artifacts[artifact_name].get_local_copy()
            else:
                raise ValueError(f"Artifact {artifact_name} not found in task {task_id} {project_name}/{task_name}")

        return self.artifact_local_path

    def download_artifacts(self, artifacts_names, task_id=None, project_name=None, task_name=None, tags=None, cache=False):
        artifact_paths = {}
        artifacts = self.load_artifacts(project_name=project_name, task_name=task_name, task_id=task_id, tags=tags)
        for artifact_name in artifacts_names:
            if artifact_name in artifacts:
                artifact_paths[artifact_name] = artifacts[artifact_name].get_local_copy()

        return artifact_paths


    def load_artifact_as_df(self, artifact_name, task_id=None, project_name=None, task_name=None, tags=None, cache=False):
        local_path = self.download(artifact_name=artifact_name, task_id=task_id, project_name=project_name, task_name=task_name, tags=tags, cache=cache)
        artifact = pd.read_csv(local_path, dtype=str)
        return artifact

    def load_pickle_artifacts(self, artifacts_names, task_id=None, project_name=None, task_name=None, tags=None, cache=False):
        local_paths = self.download_artifacts(artifacts_names=artifacts_names, task_id=task_id, project_name=project_name, task_name=task_name, tags=tags, cache=cache)
        files = {}
        for artifact_name, local_path in local_paths.items():
            # read pickle from local_path
            with open(local_path, 'rb') as f:
                files[artifact_name] = pickle.load(f)

        return files

