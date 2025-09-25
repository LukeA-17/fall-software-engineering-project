import handler as h

def startProgram():
    choice = 0

    print("Welcome to Collaborative ToDo Manager Application (CTMA)!")
    h.loadSave()

    while (choice != 7):
        choice = h.displayOptions()

        if (choice == 1):
            h.createTodo()
        if (choice == 2):
            pass
        if (choice == 3):
            pass
        if (choice == 4):
            pass
        if (choice == 5):
            pass
        if (choice == 6):
            h.viewTodos()
        if (choice == 7):
            pass

    h.saveData()
    print("Thank you for using CTMA!")
