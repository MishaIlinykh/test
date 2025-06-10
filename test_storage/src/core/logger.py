LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DEFAULT_HANDLERS = [
    "console",
]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": LOG_FORMAT,
        },
        "access": {
            "format": "%(asctime)s [ACCESS] %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "access": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "access",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "access": {
            "handlers": ["access"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
