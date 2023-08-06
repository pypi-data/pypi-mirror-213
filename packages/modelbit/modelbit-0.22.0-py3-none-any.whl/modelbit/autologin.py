#!/usr/bin/env python3

from typing import Optional

from modelbit.error import UserFacingError
from modelbit.helpers import isAuthenticated, performLogin, runtimeAuthInfo
from modelbit.api import MbApi

__mbApi: Optional[MbApi] = None


def mbApi() -> MbApi:
  global __mbApi
  if __mbApi is None:
    if not isAuthenticated():
      performLogin(refreshAuth=True)
    if isAuthenticated():
      __mbApi = MbApi(*runtimeAuthInfo())
  if __mbApi is None:
    raise UserFacingError("Unable to authenticate.")
  return __mbApi


def mbApiReadOnly() -> Optional[MbApi]:
  global __mbApi
  return __mbApi
