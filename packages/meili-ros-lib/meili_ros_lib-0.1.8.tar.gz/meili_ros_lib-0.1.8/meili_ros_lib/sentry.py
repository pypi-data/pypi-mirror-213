import os

import sentry_sdk
from sentry_sdk import capture_exception, capture_message

__all__ = ("initialize_sentry",)


def agent_sentry(exception=None, message=None):
    if message is not None:
        capture_message(message)
    if exception is not None:
        capture_exception(exception)


def initialize_sentry(key=None):
    """
    Initialize Sentry SDK

    Will only initialize sentry if key is provided or found in the configuration

    Set environemntal variable MEILI_SENTRY_DSN or ROS parameter /meili_sentry_dsn
    """
    key = key or os.environ.get("MEILI_SENTRY_DSN", None)
    if key:
        sentry_sdk.init(
            key,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1.0,
        )
