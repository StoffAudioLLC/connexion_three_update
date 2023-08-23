import logging
import connexion
import xmltodict

from connexion_experiment.controllers.controller_utils import public_endpoint

LOGGER = logging.getLogger(__name__)


@public_endpoint
def environment():
    """
    Just environment
    """
    mime_type = connexion.request.headers["Accept"]  # type: ignore
    if mime_type == "application/xml":
        root = {
            "response": {
                "status": "good",
                "last_updated": "2014-02-16T23:10:12Z",
            }
        }
        return (
            xmltodict.unparse(root, pretty=True),
            200,
            {"Content-Type": "application/xml"},
        )
    elif mime_type == "application/pdf":
        pdf_file = "./connexion_experiment/environment.pdf"
        return pdf_file
    else:
        return "This is the enviro page"


@public_endpoint
def version() -> str:
    """Just version number.

    Don't rate limit this, it gets used for health checks.
    """
    return __name__
