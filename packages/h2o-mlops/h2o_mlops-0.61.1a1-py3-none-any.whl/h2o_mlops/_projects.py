from __future__ import annotations

from typing import Any
from typing import Optional

import h2o_mlops_autogen

from h2o_mlops import _core
from h2o_mlops import _environments
from h2o_mlops import _experiments
from h2o_mlops import _models
from h2o_mlops import _utils


class MLOpsProject:
    def __init__(self, client: _core.MLOpsClient, raw_info: Any):
        self._client = client
        self._raw_info = raw_info

    @property
    def description(self) -> str:
        """Project description."""
        return self._raw_info.description

    @property
    def experiments(self) -> _experiments.MLOpsExperiments:
        """Experiments linked to the Project."""
        return _experiments.MLOpsExperiments(self._client, self)

    @property
    def models(self) -> _models.MLOpsModels:
        """Registered Models in the Project."""
        return _models.MLOpsModels(self._client, self)

    @property
    def name(self) -> str:
        """Project display name."""
        return self._raw_info.display_name

    @property
    def environments(
        self,
    ) -> _environments.MLOpsEnvironments:
        """Environments available in the Project."""
        return _environments.MLOpsEnvironments(self._client, self)

    @property
    def uid(self) -> str:
        """Project unique ID."""
        return self._raw_info.id

    def delete(self) -> None:
        """Delete Project from H2O MLOps."""
        self._client._mlops_backend.storage.project.delete_project(
            h2o_mlops_autogen.StorageDeleteProjectRequest(project_id=self.uid)
        )


class MLOpsProjects:
    def __init__(self, client: _core.MLOpsClient):
        self._client = client

    def create(self, name: str, description: Optional[str] = None) -> MLOpsProject:
        """Create a Project in H2O MLOps.

        Args:
            name: display name for Project
            description: description of Project
        """
        uid = self._client._mlops_backend.storage.project.create_project(
            h2o_mlops_autogen.StorageCreateProjectRequest(
                project=h2o_mlops_autogen.StorageProject(
                    display_name=name, description=description
                )
            )
        ).project.id
        return self.get(uid)

    def get(self, uid: str) -> MLOpsProject:
        """Get the Project object corresponding to a Project in H2O MLOps.

        Args:
            uid: H2O MLOps unique ID for the Project.
        """
        return MLOpsProject(
            self._client,
            self._client._mlops_backend.storage.project.get_project(
                h2o_mlops_autogen.StorageGetProjectRequest(project_id=uid)
            ).project,
        )

    def list(self, **selectors: Any) -> _utils.Table:
        """Retrieve Table of Projects available to the user.

        Examples::

            # filter on columns by using selectors
            mlops.projects.list(name="demo")

            # use an index to get an H2O MLOps entity referenced by the table
            project = mlops.projects.list()[0]

            # get a new Table using multiple indexes or slices
            table = mlops.projects.list()[2,4]
            table = mlops.projects.list()[2:4]
        """
        projects = self._client._mlops_backend.storage.project.list_projects(
            h2o_mlops_autogen.StorageListProjectsRequest()
        ).project
        data = [{"name": p.display_name, "uid": p.id} for p in projects]
        return _utils.Table(
            data=data,
            keys=["name", "uid"],
            get_method=lambda x: self.get(x["uid"]),
            **selectors,
        )
