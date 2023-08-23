from typing import Any, Dict


def generate_logging_config(style: str) -> Dict[str, Any]:
    config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        },
        "handlers": {
            "default": {
                "level": "DEBUG",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",  # Default is stderr
            },
        },
        "loggers": {
            # root logger can capture too much
            "": {  # root logger
                "handlers": ["default"],
                "level": "DEBUG",  # temporary
                "propagate": False,
            },
        },
    }

    packages = {
        "requests.packages.urllib3": "DEBUG",
    }
    if style == "microservice":
        print("ALL THE DEBUG")
        # packages["connexion"] = "WARNING"
        packages["connexion"] = "DEBUG"
        packages["flask"] = "DEBUG"
        packages["uvicorn"] = "DEBUG"

        packages["asgiref"] = "DEBUG"
        packages["a2wsgi"] = "DEBUG"

    for name, level in packages.items():
        config["loggers"][name] = {
            "handlers": ["default"],
            "level": level,
            "propagate": False,
        }

    return config
