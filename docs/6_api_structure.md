# Smart Access API - Estrutura da API

## 1. Blueprints e Rotas

A API é organizada em blueprints, que são registrados centralmente em `app/blueprint.py`:

```python
def register_routing(app):
    api = Api(app)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(TokenBlueprint)
    api.register_blueprint(UserGroupBlueprint)
    api.register_blueprint(RoleBlueprint)
    api.register_blueprint(PermissionBlueprint)
    api.register_blueprint(UserRoleBlueprint)
    api.register_blueprint(RolePermissionBlueprint)
    api.register_blueprint(ProfileBlueprint)
    api.register_blueprint(UserUserGroupBlueprint)
    api.register_blueprint(DeviceBlueprint)
    api.register_blueprint(DeviceTypeBlueprint)
```

Cada blueprint representa um recurso da API e é definido em um arquivo separado na pasta `app/routers/`.

### Exemplo de Blueprint

O blueprint para gerenciamento de usuários é definido em `app/routers/user/user_router.py`:

```python
blp = Blueprint("User", __name__, description="User management operations")


@blp.route("/user")
class UserList(MethodView):
    #@jwt_required()
    #@permission_required("read_user")
    @blp.arguments(UserQueryArgsSchema, location="query")
    @blp.response(200, UserPageSchema, description="Paginated list of users")
    def get(self, query_args):
        """Retrieve a paginated list of users"""
        username = query_args.get("username")
        page = query_args.get("page", 1)
        limit = query_args.get("limit", 10)
        offset = (page - 1) * limit

        users, total_users = user_service.get_valid_users(limit, offset, username)
        total_pages = (total_users + limit - 1) // limit

        return {
            "page": page,
            "limit": limit,
            "totalItems": total_users,
            "totalPages": total_pages,
            "data": users,
        }
```

## 2. Schemas

Os schemas são definidos na pasta `app/schemas/` e são utilizados para validar e serializar/deserializar dados. Eles são implementados usando a biblioteca Marshmallow.

### Exemplo de Schema

Exemplo de schema em `app/schemas/user/user_schema.py`:

```python
class PlainUserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True, dump_only=True)
    password = fields.Str(required=True, dump_only=True)
    cpf = fields.Str(dump_only=True)
    face_picture = fields.Raw(dump_only=True, allow_none=True)
    document_picture = fields.Raw(dump_only=True, allow_none=True)
    phone = fields.Str(dump_only=True)
    reason = fields.Str(dump_only=True, allow_none=True)
    description = fields.Str(dump_only=True, allow_none=True)
    console = fields.Bool(dump_only=True)
    enable = fields.Bool(dump_only=True)
    profiles = fields.Method("get_active_profiles", dump_only=True)
    tokens = fields.Nested(PlainTokenSchema, many=True, dump_only=True)
```

## 3. Serviços

Os serviços são definidos na pasta `app/services/` e implementam a lógica de negócio da aplicação. Eles são responsáveis por orquestrar as operações entre diferentes componentes.

### Exemplo de Serviço

Exemplo de serviço em `app/services/user/user_service.py`:
