from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flaskext.markdown import Markdown



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

    # добавим возмозность использовать markdown
    Markdown(app)

    # blueprints ------
    # выделяем собственно  блог
    from blog.views import blog_app
    # выделим модуль авторизации для авторов
    from author.views import author_app


    # регистрируем blueprints
    app.register_blueprint(blog_app)
    app.register_blueprint(author_app)

    return app