import pytest
import json
from unittest.mock import patch, mock_open
import handler as h
import todo as t

# TODO add docstrings and comments


def test_loadsave(capfd, mock_save_data):
    mock_json = json.dumps(mock_save_data)
    mock_file = mock_open(read_data=mock_json)
    with patch("builtins.open", mock_file):
        h.loadSave()
    
    assert len(h.todoList) == 2
    assert h.todoList[0].label == "Task 1: Groceries"
    assert h.todoList[1].priority == "Medium"
    out, _ = capfd.readouterr()
    assert "2 tasks loaded successfully" in out

def test_savedata(capfd):
    h.todoList.append(t.ToDo("Test 1", "01/01/1970", "None", "Test", 1))
    h.todoList.append(t.ToDo("Test 2", "01/01/1970", "None", "Test", 2))

    m = mock_open()
    with patch("builtins.open", m), patch("json.dump") as mock_dump:
        h.saveData()
    
    out, _ = capfd.readouterr()
    assert "Tasks saved successfully." in out

    expected_dict = {
        0: {'label': 'Test 1', 'dueDate': '01/01/1970', 'priority': 'None', 'category': 'Test'},
        1: {'label': 'Test 2', 'dueDate': '01/01/1970', 'priority': 'None', 'category': 'Test'}
    }
    assert mock_dump.call_args[0][0] == expected_dict

def test_createtodo(monkeypatch):
    input_values = ["Test Task", "01/01/1970", "3", "School"]
    monkeypatch.setattr("builtins.input", lambda _: input_values.pop(0))

    h.createTodo()

    assert len(h.todoList) == 1

def test_invalid_create(monkeypatch, capfd):
    input_values = ["", "Valid Label", "01/01/1970", "1", "Category"]
    monkeypatch.setattr("builtins.input", lambda _: input_values.pop(0))

    h.createTodo()
    out, _ = capfd.readouterr()

    assert "Task label cannot be empty" in out
    assert len(h.todoList) == 1
    assert h.todoList[0].label == "Valid Label"

def test_decideview_simple(monkeypatch, capfd):
    h.todoList.append(t.ToDo("Test Task", "01/01/1970", "None", "Test", 1))
    monkeypatch.setattr("builtins.input", lambda _: "0")

    h.decideView()
    out, _ = capfd.readouterr()
    assert "Task 1: Test Task" in out
    assert "Category:" not in out

def test_decideview_detailed(monkeypatch, capfd):
    h.todoList.append(t.ToDo("Test Task", "01/01/1970", "None", "Test", 1))
    monkeypatch.setattr("builtins.input", lambda _: "1")

    h.decideView()
    out, _ = capfd.readouterr()
    assert "Task 1: Test Task" in out
    assert "Category: Test" in out

def test_valid_selection(monkeypatch):
    h.todoList.append(t.ToDo("Test Task", "01/01/1970", "None", "Test", 1))
    monkeypatch.setattr("builtins.input", lambda _: "1")

    result = h.selectTodo()
    assert result == 1

def test_invalid_selection(monkeypatch, capfd):
    h.todoList.append(t.ToDo("Test Task", "01/01/1970", "None", "Test", 1))
    input_values = ["47", "0"]
    monkeypatch.setattr("builtins.input", lambda _: input_values.pop(0))

    result = h.selectTodo()
    out, _ = capfd.readouterr()
    assert "Invalid task number" in out
    assert result == 0

def test_delete_todo(monkeypatch, capfd):
    task1 = t.ToDo("Test Task 1", "01/01/1970", "None", "Test", 1)
    task2 = t.ToDo("Test Task 2", "01/01/1970", "None", "Test", 2)
    task3 = t.ToDo("Test Task 3", "01/01/1970", "None", "Test", 3)
    h.todoList.extend([task1, task2, task3])

    inputValues = ["2"]
    monkeypatch.setattr("builtins.input", lambda _: inputValues.pop(0))

    initialLength = len(h.todoList)

    h.deleteTodo(h.selectTodo())
    out, _ = capfd.readouterr()
    # list length decreased
    assert len(h.todoList) == initialLength - 1

    # correct task deleted
    assert "Task 2: Test Task 2 deleted successfully" in out

    # remaining tasks correct
    assert h.todoList[0].label == "Test Task 1"
    assert h.todoList[1].label == "Test Task 3"

    # remaining tasks re-indexed
    assert h.todoList[0].idNum == 1
    assert h.todoList[1].idNum == 2



# TODO tests for editing