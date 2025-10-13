"""
test_handler.py defines the logic of functionality testing

Functions:
    test_loadsave(capfd, mock_save_data): tests loading a save
    test_savedata(capfd): tests saving data
    test_createtodo(monkeypatch): tests creating todo item via CLI
    test_invalid_create(monkeypatch, capfd): tests output when input is invalid
    test_decideview_simple(monkeypatch, capfd): tests selecting simple view
    test_decideview_detailed(monkeypatch, capfd): tests selected detailed view
    test_valid_selection(monkeypatch): tests making a valid selection
    test_invalid_selection(monkeypatch, capfd): tests making an invalid selection
    def test_delete_todo(monkeypatch, capfd): test deleting a todo
"""
import pytest
import json
from unittest.mock import patch, mock_open
import todo_handler as th
import todo as t
import shared as s
import cli

# TODO add docstrings and comments


def test_loadsave(capfd, mock_save_data):
    """Tests that loading save data works properly"""
    mock_json = json.dumps(mock_save_data)
    mock_file = mock_open(read_data=mock_json)
    with patch("builtins.open", mock_file):
        th.loadSave()
    
    assert len(s.todoList) == 2
    assert s.todoList[0].label == "Task 1: Groceries"
    assert s.todoList[1].priority == "Medium"
    out, _ = capfd.readouterr()
    assert "2 tasks loaded successfully" in out

def test_savedata(capfd):
    """Tests saving data"""
    s.todoList.append(t.ToDo("Test 1", "01/01/1970", "None", "Test", 1))
    s.todoList.append(t.ToDo("Test 2", "01/01/1970", "None", "Test", 2))

    m = mock_open()
    with patch("builtins.open", m), patch("json.dump") as mock_dump:
        th.saveData()
    
    out, _ = capfd.readouterr()
    assert "Tasks saved successfully." in out

    expected_dict = {
        0: {'label': 'Test 1', 'dueDate': '01/01/1970', 'priority': 'None', 'category': 'Test'},
        1: {'label': 'Test 2', 'dueDate': '01/01/1970', 'priority': 'None', 'category': 'Test'}
    }
    assert mock_dump.call_args[0][0] == expected_dict

def test_createtodo(monkeypatch):
    """tests creating todo item via CLI"""
    input_values = ["Test Task", "01/01/1970", "3", "School"]
    monkeypatch.setattr("builtins.input", lambda _: input_values.pop(0))

    cli.createTodo()

    assert len(s.todoList) == 1

def test_invalid_create(monkeypatch, capfd):
    """tests output when input is invalid"""
    input_values = ["", "Valid Label", "01/01/1970", "1", "Category"]
    monkeypatch.setattr("builtins.input", lambda _: input_values.pop(0))

    cli.createTodo()
    out, _ = capfd.readouterr()

    assert "Task label cannot be empty" in out
    assert len(s.todoList) == 1
    assert s.todoList[0].label == "Valid Label"

def test_decideview_simple(monkeypatch, capfd):
    """tests selecting simple view"""
    s.todoList.append(t.ToDo("Test Task", "01/01/1970", "None", "Test", 1))
    monkeypatch.setattr("builtins.input", lambda _: "0")

    cli.decideView()
    out, _ = capfd.readouterr()
    assert "Task 1: Test Task" in out
    assert "Category:" not in out

def test_decideview_detailed(monkeypatch, capfd):
    """tests selected detailed view"""
    s.todoList.append(t.ToDo("Test Task", "01/01/1970", "None", "Test", 1))
    monkeypatch.setattr("builtins.input", lambda _: "1")

    cli.decideView()
    out, _ = capfd.readouterr()
    assert "Task 1: Test Task" in out
    assert "Category: Test" in out

def test_valid_selection(monkeypatch):
    """tests making a valid selection"""
    s.todoList.append(t.ToDo("Test Task", "01/01/1970", "None", "Test", 1))
    monkeypatch.setattr("builtins.input", lambda _: "1")

    result = cli.selectTodo()
    assert result == 1

def test_invalid_selection(monkeypatch, capfd):
    """tests making an invalid selection"""
    s.todoList.append(t.ToDo("Test Task", "01/01/1970", "None", "Test", 1))
    input_values = ["47", "0"]
    monkeypatch.setattr("builtins.input", lambda _: input_values.pop(0))

    result = cli.selectTodo()
    out, _ = capfd.readouterr()
    assert "Invalid task number" in out
    assert result == 0

def test_delete_todo(monkeypatch, capfd):
    """Tests deleting a todo"""
    task1 = t.ToDo("Test Task 1", "01/01/1970", "None", "Test", 1)
    task2 = t.ToDo("Test Task 2", "01/01/1970", "None", "Test", 2)
    task3 = t.ToDo("Test Task 3", "01/01/1970", "None", "Test", 3)
    s.todoList.extend([task1, task2, task3])

    inputValues = ["2"]
    monkeypatch.setattr("builtins.input", lambda _: inputValues.pop(0))

    initialLength = len(s.todoList)

    cli.deleteTodo(cli.selectTodo())
    out, _ = capfd.readouterr()
    # list length decreased
    assert len(s.todoList) == initialLength - 1

    # correct task deleted
    assert "Task 2: Test Task 2 deleted successfully" in out

    # remaining tasks correct
    assert s.todoList[0].label == "Test Task 1"
    assert s.todoList[1].label == "Test Task 3"

    # remaining tasks re-indexed
    assert s.todoList[0].idNum == 1
    assert s.todoList[1].idNum == 2


# TODO tests for editing