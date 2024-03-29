from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config import Config

db = SQLAlchemy()
mm = Marshmallow()

def create_app():
    app = Flask(__name__)
    profile = Config.get_profile()
    app.config.from_object(profile)
    app.secret_key = profile.get_secret_key()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app) #
    mm.init_app(app)
    return app

app=create_app()
Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

with app.app_context():
    from .user import user_bp
    from .cookie import cookie_bp
    from .feedback import feedback_bp
    from .todo import todo_bp
    from .general import general_bp
    from .auth import auth_bp
    from .post import post_bp
    from .todo_rest import todo_rest_bp
    from .api import api
    from app.swagger import swagger_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(cookie_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(todo_bp)
    app.register_blueprint(general_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp, url_prefix='/post')
    app.register_blueprint(todo_rest_bp, url_prefix='/api/todo')
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(swagger_bp)