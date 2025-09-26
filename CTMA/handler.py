# TODO maybe change all variable and method from todo to task

import json
import todo as todo
import constants as c


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
            todoList.append(todo.ToDo(
                item["label"],
                item["dueDate"],
                item["priority"],
                item["category"],
                (len(todoList) + 1)
            ))
            count += 1
        print(f"{count} tasks loaded successfully.\n")

def saveData():
    """
    Turns todoList into a dict, stores that dict into data.json
    """
    todoDict = {}
    for i, t in enumerate(todoList):
        todoDict[i] = {
            "label": t.label,
            "dueDate": t.dueDate,
            "priority": t.priority,
            "category": t.category
        }

    with open("data.json", "w") as f:
        json.dump(todoDict, f, indent = 4)
        print("Tasks saved successfully.")

def search():
    # have like a filtering/sorting thing here for category TODO
    pass


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

    dueDate = input("Enter due date: ").strip() # TODO could ensure consistent formatting

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
        2: ("Enter new due date: ", lambda v: curTodo.editDueDate(v)),
        3: ("Enter new priority level:\n1: None\n2: Low\n3: Medium\n 4: High\n", lambda v: curTodo.editPriority(v)),
        4: ("Enter new category: ", lambda v: curTodo.editCategory(v)),
        5: (None, lambda _v: changeCompletion(selection))
    }
    
    while True:
        editChoice = selectEditChoice(curTodo)
        if (editChoice == 0):
            break

        prompt, editCall = editOptions.get(editChoice)
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
                ))

            if 0 <= choice <= 5:
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