from datetime import datetime
from flask import Flask, jsonify, request

# Clase para registrar cada cambio realizado en una tarea
class ChangeHistory:
    def __init__(self, action, old_value, new_value, timestamp):
        self.action = action
        self.old_value = old_value
        self.new_value = new_value
        self.timestamp = timestamp

    def __str__(self):
        return f"{self.timestamp} | {self.action} | De: {self.old_value} | A: {self.new_value}"

# Clase que representa una tarea
class Task:
    def __init__(self, title, description=None, due_date=None, priority=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.history = []  # Almacenará el historial de cambios

    def update_title(self, title):
        self.add_to_history("Title", self.title, title)
        self.title = title

    def update_description(self, description):
        self.add_to_history("Description", self.description, description)
        self.description = description

    def update_due_date(self, due_date):
        self.add_to_history("Due Date", self.due_date, due_date)
        self.due_date = due_date

    def update_priority(self, priority):
        self.add_to_history("Priority", self.priority, priority)
        self.priority = priority

    def add_to_history(self, action, old_value, new_value):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(ChangeHistory(action, old_value, new_value, timestamp))

    def show_history(self):
        return [str(change) for change in self.history]

    def __str__(self):
        return f"{self.title: <20} | {self.description: <25} | {self.due_date: <10} | {self.priority: <10}"


# Clase para la gestión de tareas
class TaskList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)

    def mark_task_as_done(self, task):
        task.status = "completed"
        self.remove_task(task)

    def show_task_history(self, task):
        return task.show_history()

    def __str__(self):
        if not self.tasks:
            return "No hay tareas disponibles."
        
        header = f"{'#': <5} | {'Title': <20} | {'Description': <25} | {'Due Date': <10} | {'Priority': <10}"
        separator = "-" * len(header)
        
        task_strs = [header, separator]
        for idx, task in enumerate(self.tasks, start=1):
            task_strs.append(f"{idx: <5} | {str(task)}")
        return "\n".join(task_strs)


# Flask application
app = Flask(__name__)

# Lista global de tareas
task_list = TaskList()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = [{"title": task.title, "description": task.description, "due_date": task.due_date, "priority": task.priority} for task in task_list.tasks]
    return jsonify(tasks)

@app.route('/task', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', "")
    due_date = data.get('due_date', "")
    priority = data.get('priority', "")
    
    task = Task(title, description, due_date, priority)
    task_list.add_task(task)
    
    return jsonify({"message": "Tarea añadida correctamente."}), 201

@app.route('/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if task_id < 1 or task_id > len(task_list.tasks):
        return jsonify({"message": "Tarea no encontrada."}), 404

    task = task_list.tasks[task_id - 1]
    data = request.get_json()

    if 'title' in data:
        task.update_title(data['title'])
    if 'description' in data:
        task.update_description(data['description'])
    if 'due_date' in data:
        task.update_due_date(data['due_date'])
    if 'priority' in data:
        task.update_priority(data['priority'])

    return jsonify({"message": "Tarea actualizada correctamente."})

@app.route('/task/<int:task_id>/history', methods=['GET'])
def get_task_history(task_id):
    if task_id < 1 or task_id > len(task_list.tasks):
        return jsonify({"message": "Tarea no encontrada."}), 404

    task = task_list.tasks[task_id - 1]
    history = task.show_history()

    return jsonify(history)

@app.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id < 1 or task_id > len(task_list.tasks):
        return jsonify({"message": "Tarea no encontrada."}), 404

    task = task_list.tasks[task_id - 1]
    task_list.remove_task(task)

    return jsonify({"message": "Tarea eliminada correctamente."})

# Función para ejecutar el servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
