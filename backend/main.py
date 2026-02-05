from flask import Flask
from database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    with app.app_context():
        import models
        db.create_all()

    return app

app = create_app()

