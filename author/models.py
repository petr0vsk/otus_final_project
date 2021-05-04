from application import db

#класс автор поста

class Author(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True) # будем счтитать уникальным ключом e-mail автора
    password = db.Column(db.String(128))

    def __init__(self, full_name, email, password):
        self.full_name = full_name
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<Author {self.full_name}>'    

