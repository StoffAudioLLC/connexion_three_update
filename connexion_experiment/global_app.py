"""
This is here to avoid circular imports and to not launch the webserver too early
"""
import os

import connexion

APP = connexion.AsyncApp(
    __name__, specification_dir=os.environ.get("OPENAPI_LOCATION", ".")
)
