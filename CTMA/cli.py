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
 - createTodo(): Prompts user to create a new todo item, adds to th.todoList
 - editTodo(selection): Takes int task id and prompts user to edit that task
 - deleteTodo(selection): Takes int task id and deletes that task
 - searchTodo(): Prompts user for a search term and displays matches

 System:
 - viewProfiles(): Prints a list of all currently available profiles
 - manageProfiles(): Handles adding, deleting, and switching between save profiles
 - displayOptions(): Displays main menu options. Returns a valid integer choice
 - startProgram(): Start the loop that allows user interaction
"""

import todo as todo
import todo_handler as th
from datetime import date, datetime
import sys


####################
# ToDo Interaction #
####################
def viewTodos():
    """Print label only of all todos"""
    for t in th.todoList:
        t.printLabel()


def viewTodosInfoed():
    """Print all information about all todos"""
    for t in th.todoList:
        print(t)


def decideView():
    """Prompts user to select a detailed or simple view, and then calls the associated function"""
    while True:
        try:
            detail = int(
                input(f"Select viewing option:\n" f"0: Simple\n" f"1: Detailed\n")
            )
            print()
            if detail == 0:
                viewTodos()
                print()
                return
            if detail == 1:
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
    while True:  # loops until a valid input is returned
        print(f"Select a task number:\n" f"Cancel: 0")
        viewTodos()
        selection = input("Task number: ")
        if selection.isdigit():
            selection = int(selection)
            if 0 <= selection <= len(th.todoList):
                print()
                return selection
            else:
                print("Invalid task number.\n")
        else:
            print("Invalid input. Please enter a number.\n")


def selectEditChoice(curTodo):
    """Accepts a todo object, and prompts user to select attribute to edit. Returns int of attribute selection."""
    people_str = ", ".join(curTodo.people) if curTodo.people else "None"
    while True: 
        try:
            editChoice = int(
                input(
                    f"What would you like to edit?\n"
                    f"0: Exit Editing\n"
                    f"1: Label - Current: {curTodo.label}\n"
                    f"2: Due Date - Current: {curTodo.dueDate}\n"
                    f"3: Priority - Current: {curTodo.priority}\n"
                    f"4: Category - Current: {curTodo.category}\n"
                    f"5: People - Current: {people_str}\n"
                    f"6: Completion - Current: {curTodo.status}\n"
                    f"7: Copy Task\n"
                )
            )
            if 0 <= editChoice <= 7:
                print()
                return editChoice
            else:
                print("Invalid choice. Please enter a number between 0 and 7.\n")
        except ValueError:
            print("Invalid input. Please enter a number.\n")


#############################
# ToDo Management Functions #
#############################
def changeCompletion(selection):
    """Accepts int selected task id. Prompts user to select a completion option,
    then calls curTodo.toggleComplete() on that todo object"""
    if selection == 0:
        return
    try:
        curTodo = th.todoList[selection - 1]
    except IndexError:
        print("Error: Task not found with that number.")
        return

    while True:
        try:
            choice = int(
                input(
                    f"Select {curTodo.label} completion status - Current: {curTodo.status}: \n"
                    f"0: Cancel\n"
                    f"1: Complete\n"
                    f"2: Ongoing\n"
                )
            )

            if choice in [0, 1, 2]:
                if choice == 0:
                    return
                try:
                    curTodo.toggleComplete(choice)
                    return
                except (ValueError, TypeError) as e:
                    print(f"Error updating status: {e}\n")
            else:
                print("Invalid choice. Select 0, 1, or 2.\n")
        except ValueError:
            print("Invalid input. Enter a number.\n")


def createTodo():
    """Creates a new ToDo object from user input, appends to th.todoList"""
    # provide paste option
    while True:
        try:
            doPaste = int(input("Paste copied task?\n(0: No, 1: Yes)\n"))
            if doPaste in {0, 1}:
                break
            print("Input not recognized.\n")
        except ValueError:
            print("Invalid input. Please enter 0 or 1.\n")

    if (doPaste == 1):
        copiedTask = th.copiedTask

        if (copiedTask == None):
            print("Paste Error: No task has been copied yet.\n")
            return

        label = (f"COPY: {copiedTask.label}")
        dueDate = copiedTask.dueDate 
        priority = copiedTask.priority
        category = copiedTask.category
        people = list(copiedTask.people) # Copy list
        idNum = len(th.todoList) + 1

        try:
            th.todoList.append(todo.ToDo(label, dueDate, priority, category, people, idNum))
            print(f"{label} added.\n")
        except (ValueError, TypeError) as e:
            print(f"Error pasting task: {e}\n")

    if (doPaste == 0):
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
            if priority in th.PRIORITYDICT:
                priority = th.PRIORITYDICT[priority]
                break
            else:
                print("Invalid priority choice.\n")

        category = input("Enter task category: ").strip()
        
        # Process people input string into list
        people_input = input("Enter people involved (comma separated): ")
        people = [p.strip() for p in people_input.split(",") if p.strip()]
        
        idNum = len(th.todoList) + 1

        try:
            new_task = todo.ToDo(label, dueDate, priority, category, people, idNum)
            th.todoList.append(new_task)
            print(f"{label} added.\n")
        except (ValueError, TypeError) as e:
            print(f"Error creating task: {e}\n")


def editTodo(selection):
    """Takes int task id, and prompts user to edit the associated todo object"""
    if selection == 0:
        return
    try:
        curTodo = th.todoList[selection - 1]
    except IndexError:
        print("Invalid task selection.")
        return

    editOptions = {
        1: ("Enter new label: ", lambda v: curTodo.editLabel(v)),
        2: ("Enter new due date (MM/DD/YYYY): ", lambda v: curTodo.editDueDate(v)),
        3: (
            "Enter new priority level:\n1: None\n2: Low\n3: Medium\n 4: High\n",
            lambda v: curTodo.editPriority(v),
        ),
        4: ("Enter new category: ", lambda v: curTodo.editCategory(v)),
        5: ("Enter people involved (comma separated): ", lambda v: curTodo.editPeople([p.strip() for p in v.split(",") if p.strip()])),
        6: (None, lambda _v: changeCompletion(selection)),
        7: (None, lambda _v: th.copyTask(curTodo))
    }

    while True:
        editChoice = selectEditChoice(curTodo)
        if editChoice == 0:
            break

        prompt, editCall = editOptions.get(editChoice, (None, None))

        if editChoice == 7:
            try:
                th.copyTask(curTodo)
                print(f"{curTodo.label} copied.\n")
            except ValueError as e:
                print(f"Copy Error: {e}\n")
            continue
        
        elif editChoice == 6:
            editCall(None)
            
        elif prompt:
            newVal = input(prompt).strip()

            if editChoice == 3:
                if newVal not in th.PRIORITYDICT:
                    print("Invalid priority choice.\n")
                    continue
            
            try:
                editCall(newVal)
            except (ValueError, TypeError) as e:
                print(f"Error updating task: {e}\n")

        return


def deleteTodo(selection):
    """Takes in task id, and deletes the associated todo object"""
    try:
        # task num is 1 indexed
        deletedTask = th.todoList.pop(selection - 1)
        print(f"Task {selection}: {deletedTask.label} deleted successfully.\n")

        # re-index tasks
        for i, t in enumerate(th.todoList):
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

    if len(foundTodos) == 0:
        print(f"{searchTerm} not found.")
    else:
        print(f"{len(foundTodos)} matches found:\n")
        for td in foundTodos:
            print(td)

    return


####################
# System functions #
####################
def viewProfiles():
    """Prints list of currently available profiles"""
    # Determine current profile name by matching path in fileDict
    current_name = "Unknown"
    for name, path in th.fileDict.items():
        if path == th.curFile:
            current_name = name
            break

    print("\nProfile Management:")
    print(f"Current Profile: {current_name} ({th.curFile})")
    print("Available Profiles:")
    for name, path in th.fileDict.items():
        print(f"  - {name}: {path}")

def manageProfiles():
    """Menu for managing save profiles (Multi-file support)"""
    while True:
        viewProfiles() # Show list on start of loop

        try:
            choice = int(input(
                "\nSelect an option:\n"
                "0: Back to Main Menu\n"
                "1: Switch Profile\n"
                "2: Add Profile\n"
                "3: Delete Profile\n"
                "4: View Profiles\n"
            ))
        except ValueError:
            print("Invalid input. Please enter a number.\n")
            continue

        if choice == 0:
            return
        
        elif choice == 1:
            target = input("Enter the name of the profile to switch to: ").strip()
            if target in th.fileDict:
                try:
                    th.changeProfile(target)
                    print(f"Successfully switched to profile: {target}\n")
                except ValueError as e:
                    print(f"Error switching profile: {e}\n")
            else:
                print("Profile not found.\n")

        elif choice == 2:
            name = input("Enter new profile name: ").strip()
            if not name:
                print("Name cannot be empty.\n")
                continue
            if name in th.fileDict:
                print("A profile with that name already exists.\n")
                continue
            
            # Note: User must enter a relative or absolute path manually in CLI
            path = input(r"Enter file path (e.g., CTMA\school.json): ").strip()
            if not path.lower().endswith(".json"):
                print("File must be a .json file.\n")
                continue
            
            th.fileDict[name] = path
            print(f"Profile '{name}' added. Switch to it to create the file if it doesn't exist.\n")

        elif choice == 3:
            target = input("Enter the name of the profile to delete: ").strip()
            if target == "Default":
                print("Cannot delete the Default profile.\n")
                continue
            
            if target in th.fileDict:
                confirm = input(f"Are you sure you want to delete profile '{target}'? (y/n): ").lower()
                if confirm == 'y':
                    del th.fileDict[target]
                    # If we deleted the current profile, switch to Default
                    if target == th.curFile: # Check if deleted path was current
                         print("Current profile deleted. Switching to Default...")
                         try:
                            th.changeProfile("Default")
                         except:
                            pass
                    print(f"Profile '{target}' deleted.\n")
            else:
                print("Profile not found.\n")

        elif choice == 4:
            viewProfiles()
            input("Press Enter to continue...")
        
        else:
            print("Invalid option.\n")


def displayOptions():
    """
    Displays main menu options. Returns a valid integer choice.
    """
    while True:
        try:
            choice = int(
                input(
                    f"Select an option:\n"
                    f"0: Exit CTMA\n"
                    f"1: Create a task\n"
                    f"2: Edit a task\n"
                    f"3: Delete a task\n"
                    f"4: Change a task's completion\n"
                    f"5: View tasks\n"
                    f"6: Search tasks\n"
                    f"7: Manage Profiles\n"
                )
            )

            if 0 <= choice <= 7:
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

    try:
        th.loadSave()
    except ValueError as e:
        print(f"Error: {e}")
        print("Program Terminating")
        sys.exit()

    while choice != 0:
        choice = displayOptions()

        if choice == 0:
            pass

        if choice == 1:
            createTodo()

        if choice == 2:
            editTodo(selectTodo())

        if choice == 3:
            deleteTodo(selectTodo())

        if choice == 4:
            changeCompletion(selectTodo())

        if choice == 5:
            decideView()

        if choice == 6:
            searchTodo()
            
        if choice == 7:
            manageProfiles()

    try:
        th.saveData()
    except OSError as e:
        print(f"Failed to save data: {e}")
        
    print("\nThank you for using CTMA!")
