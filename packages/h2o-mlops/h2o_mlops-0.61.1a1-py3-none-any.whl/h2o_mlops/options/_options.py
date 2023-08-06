from typing import Dict
from typing import Optional


class KubernetesOptions:
    def __init__(
        self,
        replicas: int = 1,
        requests: Optional[Dict[str, str]] = None,
        limits: Optional[Dict[str, str]] = None,
        affinity: Optional[str] = None,
        toleration: Optional[str] = None,
    ):
        KubernetesOptions._validate_replicas(replicas)
        self._replicas = replicas
        self._requests = requests
        self._limits = limits
        self._affinity = affinity
        self._toleration = toleration

    @property
    def replicas(self) -> int:
        return self._replicas

    @replicas.setter
    def replicas(self, x: int) -> None:
        KubernetesOptions._validate_replicas(x)
        self._replicas = x

    @property
    def requests(self) -> Optional[Dict[str, str]]:
        return self._requests

    @requests.setter
    def requests(self, x: Optional[Dict[str, str]]) -> None:
        self._requests = x

    @property
    def limits(self) -> Optional[Dict[str, str]]:
        return self._limits

    @limits.setter
    def limits(self, x: Optional[Dict[str, str]]) -> None:
        self._limits = x

    @property
    def affinity(self) -> Optional[str]:
        return self._affinity

    @affinity.setter
    def affinity(self, x: Optional[str]) -> None:
        self._affinity = x

    @property
    def toleration(self) -> Optional[str]:
        return self._toleration

    @toleration.setter
    def toleration(self, x: Optional[str]) -> None:
        self._toleration = x

    @staticmethod
    def _validate_replicas(count: int) -> None:
        if count < 1:
            raise RuntimeError("Replica count must be at least 1.")


class SecurityOptions:
    def __init__(
        self, passphrase: Optional[str] = None, hashed_passphrase: Optional[bool] = None
    ):
        self._passphrase = passphrase
        self._hashed_passphrase = hashed_passphrase

    @property
    def passphrase(self) -> Optional[str]:
        return self._passphrase

    @passphrase.setter
    def passphrase(self, x: Optional[str]) -> None:
        self._passphrase = x

    @property
    def hashed_passphrase(self) -> Optional[bool]:
        return self._hashed_passphrase

    @hashed_passphrase.setter
    def hashed_passphrase(self, x: Optional[bool]) -> None:
        self._hashed_passphrase = x
