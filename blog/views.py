from flask import Blueprint, render_template, session, flash, redirect, url_for, request, redirect
from slugify import slugify
import uuid
import os
from PIL import Image

from application import db
from blog.models import Post, Category
from blog.forms import PostForm
from author.models import Author
from author.decorators import login_required
from settings import BLOG_POST_IMAGES_PATH


blog_app = Blueprint('blog_app', __name__)

POSTS_PER_PAGE = 3 # 3 - для наглядности

@blog_app.route('/')
def index():
    page = int(request.values.get('page', '1'))
    posts = Post.query.filter_by(live=True).order_by(Post.publish_date.desc())\
        .paginate(page, POSTS_PER_PAGE, False) # выведем посты в порядке поступления c пагинатором
    return render_template('blog/index.html', posts=posts )


@blog_app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()

    if form.validate_on_submit():
        image_id = None

        # картинка
        if form.image.data:
            f = form.image.data
            image_id = str(uuid.uuid4())
            file_name = image_id + '.png'
            file_path = os.path.join(
                BLOG_POST_IMAGES_PATH, file_name
            )
            Image.open(f).save(file_path)
            # приведем изображение к рамзеру 600 на 300 pix
            _image_resize(BLOG_POST_IMAGES_PATH, image_id, 600, 'lg')
            _image_resize(BLOG_POST_IMAGES_PATH, image_id, 300, 'sm')
        # проверка есть ли искомая категория поста
        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush() #
            category = new_category
        else:
            category = form.category.data
 
        author = Author.query.get(session['id'])
        title = form.title.data.strip()
        body = form.body.data.strip()
        post = Post(
            author=author,
            title=title,
            body=body,
            image = image_id,
            category=category,
        )

        db.session.add(post)
        db.session.commit()

        slug = slugify(str(post.id) + '-' + post.title)
        post.slug = slug
        db.session.commit()

        flash('Article posted')
        return redirect(url_for('.article', slug=slug))

    return render_template('blog/post.html', form=form, action="new")#action for editing    

@blog_app.route('/posts/<slug>')
def article(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('blog/article.html', post=post)

@blog_app.route('/edit/<slug>', methods=('GET', 'POST'))
@login_required
def edit(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    form = PostForm(obj=post)

    return render_template('blog/post.html',
        form=form,
        post=post,
        action="edit"
    )


# -------------------------------------------------------
# сожмем картинку
def _image_resize(original_file_path,image_id, image_base, extension):
    file_path = os.path.join(
        original_file_path, image_id + '.png'
    )
    image = Image.open(file_path)
    wpercent = (image_base / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((image_base, hsize), Image.ANTIALIAS)
    modified_file_path = os.path.join(
        original_file_path, image_id + '.' + extension + '.png'
    )
    image.save(modified_file_path)
    return    