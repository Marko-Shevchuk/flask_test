from flask import redirect, url_for, flash, request, render_template
from flask_login import login_required
import os, datetime
from app.general.controller import menu
from app import db
from . import tag_bp
from .forms import TagForm
from app.domain.Tag import Tag


@tag_bp.route("/create", methods=['GET'])
@login_required
def create_tag():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    form = TagForm()
    return render_template('create_tag.html', form=form, data=data, menu=menu)


@tag_bp.route("/create", methods=['POST'])
@login_required
def create_tag_handle():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    form = TagForm()
    if not form.validate_on_submit():
        return render_template('create_tag.html', form=form, data=data, menu=menu)

    name = form.name.data

    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()

    flash(f"Successfully created tag {name}.", category='success')
    return redirect(url_for('post.tag.tag_list'))


@tag_bp.route("/<int:id>/update", methods=['GET'])
@login_required
def update_tag(id=None):
    data = [os.name, datetime.datetime.now(), request.user_agent]
    if id is None:
        return redirect(url_for('post.tag.tag_list'))

    tag = Tag.query.get_or_404(id)
    form = TagForm(tag.id)
    form.process()

    return render_template('update_tag.html', form=form, tag=tag, data=data, menu=menu)


@tag_bp.route("/<int:id>/update", methods=['POST'])
@login_required
def update_tag_handle(id=None):
    data = [os.name, datetime.datetime.now(), request.user_agent]
    if id is None:
        return redirect(url_for('post.tag.tag_list'))

    tag = Tag.query.get_or_404(id)
    form = TagForm(id)
    if not form.validate_on_submit():
        return render_template('update_tag.html', form=form, tag=tag, data=data, menu=menu)

    name = form.name.data
    tag.name = name


    db.session.commit()
    flash("You successfully updated your Tag!", category="success")
    return redirect(url_for('post.tag.tag_list'))


@tag_bp.route('/list', methods=['GET'])
@login_required
def tag_list():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags, data=data, menu=menu)


@tag_bp.route('/<int:id>/delete')
@login_required
def delete_tag(id=None):
    if id is None:
        return redirect(url_for('post.tag.tag_list'))

    tags = Tag.query.get_or_404(id)
    db.session.delete(tags)
    db.session.commit()
    flash('Successfully deleted tag.', category='success')

    return redirect(url_for('post.tag.tag_list'))