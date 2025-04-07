LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "simpleFormatter": {
            "format": "%(asctime)s %(levelname)5s %(threadName)-10s %(message)s",
        },
    },

    "handlers": {
        "fileHandler": {
            "class": "logging.FileHandler",
            "formatter": "simpleFormatter",
            "level": "DEBUG",
            "filename": "current.log",
            "mode": "w",
        },
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "formatter": "simpleFormatter",
            "level": "DEBUG",
            "stream": "ext://sys.stdout",
        },
    },

    "loggers": {
        # If you want to add more, like "uvicorn" or others, you can put them here
    },

    "root": {
        "level": "DEBUG",
        "handlers": ["fileHandler", "consoleHandler"],
    },
}
