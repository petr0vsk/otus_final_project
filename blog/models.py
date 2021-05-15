from datetime import datetime

from application import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id')) # ссылка на категорию
    author_id = db.Column(db.Integer, db.ForeignKey('author.id')) # ссылка на автора поста
    title = db.Column(db.String(80)) # название
    body = db.Column(db.Text)        # текст поста 
    image = db.Column(db.String(36)) # строка с hash на картинку
    slug = db.Column(db.String(255), unique=True)  
    publish_date = db.Column(db.DateTime) # таймтстамп поста
    live = db.Column(db.Boolean)     # видимость поста--удаление поста

    author = db.relationship('Author',
        backref=db.backref('posts', lazy='dynamic'))

    category = db.relationship('Category',
        backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, author, title, body, category=None, image=None,
        slug=None, publish_date=None, live=True):
        self.author_id = author.id
        self.title = title
        self.body = body
        self.image = image
        if category:
            self.category_id = category.id
        self.image = image
        self.slug = slug
        if publish_date is None:
            self.publish_date = datetime.utcnow()
        self.live = live

    def __repr__(self):
        return '<Post %r>' % self.title

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name        