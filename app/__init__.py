from flask import Flask
from config import Config
from app.routes import funds_bp
from app.dao import create_table
from app.docs import swagger_ui_blueprint, SWAGGER_URL
from app.extensions import db
from flask_migrate import Migrate


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configs
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.update(test_config)
    
    # Initialize db and migration engine
    db.init_app(app)
    Migrate(app, db)
    
    # Register funds API
    app.register_blueprint(funds_bp)

    # Register Swagger UI
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    
    return app