from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()

def create_app(**config_overrides):
    app = Flask(__name__)

    # грузим config
    app.config.from_pyfile('settings.py')

    # конфиг для тестов
    app.config.update(config_overrides)

    # инициализируем db
    db.init_app(app)
    migrate = Migrate(app, db)

    # выделям блог в blueprints
    from blog.views import blog_app

    # регистрируем blueprints
    app.register_blueprint(blog_app)

    return app