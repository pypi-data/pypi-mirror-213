import os

from pydantic import BaseSettings


def get_bool_from_string(string: str):
    return string.lower() in ("true", "1")


class AppSettings(BaseSettings):
    # General
    APP_VERSION: str = ""

    # Firebase config
    FIRESTORE_JSON_CONFIG: str = ""

    # Openai config
    OPENAI_API_KEY: str = ""
    OPENAI_MOCK_RESPONSES: str = ""
    OPENAI_MODEL_ABILITY: int = 1

    # Clerk config
    CLERK_JWT_PEM_KEY: str = os.getenv("CLERK_JWT_PEM_KEY", "").replace(r"\n", "\n")
    CLERK_TOKEN_LEEWAY: int = 300
    CLERK_USER_WEBHOOK_SECRET: str = ""
    CLERK_SECRET_KEY: str = ""
    CLERK_API_BASE_URL: str = ""

    DEFAULT_PAGE_LIMIT: int = 20

    LOCAL_TESTING: bool = get_bool_from_string(os.getenv("LOCAL_TESTING", "false"))
    ENABLED_KAFKA_EVENTS: bool = get_bool_from_string(
        os.getenv("ENABLED_KAFKA_EVENTS", "false")
    )

    # Algolia config
    ALGOLA_APP_ID: str = ""
    ALGOLIA_API_KEY: str = ""

    # Kafka config
    KAFKA_BOOTSTRAP_SERVER: str = ""
    KAFKA_USERNAME: str = ""
    KAFKA_PASSWORD: str = ""
    KAFKA_JWT_SECRET: str = ""

    # Sendgrid config
    SENDGRID_API_KEY: str = ""
    SENDGRID_FROM_EMAIL: str = ""

    # Sentry config
    SENTRY_DSN: str = ""
    SENTRY_TRACES_RATE: float = 1.0

    class Config:
        env_file = ".env"


SETTINGS = AppSettings()  # type: ignore
