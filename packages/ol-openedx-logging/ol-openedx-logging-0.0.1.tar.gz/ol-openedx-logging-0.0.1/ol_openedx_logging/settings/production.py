from typing import Any, Dict
import platform
import sys


def _load_env_tokens(edx_settings, default_settings: Dict[str, Any]) -> Dict[str, Any]:
    configured_tokens = getattr(edx_settings, "ENV_TOKENS", {})
    default_settings.update(configured_tokens)
    return default_settings


def plugin_settings(edx_settings):
    # Taken directly from Tutor from overhang.io

    # This file and other files adapted from Tutor are covered by
    # and subject to the AGPL-3 as a clause 5 'aggregate'.
    hostname = platform.node().split(".")[0]
    syslog_format = (
        "[service_variant={service_variant}]"
        "[%(name)s][env:{logging_env}] %(levelname)s "
        "[{hostname}  %(process)d] [%(filename)s:%(lineno)d] "
        "- %(message)s"
    ).format(
        service_variant=edx_settings.SERVICE_VARIANT,
        logging_env=edx_settings.LOGGING_ENV,
        hostname=hostname,
    )

    handlers = ["console"]

    logger_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s %(levelname)s %(process)d "
                "[%(name)s] %(filename)s:%(lineno)d - %(message)s",
            },
            "syslog_format": {"format": syslog_format},
            "raw": {"format": "%(message)s"},
        },
        "filters": {
            "require_debug_false": {
                "()": "django.utils.log.RequireDebugFalse",
            },
            "userid_context": {
                "()": "edx_django_utils.logging.UserIdFilter",
            },
            "remoteip_context": {
                "()": "edx_django_utils.logging.RemoteIpFilter",
            },
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "filters": ["userid_context", "remoteip_context"],
                "stream": sys.stderr,
            },
            "tracking": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "/openedx/data/var/logs/tracking_logs.log",
                "backupCount": 5,
                "formatter": "raw",
                "maxBytes": 10485760,
            },
        },
        "loggers": {
            "django": {"handlers": handlers, "propagate": True, "level": "INFO"},
            "tracking": {
                "handlers": ["tracking"],
                "level": "DEBUG",
                "propagate": False,
            },
            "requests": {"handlers": handlers, "propagate": True, "level": "WARNING"},
            "factory": {"handlers": handlers, "propagate": True, "level": "WARNING"},
            "django.request": {
                "handlers": handlers,
                "propagate": True,
                "level": "ERROR",
            },
            "": {"handlers": handlers, "level": "INFO", "propagate": False},
        },
    }

    edx_settings.LOGGING = logger_config
