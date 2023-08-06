#!/usr/bin/env python3

from typing import Callable, Optional, TypeVar
import logging
import time
import os
from functools import wraps

from modelbit.error import NonRetryableError

T = TypeVar("T")


def retry(retries: int, logger: Optional[logging.Logger]):

  def decorator(func: Callable[..., T]) -> Callable[..., T]:
    if os.getenv("NORETRY", None):
      return func

    @wraps(func)
    def innerFn(*args, **kwargs):
      lastError: Optional[Exception] = None
      for attempt in range(retries):
        try:
          return func(*args, **kwargs)
        except NonRetryableError:
          raise
        except Exception as e:
          lastError = e
          retryTime = 2**attempt
          if logger and attempt > 2:
            logger.warn("Retrying in %ds.", retryTime)
          time.sleep(retryTime)
      if lastError is None:
        raise Exception(f"Failed after {retries} retries. Please contact support.")
      raise lastError

    return innerFn

  return decorator
