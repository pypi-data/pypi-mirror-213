from __future__ import annotations

import mimetypes
from typing import Any
from typing import List
from typing import Optional

import h2o_mlops_autogen

from h2o_mlops import _core
from h2o_mlops import _projects
from h2o_mlops import _utils


class MLOpsExperiment:
    """Interact with an Experiment on H2O MLOps."""

    def __init__(
        self, client: _core.MLOpsClient, project: _projects.MLOpsProject, raw_info: Any
    ):
        self._artifacts: Optional[List[Any]] = None
        self._client = client
        self._project = project
        self._raw_info = raw_info

    @property
    def artifact_types(self) -> List[str]:
        """List artifact types available for the Experiment."""
        if not self._artifacts:
            srv = self._client._mlops_backend.storage.artifact
            self._artifacts = srv.list_entity_artifacts(
                h2o_mlops_autogen.StorageArtifact(entity_id=self.uid)
            ).artifact

        artifact_name_mapping = {
            "python/mlflow": "python/mlflow.zip",
            "dai/mojo_pipeline": "dai_mojo_pipeline",
            "dai/scoring_pipeline": "dai_python_scoring_pipeline",
            "h2o3/mojo": "h2o3_mojo",
            "python/pickle": "python/pickle",
            "mlflow/mojo_pipeline": "mlflow_mojo_pipeline",
            "mlflow/scoring_pipeline": "mlflow_scoring_pipeline",
            "mlflow/h2o3_mojo": "mlflow_h2o3_mojo",
        }

        return [
            artifact_name_mapping[a.type]
            for a in self._artifacts
            if a.type in artifact_name_mapping
        ]

    @property
    def name(self) -> str:
        """Experiment display name."""
        return self._raw_info.display_name

    @property
    def uid(self) -> str:
        """Experiment unique ID."""
        return self._raw_info.id

    def delete(self) -> None:
        """Delete Experiment from all Projects in H2O MLOps."""
        self._client._mlops_backend.storage.experiment.delete_experiment(
            h2o_mlops_autogen.StorageDeleteExperimentRequest(self.uid)
        )


class MLOpsExperiments:
    def __init__(self, client: _core.MLOpsClient, project: _projects.MLOpsProject):
        self._client = client
        self._project = project

    def create(self, data: str, name: str) -> MLOpsExperiment:
        """Create an Experiment in H2O MLOps.

        Args:
            data: relative path to the experiment artifact being uploaded
            name: display name for Experiment
        """
        artifact = self._client._mlops_backend.storage.artifact.create_artifact(
            h2o_mlops_autogen.StorageCreateArtifactRequest(
                h2o_mlops_autogen.StorageArtifact(
                    entity_id=self._project.uid, mime_type=mimetypes.types_map[".zip"]
                )
            )
        ).artifact

        with open(data, mode="rb") as z:
            self._client._mlops_backend.storage.artifact.upload_artifact(
                file=z, artifact_id=artifact.id
            )

        ingestion = self._client._mlops_backend.ingest.model.create_model_ingestion(
            h2o_mlops_autogen.IngestModelIngestion(artifact_id=artifact.id)
        ).ingestion

        model_metadata = _utils._convert_metadata(ingestion.model_metadata)
        model_params = h2o_mlops_autogen.StorageExperimentParameters(
            target_column=ingestion.model_parameters.target_column
        )

        experiment = self._client._mlops_backend.storage.experiment.create_experiment(
            h2o_mlops_autogen.StorageCreateExperimentRequest(
                project_id=self._project.uid,
                experiment=h2o_mlops_autogen.StorageExperiment(
                    display_name=name,
                    metadata=model_metadata,
                    parameters=model_params,
                ),
            )
        ).experiment

        artifact.entity_id = experiment.id
        artifact.type = ingestion.artifact_type

        self._client._mlops_backend.storage.artifact.update_artifact(
            h2o_mlops_autogen.StorageUpdateArtifactRequest(
                artifact=artifact, update_mask="type,entityId"
            )
        )

        return self.get(experiment.id)

    def get(self, uid: str) -> MLOpsExperiment:
        """Get the Experiment object corresponding to an H2O MLOps Experiment.

        Args:
            uid: H2O MLOps unique ID for the Experiment.
        """
        experiment = self._client._mlops_backend.storage.experiment.get_experiment(
            h2o_mlops_autogen.StorageExperiment(uid)
        ).experiment
        return MLOpsExperiment(self._client, self._project, experiment)

    def list(self, **selectors: Any) -> _utils.Table:
        """Retrieve Table of Experiments available in the Project.

        Examples::

            # filter on columns by using selectors
            project.experiments.list(name="experiment-demo")

            # use an index to get an H2O MLOps entity referenced by the table
            experiment = project.experiments.list()[0]

            # get a new Table using multiple indexes or slices
            table = project.experiments.list()[2,4]
            table = project.experiments.list()[2:4]
        """
        experiments = self._client._mlops_backend.storage.experiment.list_experiments(
            h2o_mlops_autogen.StorageListExperimentsRequest(
                project_id=self._project.uid
            )
        ).experiment
        data = [{"name": m.display_name, "uid": m.id} for m in experiments]
        return _utils.Table(
            data=data,
            keys=["name", "uid"],
            get_method=lambda x: self.get(x["uid"]),
            **selectors,
        )
