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
    print(
        f"Select a task number:\n"
        f"Cancel: 0"
         )
    viewTodos()
    selection = int(input(""))
    print()
    return(selection)
    # TODO input validation

def selectEditChoice(curTodo):
    editChoice = int(input( 
        f"What would you like to edit?\n"
        f"0: Exit Editing\n"
        f"1: Label - Current: {curTodo.label}\n"
        f"2: Due Date - Current: {curTodo.dueDate}\n"
        f"3: Priority - Current: {curTodo.priority}\n"
        f"4: Category - Current: {curTodo.category}\n"
        f"5: Completion - Current: {curTodo.status}\n"
    ))
    print()
    return editChoice

def changeCompletion(selection):
    if (selection == 0):
        return
    curTodo = todoList[selection - 1]

    choice = int(input(
        f"Select {curTodo.label} completion status - Current: {curTodo.status}: \n"
        f"0: Cancel\n"
        f"1: Complete\n"
        f"2: Ongoing\n"
    ))
    curTodo.toggleComplete(choice)
    return

def createTodo():
    """
    Takes user input to create a new todo object, stores at end of todoList
    """
    label = input("Enter task label: ")
    dueDate = input("Enter due date: ") # TODO could ensure consistent formatting
    priority = c.PRIORITYDICT[input("Enter priority:\n(1: None, 2: Low, 3: Medium, 4: High)\n")] # TODO make it so it only accepts valid input
    category = input("Enter task category: ")
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
        # TODO input validation here
        editChoice = selectEditChoice(curTodo)
        if (editChoice == 0):
            break

        prompt, editCall = editOptions.get(editChoice)
        if prompt:
            newVal = input(prompt)
            editCall(newVal)
        else:
            editCall(None)

    return
    

####################
# User Interaction #
####################
def displayOptions():
    choice = input(
        f"Select an option:\n"
        f"0: Exit CTMA\n"
        f"1: Create a task\n"
        f"2: Edit a task\n"
        f"3: Delete a task\n"
        f"4: Change a task's completion\n"
        f"5: View tasks\n"
        )
    print()
    return int(choice) # TODO type and bounds testing

def decideView():
    detail = int(input(
        f"Select viewing option:\n"
        f"0: Simple\n"
        f"1: Detailed\n"
    ))
    print()
    if (detail == 0):
        viewTodos()
    if (detail == 1):
        viewTodosInfoed()
    print()
    return