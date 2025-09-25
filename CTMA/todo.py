

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

    def delete():
        pass

    def edit():
        pass