import logging.config

from pythonjsonlogger.jsonlogger import JsonFormatter

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': JsonFormatter,
            'format': '%(asctime)%(levelname)%(processName)%(name)%(message)'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "gunicorn": {"propagate": True, 'level': 'INFO'},
        "gunicorn.access": {"propagate": True, 'level': 'INFO'},
        "gunicorn.error": {"propagate": True, 'level': 'INFO'},
        "uvicorn": {"propagate": True, 'level': 'INFO'},
        "uvicorn.access": {"propagate": False, 'level': 'INFO'},
        "uvicorn.error": {"propagate": True, 'level': 'INFO'},
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
