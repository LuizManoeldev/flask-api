# Smart Access API - Autenticação e Autorização

## 1. JWT (JSON Web Tokens)

O sistema utiliza JWT para autenticação, implementado através da biblioteca Flask-JWT-Extended. Os tokens JWT são utilizados para autenticar usuários e proteger rotas.

### Configuração do JWT

A configuração do JWT é feita no arquivo `config.py`:

```python
# Configuration of Flask-JWT-Extended
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=45)
JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
JWT_ALGORITHM = "HS256"
JWT_DECODE_ALGORITHMS = "HS256"
JWT_HEADER_NAME = "Authorization"
JWT_HEADER_TYPE = "Bearer"
JWT_TOKEN_LOCATION = "headers"
```

A instância do JWT é inicializada em `app/__init__.py`:

```python
from app.utils.auth import jwt

def create_app(settings_module):
    # ...
    jwt.init_app(app)
    # ...
```

### Handlers do JWT

Os handlers do JWT são definidos em `app/utils/auth.py` e incluem:

```python
@jwt.token_verification_loader
def custom_token_verification_callback(jwt_header, jwt_data):
    # Query in database
    user = UserModel.query.filter_by(id=jwt_data["sub"]).first()

    # If user was blocked, user will not access.
    if user.enable is False:
        return False

    return True


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return BlocklistModel.query.filter_by(jti_blocklist=jwt_payload["jti"]).first()


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked", "error": "token_revoked"}
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token is not fresh", "error": "fresh_token_reqired"}
        ),
        401,
    )


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    # Look in admin in database
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "Token has expired.", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def miss_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token",
                "error": "authorization_required",
            }
        ),
        401,
    )
```

## 2. Sistema de Permissões

O sistema implementa um controle de acesso baseado em papéis (RBAC - Role-Based Access Control), onde:

1. **Permissões** (`PermissionModel`): Representam ações específicas que podem ser realizadas no sistema
2. **Papéis** (`RoleModel`): Agrupam permissões relacionadas
3. **Associação Papel-Permissão** (`RolePermissionModel`): Relaciona papéis e permissões
4. **Perfis** (`ProfileModel`): Representam o contexto de acesso
