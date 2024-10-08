import os
from flask import Flask, request
from flask_smorest import Api

from db import db
import models

from resources.product import blp as ProductBlueprint
from resources.news import blp as NewsBlueprint

def create_app(db_url=None):
    app = Flask(__name__)

    @app.route('/hello')
    def hello_world():
        return 'Hello, World!'


    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Product News REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = '3.0.3'
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPEN_SWAGGER_UI_URL"] = "https://cdn.jsdelvr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)

    api = Api(app)
    
    with app.app_context():
        db.create_all()
    
    api.register_blueprint(ProductBlueprint)
    api.register_blueprint(NewsBlueprint)


    if __name__ == '__main__':
        print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
        app.run(debug=True)
        
    return app