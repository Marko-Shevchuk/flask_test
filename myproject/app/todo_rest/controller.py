from flask import jsonify, make_response, abort, request

from app import db
from app.domain.Todo import Task, Status
from app.jwt_utils import JWTUtils
from . import todo_rest_bp


@todo_rest_bp.errorhandler(404)
@JWTUtils.verify_token
def not_found(error):
    message = error.description['message'] or 'Could not find resource.'
    return make_response(jsonify({'error': message})), 404


@todo_rest_bp.route('/<int:id>', methods=['GET'])
@JWTUtils.verify_token
def get_task(id=None):
    task = Task.query.get(id)
    if not task:
        abort(404, {'message': f"Undefined Task {id}."})
    return jsonify(task.to_dict()), 200


@todo_rest_bp.route("/", methods=['GET'])
@todo_rest_bp.route("/list", methods=['GET'])
@JWTUtils.verify_token
def task_list():
    return jsonify([task.to_dict() for task in Task.query.all()]), 200

@todo_rest_bp.route("/", methods=['POST'])
@JWTUtils.verify_token
def create_task():
    json = request.json
    task_name = json['name']
    task_description = json['description']

    task = Task(name=task_name, description=task_description, status=Status.TODO)
    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201


@todo_rest_bp.route("/<int:id>", methods=['PUT'])
@JWTUtils.verify_token
def update_task(id=None):
    json = request.json

    task: Task = Task.query.get(id)
    if not task:
        abort(404, {'message': f"Undefined Task  {id}."})

    task_name = json['name']

    existing_task = Task.query.filter(Task.name == task_name).first()
    if existing_task is not None and existing_task.id != task.id:
        abort(400)

    task_description = json['description']
    task_status = Status[json['status']]

    task.name = task_name
    task.description = task_description
    task.status = task_status

    db.session.commit()
    return jsonify(task.to_dict()), 200


@todo_rest_bp.route('/<int:id>', methods=['DELETE'])
@JWTUtils.verify_token
def delete_task(id=None):
    task: Task = Task.query.get(id)
    if not task:
        abort(404, {'message': f"Undefined Task  {id}."})

    db.session.delete(task)
    db.session.commit()
    return jsonify({}), 200