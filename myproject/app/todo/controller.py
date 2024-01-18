from flask import redirect, url_for, request, flash, render_template
from flask_login import login_required
import os, datetime
from app import db
from app.domain.Todo import Task, Status
from . import todo_bp
from .forms import AddTask, UpdateTask
from app.general.controller import menu

@todo_bp.route('/todo', methods=['GET'])
def todo():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    task_list = db.session.query(Task).all()
    return render_template('todo.html', tasks=task_list, data=data, menu=menu)


@todo_bp.route('/todo/add', methods=['GET', 'POST'])
@login_required
def add_task():
    data = [os.name, datetime.datetime.now(), request.user_agent]

    add_task_form = AddTask()
    if request.method == 'GET':
        return render_template('add_task.html', form=add_task_form, data=data, menu=menu)
    if add_task_form.validate_on_submit():
        task_name = add_task_form.name.data
        description = add_task_form.description.data

        existing_task = Task.query.filter(Task.name == task_name).first()
        if existing_task is not None:
            flash("There is ALREADY a task with this name.", category="danger")
            return redirect(url_for('todo.add_task'))

        task = Task(name=task_name, description=description)
        db.session.add(task)
        db.session.commit()
        flash(f"Successfully created task {task_name}", category='success')
        return redirect(url_for('todo.todo'))
    return render_template('add_task.html', form=add_task_form, data=data, menu=menu)


@todo_bp.route('/todo/<int:id>', methods=['GET'])
@login_required
def get_task(id=None):
    data = [os.name, datetime.datetime.now(), request.user_agent]
    
    if id is None:
        return redirect(url_for('todo.todo'))

    task = db.get_or_404(Task, id)
    update_form = UpdateTask()
    update_form.status.default = task.status.value
    return render_template('update_task.html', task=task, form=update_form, data=data, menu=menu)


@todo_bp.route('/todo/<int:id>', methods=['POST'])
@login_required
def update_task(id=None):
    data = [os.name, datetime.datetime.now(), request.user_agent]
    
    if id is None:
        return redirect(url_for('todo.todo'))

    task = db.get_or_404(Task, id)
    update_form = UpdateTask()
    if not update_form.validate_on_submit():
        return render_template('update_task.html', task=task, form=update_form, data=data, menu=menu)

    name = update_form.name.data
    description = update_form.description.data
    status = Status[update_form.status.data]

    existing_task = db.session.query(Task).filter(Task.name == name).first()
    if existing_task is not None and existing_task.id != task.id:
        flash("There is ALREADY a task with this name.", category="danger")
        return redirect(url_for('todo.add_task'))

    task.name = name
    task.description = description
    task.status = status
    db.session.commit()
    flash("Successfully updated task", category='success')
    return redirect(url_for('todo.todo'))


@todo_bp.route('/todo/<int:id>/delete')
@login_required
def delete_task(id=None):
    if id is None:
        return redirect(url_for('todo.todo'))

    task = db.get_or_404(Task, id)
    db.session.delete(task)
    db.session.commit()
    flash(f"Successfully deleted task {task.name}", category='success')
    return redirect(url_for('todo.todo'))

