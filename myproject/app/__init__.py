from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#postgres://base_demo_user:XJXY08jGxhJ94h6aYn4ohZL5u1xpslTW@dpg-cmk9g2q1hbls739udos0-a.frankfurt-postgres.render.com/base_demo

def create_app():
    app = Flask(__name__)
    app.secret_key = "pleasedosha512fiwkeokweowoefkm3r8j"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://base_demo_user:XJXY08jGxhJ94h6aYn4ohZL5u1xpslTW@dpg-cmk9g2q1hbls739udos0-a.frankfurt-postgres.render.com/base_demo'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

app=create_app()
Migrate(app, db)


from app import views
