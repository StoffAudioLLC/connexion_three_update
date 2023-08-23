import logging
from functools import wraps
from typing import Any
from starlette.types import Receive, Scope, Send
from typing import Tuple
from ipaddress import ip_address
from ratelimit.auths import EmptyInformation

LOGGER = logging.getLogger(__name__)

async def client_ip(scope: Scope) -> Tuple[str, str]:
    """
    parse ip
    """
    real_ip = ""
    if scope["client"]:
        ip, port = tuple(scope["client"])
        if ip_address(ip).is_global:
            real_ip = ip
    else:
        raise EmptyInformation(scope)

    for name, value in scope["headers"]: 
        if name == b"x-real-ip":
            ip = value.decode("utf8")

        if not real_ip:
            real_ip = ip

    if not real_ip:
        raise EmptyInformation(scope)
    return real_ip, "default"

async def client_ip_own(scope: Scope) -> Tuple[str, str]:
    """
    temp for testing
    """
    return "127.0.0.0", "default"
def yourself_429(retry_after: int):
    async def inside_yourself_429(scope: Scope, receive: Receive, send: Send) -> None:
        await send({"type": "http.response.start", "status": 429})
        await send(
            {
                "type": "http.response.body",
                "body": b"TOO MANY REQUESTS",
                "more_body": False,
            }
        )

    return inside_yourself_429
def public_endpoint(func: Any) -> Any:
    """Just to Tag"""

    @wraps(func)
    def func_wrapper(*args: Any, **kwargs: Any) -> Any:
        """Wrapper"""
        return func(*args, **kwargs)

    return func_wrapper
