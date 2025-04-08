import requests

BASE_URL = "http://127.0.0.1:5000"

#UNITARIAS

def test_update_task_title_and_history():
    task = {
        "title": "Tarea inicial",
        "description": "Desc",
        "due_date": "2025-04-07",
        "priority": "Alta"
    }
    post = requests.post(f"{BASE_URL}/task", json=task)
    assert post.status_code == 201

    update = {"title": "Tarea actualizada"}
    put = requests.put(f"{BASE_URL}/task/1", json=update)
    assert put.status_code == 200

    get = requests.get(f"{BASE_URL}/tasks")
    assert get.status_code == 200
    assert get.json()[0]["title"] == "Tarea actualizada"

    history = requests.get(f"{BASE_URL}/task/1/history")
    assert history.status_code == 200
    assert any("Title" in h for h in history.json())

def test_add_and_remove_task():
    task = {
        "title": "Para eliminar",
        "description": "Borrar",
        "due_date": "2025-04-07",
        "priority": "Media"
    }
    post = requests.post(f"{BASE_URL}/task", json=task)
    assert post.status_code == 201

    delete = requests.delete(f"{BASE_URL}/task/2")
    assert delete.status_code == 200

    get = requests.get(f"{BASE_URL}/tasks")
    tasks = get.json()
    titles = [t["title"] for t in tasks]
    assert "Para eliminar" not in titles
