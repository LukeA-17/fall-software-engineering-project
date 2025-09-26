import handler as h

def startProgram():
    choice = None

    print("Welcome to Collaborative ToDo Manager Application (CTMA)!")
    h.loadSave()

    while (choice != 0):
        choice = h.displayOptions()

        if (choice == 0):
            pass

        if (choice == 1):
            h.createTodo()

        if (choice == 2):
            h.editTodo(h.selectTodo())

        if (choice == 3):
            pass

        if (choice == 4):
            h.changeCompletion(h.selectTodo())

        if (choice == 5):
            h.decideView()

    h.saveData()
    print("\nThank you for using CTMA!")
