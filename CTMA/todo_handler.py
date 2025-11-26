"""
todo_handler.py acts as the logic layer of the program
Functions:
    System:
    - loadSave(): loads save data from tasks.json and settings.json
    - saveData(): saves runtime data into tasks.json and settings.json
    - search(term): creates a list of todo items containing a certain string

    GUI Support:
    - get_tasks_for_view(view_type="All", category=None, sort_key="Priority", reverse=False):
      Filters and sorts the todoList for display
"""

import json
import os
import todo as todo
from datetime import date


#####################
# Handler Variables #
#####################
# constants
PRIORITYDICT = {"1": "None", "2": "Low", "3": "Medium", "4": "High"}

# get the absolute path of the directory this file is in
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# runtime vars
todoList = []  # stores todo objects during runtime
curTheme = "Dark"

fileDict = {"Default": os.path.join(BASE_DIR, "tasks.json")}
curFile = fileDict["Default"]

copiedTask: todo.ToDo = None


####################
# System Functions #
####################
def loadSave():
    """
    Pulls dict of todos from tasks.json, converts to list of todo objs stored in todoList.
    Also loads the user's saved settings.

    Raises:
        ValueError: If save file is corrupt, contains invalid data, OR exceeds 250 tasks.
    """
    # Load the todoList
    global todoList
    global fileDict
    global curFile

    todoList = []

    if not fileDict:
        fileDict = {"Default": os.path.join(BASE_DIR, "tasks.json")}
        curFile = fileDict["Default"]

    try:
        with open(curFile, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    except json.JSONDecodeError as e:
        raise ValueError(f"Critical Error: Corrupt save file ({curFile}). {e}")

    if len(data) > 0:
        count = 0
        for i, item in enumerate(data.values()):
            try:
                new_task = todo.ToDo(
                    item.get("label", ""),
                    item.get("dueDate"),
                    item.get("priority"),
                    item.get("category"),
                    item.get("people", []),  # Default to empty list
                    (len(todoList) + 1),
                )

                if "complete" in item and item["complete"]:
                    new_task.toggleComplete(1)

                todoList.append(new_task)
                count += 1

                if count > 250:
                    raise ValueError("Task amount exceeds allotted limit of 250")

            except (ValueError, TypeError) as e:
                # Raise error immediately to stop loading if data is bad OR limit exceeded
                raise ValueError(f"Critical Load Error in Task #{i + 1}: {e}")

    # Load data from settings
    settingsPath = os.path.join(BASE_DIR, "settings.json")
    try:
        with open(settingsPath, "r") as f:
            data = json.load(f)

        if "theme" in data:
            global curTheme
            curTheme = data["theme"]

        if "files" in data:
            fileDict.clear()
            fileDict = data["files"]

        else:
            curTheme = "UVU"

    except FileNotFoundError:
        pass  # Settings optional
    except json.JSONDecodeError as e:
        raise ValueError(f"Critical Error: Corrupt settings file. {e}")


def saveData():
    """
    Turns todoList into a dict, stores that dict into tasks.json

    Raises:
        OSError: If saving to disk fails.
    """

    # Save task list
    todoDict = {}
    for i, t in enumerate(todoList):
        date_str = t.dueDate.strftime("%m/%d/%Y") if t.dueDate else ""
        todoDict[i] = {
            "label": t.label,
            "dueDate": date_str,
            "priority": t.priority,
            "category": t.category,
            "people": t.people,  # Save list of people
            "complete": t.complete,
            "status": t.status,
        }

    try:
        with open(curFile, "w") as f:
            json.dump(todoDict, f, indent=4)
    except Exception as e:
        raise OSError(f"Critical Save Error: Failed to save tasks.json: {e}")

    # save system
    global curTheme
    global fileDict

    settingsDict = {"theme": curTheme, "files": fileDict}

    settingsPath = os.path.join(BASE_DIR, "settings.json")
    try:
        with open(settingsPath, "w") as f:
            json.dump(settingsDict, f, indent=4)
    except Exception as e:
        raise OSError(f"Critical Save Error: Failed to save {settingsPath}: {e}")


def search(term):
    """
    Search todo item attributes for a string

    Parameters:
        term (string): the term to search for

    Returns:
        foundTodos (list): list of todos matching the search
    """
    term = term.lower()
    foundTodos = []

    for todo in todoList:
        if todo.search(term):
            foundTodos.append(todo)

    return foundTodos


def copyTask(task):
    """Duplicates a task. Raises ValueError if task is None."""
    global copiedTask
    if task:
        # Copy people list (using list() to ensure it's a new reference)
        copiedTask = todo.ToDo(
            task.label,
            task.dueDate,
            task.priority,
            task.category,
            list(task.people),
            task.idNum,
        )
    else:
        raise ValueError("Cannot copy empty task.")


def changeProfile(profileName):
    try:
        global curFile
        global fileDict
        saveData()
        curFile = fileDict[profileName]
        loadSave()
    except (ValueError, TypeError) as e:
        raise ValueError(f"Critical Error Loading Profile {profileName}: {e}")


#######################
# GUI Support Methods #
#######################
def get_tasks_for_view(
    view_type="All", category=None, sort_key="Priority", reverse=False
):
    """Filters and sorts the todoList for display in the GUI task view"""
    filtered_tasks = todoList

    # convert strings in priority map to ints
    PRIORITY_SORT_MAP = {v: int(k) for k, v in PRIORITYDICT.items()}

    # Filter by view type
    if view_type == "Completed":
        filtered_tasks = [t for t in filtered_tasks if t.complete]
    elif view_type == "Due Today":
        today = date.today()
        filtered_tasks = [t for t in filtered_tasks if t.dueDate and t.dueDate == today]

    # Filter by category
    if category:
        filtered_tasks = [t for t in filtered_tasks if t.category == category]

    # Sort
    def get_priority_value(task):
        return PRIORITY_SORT_MAP.get(task.priority, 0)

    sort_functions = {
        "Priority": get_priority_value,
        "dueDate": lambda t: t.dueDate if t.dueDate else date(9999, 1, 1),
        "label": lambda t: t.label.lower(),
    }

    key_func = sort_functions.get(sort_key, sort_functions["Priority"])

    if sort_key == "Priority":
        reverse = True

    try:
        sorted_tasks = sorted(filtered_tasks, key=key_func, reverse=reverse)
        return sorted_tasks
    except Exception:
        # Fallback if sort fails
        return filtered_tasks


def update_task_attributes(task_id, label, dueDate, priority_key, category, people):
    """
    Updates the attributes of a ToDo object found by its ID.
    """
    if task_id < 1 or task_id > len(todoList):
        return False

    curTodo = todoList[task_id - 1]

    if curTodo.label != label:
        curTodo.editLabel(label)

    if curTodo.dueDate != curTodo._parse_date(dueDate):
        curTodo.editDueDate(dueDate)

    new_priority_value = PRIORITYDICT.get(priority_key)
    if curTodo.priority != new_priority_value:
        curTodo.editPriority(priority_key)

    if curTodo.category != category:
        curTodo.editCategory(category)

    # Check if people list changed
    if curTodo.people != people:
        curTodo.editPeople(people)

    return True
