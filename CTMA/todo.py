import constants as c

class ToDo():
    def __init__(self, label, dueDate, priority, category, idNum):
        self.label = label
        self.dueDate = dueDate
        self.priority = priority
        self.category = category
        self.idNum = idNum

        self.complete = False
        self.status = "Ongoing"

    def __str__(self):
        return (
            f"Task {self.idNum}: {self.label}\n"
            f"Category: {self.category}\n"
            f"Status: {self.status}\n"
            f"Due: {self.dueDate}\n"
            f"Priority: {self.priority}\n"
        )
    
    def printLabel(self):
        print(f"Task {self.idNum}: {self.label}")

    def editLabel(self, newVal):
        self.label = newVal
        print(f"Label saved as {newVal}\n")

    def editDueDate(self, newVal):
        self.dueDate = newVal
        print(f"Due Date saved as {newVal}\n")

    def editPriority(self, newVal):
        self.priority = c.PRIORITYDICT[newVal]
        print(f"Priority set to {c.PRIORITYDICT[newVal]}\n")

    def editCategory(self, newVal):
        self.category = newVal
        print(f"Category saved as {newVal}\n")

    def toggleComplete(self, choice):
        if (choice == 1):
            self.complete = True
            self.status = "Complete"
            print(f"{self.label} marked as complete.\n")

        if (choice == 2):
            self.complete = False
            self.status = "Ongoing"
            print(f"{self.label} marked as ongoing.\n")
        return

    def delete():
        pass