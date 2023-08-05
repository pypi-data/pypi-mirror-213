import sentry_sdk

from getajob.config.settings import SETTINGS


def initialize_sentry():
    sentry_sdk.init(
        dsn=SETTINGS.SENTRY_DSN,
        traces_sample_rate=SETTINGS.SENTRY_TRACES_RATE,
    )
