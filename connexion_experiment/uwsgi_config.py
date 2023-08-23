import logging
from typing import Any, Optional

import connexion
from connexion.lifecycle import ConnexionResponse

import connexion_experiment.global_app as global_app
from connexion_experiment.global_app import APP

from ratelimit.auths.ip import client_ip
from ratelimit import RateLimitMiddleware, Rule
from ratelimit.backends.simple import MemoryBackend
from starlette.types import Receive, Scope, Send
from ipaddress import ip_address
from typing import Tuple
from starlette.types import Receive, Scope, Send


LOGGER = logging.getLogger(__name__)

# broken too....
# def any_error_as_problem(exception: Exception) -> ConnexionResponse:
#     """Customize exceptions"""
#     LOGGER.warning(exception)
#     traceback.print_exc()
#
#     error_document = {"code": 1, "message": str(exception)}
#
#     log = logging.getLogger(__name__)
#     log.error(error_document["message"])
#     log.exception("HTTP Error")  # exception() includes exec_info automatically
#
#     if os.environ.get("ENV", "") in ["WORKSTATION", "DEV", "TEST"]:
#         problem = connexion.problem(500, type(exception).__name__, str(exception))
#     else:
#         problem = connexion.problem(500, type(exception).__name__, "An error occurred")
#     return connexion.FlaskApi.get_response(problem)


YAML = "openapi.yaml"


print("got env workstation")
global_app.APP.add_api(
    YAML,
    strict_validation=True,
    validate_responses=True,
    # connexion tries to json encode all mimetypes
    # validator_map={"response": CustomResponseValidator},
)


async def client_ip_own(scope: Scope) -> Tuple[str, str]:
    """
    parse ip
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

rate_limit = RateLimitMiddleware(
    global_app.APP,
    client_ip_own,  # switch out
    MemoryBackend(),
    {
        r"^/environment": [Rule(second=1), Rule(group="admin")],
        r"^/version": [Rule(minute=100), Rule(group="admin")],
    },
    on_blocked=yourself_429,
)

# broken too
# global_app.APP.add_error_handler(Exception, any_error_as_problem)
