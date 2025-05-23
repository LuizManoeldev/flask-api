# Smart Access API - Banco de Dados e ORM

## 1. SQLAlchemy

O SQLAlchemy é um ORM (Object-Relational Mapping) que permite trabalhar com bancos de dados relacionais usando objetos Python. No Smart Access API, o SQLAlchemy é configurado através do Flask-SQLAlchemy.

### Configuração do SQLAlchemy

A configuração do SQLAlchemy é feita no arquivo `app/db.py`, que cria uma instância do SQLAlchemy:

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

Esta instância é inicializada na função `create_app` em `app/__init__.py`:

```python
def create_app(settings_module):
    app = Flask(__name__)
    app.config.from_object(settings_module)

    # Inicializacao das extensoes
    db.init_app(app)
    # ...
```

### Principais Configurações do SQLAlchemy

No arquivo `config.py`, são definidas as seguintes configurações para o SQLAlchemy:

- **SQLALCHEMY_DATABASE_URI**: URL de conexão com o banco de dados
- **SQLALCHEMY_TRACK_MODIFICATIONS**: Desativado para melhorar o desempenho
- **SHOW_SQLALCHEMY_LOG_MESSAGES**: Controla a exibição de logs do SQLAlchemy

## 2. Modelos de Dados

Os modelos de dados são definidos na pasta `app/models/` e representam as tabelas do banco de dados. Cada modelo é uma classe Python que herda de `db.Model`.

### Estrutura dos Modelos

Os modelos são organizados em subpastas por domínio:
- `app/models/user/`: Modelos relacionados a usuários
- `app/models/auth/`: Modelos relacionados a autenticação e autorização
- `app/models/profile/`: Modelos relacionados a perfis
- `app/models/device/`: Modelos relacionados a dispositivos
- `app/models/token/`: Modelos relacionados a tokens de acesso
- `app/models/user_group/`: Modelos relacionados a grupos de usuários

### Exemplo de Modelo

O modelo `UserModel` em `app/models/user/user_model.py` define a estrutura da tabela de usuários:

```python
class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    face_picture = db.Column(db.LargeBinary, nullable=True)
    document_picture = db.Column(db.LargeBinary, nullable=True)
    phone = db.Column(db.String(11), nullable=True)
    reason = db.Column(db.String(), nullable=True)
    description = db.Column(db.String(), nullable=True)
    console = db.Column(db.Boolean, default=False, nullable=False)
    enable = db.Column(db.Boolean, default=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    super_user = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relacionamentos
    profiles = db.relationship('ProfileModel', back_populates='user', cascade="all, delete-orphan")
    tokens = db.relationship("TokenModel", back_populates="user", cascade="all, delete-orphan")
```

### Principais Modelos do Sistema

#### Modelos de Autenticação e Autorização

1. **PermissionModel**: Define permissões específicas no sistema
2. **RoleModel**: Define papéis (roles) que agrupam permissões
3. **RolePermissionModel**: Associa pap
