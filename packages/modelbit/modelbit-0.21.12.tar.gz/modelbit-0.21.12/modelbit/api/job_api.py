from typing import Any, Dict, List, Optional

from .api import MbApi


class JobRunDesc:
  _id: str
  jobName: str
  state: str
  finishedAtMs: Optional[int] = None
  startedAtMs: Optional[int] = None
  errorMessage: Optional[str]
  successMessage: Optional[str]
  newRuntimeVersion: Optional[str]
  runtimeName: str

  def __init__(self, data: Dict[str, Any]):
    self._id = data["id"]
    self.jobName = data["jobName"]
    self.runtimeName = data["runtimeName"]
    self.state = data["state"]
    if "finishedAtMs" in data:
      self.finishedAtMs = int(data["finishedAtMs"])
    if "startedAtMs" in data:
      self.startedAtMs = int(data["startedAtMs"])
    self.errorMessage = data.get("errorMessage", None)
    self.successMessage = data.get("successMessage", None)
    self.newRuntimeVersion = data.get("newRuntimeVersion", None)

  def __repr__(self):
    return str(self.__dict__)


class JobApi:
  api: MbApi

  def __init__(self, api: MbApi):
    self.api = api

  def runJob(self, branch: str, runtimeName: str, jobName: str, args: Optional[List[Any]] = []) -> JobRunDesc:
    resp = self.api.getJsonOrThrow("api/cli/v1/jobs/run_job",
                                   dict(runtimeName=runtimeName, branch=branch, jobName=jobName, args=args))
    return JobRunDesc(resp["jobRun"])
