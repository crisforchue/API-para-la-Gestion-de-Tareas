import requests

BASE_URL = "http://127.0.0.1:5000"

#FUNCIONALES

def test_create_task_api():
    task = {
        "title": "Funcional 1",
        "description": "Test POST",
        "due_date": "2025-04-07",
        "priority": "Alta"
    }
    res = requests.post(f"{BASE_URL}/task", json=task)
    assert res.status_code == 201
    assert "Tarea añadida correctamente" in res.json()["message"]

def test_get_tasks_api():
    task = {
        "title": "Funcional 2",
        "description": "Otra tarea",
        "due_date": "2025-04-07",
        "priority": "Baja"
    }
    requests.post(f"{BASE_URL}/task", json=task)

    res = requests.get(f"{BASE_URL}/tasks")
    assert res.status_code == 200
    tareas = res.json()
    assert len(tareas) > 0
    assert any(t["title"] == "Funcional 2" for t in tareas)
