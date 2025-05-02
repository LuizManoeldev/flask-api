import os
from flask import Flask

from app.db import db
from app.extentions import cors, migrate
from app.blueprint import register_routing

import manage

def create_app(settings_module):
    app = Flask(__name__)
    app.config.from_object(settings_module)

    # Extentions Init
    db.init_app(app)
    migrate.init_app(app, db)
    #jwt.init_app(app)
    cors.init_app(
        app, 
        supports_credentials=True,  
        resources={r"*": {"origins": "*"}})
    
    manage.init_app(app)

    # Log config

    # Route registration
    register_routing(app)

    return app


settings_modules = os.getenv("APP_SETTINGS_MODULE")
app = create_app(settings_modules)

