import logging
import logging.handlers
import os
import sys
import traceback
from typing import Callable, List, Optional, TypeVar, cast
from functools import wraps

from modelbit.api.api import MbApi  # For perf, skip __init__
from modelbit.error import ModelbitError, UserFacingError

from .ux import printTemplate

logger = logging.getLogger(__name__)


def enableFileLogging():
  return os.environ.get("MB_LOG", None) is not None


def initLogging():
  LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
  streamHandler = logging.StreamHandler()
  handlers: List[logging.Handler] = [streamHandler]
  streamHandler.setLevel(LOGLEVEL)
  if enableFileLogging():
    try:
      import appdirs
      logDir = appdirs.user_log_dir("modelbit")
      if not os.path.exists(logDir):
        os.makedirs(logDir, exist_ok=True)
      fileHandler = logging.handlers.RotatingFileHandler(os.path.join(logDir, "log.txt"),
                                                         maxBytes=10485760,
                                                         backupCount=5)
      fileHandler.setLevel(level="INFO")
      handlers.append(fileHandler)
    except Exception as e:
      print(e)
      logging.info(e)

  logging.basicConfig(level="INFO", handlers=handlers)


def _logErrorToWeb(mbApi: Optional[MbApi], userErrorMsg: str):
  from modelbit.api import MbApi
  mbApi = mbApi or MbApi()
  errStack = traceback.format_exception(*sys.exc_info())[1:]
  errStack.reverse()
  errorMsg = userErrorMsg + "\n" + "".join(errStack)
  try:
    mbApi.getJson("api/cli/v1/error", {"errorMsg": errorMsg})
  except Exception as e:
    logger.info(e)


T = TypeVar("T")


def eatErrorAndLog(mbApi: Optional[MbApi], genericMsg: str):

  def decorator(func: Callable[..., T]) -> Callable[..., T]:

    @wraps(func)
    def innerFn(*args: object, **kwargs: object) -> T:
      error = None  # Store and raise outside the handler so the trace is more compact.
      try:
        return func(*args, **kwargs)
      except TypeError as e:
        _logErrorToWeb(mbApi, genericMsg)
        error = str(e)
      except UserFacingError as e:
        if e.logToModelbit:
          _logErrorToWeb(mbApi, e.userFacingErrorMessage)
        printTemplate("error", None, errorText=genericMsg + " " + e.userFacingErrorMessage)
        error = e.userFacingErrorMessage
      except Exception as e:
        specificError = getattr(e, "userFacingErrorMessage", None)
        error = genericMsg + (" " + specificError if specificError is not None else "")
        _logErrorToWeb(mbApi, cast(str, error))
        printTemplate("error_details", None, errorText=error, errorDetails=traceback.format_exc())
      # Convert to generic ModelbitError.
      raise ModelbitError(error)

    return innerFn

  return decorator
