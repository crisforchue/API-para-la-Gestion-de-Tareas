import requests

BASE_URL = "http://127.0.0.1:5000"

#INTEGRACIÓN

def test_update_task_and_check_title():
    task = {
        "title": "Integración 1",
        "description": "Cambio",
        "due_date": "2025-04-07",
        "priority": "Media"
    }
    res = requests.post(f"{BASE_URL}/task", json=task)
    assert res.status_code == 201  # Verificar que la tarea fue creada correctamente

    # Obtener el ID de la tarea recién creada
    task_id = len(requests.get(f"{BASE_URL}/tasks").json())

    update = {"title": "Integración 1 editada"}
    res = requests.put(f"{BASE_URL}/task/{task_id}", json=update)
    assert res.status_code == 200

    res = requests.get(f"{BASE_URL}/tasks")
    assert any(t["title"] == "Integración 1 editada" for t in res.json())

def test_task_change_reflected_in_history():
    task = {
        "title": "Historial Test",
        "description": "Ver historial",
        "due_date": "2025-04-07",
        "priority": "Alta"
    }
    res = requests.post(f"{BASE_URL}/task", json=task)
    assert res.status_code == 201  # Verifica que la tarea se haya creado

    # Obtén el ID de la tarea recién creada (suponiendo que se añade al final)
    task_list = requests.get(f"{BASE_URL}/tasks").json()
    task_id = len(task_list)  # Suponiendo que el ID es el último en la lista

    # Actualiza el título de la tarea
    update = {"title": "Historial Actualizado"}
    res = requests.put(f"{BASE_URL}/task/{task_id}", json=update)
    assert res.status_code == 200  # Verifica que la tarea se haya actualizado correctamente

    # Obtén el historial de la tarea
    res = requests.get(f"{BASE_URL}/task/{task_id}/history")
    history = res.json()

    print("Historial recibido:", history)  # Imprime el historial para ver su estructura

    # Verifica que el historial contenga el cambio correcto
    assert len(history) > 0

    # Como el historial es una lista de cadenas, desglosamos la cadena para obtener los valores
    assert any(
        "Title" in h and "De: Historial Test" in h and "A: Historial Actualizado" in h
        for h in history
    )

