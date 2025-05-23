# Smart Access API - Implantação e Containerização

## 1. Gunicorn

O sistema utiliza Gunicorn como servidor WSGI para produção. A configuração do Gunicorn é definida em `gunicorn/gunicorn_config.py`:

```python
import multiprocessing
import os

host = os.getenv("API_HOST", "0.0.0.0")
port = os.getenv("API_PORT", "5000")
bind_env = os.getenv("BIND", None)

use_bind = bind_env if bind_env else f"{host}:{port}"

workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
max_workers_str = os.getenv("MAX_WORKERS")
web_concurrency_str = os.getenv("WEB_CONCURRENCY", None)

cores = multiprocessing.cpu_count()
workers_per_core = int(workers_per_core_str)
default_web_concurrency = workers_per_core * cores + 1

if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = max(int(default_web_concurrency), 2)
    if max_workers_str:
        use_max_workers = int(max_workers_str)
        web_concurrency = min(web_concurrency, use_max_workers)

graceful_timeout_str = os.getenv("GRACEFUL_TIMEOUT", "120")
timeout_str = os.getenv("TIMEOUT", "120")
keepalive_str = os.getenv("KEEP_ALIVE", "5")
use_loglevel = os.getenv("LOG_LEVEL", "info")

# Gunicorn config variables
loglevel = use_loglevel
workers = web_concurrency
bind = use_bind
worker_tmp_dir = "/dev/shm"
graceful_timeout = int(graceful_timeout_str)
timeout = int(timeout_str)
keepalive = int(keepalive_str)
```

## 2. Docker

O sistema é containerizado usando Docker. O `Dockerfile` define como a imagem é construída:

```dockerfile
FROM python:3.10.15

WORKDIR /app

# Update the package lists and install the PostgreSQL client
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    apt clean && \
    rm -rf /var/cache/apt/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Chmod to entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
```

## 3. Script de Inicialização

O script `entrypoint.sh` é executado quando o container é iniciado:

```bash
#!/bin/sh
# 
# Autor: Luiz Dantas
# Data: 11/02/2025
# Descrição:
#     Este script de entrypoint gerencia a inicialização da aplicação, garantindo que o banco de dados esteja acessível antes da execução do servidor.
#     Ele também executa tarefas específicas de inicialização, dependendo do ambiente configurado (local ou produção).

echo "Start run entrypoint script..."  # Mensagem indicando o início da execução do script

echo "Database:" $DATABASE  # Exibe qual banco de dados está configurado

# Verifica se o banco de dados definido é PostgreSQL
if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."  

    # Loop que verifica se o Postgre
