from __future__ import annotations

from typing import Any
from typing import List
from typing import Optional
from typing import Union

import h2o_mlops_autogen
import httpx

from h2o_mlops import _core
from h2o_mlops import _environments
from h2o_mlops import _experiments
from h2o_mlops import _models
from h2o_mlops import _projects
from h2o_mlops import _runtimes
from h2o_mlops import _utils
from h2o_mlops import options
from h2o_mlops.errors import MLOpsDeploymentError


class MLOpsRealTimeScoringDeployment:
    """Interact with a real-time scoring Deployment on H2O MLOps."""

    def __init__(
        self,
        client: _core.MLOpsClient,
        deployment_id: str,
        environment: _environments.MLOpsEnvironment,
        project: _projects.MLOpsProject,
    ):
        self._client = client
        self._deployment_id = deployment_id
        self._environment = environment
        self._experiments: List[_experiments.MLOpsExperiment]
        self._project = project
        self._mode: str
        self._init()

    def _init(self) -> None:
        raw_info = self._get_raw_info()
        if raw_info.shadow_deployment:
            self._mode = "Champion/Challenger"
            primary_element = raw_info.shadow_deployment.primary_element
            secondary_element = raw_info.shadow_deployment.secondary_element
            self._experiments = [
                self._project.experiments.get(
                    primary_element.deployment_composition.experiment_id
                ),
                self._project.experiments.get(
                    secondary_element.deployment_composition.experiment_id
                ),
            ]
        if raw_info.single_deployment:
            self._mode = "Single Model"
            self._experiments = [
                self._project.experiments.get(
                    raw_info.single_deployment.deployment_composition.experiment_id
                )
            ]
        if raw_info.split_deployment:
            self._mode = "A/B Test"
            self._experiments = [
                self._project.experiments.get(
                    element.deployment_composition.experiment_id
                )
                for element in raw_info.split_deployment.split_elements
            ]

    @staticmethod
    def _get_deployment_mode(raw_info: Any) -> Optional[str]:
        if getattr(raw_info, "shadow_deployment"):
            return "Champion/Challenger"
        if raw_info.single_deployment:
            return "Single Model"
        if raw_info.split_deployment:
            return "A/B Test"
        return None

    def _get_raw_info(self) -> Any:
        for (
            deployment
        ) in self._client._mlops_backend.deployer.deployment.list_project_deployments(
            h2o_mlops_autogen.DeployListProjectDeploymentsRequest(
                project_id=self._project.uid
            )
        ).deployment:
            if deployment.id == self.uid:
                return deployment

    def _get_raw_status(self) -> Any:
        deployer_status = self._client._mlops_backend.deployer.deployment_status
        return deployer_status.get_deployment_status(
            h2o_mlops_autogen.DeployGetDeploymentStatusRequest(self.uid)
        ).deployment_status

    @property
    def environment(self) -> _environments.MLOpsEnvironment:
        """Deployment environment."""
        return self._environment

    @property
    def experiments(self) -> List[_experiments.MLOpsExperiment]:
        """List of experiments in Deployment."""
        return self._experiments

    @property
    def mode(self) -> str:
        """Deployment mode (Single Model, A/B Test, Champion Challenger)."""
        return self._mode

    @property
    def name(self) -> str:
        """Deployment display name."""
        return self._get_raw_info().display_name

    @property
    def uid(self) -> str:
        """Deployment unique ID."""
        return self._deployment_id

    @property
    def url_for_capabilities(self) -> str:
        """Deployment capabilities URL."""
        return self._get_raw_status().scorer.capabilities.url

    @property
    def url_for_sample_request(self) -> str:
        """Deployment sample request URL."""
        return self._get_raw_status().scorer.sample_request.url

    @property
    def url_for_schema(self) -> str:
        """Deployment schema URL."""
        base_url = "/".join(self.url_for_sample_request.split("/")[:-1])
        return f"{base_url}/schema"

    @property
    def url_for_scoring(self) -> str:
        """Deployment scoring URL."""
        return self._get_raw_status().scorer.score.url

    def delete(self) -> None:
        """Delete Deployment."""
        self._client._mlops_backend.deployer.deployment.delete_deployment(
            h2o_mlops_autogen.DeployDeleteDeploymentRequest(self.uid)
        )

    def get_capabilities(self, passphrase: Optional[str] = None) -> str:
        """Get capabilities supported by the Deployment, in JSON format.

        Args:
            passphrase: Deployment passphrase (if required)
        """
        headers = {}
        if passphrase:
            headers["Authorization"] = f"Bearer {passphrase}"
        result = httpx.get(self.url_for_capabilities, headers=headers)
        result.raise_for_status()
        return result.json()

    def get_sample_request(self, passphrase: Optional[str] = None) -> str:
        """Get sample request for the Deployment, in JSON format.

        Args:
            passphrase: Deployment passphrase (if required)
        """
        headers = {}
        if passphrase:
            headers["Authorization"] = f"Bearer {passphrase}"
        result = httpx.get(self.url_for_sample_request, headers=headers)
        result.raise_for_status()
        return result.json()

    def get_schema(self, passphrase: Optional[str] = None) -> str:
        """Get schema for the Deployment, in JSON format.

        Args:
            passphrase: Deployment passphrase (if required)
        """
        headers = {}
        if passphrase:
            headers["Authorization"] = f"Bearer {passphrase}"
        result = httpx.get(self.url_for_schema, headers=headers)
        result.raise_for_status()
        return result.json()["schema"]

    def is_healthy(self) -> bool:
        """Check if Deployment status is Healthy."""
        return self.status() == "HEALTHY"

    def raise_for_failure(self) -> None:
        """Raise an error if Deployment status is Failed."""
        if self.status() == "FAILED":
            raise MLOpsDeploymentError("Deployment failed.")

    def status(self) -> str:
        """Deployment status."""
        return self._get_raw_status().state


class MLOpsRealTimeScoringDeployments:
    def __init__(
        self,
        client: _core.MLOpsClient,
        environment: _environments.MLOpsEnvironment,
        project: _projects.MLOpsProject,
    ):
        self._client = client
        self._environment = environment
        self._project = project

    def create_a_b_test(self) -> None:
        raise NotImplementedError

    def create_create_champion_challenger(self) -> None:
        raise NotImplementedError

    def create_single(
        self,
        name: str,
        model: _models.MLOpsModel,
        scoring_runtime: _runtimes.MLOpsScoringRuntime,
        model_version: Union[int, str] = "latest",
        description: Optional[str] = None,
        kubernetes_options: Optional[options.KubernetesOptions] = None,
        security_options: Optional[options.SecurityOptions] = None,
    ) -> MLOpsRealTimeScoringDeployment:
        """Create a single model real-time Deployment in H2O MLOps.

        Args:
            name: Deployment display name
            model: MLOps Registered Model object
            scoring_runtime: MLOps Scoring Runtime object
            model_version: MLOps Registered Model version number
            description: Deployment description
            kubernetes_options: Kubernetes Options object
            security_options: Security Options object
        """
        experiment = model.get_experiment(model_version=model_version)
        deployable_artifact_type = scoring_runtime._raw_info.deployable_artifact_type
        artifact_processor = scoring_runtime._raw_info.artifact_processor
        composition = h2o_mlops_autogen.DeployDeploymentComposition(
            experiment_id=experiment.uid,
            deployable_artifact_type_name=deployable_artifact_type.name,
            artifact_processor_name=artifact_processor.name,
            runtime_name=scoring_runtime.uid,
        )
        if not kubernetes_options:
            kubernetes_options = options.KubernetesOptions()
        kubernetes_resource_requirement = (
            h2o_mlops_autogen.DeployKubernetesResourceRequirement(
                limits=kubernetes_options.limits,
                requests=kubernetes_options.requests,
            )
        )
        kubernetes_resource_spec = h2o_mlops_autogen.DeployKubernetesResourceSpec(
            kubernetes_resource_requirement=kubernetes_resource_requirement,
            replicas=kubernetes_options.replicas,
        )
        self._environment._raise_for_unallowed_affinity(
            affinity=kubernetes_options.affinity
        )
        self._environment._raise_for_unallowed_toleration(
            toleration=kubernetes_options.toleration
        )
        kubernetes_configuration_shortcut = (
            h2o_mlops_autogen.DeployKubernetesConfigurationShortcut(
                kubernetes_affinity_shortcut_name=kubernetes_options.affinity,
                kubernetes_toleration_shortcut_name=kubernetes_options.toleration,
            )
        )
        if not security_options:
            security_options = options.SecurityOptions()
        if security_options.hashed_passphrase:
            passphrase_hash_type = h2o_mlops_autogen.DeployPassphraseHashType.BCRYPT
        else:
            passphrase_hash_type = h2o_mlops_autogen.DeployPassphraseHashType.PLAINTEXT
        if not security_options.passphrase:
            passphrase_hash_type = None
        security = h2o_mlops_autogen.DeploySecurity(
            h2o_mlops_autogen.DeployAuthenticationPassphrase(
                hash=security_options.passphrase,
                passphrase_hash_type=passphrase_hash_type,
            )
        )
        to_deploy = h2o_mlops_autogen.DeployDeployment(
            project_id=self._project.uid,
            deployment_environment_id=self._environment.uid,
            single_deployment=h2o_mlops_autogen.DeploySingleDeployment(
                deployment_composition=composition,
                kubernetes_configuration_shortcut=kubernetes_configuration_shortcut,
                kubernetes_resource_spec=kubernetes_resource_spec,
            ),
            display_name=name,
            description=description,
            security=security,
        )
        deployment = self._client._mlops_backend.deployer.deployment.create_deployment(
            h2o_mlops_autogen.DeployCreateDeploymentRequest(deployment=to_deploy)
        ).deployment
        return self.get(deployment.id)

    def get(self, uid: str) -> MLOpsRealTimeScoringDeployment:
        """Get the Deployment object corresponding to a Deployment in H2O MLOps.

        Args:
            uid: H2O MLOps unique ID for the Deployment.
        """
        return MLOpsRealTimeScoringDeployment(
            self._client, uid, self._environment, self._project
        )

    def list(self, **selectors: Any) -> _utils.Table:
        """Retrieve Table of Deployments available in the Project.

        Examples::

            # filter on columns by using selectors
            environment.deployments.list(name="demo")

            # use an index to get an H2O MLOps entity referenced by the table
            deployment = environment.deployments.list()[0]

            # get a new Table using multiple indexes or slices
            table = environment.deployments.list()[2,4]
            table = environment.deployments.list()[2:4]
        """
        srv = self._client._mlops_backend.deployer.deployment
        deployments = srv.list_project_deployments(
            h2o_mlops_autogen.DeployListProjectDeploymentsRequest(
                project_id=self._project.uid
            )
        ).deployment
        data = [
            d
            for d in deployments
            if d.deployment_environment_id == self._environment.uid
        ]
        data_as_dicts = [
            {
                "name": d.display_name,
                "mode": MLOpsRealTimeScoringDeployment._get_deployment_mode(d),
                "uid": d.id,
            }
            for d in data
        ]
        return _utils.Table(
            data=data_as_dicts,
            keys=["name", "mode", "uid"],
            get_method=lambda x: self.get(x["uid"]),
            **selectors,
        )
