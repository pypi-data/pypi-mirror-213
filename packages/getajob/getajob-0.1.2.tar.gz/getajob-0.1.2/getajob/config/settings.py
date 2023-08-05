import os

from pydantic import BaseSettings


def get_bool_from_string(string: str):
    return string.lower() in ("true", "1")


class AppSettings(BaseSettings):
    # General
    APP_VERSION: str = ""

    # Firebase config
    FIRESTORE_COLLECTION_NAME: str = os.getenv("FIRESTORE_COLLECTION_NAME", "")
    FIRESTORE_PROJECT_ID: str = os.getenv("FIRESTORE_PROJECT_ID", "")
    FIRESTORE_PRIVATE_KEY_ID: str = os.getenv("FIRESTORE_PRIVATE_KEY_ID", "")
    FIRESTORE_PRIVATE_KEY: str = os.getenv("FIRESTORE_PRIVATE_KEY", "")
    FIRESTORE_CLIENT_EMAIL: str = os.getenv("FIRESTORE_CLIENT_EMAIL", "")
    FIRESTORE_CLIENT_ID: str = os.getenv("FIRESTORE_CLIENT_ID", "")
    FIRESTORE_AUTH_URI: str = os.getenv("FIRESTORE_AUTH_URI", "")
    FIRESTORE_TOKEN_URI: str = os.getenv("FIRESTORE_TOKEN_URI", "")
    FIRESTORE_AUTH_PROVIDER_X509_CERT_URL: str = os.getenv("FIRESTORE_AUTH_PROVIDER_X509_CERT_URL", "")
    FIRESTORE_CLIENT_X509_CERT_URL: str = os.getenv("FIRESTORE_CLIENT_X509_CERT_URL", "")

    # Openai config
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MOCK_RESPONSES: str = os.getenv("OPENAI_MOCK_RESPONSES", "")
    OPENAI_MODEL_ABILITY: int = int(os.getenv("OPENAI_MODEL_ABILITY", "1"))

    # Clerk config
    CLERK_JWT_PEM_KEY: str = os.getenv("CLERK_JWT_PEM_KEY", "")
    CLERK_TOKEN_LEEWAY: int = int(os.getenv("CLERK_TOKEN_LEEWAY", "300"))
    CLERK_USER_WEBHOOK_SECRET: str = os.getenv("CLERK_USER_WEBHOOK_SECRET", "")
    CLERK_SECRET_KEY: str = os.getenv("CLERK_SECRET_KEY", "")
    CLERK_API_BASE_URL: str = os.getenv("CLERK_API_BASE_URL", "")

    DEFAULT_PAGE_LIMIT: int = 20

    LOCAL_TESTING: bool = get_bool_from_string(os.getenv("LOCAL_TESTING", "false"))
    ENABLED_KAFKA_EVENTS: bool = get_bool_from_string(
        os.getenv("ENABLED_KAFKA_EVENTS", "false")
    )

    # Algolia config
    ALGOLA_APP_ID: str = os.getenv("ALGOLA_APP_ID", "")
    ALGOLIA_API_KEY: str = os.getenv("ALGOLIA_API_KEY", "")

    # Kafka config
    KAFKA_BOOTSTRAP_SERVER: str = os.getenv("KAFKA_BOOTSTRAP_SERVER", "")
    KAFKA_USERNAME: str = os.getenv("KAFKA_USERNAME", "")
    KAFKA_PASSWORD: str = os.getenv("KAFKA_PASSWORD", "")
    KAFKA_JWT_SECRET: str = os.getenv("KAFKA_JWT_SECRET", "")

    # Sendgrid config
    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY", "")
    SENDGRID_FROM_EMAIL: str = os.getenv("SENDGRID_FROM_EMAIL", "")

    # Sentry config
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    SENTRY_TRACES_RATE: float = float(os.getenv("SENTRY_TRACES_RATE", "1.0"))

    class Config:
        env_file = ".env"


SETTINGS = AppSettings()  # type: ignore
