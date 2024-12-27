from flask import Blueprint, jsonify, request
from models import Task, db

task_routes = Blueprint('task_routes', __name__)

@task_routes.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_list = [{"id": task.id, "title": task.title, "status": task.status} for task in tasks]
    return jsonify(task_list)


@task_routes.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added successfully!"}), 201


@task_routes.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.json
    task = Task.query.get_or_404(id)
    task.status = data['status']
    db.session.commit()
    return jsonify({"message": "Task updated successfully!"})


@task_routes.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully!"})
