from flask import redirect, url_for, flash, request, render_template, current_app
from flask_login import current_user, login_required
from sqlalchemy import desc
import os, datetime
from app.general.controller import menu
from app import db

from app.auth.controller import upload_file, delete_file
from app.domain.Post import Post, PostType
from . import post_bp
from .forms import PostForm, CategorySearchForm
from ..domain.Tag import Tag


@post_bp.route("/create", methods=['GET'])
@login_required
def create_post():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    form = PostForm()
    return render_template('create_post.html', form=form, data=data, menu=menu)


@post_bp.route("/create", methods=['POST'])
@login_required
def create_post_handle():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    form = PostForm()
    if not form.validate_on_submit():
        return render_template('create_post.html', form=form, data=data, menu=menu)

    title = form.title.data
    text = form.text.data
    enabled = form.enabled.data
    post_type = form.type.data
    category_id = form.categories.data
    tags = [tag for tag in Tag.query.filter(Tag.name.in_(form.tags.data)).all()]

    post = Post(title=title, text=text, enabled=enabled, type=post_type, user_id=current_user.id,
                category_id=category_id, tags=tags)

    image = upload_file(form.image.data)
    if image:
        post.image = image

    db.session.add(post)
    db.session.commit()

    flash("Successfully created post", category='success')
    return redirect(url_for('post.post_list'))


@post_bp.route("/<int:id>/update", methods=['GET'])
@login_required
def update_post(id=None):
    data = [os.name, datetime.datetime.now(), request.user_agent]
    if id is None:
        return redirect(url_for('post.post_list'))

    post = Post.query.get_or_404(id)
    form = PostForm()
    form.text.default = post.text
    form.type.default = post.type.name
    form.categories.default = post.category_id
    form.tags.default = [tag.name for tag in post.tags]
    form.process()

    return render_template('update_post.html', form=form, post=post, data=data, menu=menu)


@post_bp.route("/<int:id>/update", methods=['POST'])
@login_required
def update_post_handle(id=None):
    data = [os.name, datetime.datetime.now(), request.user_agent]
    if id is None:
        return redirect(url_for('post.post_list'))

    post = Post.query.get_or_404(id)
    form = PostForm()
    if not form.validate_on_submit():
        return render_template('post', form=form, post=post, data=data, menu=menu)

    post.title = form.title.data
    post.text = form.text.data
    post.type = PostType[form.type.data]
    post.enabled = form.enabled.data
    post.category_id = form.categories.data
    post.tags = [tag for tag in Tag.query.filter(Tag.name.in_(form.tags.data)).all()]

    if form.image.data:
        delete_file(post.image)
        post.image = upload_file(form.image.data)

    db.session.commit()
    flash("Successfully updated post.", category="success")
    return redirect(url_for('post.post_list'))


@post_bp.route('/list', methods=['GET'])
@login_required
def post_list():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    form = CategorySearchForm(request.args, meta={'csrf': False})
    page = request.args.get('page', 1, type=int)

    query = Post.query
    if form.validate():
        category_id = form.categories.data
        query = query.filter(Post.category_id == category_id)
    else:
        form.categories.errors = []

    posts = query.order_by(desc(Post.created_at)).paginate(page=page, per_page=current_app.config['POST_PAGINATION_SIZE'])
    return render_template('posts.html', posts=posts, form=form, data=data, menu=menu)


@post_bp.route('/<int:id>', methods=['GET'])
@login_required
def get_post(id=None):
    data = [os.name, datetime.datetime.now(), request.user_agent]
    if id is None:
        return redirect(url_for('post.post_list'))

    post = Post.query.get_or_404(id)
    return render_template('post.html', post=post, data=data, menu=menu)


@post_bp.route('/<int:id>/delete')
@login_required
def delete_post(id=None):
    if id is None:
        return redirect(url_for('post.post_list'))

    post = Post.query.get_or_404(id)
    if post.user_id == current_user.id:
        db.session.delete(post)
        db.session.commit()
        flash('Successfully deleted post.', category='success')
    else:
        flash("Cannot delete this post.", category='danger')

    return redirect(url_for('post.post_list'))