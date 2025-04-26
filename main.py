from flask import Flask, request, jsonify
from flask_cors import CORS
from mongo_manager import MongoManager  # دقت کن اسم فایلتو همینه

app = Flask(__name__)
CORS(app)


# ساخت شی از کلاس MongoManager
db = MongoManager()

# گرفتن همه تسک‌ها
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = db.get_all_tasks()
    return jsonify(tasks), 200

# ساخت تسک جدید
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    if not title or not description:
        return jsonify({'error': 'Title and description are required'}), 400
    task_id = db.create_task(title, description)
    return jsonify({'id': task_id}), 201

# گرفتن تسک خاص
@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = db.get_task_by_id(task_id)
    if task:
        return jsonify(task), 200
    else:
        return jsonify({'error': 'Task not found'}), 404

# آپدیت تسک
@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    updated = db.update_task(task_id, title, description)
    if updated:
        return jsonify({'message': 'Task updated successfully'}), 200
    else:
        return jsonify({'error': 'Task not found or nothing to update'}), 404

# حذف تسک
@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    deleted = db.delete_task(task_id)
    if deleted:
        return jsonify({'message': 'Task deleted successfully'}), 200
    else:
        return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
