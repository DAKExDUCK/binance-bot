import logging.config


config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "custom": {
            "format": "{asctime} - {levelname} - {message}",
            "style": "{",
            "datefmt": "%d/%m %H:%M:%S"
        }
    },
    "handlers": {
        "stdout": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "custom"
        }
    },
    "loggers": {
        "custom_std": {
            "handlers": ["stdout"],
            "level": "INFO",
            "propagate": True
        }
    }
}

logging.config.dictConfig(config)
logger = logging.getLogger('custom_std')
