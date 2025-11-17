"""
todo_handler.py acts as the logic layer of the program
Functions:
    System:
    - loadSave(): loads save data from tasks.json
    - saveData(): saves runtime todos into tasks.json
    - search(term): creates a list of todo items containing a certain string

    GUI Support:
    - get_tasks_for_view(view_type="All", category=None, sort_key="Priority", reverse=False): 
      Filters and sorts the todoList for display
"""

import json
import todo as todo
from datetime import date, datetime


#####################
# Handler Variables #
#####################
# mapping of numbers to priorities
PRIORITYDICT = {
    "1": "None",
    "2": "Low",
    "3": "Medium",
    "4": "High"  
}

todoList = [] # stores todo objects during runtime
curTheme = "Dark"

####################
# System Functions #
####################
def loadSave():
    """
    Pulls dict of todos from tasks.json, converts to list of todo objs stored in todoList. Also loads the user's saved settings.
    """
    # Load the todoList
    try:
        with open(r"CTMA\tasks.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
        with open(r"CTMA\tasks.json", "w") as f:
            json.dump(data, f)

    if len(data) == 0:
        print("No save data found.\n")
    else:
        count = 0
        for item in data.values():
            new_task = todo.ToDo(
                item["label"],
                item["dueDate"],
                item["priority"],
                item["category"],
                (len(todoList) + 1)
            )
            if "complete" in item and item["complete"]:
                new_task.toggleComplete(1)
            
            todoList.append(new_task)
            count += 1
        print(f"{count} tasks loaded successfully.\n")
    
    # Load data from settings
    try:
        with open(r"CTMA\settings.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
        with open(r"CTMA\settings.json", "w") as f:
            json.dump(data, f)
    
    if "theme" in data:
        global curTheme
        curTheme = data["theme"]
    else:
        curTheme = "UVU"


def saveData():
    """
    Turns todoList into a dict, stores that dict into tasks.json
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
            "complete": t.complete,
            "status": t.status
        }

    with open(r"CTMA\tasks.json", "w") as f:
        json.dump(todoDict, f, indent = 4)
        print("Tasks saved successfully.")

    # Save settings
    global curTheme
    settingsDict = {
        "theme": curTheme
        }
    with open(r"CTMA\settings.json", "w") as f:
        json.dump(settingsDict, f, indent = 4)
        print("Settings saved successfully.")


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


#######################
# GUI Support Methods #
#######################
def get_tasks_for_view(view_type="All", category=None, sort_key="Priority", reverse=False):
    """Filters and sorts the todoList for display in the GUI task view

    Args:
        view_type: 'All', 'Due Today', or 'Completed'
        category: Specific category name or None for all categories
        sort_key: Attribute to sort by ('Priority', 'dueDate', 'label')
        reverse: Boolean to reverse the sort order
    
    Returns:
        A list of filtered and sorted ToDo objects
    """
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
        # None dates are set far in future to sort last
        "dueDate": lambda t: t.dueDate if t.dueDate else date(9999, 1, 1),
        "label": lambda t: t.label.lower()
    }

    key_func = sort_functions.get(sort_key, sort_functions["Priority"])

    if sort_key == "Priority":
        reverse = True
    else:
        reverse = reverse
    
    try:
        sorted_tasks = sorted(filtered_tasks, key=key_func, reverse=reverse)
        return sorted_tasks
    except Exception as e:
        print(f"Error during task sorting: {e}")
        return filtered_tasks


def update_task_attributes(task_id, label, dueDate, priority_key, category):
    """
    Updates the attributes of a ToDo object found by its ID

    Args:
        task-id (int): The ID of the task to update (1-indexed).
        label (str): The new label.
        dueDate (str): The new due date string (MM/DD/YYYY).
        priority_key (str): The new priority key ('1' through '4')
        category (str): The new category.

    Returns:
        bool: True if task was found and updated, False otherwise.
    """
    try:
        curTodo = todoList[task_id - 1]
    except IndexError:
        print(f"Error: Task ID {task_id} not found.")
        return False

    if curTodo.label != label:
        curTodo.editLabel(label)

    if curTodo.dueDate != curTodo._parse_date(dueDate):
        curTodo.editDueDate(dueDate)

    new_priority_value = PRIORITYDICT.get(priority_key)
    if curTodo.priority != new_priority_value:
        curTodo.editPriority(priority_key)

    if curTodo.category != category:
        curTodo.editCategory(category)

    # NOTE completion status is handled separately by the checkbox in the GUI
    return True