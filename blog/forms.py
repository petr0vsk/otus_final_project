from flask_wtf import FlaskForm
from wtforms import validators, StringField, TextAreaField, SelectField, FileField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileAllowed

from blog.models import Category

def categories():
    return Category.query

class PostForm(FlaskForm):
    
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'png'], 'Загружаем картинки только в JPG или PNG формате')
    ])
    
    title = StringField('Название', [
            validators.InputRequired(),
            validators.Length(max=80)
        ])
    body = TextAreaField('Сообщение', validators=[validators.InputRequired()])
    category = QuerySelectField('Категория', query_factory=categories,
        allow_blank=True)
    new_category = StringField('Новая категория')