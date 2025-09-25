import json
import todo as todo


#####################
# Handler Variables #
#####################
todoList = [] # stores todo objects

priorityDict = {
    "1": "None",
    "2": "Low",
    "3": "Medium",
    "4": "High"  
       }


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
    print()

def viewTodosInfoed():
    for t in (todoList):
        print(t)
    print()

def createTodo():
    """
    Takes user input to create a new todo object, stores at end of todoList
    """
    label = input("Enter task label: ")
    dueDate = input("Enter due date: ") # TODO could ensure consistent formatting
    priority = priorityDict[input("Enter priority:\n(1: None, 2: Low, 3: Medium, 4: High)\n")] # TODO make it so it only accepts valid input
    category = input("Enter task category: ")
    idNum = len(todoList) + 1

    todoList.append(todo.ToDo(label, dueDate, priority, category, idNum))
    print("Task created.\n")


####################
# User Interaction #
####################
def displayOptions():
    choice = input(
        f"Select an option:\n"
        f"1: Create a task\n"
        f"2: Edit a task\n"
        f"3: Delete a task\n"
        f"4: Mark a task as complete\n"
        f"5: Mark a task as incomplete\n"
        f"6: View tasks\n"
        f"7: Exit CTMA\n"
        )
    print()
    return int(choice) # TODO type and bounds testing