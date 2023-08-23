import logging
from functools import wraps
from typing import Any


LOGGER = logging.getLogger(__name__)


def public_endpoint(func: Any) -> Any:
    """Just to Tag"""

    @wraps(func)
    def func_wrapper(*args: Any, **kwargs: Any) -> Any:
        """Wrapper"""
        return func(*args, **kwargs)

    return func_wrapper
