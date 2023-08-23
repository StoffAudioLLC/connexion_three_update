import logging.config

from connexion_experiment.controllers.utility_api import (
    environment,
    version,
)
from connexion_experiment.logging_config import generate_logging_config

__all__ = [
    "environment",
    "version",
]
logging.config.dictConfig(generate_logging_config("microservice"))
