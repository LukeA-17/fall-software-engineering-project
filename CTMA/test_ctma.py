"""
Tests the core functions of the CTMA and the ToDo objects. There are two
test cases for each CLI use case in the design document.
"""

import pytest
import json
import os
from unittest.mock import patch, MagicMock, mock_open

import todo as todo
import cli as c
import todo_handler as th
from todo import PRIORITYDICT


@pytest.fixture(autouse=True)
def cleanup_handler_list():
    """
    Clears the global todoList in handler before and after each test
    to ensure clean test environment.
    """
    th.todoList.clear()
    yield
    th.todoList.clear()


@pytest.fixture
def sample_task():
    """Helper fixture to create a standard ToDo object for core method tests."""
    # Priority key "2" maps to "Low"
    return todo.ToDo(
        "Milestone Review", "09/29/2025", PRIORITYDICT["2"], "Work", ["John", "Jane"], 1
    )


@pytest.fixture
def load_mock_tasks():
    """Loads a consistent set of 3 tasks into th.todoList for handler testing."""
    initial_data = {
        "0": {
            "label": "Group Project Milestone 03",
            "dueDate": "10/10/2025",
            "priority": "4",
            "category": "School",
            "people": ["Group A"],
        },
        "1": {
            "label": "Pack for Austin",
            "dueDate": "10/15/2025",
            "priority": "3",
            "category": "Personal",
            "people": [],
        },
        "2": {
            "label": "Write Quarterly Report",
            "dueDate": "11/20/2025",
            "priority": "4",
            "category": "Work",
            "people": ["Adam"],
        },
    }

    for id_key, data in initial_data.items():
        idNum = int(id_key) + 1
        new_task = todo.ToDo(
            data["label"],
            data["dueDate"],
            th.PRIORITYDICT[data["priority"]],
            data["category"],
            data["people"],
            idNum,
        )
        th.todoList.append(new_task)
    return th.todoList


# -----------------------------------
# Create new tasks
# -----------------------------------


def test_handler_create_task_success(load_mock_tasks):
    """
    Verifies adding a new task to todoList.

    Use Case: User creates a new task with all attributes.
    Inputs: Initial list of 3 tasks. New ToDo object added.
    Expected Output: th.todoList size increases to 4. New task has ID 4.
    """
    initial_len = len(th.todoList)
    new_task = todo.ToDo(
        "New Task", "12/01/2025", th.PRIORITYDICT["2"], "Other", [], initial_len + 1
    )
    th.todoList.append(new_task)

    assert len(th.todoList) == 4
    assert th.todoList[3].idNum == 4


def test_handler_create_task_failure_invalid_date():
    """
    Checks that creating a task with an invalid date string raises a ValueError.

    Use Case: User attempts to create a task with an invalid date format.
    Inputs: Due Date: "12-01-2025" (invalid format)
    Expected Output: ValueError is raised.
    """
    with pytest.raises(ValueError):
        todo.ToDo("Bad Date", "12-01-2025", th.PRIORITYDICT["2"], "Other", [], 1)


# -----------------------------------
# Search tasks (keyword)
# -----------------------------------


def test_search_by_keyword_success(load_mock_tasks):
    """
    Verifies the search function returns all tasks whose label or category contains the keyword.

    Use Case: User searches for a key word or phrase ("Project").
    Inputs: Tasks loaded. Search Keyword: "Project"
    Expected Output: A list containing only "Group Project Milestone 03".
    """
    found_tasks = th.search("Project")
    assert len(found_tasks) == 1
    assert found_tasks[0].label == "Group Project Milestone 03"


def test_search_by_keyword_failure_no_match(load_mock_tasks):
    """
    Verifies the search function correctly returns an empty list when no tasks match the keyword.

    Use Case: User searches for a non-existent word ("Zyxwv").
    Inputs: Tasks loaded. Search Keyword: "Zyxwv"
    Expected Output: An empty list is returned.
    """
    found_tasks = th.search("Zyxwv")
    assert len(found_tasks) == 0
    assert found_tasks == []


## -----------------------------------
## Mark Task as Complete/Incomplete
## -----------------------------------


def test_toggle_complete_success_complete(sample_task):
    """
    Verifies the task is correctly marked as complete (choice 1).

    Use Case: User selects a task and marks it as complete.
    Inputs: Initial Status: complete=False, Choice: 1
    Expected Output: complete=True, status="Complete".
    """
    sample_task.toggleComplete(1)
    assert sample_task.complete is True
    assert sample_task.status == "Complete"


def test_toggle_complete_success_incomplete(sample_task):
    """
    Verifies the task is correctly marked as incomplete (choice 2) from a completed state.

    Use Case: User selects a task and marks it as incomplete.
    Inputs: Initial Status: complete=True (after completion), Choice: 2
    Expected Output: complete=False, status="Ongoing".
    """
    # mark complete first
    sample_task.toggleComplete(1)
    # mark as ongoing
    sample_task.toggleComplete(2)
    assert sample_task.complete is False
    assert sample_task.status == "Ongoing"


# -----------------------------------
# Save and Load Data
# -----------------------------------


def test_save_data_success(load_mock_tasks, tmp_path):
    """
    Verifies th.saveData creates the correct JSON structure for tasks and settings.

    Use Case: User closes the program (saveData is triggered).
    Inputs: Mock tasks loaded. Mocks the file I/O to check the written content.
    Expected Output: The mocked file content matches the current task state dictionary.
    """
    tasks_handle_mock = mock_open().return_value
    settings_handle_mock = mock_open().return_value

    tasksPath = os.path.join("CTMA", "tasks.json")
    settingsPath = os.path.join("CTMA", "settings.json")

    def mock_open_side_effect(file_path, mode):
        if file_path == tasksPath:
            return tasks_handle_mock
        elif file_path == settingsPath:
            return settings_handle_mock
        raise FileNotFoundError(f"File not found: {file_path}")

    with patch.object(
        th, "open", MagicMock(side_effect=mock_open_side_effect)
    ) as mock_open_func:
        th.saveData()

    mock_open_func.assert_any_call(tasksPath, "w")
    mock_open_func.assert_any_call(settingsPath, "w")

    written_data_chunks = [
        call[0][0] for call in tasks_handle_mock.write.call_args_list
    ]
    written_data = "".join(written_data_chunks)

    saved_dict = json.loads(written_data)

    assert "0" in saved_dict
    assert saved_dict["0"]["label"] == "Group Project Milestone 03"
    assert saved_dict["2"]["category"] == "Work"


def test_load_data_success(tmp_path):
    """
    Verifies th.loadSave successfully restores tasks from a mocked file content.

    Use Case: User starts the program (loadSave is triggered).
    Inputs: Mocked file content with 2 tasks. Call th.loadSave().
    Expected Output: th.todoList contains the two mock tasks.
    """
    mock_task_content = json.dumps(
        {
            "0": {
                "label": "Loaded Task A",
                "dueDate": "11/20/2025",
                "priority": "High",
                "category": "Test Load",
                "complete": True,
                "status": "Complete",
            },
            "1": {
                "label": "Loaded Task B",
                "dueDate": "",
                "priority": "None",
                "category": "Test Load",
                "complete": False,
                "status": "Ongoing",
            },
        }
    )
    mock_settings_content = json.dumps({"theme": "Dark"})

    tasks_file_mock = mock_open(read_data=mock_task_content)
    settings_file_mock = mock_open(read_data=mock_settings_content)

    tasksPath = os.path.join("CTMA", "tasks.json")
    settingsPath = os.path.join("CTMA", "settings.json")

    def mock_open_side_effect(file_path, mode):
        if file_path == tasksPath:
            return tasks_file_mock()
        elif file_path == settingsPath:
            return settings_file_mock()
        raise FileNotFoundError

    with patch.object(
        th, "open", MagicMock(side_effect=mock_open_side_effect)
    ) as mock_open_func:
        th.loadSave()

    assert len(th.todoList) == 2
    assert th.todoList[0].label == "Loaded Task A"
    assert th.todoList[0].complete is True


# -----------------------------------
# Delete Task
# -----------------------------------


def test_delete_task_success_reindex(load_mock_tasks):
    """
    Verifies a task is deleted and the remaining tasks are correctly re-indexed.

    Use Case: User selects the delete task option, selects the task number to be deleted, and deletes the task.
    Inputs: Initial List: IDs 1, 2, 3. Delete ID: 1.
    Expected Output: List size is 2. Task originally at ID 2 is now at ID 1.
    """
    task_2_label = th.todoList[1].label

    c.deleteTodo(1)

    assert len(th.todoList) == 2

    assert th.todoList[0].idNum == 1
    assert th.todoList[0].label == task_2_label


def test_delete_task_failure_invalid_id(load_mock_tasks, capsys):
    """
    Verifies that deleting a non-existent ID fails gracefully and preserves the list.

    Use Case: User attempts to delete a task with a non-existent ID.
    Inputs: Initial List: IDs 1, 2, 3. Delete ID: 999.
    Expected Output: List size remains 3. Prints "Error: Task not found...".
    """
    initial_len = len(th.todoList)

    c.deleteTodo(999)
    captured = capsys.readouterr()

    assert len(th.todoList) == initial_len
    assert th.todoList[0].idNum == 1
    assert "Error: Task not found with that number." in captured.out


# -----------------------------------
# Edit Task Label
# -----------------------------------


def test_edit_label_success(sample_task):
    """
    Verifies the task's label attribute can be successfully changed.

    Use Case: User selects the edit task option, selects the task to be edited, selects the label option, and renames the task.
    Inputs: New Value: "Submit Quarterly Report"
    Expected Output: label attribute is updated to "Submit Quarterly Report".
    """
    sample_task.editLabel("Submit Quarterly Report")
    assert sample_task.label == "Submit Quarterly Report"


def test_edit_label_failure_empty_string(sample_task):
    """
    Verifies the task's label attribute cannot be changed to an empty string.

    Use Case: User attempts to clear the label.
    Inputs: New Value: ""
    Expected Output: ValueError is raised.
    """
    with pytest.raises(ValueError):
        sample_task.editLabel("")


# -----------------------------------
# Search by Priority
# -----------------------------------


def test_search_by_priority_success(load_mock_tasks):
    """
    Verifies the search function returns all tasks matching a specific priority level.

    Use Case: User selects the search option, enters "High," and is able to see all high priority tasks.
    Inputs: Search Priority: "High"
    Expected Output: A list containing two "High" priority tasks ("Group Project..." and "Write Quarterly Report").
    """
    found_tasks = th.search("High")

    assert len(found_tasks) == 2
    assert all(t.priority == "High" for t in found_tasks)


def test_search_by_priority_failure_none(load_mock_tasks):
    """
    Verifies the search function returns an empty list when searching for a priority level that has no matching tasks.

    Use Case: User searches for an unused priority ("None").
    Inputs: Search Priority: "None"
    Expected Output: An empty list is returned (since no tasks are set to None in the mock data).
    """

    found_tasks = th.search("None")

    assert len(found_tasks) == 0
    assert found_tasks == []


# -----------------------------------
# View Tasks in Detail
# -----------------------------------


def test_detailed_view_success_multiple_tasks(load_mock_tasks):
    """
    Verifies all tasks are present and accessible in the handler list.

    Use Case: User selects view task, then detailed view, and is presented with information on all existing tasks.
    Inputs: 3 mock tasks loaded.
    Expected Output: The list contains 3 tasks with correct labels and ID numbers.
    """
    assert len(th.todoList) == 3
    assert th.todoList[0].idNum == 1
    assert th.todoList[2].label == "Write Quarterly Report"

    assert "Priority: High" in str(th.todoList[0])


def test_detailed_view_success_empty_list():
    """
    Verifies the list is empty when no tasks have been created or loaded.

    Use Case: User selects view task, then detailed view in an empty list.
    Inputs: Empty handler list.
    Expected Output: List length is 0.
    """
    assert len(th.todoList) == 0


# -----------------------------------
# Edit Task Category
# -----------------------------------


def test_edit_task_category_handler_success(load_mock_tasks):
    """
    Verifies the handler function successfully updates a task's category.

    Use Case: User selects edit a task, selects the task they wish to edit, selects the category attribute, enters a new category for the task, and is presented with confirmation the category was changed.
    Inputs: Task ID: 2. New Category: "Trip Planning".
    Expected Output: Task 2's category is updated to "Trip Planning".
    """
    task_id = 2

    success = th.update_task_attributes(
        task_id,
        th.todoList[task_id - 1].label,  # Keep existing label
        "10/15/2025",
        "3",  # Keep existing priority
        "Trip Planning",
        [],
    )

    assert success is True
    assert th.todoList[1].category == "Trip Planning"


def test_edit_task_attribute_failure_invalid_id(load_mock_tasks):
    """
    Verifies an attribute update attempt on a non-existent task fails.

    Use Case: User attempts to edit a task with a non-existent ID.
    Inputs: Task ID: 999.
    Expected Output: update_task_attributes returns False.
    """
    success = th.update_task_attributes(999, "Fail", "", "1", "Fail", [])

    assert success is False
    assert len(th.todoList) == 3
