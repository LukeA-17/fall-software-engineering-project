"""
todo.py stores the ToDo class and all related data

Methods:
    __init__(self, label, dueDate, priority, category, idNum): defines instantiation of a ToDo object
    __str__(self): defines how objects should be represented as a string

    printLabel(self): prints the label of self
    search(self, term): checks if term is present in self
    _parse_date(self, date_str): returns a datetime date

    editLabel(self, newVal): Accepts string newVal, sets label to newVal
    editDueDate(self, newVal): Accepts datetime newVal, sets dueDate to newVal
    editPriority(self, newVal): Accepts int newVal, uses PRIORITYDICT to change priority
    editCategory(self, newVal): Accepts string newVal, sets category to newVal
    toggleComplete(self, choice): Accepts int choice. 1 marks todo complete, 2 marks incomplete
"""

from datetime import date, datetime
PRIORITYDICT = {
    "1": "None",
    "2": "Low",
    "3": "Medium",
    "4": "High"  
}

class ToDo():
    """
    A class representing a todo item

    Attributes:
        label (string): title of the todo
        dueDate (datetime date): todo due date
        priority (string): todo completion priority
        category (string): todo category
        idNum (int): todo id number, assigned in order of creation
        complete (boolean): boolean denoting if todo is complete
        status (string): either Completed or Ongoing
    """
    ###################
    # Special Methods #
    ###################
    def __init__(self, label, dueDate, priority, category, idNum):
        """
        Initialize an Employee object

        Parameters:
            label (string): title of the todo
            dueDate (datetime date): todo due date
            priority (string): todo completion priority
            category (string): todo category
            idNum (int): todo id number, assigned in order of creation 
        """
        self.label = label
        self.dueDate = self._parse_date(dueDate)
        self.priority = priority
        self.category = category
        self.idNum = idNum

        self.complete = False
        self.status = "Ongoing"

    def __str__(self):
        """Defines how todo objects are represented as strings"""
        date_display = self.dueDate.strftime("%m/%d/%Y") if self.dueDate else "N/A"
        return (
            f"Task {self.idNum}: {self.label}\n"
            f"Category: {self.category}\n"
            f"Status: {self.status}\n"
            f"Due: {date_display}\n"
            f"Priority: {self.priority}\n"
        )
    
    ################
    # Core Methods #
    ################
    def printLabel(self):
        """Prints object's own label"""
        print(f"Task {self.idNum}: {self.label}")
    
    
    def search(self, term):
        """Check if (string) term is in self, returns T/F"""
        for attr, value in vars(self).items():
            if term in str(value).lower():
                return True
        return False
    
    
    def _parse_date(self, date_str):
        """
        Parse a string to datetime date variable
        
        Parameters:
            date_str (string): string to be parsed

        Returns:
            None or datetime date
        """
        if not date_str or date_str.lower() in ["none", ""]:
            return None
        
        try:
            return datetime.strptime(date_str.strip(), "%m/%d/%Y").date()
        except ValueError:
            print(f"Warning: Date string '{date_str}' is not in MM/DD/YYYY format. Storing as None.")
            return None

    ###################
    # Editing Methods #
    ###################
    def editLabel(self, newVal):
        """
        Edit the label of an existing todo

        Parameters:
            newVal (string): new label to replace the old
        """
        self.label = newVal
        print(f"Label saved as {newVal}\n")

    def editDueDate(self, newVal):
        """
        Edit the due date of an existing todo

        Parameters:
            newVal (string): new due date to replace the old
        """
        new_date_obj = self._parse_date(newVal)
        self.dueDate = new_date_obj
        date_display = new_date_obj.strftime("%m/%d/%Y") if new_date_obj else "N/A"
        print(f"Due Date saved as {date_display}\n")

    def editPriority(self, newVal):
        """
        Edit the priority of an existing todo

        Parameters:
            newVal (int): value that corresponds to desired new priority from PRIORITYDICT
        """
        self.priority = PRIORITYDICT[newVal]
        print(f"Priority set to {PRIORITYDICT[newVal]}\n")

    def editCategory(self, newVal):
        """
        Edit the category of an existing todo

        Parameters:
            newVal (string): replacement category for the todo
        """
        self.category = newVal
        print(f"Category saved as {newVal}\n")

    def toggleComplete(self, choice):
        """
        Mark an existing todo as complete or ongoing

        Parameters:
            choice (int): 1 sets complete, 2 sets to ongoing
        """
        if (choice == 1):
            self.complete = True
            self.status = "Complete"
            print(f"{self.label} marked as complete.\n")

        if (choice == 2):
            self.complete = False
            self.status = "Ongoing"
            print(f"{self.label} marked as ongoing.\n")
        return
