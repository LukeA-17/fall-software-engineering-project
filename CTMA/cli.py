"""
cli.py allows the user to interact with the program through the command line.
Functions:
 Todo Interaction
 - viewTodos(): prints the label of all tasks
 - viewTodosInfoed(): prints all info of all tasks
 - def decideView(): prompts user to choose between viewTodos() and viewTodosInfoed()
 - selectTodo(): prompts user to select a task, and returns int task id
 - selectEditChoice(curTodo): Takes a selected todo item. Prompts to select trait to edit, returns int choice
 
 ToDo Management:
 - changeCompletion(selection): Takes int task id. Prompts user to change completion status
 - createTodo(): Prompts user to create a new todo item, adds to s.todoList
 - editTodo(selection): Takes int task id and prompts user to edit that task
 - deleteTodo(selection): Takes int task id and deletes that task
 - searchTodo(): Prompts user for a search term and displays matches

 System:
 - def displayOptions(): Displays main menu options. Returns a valid integer choice
 - def startProgram(): Start the loop that allows user interaction
"""

import todo as todo
import shared as s
import todo_handler as th
from datetime import date, datetime


####################
# ToDo Interaction #
####################
def viewTodos():
    """Print label only of all todos"""
    for t in (s.todoList):
        t.printLabel()


def viewTodosInfoed():
    """Print all information about all todos"""
    for t in (s.todoList):
        print(t)


def decideView():
    """Prompts user to select a detailed or simple view, and then calls the associated function"""
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


def selectTodo():
    """Calls viewTodos() and prompts user to select a todo via todo id. 
    Returns id of selected todo as an integer"""
    while True: # loops until a valid input is returned
        print(
            f"Select a task number:\n"
            f"Cancel: 0"
            )
        viewTodos()
        selection = input("Task number: ")
        if selection.isdigit():
            selection = int(selection)
            if 0 <= selection <= len(s.todoList):
                print()
                return selection
            else:
                print("Invalid task number.\n")
        else:
            print("Invalid input. Please enter a number.\n")


def selectEditChoice(curTodo):
    """Accepts a todo object, and prompts user to select attribute to edit.
    Returns int of attribute selection."""
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

#############################
# ToDo Management Functions #
#############################
def changeCompletion(selection):
    """Accepts int selected task id. Prompts user to select a completion option,
    then calls curTodo.toggleComplete() on that todo object"""
    if (selection == 0):
        return
    try:
        curTodo = s.todoList[selection - 1]
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
    """Creates a new ToDo object from user input, appends to s.todoList"""
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
        if priority in s.PRIORITYDICT:
            priority = s.PRIORITYDICT[priority]
            break
        else:
            print("Invalid priority choice.\n")

    category = input("Enter task category: ").strip()
    idNum = len(s.todoList) + 1

    s.todoList.append(todo.ToDo(label, dueDate, priority, category, idNum))
    print(f"{label} added.\n")


def editTodo(selection):
    """Takes int task id, and prompts user to edit the associated todo object"""
    if (selection == 0):
        return
    try:
        curTodo = s.todoList[selection - 1]
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
                if newVal not in s.PRIORITYDICT:
                    print("Invalid priority choice.\n")
                    continue # restart loop

            editCall(newVal)
        else:
            editCall(None)

    return


def deleteTodo(selection):
    """Takes in task id, and deletes the associated todo object"""
    try:
        # task num is 1 indexed
        deletedTask = s.todoList.pop(selection - 1)
        print(f"Task {selection}: {deletedTask.label} deleted successfully.\n")

        # re-index tasks
        for i, t in enumerate(s.todoList):
            t.idNum = i + 1
    except IndexError:
        print("Error: Task not found with that number.\n")
    except Exception as e:
        print(f"An error occurred during deletion: {e}\n")


def searchTodo():
    """Search todos for a user inputted term"""
    searchTerm = input("Enter search term: ")
    if not searchTerm:
        print("Search term cannot be empty.\n")
        return
    
    foundTodos = th.search(searchTerm)

    if (len(foundTodos) == 0):
        print(f"{searchTerm} not found.")
    else:
        print(f"{len(foundTodos)} matches found:\n")
        for td in (foundTodos):
            print(td)

    return


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
    
    new_priority_value = c.PRIORITYDICT.get(priority_key)
    if curTodo.priority != new_priority_value:
        curTodo.editPriority(priority_key)
    
    if curTodo.category != category:
        curTodo.editCategory(category)
    
    # NOTE completion status is handled separately by the checkbox in the GUI
    return True

####################
# System functions #
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


def startProgram():
    """Starts a loop of CLI user interaction"""
    choice = None

    print("Welcome to Collaborative ToDo Manager Application (CTMA)!")
    th.loadSave()

    while (choice != 0):
        choice = displayOptions()

        if (choice == 0):
            pass

        if (choice == 1):
            createTodo()

        if (choice == 2):
            editTodo(selectTodo())

        if (choice == 3):
            deleteTodo(selectTodo())

        if (choice == 4):
            changeCompletion(selectTodo())

        if (choice == 5):
            decideView()
        
        if (choice == 6):
            searchTodo()

    th.saveData()
    print("\nThank you for using CTMA!")