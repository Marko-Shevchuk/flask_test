from flask import redirect, url_for, flash, render_template, request
from flask_login import login_required
import os, datetime
from app.general.controller import menu
from app import db
from . import category_bp
from .forms import CategoryForm
from app.domain.Category import Category


@category_bp.route("/create", methods=['GET'])
@login_required
def create_category():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    form = CategoryForm()
    return render_template('create_category.html', form=form, data=data, menu=menu)


@category_bp.route("/create", methods=['POST'])
@login_required
def create_category_handle():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    form = CategoryForm()
    if not form.validate_on_submit():
        return render_template('create_category.html', form=form, data=data, menu=menu)

    name = form.name.data
    category = Category(name=name)

    db.session.add(category)
    db.session.commit()

    flash(f"Successfully created category {name}.", category='success')
    return redirect(url_for('post.category.category_list'))


@category_bp.route("/<int:id>/update", methods=['GET'])
@login_required
def update_category(id=None):
    data = [os.name, datetime.datetime.now(), request.user_agent]
    if id is None:
        return redirect(url_for('post.category.category_list'))

    category = Category.query.get_or_404(id)
    form = CategoryForm(category.id)
    form.name.data = category.name

    return render_template('update_category.html', form=form, category=category, data=data, menu=menu)


@category_bp.route("/<int:id>/update", methods=['POST'])
@login_required
def update_category_handle(id=None):
    data = [os.name, datetime.datetime.now(), request.user_agent]
    if id is None:
        return redirect(url_for('post.category.category_list'))

    category = Category.query.get_or_404(id)
    form = CategoryForm(id)
    if not form.validate_on_submit():
        return render_template('update_category.html', form=form, category=category, data=data, menu=menu)

    name = form.name.data
    category.name = name

    db.session.commit()
    flash("Successfully updated category.", category="success")
    return redirect(url_for('post.category.category_list'))


@category_bp.route('/list', methods=['GET'])
@login_required
def category_list():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    categories = Category.query.all()
    return render_template('categories.html', categories=categories, data=data, menu=menu)


@category_bp.route('/<int:id>/delete')
@login_required
def delete_category(id=None):
    if id is None:
        return redirect(url_for('post.category.category_list'))

    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Successfully deleted category.', category='success')

    return redirect(url_for('post.category.category_list'))