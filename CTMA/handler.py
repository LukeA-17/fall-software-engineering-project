import json
import todo as todo
import constants as c
from datetime import date, datetime


#####################
# Handler Variables #
#####################
todoList = [] # stores todo objects

##################
# System Methods #
##################
def loadSave():
    """
    Pulls dict of todos from data.json, converts to list of todo objs stored in todoList
    """
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
        with open("data.json", "w") as f:
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

# TODO implement saving completion status as well
def saveData():
    """
    Turns todoList into a dict, stores that dict into data.json
    """
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

    with open("data.json", "w") as f:
        json.dump(todoDict, f, indent = 4)
        print("Tasks saved successfully.")

def search():
    if not todoList:
        print("No tasks available to search.\n")
        return
    
    searchTerm = input("Enter search term: ")
    if not searchTerm:
        print("Search term cannot be empty.\n")
        return
    
    results = [
        t for t in todoList
        if searchTerm in t.label.lower() or
        searchTerm in t.category.lower() or
        searchTerm in t.priority.lower()
    ]

    if results:
        print("\n--- Search Results ---")
        for t in results:
            print(t)
        print("--------------------- \n")
    else:
        print("No tasks matched your search criteria.\n")


####################
# ToDo Interaction #
####################
def viewTodos():
    for t in (todoList):
        t.printLabel()

def viewTodosInfoed():
    for t in (todoList):
        print(t)

def selectTodo():
    """
    Prompts user to select a task number. Validates input.
    Returns the valid selection.
    """
    while True: # loops until a valid input is returned
        print(
            f"Select a task number:\n"
            f"Cancel: 0"
            )
        viewTodos()
        selection = input("Task number: ")
        if selection.isdigit():
            selection = int(selection)
            if 0 <= selection <= len(todoList):
                print()
                return selection
            else:
                print("Invalid task number.\n")
        else:
            print("Invalid input. Please enter a number.\n")


def selectEditChoice(curTodo):
    """
    Prompts user for an edit choice. Validates input.
    Returns the valid selecion.
    """
    while True: # loop until valid input returns
        try:
            editChoice = int(input( 
                f"What would you like to edit?\n"
                f"0: Exit Editing\n"
                f"1: Label - Current: {curTodo.label}\n"
                f"2: Due Date - Current: {curTodo.dueDate}\n"
                f"3: Priority - Current: {curTodo.priority}\n"
                f"4: Category - Current: {curTodo.category}\n"
                f"5: Completion - Current: {curTodo.status}\n"
            ))
            if 0 <= editChoice <= 5:
                print()
                return editChoice
            else:
                print("Invalid choice. Please enter a number between 0 and 5.\n")
        except ValueError: # couldn't convert to int
            print("Invalid input. Please enter a number.\n")

def changeCompletion(selection):
    if (selection == 0):
        return
    try:
        curTodo = todoList[selection - 1]
    except IndexError:
        print("Error: Task not found with that number.")
        return

    while True:
        try:
            choice = int(input(
                f"Select {curTodo.label} completion status - Current: {curTodo.status}: \n"
                f"0: Cancel\n"
                f"1: Complete\n"
                f"2: Ongoing\n"
            ))

            if choice in [0, 1, 2]:
                curTodo.toggleComplete(choice)
                return
            else:
                print("Invalid choice. Select 0, 1, or 2.\n")
        except ValueError:
            print("Invalid input. Enter a number.\n")

def createTodo():
    """
    Takes user input to create a new todo object, stores at end of todoList
    """
    # validate label input
    while True:
        label = input("Enter task label: ").strip()
        if label:
            break
        else:
            print("Task label cannot be empty.\n")

    # validate date input
    while True:
        dueDate = input("Enter due date (MM/DD/YYYY, or leave blank): ").strip()
        if not dueDate:
            break

        try:
            datetime.strptime(dueDate, "%m/%d/%Y")
            break
        except ValueError:
            print("Invalid date format. Use MM/DD/YYYY or leave blank.\n")

    # validate priority input
    while True:
        priority = input("Enter priority:\n(1: None, 2: Low, 3: Medium, 4: High)\n")
        if priority in c.PRIORITYDICT:
            priority = c.PRIORITYDICT[priority]
            break
        else:
            print("Invalid priority choice.\n")

    category = input("Enter task category: ").strip()
    idNum = len(todoList) + 1

    todoList.append(todo.ToDo(label, dueDate, priority, category, idNum))
    print(f"{label} added.\n")

def editTodo(selection):
    """
    Edit attributes of tasks via terminal
    """
    if (selection == 0):
        return
    try:
        curTodo = todoList[selection - 1]
    except IndexError:
        print("Invalid task selection.")
        return

    editOptions = {
        1: ("Enter new label: ", lambda v: curTodo.editLabel(v)),
        2: ("Enter new due date (MM/DD/YYYY): ", lambda v: curTodo.editDueDate(v)),
        3: ("Enter new priority level:\n1: None\n2: Low\n3: Medium\n 4: High\n", lambda v: curTodo.editPriority(v)),
        4: ("Enter new category: ", lambda v: curTodo.editCategory(v)),
        5: (None, lambda _v: changeCompletion(selection))
    }
    
    while True:
        editChoice = selectEditChoice(curTodo)
        if (editChoice == 0):
            break

        prompt, editCall = editOptions.get(editChoice, (None, None))
        if prompt:
            newVal = input(prompt).strip()

            if editChoice == 3:
                if newVal not in c.PRIORITYDICT:
                    print("Invalid priority choice.\n")
                    continue # restart loop

            editCall(newVal)
        else:
            editCall(None)

    return

def deleteTodo(selection):
    try:
        # task num is 1 indexed
        deletedTask = todoList.pop(selection - 1)
        print(f"Task {selection}: {deletedTask.label} deleted successfully.\n")

        # re-index tasks
        for i, t in enumerate(todoList):
            t.idNum = i + 1
    except IndexError:
        print("Error: Task not found with that number.\n")
    except Exception as e:
        print(f"An error occurred during deletion: {e}\n")
    

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
    PRIORITY_SORT_MAP = {v: int(k) for k, v in c.PRIORITYDICT.items()}

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

####################
# User Interaction #
####################
def displayOptions():
    """
    Displays main menu options. Returns a valid integer choice.
    """
    while True:
        try:
            choice = int(input(
                f"Select an option:\n"
                f"0: Exit CTMA\n"
                f"1: Create a task\n"
                f"2: Edit a task\n"
                f"3: Delete a task\n"
                f"4: Change a task's completion\n"
                f"5: View tasks\n"
                f"6: Search tasks\n"
                ))

            if 0 <= choice <= 6:
                print()
                return choice
            else:
                print("Invalid option.\n")
        except ValueError:
            print("Invalid input.\n")

def decideView():
    while True:
        try:
            detail = int(input(
                f"Select viewing option:\n"
                f"0: Simple\n"
                f"1: Detailed\n"
            ))
            print()
            if (detail == 0):
                viewTodos()
                print()
                return
            if (detail == 1):
                viewTodosInfoed()
                print()
                return
            else:
                print("Invalid option.\n")
        except ValueError:
            print("Invalid input.\n")