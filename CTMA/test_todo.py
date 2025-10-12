import pytest
from unittest.mock import patch, mock_open
import todo as t
import constants as c

def test_todo_initialization():
    """
    Tests that attributes are correctly set for a new task.
    """
    task = t.ToDo("Test Label", "01/01/1970", "Medium", "Dev", 99)
    assert task.label == "Test Label"
    assert task.priority == "Medium"
    assert task.idNum == 99
    assert task.complete is False
    assert task.status == "Ongoing"

def test_todo_str_method():
    """
    Tests that Task object formats to string correctly.
    """
    task = t.ToDo("Test Str", "01/01/1970", "Low", "Test", 1)
    expected_output = [
        "Task 1: Test Str", "Category: Test", "Status: Ongoing", "Due: 01/01/1970", "Priority: Low"
    ]
    task_str = str(task)
    for part in expected_output:
        assert part in task_str
    
def test_todo_printlabel(capfd):
    """
    Tests that simple label format prints correctly.
    """
    task = t.ToDo("Test Simple", "01/01/1970", "High", "Test", 5)
    task.printLabel()
    out, err = capfd.readouterr()
    assert out.strip() == "Task 5: Test Simple"

def test_todo_edit_label(capfd):
    """
    Tests that label is changed correctly with a confirmation message.
    """
    task = t.ToDo("Old Label", "01/01/1970", "None", "Test", 1)
    task.editLabel("New Task Name")
    out, err = capfd.readouterr()
    assert task.label == "New Task Name"
    assert "Label saved as New Task Name" in out

def test_todo_edit_priority(capfd):
    """
    Tests that priority is changed correctly with a confirmation message.
    """
    task = t.ToDo("Test Task", "01/01/1970", "None", "Test", 1)
    task.editPriority("2")
    out, err = capfd.readouterr()
    assert task.priority == "Low"
    assert "Priority set to Low" in out

def test_toggle_complete(capfd):
    """
    Tests that tasks can be marked as complete with a confirmation message.
    """
    task = t.ToDo("Test Task", "01/01/1970", "None", "Test", 1)
    task.toggleComplete(1)
    out, err = capfd.readouterr()
    assert task.complete is True
    assert task.status == "Complete"
    assert "Test Task marked as complete." in out

def test_toggle_ongoing(capfd):
    """
    Tests that tasks can be changed back to "Ongoing" after being completed
    with a confirmation message.
    """
    task = t.ToDo("Test Task", "01/01/1970", "None", "Test", 1)
    task.complete = True
    task.status = "Complete"
    task.toggleComplete(2)
    out, err = capfd.readouterr()
    assert task.complete is False
    assert task.status == "Ongoing"
    assert "Test Task marked as ongoing." in out

