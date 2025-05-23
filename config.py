import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig:
    """
    Default Configuration
    """

    # Flask Configuration
    APP_NAME = os.environ.get("APP_NAME")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    PROPAGATE_EXCEPTIONS = True
    DEBUG = False
    TESTING = False

    # Configuration of Flask-JWT-Extended
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    # Determines the minutes that the access token remains active
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=45)
    # Determines the days that the refresh token remains active
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
    # Algorithm used to generate the token
    JWT_ALGORITHM = "HS256"
    # Algorithm used to decode the token
    JWT_DECODE_ALGORITHMS = "HS256"
    # Header that should contain the JWT in a request
    JWT_HEADER_NAME = "Authorization"
    # Word that goes before the token in the Authorization header in this case empty
    JWT_HEADER_TYPE = "Bearer"
    # Where to look for a JWT when processing a request.
    JWT_TOKEN_LOCATION = "headers"

    # Config API documents
    API_TITLE = "Security API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/api/docs"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = "https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js"

    # Database configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SHOW_SQLALCHEMY_LOG_MESSAGES = False

    # App Environments
    APP_ENV_LOCAL = "local"
    APP_ENV_TESTING = "testing"
    APP_ENV_DEVELOP = "develop"
    APP_ENV_PRODUCTION = "production"
    APP_ENV = ""

    # Logging
    DATE_FMT = "%Y-%m-%d %H:%M:%S"
    LOG_FILE_API = f"{basedir}/logs/api.log"


class DevelopConfig(DefaultConfig):
    # App environment
    APP_ENV = DefaultConfig.APP_ENV_DEVELOP

    # Activate debug mode
    DEBUG = True

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")



class TestingConfig(DefaultConfig):
    # App environment
    APP_ENV = DefaultConfig.APP_ENV_TESTING

    # Flask disables error catching during request handling for better error reporting in tests
    TESTING = True

    # Activate debug mode
    DEBUG = True

    # False to disable CSRF protection during tests
    WTF_CSRF_ENABLED = False

    # Logging
    LOG_FILE_API = f"{basedir}/logs/api_tests.log"

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")


class LocalConfig(DefaultConfig):
    # App environment
    APP_ENV = DefaultConfig.APP_ENV_LOCAL

    # Activate debug mode
    DEBUG = False

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class ProductionConfig(DefaultConfig):
    # App environment
    APP_ENV = DefaultConfig.APP_ENV_PRODUCTION

    # Activate debug mode
    DEBUG = False

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
