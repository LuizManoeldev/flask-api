# Smart Access API - Configuração do Sistema

## 1. Estrutura de Configuração

O sistema utiliza classes de configuração definidas em `config.py` para diferentes ambientes:

- **DefaultConfig**: Configuração base com valores padrão
- **DevelopConfig**: Configuração para ambiente de desenvolvimento
- **TestingConfig**: Configuração para ambiente de testes
- **LocalConfig**: Configuração para ambiente local
- **ProductionConfig**: Configuração para ambiente de produção

### Configurações Padrão (DefaultConfig)

A classe `DefaultConfig` define as configurações básicas que são compartilhadas por todos os ambientes:

```python
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
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=45)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
    JWT_ALGORITHM = "HS256"
    JWT_DECODE_ALGORITHMS = "HS256"
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
    JWT_TOKEN_LOCATION = "headers"

    # Config API documents
    API_TITLE = "Smart Access API"
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
```

### Configurações Específicas por Ambiente

Cada ambiente tem sua própria classe de configuração que herda de `DefaultConfig` e sobrescreve valores específicos:

#### Ambiente de Desenvolvimento (DevelopConfig)

```python
class DevelopConfig(DefaultConfig):
    # App environment
    APP_ENV = DefaultConfig.APP_ENV_DEVELOP

    # Activate debug mode
    DEBUG = True

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
```

#### Ambiente de Testes (TestingConfig)

```python
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
```

#### Ambiente Local (LocalConfig)

```python
class LocalConfig(DefaultConfig):
    # App environment
    APP_ENV = DefaultConfig
