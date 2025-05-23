# Smart Access API - Migrações e Gerenciamento de Banco de Dados

## 1. Migrações de Banco de Dados

O sistema utiliza Flask-Migrate (baseado no Alembic) para gerenciar migrações de banco de dados. As migrações permitem evoluir o esquema do banco de dados de forma controlada.

### Configuração das Migrações

As migrações são configuradas em `app/__init__.py`:

```python
from app.extention import migrate

def create_app(settings_module):
    # ...
    migrate.init_app(app, db)
    # ...
```

A extensão Flask-Migrate é definida em `app/extention.py`:

```python
from flask_migrate import Migrate

migrate = Migrate()
```

### Arquivos de Migração

Os arquivos de migração são armazenados na pasta `migrations/`:
- `migrations/env.py`: Configuração do ambiente de migração
- `migrations/alembic.ini`: Configuração do Alembic
- `migrations/versions/`: Contém os scripts de migração gerados

### Comandos de Migração

O sistema fornece comandos CLI para gerenciar o banco de dados, definidos em `manage.py`:

```python
def create_db():
    """
    Create Database.
    """
    db.create_all()
    db.session.commit()


def reset_db():
    """
    Reset Database.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


def drop_db():
    """
    Drop Database.
    """
    db.drop_all()
    db.session.commit()


def populate_db(username="root"):
    """
    Popular banco com Usuario Root e Permissoes basicas
    """
    root = UserModel.query.filter_by(username=username).first()

    if root is None:
        print("root-user is not created before!")
        init_db()
    else:
        print("root-user is created!")
```

Estes comandos são registrados na aplicação Flask em `manage.py`:

```python
def init_app(app):
    if app.config["APP_ENV"] == "production":
        commands = [create_db, reset_db, drop_db, populate_db]
    else:
        commands = [
            create_db,
            reset_db,
            drop_db,
            populate_db,
            tests,
            cov_html,
            cov,
        ]

    for command in commands:
        app.cli.add_command(app.cli.command()(command))
```

## 2. Inicialização do Banco de Dados

O sistema inclui um script `seed.py` para inicializar o banco de dados com dados básicos:

### Permissões Básicas

```python
create_user_permission = PermissionModel(name="create_user", description="Create users")
read_user_permission = PermissionModel(name="read_user", description="Read users")
delete_user_permission = PermissionModel(name="delete_user", description="Delete users")
# ... outras permissões
```

### Papéis (Roles)

```python
admin_role = RoleModel(name="Admin", description="Manage Permission")
operator_role = RoleModel(name="Operator", description="Operational Permission")
```

### Associação de Papéis e Permissões

```python
role_permission_admin1 = RolePermissionModel(role_id=1, permission_id=1)
role_permission_admin2 = RolePermissionModel(role_id=1, permission_id=2)
# ... outras associações
```

### Usuário Root

```python
root_password = pbkdf2_sha256.hash("123456789")
root_user = UserModel(username="root", 
                      password=root_password, 
                      super_user=True
