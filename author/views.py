from flask import Blueprint, render_template, redirect, session, url_for, flash 
from werkzeug.security import generate_password_hash

from author.models import Author
from author.forms import RegisterForm, LoginForm
from application import db

author_app = Blueprint('author_app', __name__)

@author_app.route('/register', methods=['GET', 'POST']) # регистрация
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data) # сохраним пароль в хешированном виде
        author = Author(
            form.full_name.data,
            form.email.data,
            hashed_password
        )
        db.session.add(author)
        db.session.commit()
        flash('Подзравляем, Вы зарегестрировались! Можете войти на форум.')
        return redirect(url_for('author_app.login'))
    return render_template('author/register.html', form = form)
    

@author_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        #return 'Logged in'
        author = Author.query.filter_by(email = form.email.data).first()
        session['id'] = author.id
        session['full_name'] = author.full_name
        return redirect(url_for('blog_app.index')) 

    return render_template('author/login.html', form=form, error=error)      

@author_app.route('/logout')
def logout():
    session.pop('id')
    session.pop('full_name')
    flash('Вы покинули форум. До новых встречь!')
    return redirect(url_for('author_app.login'))

