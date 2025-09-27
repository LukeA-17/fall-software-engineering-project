import pytest
import json
import handler as h

MOCK_SAVE_DATA = {
    "0": {
        "label": "Task 1: Groceries",
        "dueDate": "2025-09-28",
        "priority": "High",
        "category": "Home"
    },
    "1": {
        "label": "Task 2: Code Test Cases",
        "dueDate": "2025-09-26",
        "priority": "Medium",
        "category": "School"
    }
}

@pytest.fixture(autouse=True)
def cleanup_handler_list():
    """
    Clears the global todoList in handler before and after each test
    to ensure clean test environment.
    """
    h.todoList.clear()
    yield
    h.todoList.clear()

@pytest.fixture
def mock_save_data():
    """
    Provides the dictionary structure used for mocking loaded data.
    """
    return MOCK_SAVE_DATA