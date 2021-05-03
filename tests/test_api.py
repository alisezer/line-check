from lc.models import Task


def test_get_all_tasks_no_data(test_client, test_db):
    response = test_client.get("/v1/tasks/")
    response.status_code == 200
    assert response.json["tasks"] == []


def test_get_all_tasks_single_task(test_client, test_db):
    lines = "victoria,bakerloo"
    status = "scheduled"
    test_task = Task(lines=lines, status=status)
    test_db.session.add(test_task)
    test_db.session.commit()

    response = test_client.get("/v1/tasks/")

    assert response.status_code == 200
    assert len(response.json["tasks"]) == 1
    assert response.json["tasks"][0]["lines"] == lines
    assert response.json["tasks"][0]["status"] == status

def test_get_all_tasks_multiple_tasks(test_client, test_db):
    lines = "victoria,bakerloo"
    status = "scheduled"
    test_task = Task(lines=lines, status=status)
    test_task_2 = Task(lines=lines, status=status)
    test_db.session.add(test_task)
    test_db.session.add(test_task_2)
    test_db.session.commit()

    response = test_client.get("/v1/tasks/")

    assert response.status_code == 200
    assert len(response.json["tasks"]) == 2


def test_get_one_task(test_client, test_db):
    lines = "victoria,bakerloo"
    status = "scheduled"
    test_task = Task(lines=lines, status=status)
    test_db.session.add(test_task)
    test_db.session.commit()

    response = test_client.get("/v1/tasks/1")

    assert response.status_code == 200
    assert response.json["id"] == 1
    assert response.json["lines"] == lines
    assert response.json["status"] == status

def test_create_task(test_client, test_db):
    lines = "victoria,bakerloo"

    response = test_client.post("/v1/tasks/", data={"lines": lines})

    assert response.status_code == 200
    assert response.json["success"] == "Task has been created"
    assert response.json["task"]["id"] == 1
    assert response.json["task"]["lines"] == lines

def test_update_task(test_client, test_db):
    lines = "victoria,bakerloo"
    status = "scheduled"
    test_task = Task(lines=lines, status=status)
    test_db.session.add(test_task)
    test_db.session.commit()

    new_line = "central"
    response = test_client.put("/v1/tasks/1", data={"lines": new_line})

    assert response.status_code == 200
    assert response.json["task"]["lines"] == new_line
