import constants as c
from datetime import date, datetime

class ToDo():
    def __init__(self, label, dueDate, priority, category, idNum):
        self.label = label
        self.dueDate = self._parse_date(dueDate)
        self.priority = priority
        self.category = category
        self.idNum = idNum

        self.complete = False
        self.status = "Ongoing"
    
    def _parse_date(self, date_str):
        if not date_str or date_str.lower() in ["none", ""]:
            return None
        
        try:
            return datetime.strptime(date_str.strip(), "%m/%d/%Y").date()
        except ValueError:
            print(f"Warning: Date string '{date_str}' is not in MM/DD/YYYY format. Storing as None.")
            return None

    def __str__(self):
        date_display = self.dueDate.strftime("%m/%d/%Y") if self.dueDate else "N/A"
        return (
            f"Task {self.idNum}: {self.label}\n"
            f"Category: {self.category}\n"
            f"Status: {self.status}\n"
            f"Due: {date_display}\n"
            f"Priority: {self.priority}\n"
        )
    
    def printLabel(self):
        print(f"Task {self.idNum}: {self.label}")

    def editLabel(self, newVal):
        self.label = newVal
        print(f"Label saved as {newVal}\n")

    def editDueDate(self, newVal):
        new_date_obj = self._parse_date(newVal)
        self.dueDate = new_date_obj
        date_display = new_date_obj.strftime("%m/%d/%Y") if new_date_obj else "N/A"
        print(f"Due Date saved as {date_display}\n")

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
