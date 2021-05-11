from flask_wtf import FlaskForm
from wtforms import validators, StringField, TextAreaField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from blog.models import Category

def categories():
    return Category.query

class PostForm(FlaskForm):
    #----- пока не понятно как и откуда подгружать картинку  в html---
    #image = FileField('Image', validators=[
    #    FileAllowed(['jpg', 'png'], 'We only accept JPG or PNG images')
    #])
    #------------- расскоментировать после решения  ----------------------------
    title = StringField('Название', [
            validators.InputRequired(),
            validators.Length(max=80)
        ])
    body = TextAreaField('Сообщение', validators=[validators.InputRequired()])
    category = QuerySelectField('Категория', query_factory=categories,
        allow_blank=True)
    new_category = StringField('Новая категория')