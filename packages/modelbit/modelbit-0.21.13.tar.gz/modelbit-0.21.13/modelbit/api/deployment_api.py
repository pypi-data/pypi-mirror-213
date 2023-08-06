import logging
from enum import Enum
from typing import Any, Dict, List

from .api import MbApi
from .common import OwnerInfo

logger = logging.getLogger(__name__)


class DeploymentDesc:

  def __init__(self, data: Dict[str, Any]):
    self.id: str = data["id"]
    self.name: str = data["name"]
    self.version: str = data["version"]
    self.deployedAtMs: int = data["deployedAtMs"]
    self.ownerInfo = OwnerInfo(data["ownerInfo"])


class DeploymentApi:
  api: MbApi

  def __init__(self, api: MbApi):
    self.api = api

  def listDeployments(self, branch: str) -> List[DeploymentDesc]:
    resp = self.api.getJsonOrThrow("api/cli/v1/deployments/list", {"branch": branch})
    deployments = [DeploymentDesc(ds) for ds in resp.get("deployments", [])]
    return deployments
