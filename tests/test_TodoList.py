import pytest
from brownie import accounts, TodoList


@pytest.fixture
def todo_list():
    return TodoList.deploy({"from": accounts[0]})


def test_add_task(todo_list):
    user = accounts[1]
    tx = todo_list.addTask("My first task", {"from": user})
    task = todo_list.getTask(1, {"from": user})

    assert task[0] == 1
    assert task[1] == "My first task"
    assert task[2] is False

    # check event
    assert "TaskCreated" in tx.events
    assert tx.events["TaskCreated"]["user"] == user
    assert tx.events["TaskCreated"]["id"] == 1


def test_toggle_task(todo_list):
    user = accounts[1]
    todo_list.addTask("Toggle test", {"from": user})

    tx = todo_list.toggleCompletion(1, {"from": user})
    task = todo_list.getTask(1, {"from": user})

    assert task[2] is True
    assert "TaskCompleted" in tx.events
    assert tx.events["TaskCompleted"]["completed"] is True

    # toggle back
    todo_list.toggleCompletion(1, {"from": user})
    task = todo_list.getTask(1, {"from": user})
    assert task[2] is False


def test_delete_task(todo_list):
    user = accounts[1]
    todo_list.addTask("Delete me", {"from": user})
    tx = todo_list.deleteTask(1, {"from": user})

    assert "TaskDeleted" in tx.events
    with pytest.raises(Exception):
        todo_list.getTask(1, {"from": user})


def test_multiple_users(todo_list):
    user1, user2 = accounts[1], accounts[2]

    todo_list.addTask("Task A", {"from": user1})
    todo_list.addTask("Task B", {"from": user2})

    task_user1 = todo_list.getTask(1, {"from": user1})
    task_user2 = todo_list.getTask(1, {"from": user2})

    assert task_user1[1] == "Task A"
    assert task_user2[1] == "Task B"


def test_get_all_tasks(todo_list):
    user = accounts[1]
    todo_list.addTask("Task 1", {"from": user})
    todo_list.addTask("Task 2", {"from": user})
    todo_list.addTask("Task 3", {"from": user})

    todo_list.deleteTask(2, {"from": user})

    tasks = todo_list.getAllTasks({"from": user})

    assert len(tasks) == 2
    descriptions = [t[1] for t in tasks]
    assert "Task 1" in descriptions
    assert "Task 3" in descriptions
