# Smart Access API - Documentação Técnica

## 1. Visão Geral do Projeto

O Smart Access API é uma aplicação backend desenvolvida em Flask que gerencia o controle de acesso inteligente para dispositivos físicos como fechaduras e catracas. A API fornece uma interface robusta para gerenciamento de usuários, perfis, permissões, grupos e dispositivos, permitindo um controle granular sobre quem pode acessar determinados recursos.

### Escopo do Projeto

O sistema foi projetado para:
- Gerenciar usuários e seus perfis de acesso
- Controlar permissões através de um sistema de roles (papéis)
- Agrupar usuários em grupos para facilitar a administração
- Gerenciar dispositivos físicos de controle de acesso
- Fornecer autenticação segura via JWT (JSON Web Tokens)
- Registrar e validar diferentes tipos de tokens de acesso (RFID, biometria, reconhecimento facial)

## 2. Arquitetura do Sistema

O Smart Access API segue uma arquitetura em camadas bem definida, separando claramente as responsabilidades:

### Camadas da Aplicação

1. **Routers (Controllers)**: Gerenciam as requisições HTTP e respostas, definindo os endpoints da API.
2. **Services**: Implementam a lógica de negócio, orquestrando as operações entre diferentes componentes.
3. **Models**: Definem a estrutura dos dados e interagem com o banco de dados.
4. **Schemas**: Validam e serializam/deserializam dados de entrada e saída.
5. **Utils**: Fornecem funcionalidades auxiliares como autenticação, logging e decoradores.

### Padrão de Design

A aplicação utiliza o padrão MVC (Model-View-Controller) adaptado para APIs:
- **Model**: Representado pelos arquivos em `app/models/`
- **View**: Representado pelos schemas em `app/schemas/` que formatam as respostas
- **Controller**: Representado pelos routers em `app/routers/`

Além disso, a aplicação implementa o padrão de Service Layer, onde a lógica de negócio é encapsulada em serviços específicos (`app/services/`).

## 3. Tecnologias e Bibliotecas Principais

### Framework Web
- **Flask**: Framework web leve e flexível para Python
- **Flask-Smorest**: Extensão para criar APIs RESTful com documentação automática via OpenAPI

### ORM e Banco de Dados
- **SQLAlchemy**: ORM (Object-Relational Mapping) para interação com o banco de dados
- **Flask-SQLAlchemy**: Integração do SQLAlchemy com Flask
- **PostgreSQL**: Sistema de gerenciamento de banco de dados relacional

### Autenticação e Segurança
- **Flask-JWT-Extended**: Gerenciamento de JSON Web Tokens para autenticação
- **Passlib**: Biblioteca para hash de senhas (usando pbkdf2_sha256)

### Validação e Serialização
- **Marshmallow**: Biblioteca para validação, serialização e desserialização de dados

### Outros
- **Flask-Migrate**: Gerenciamento de migrações de banco de dados
- **Flask-CORS**: Suporte a Cross-Origin Resource Sharing
- **Gunicorn**: Servidor WSGI HTTP para Python
- **Docker**: Containerização da aplicação
