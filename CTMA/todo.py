"""
todo.py stores the ToDo class and all related data

Methods:
    __init__(self, label, dueDate, priority, category, people, idNum): defines instantiation of a ToDo object
    __str__(self): defines how objects should be represented as a string

    printLabel(self): prints the label of self
    search(self, term): checks if term is present in self
    _parse_date(self, date_str): returns a datetime date

    editLabel(self, newVal): Accepts string newVal, sets label to newVal
    editDueDate(self, newVal): Accepts datetime newVal, sets dueDate to newVal
    editPriority(self, newVal): Accepts int newVal, uses PRIORITYDICT to change priority
    editCategory(self, newVal): Accepts string newVal, sets category to newVal
    editPeople(self, newVal): Accepts list of strings newVal, sets people to newVal
    toggleComplete(self, choice): Accepts int choice. 1 marks todo complete, 2 marks incomplete
"""

from datetime import date, datetime

PRIORITYDICT = {
    "1": "None",
    "2": "Low",
    "3": "Medium",
    "4": "High"  
}

def validateAttributes(label, dueDate, priority, category, people, idNum):
    """
    Validates that all attributes match their expected types.
    Raises TypeError if any attribute is invalid.
    Raises ValueError if required attributes are empty.
    """
    # Label must be a string and have content
    if not isinstance(label, str):
        raise TypeError(f"Label must be a string, got {type(label)}")
    if not label.strip():
        raise ValueError("Label cannot be empty")
        
    # dueDate can be a date object or None (can be empty)
    if dueDate is not None and not isinstance(dueDate, (date, datetime)):
        raise TypeError(f"DueDate must be a date object, got {type(dueDate)}")
        
    # Priority can be empty (None allowed), otherwise must be string
    if priority is not None and not isinstance(priority, str):
        raise TypeError(f"Priority must be a string or None, got {type(priority)}")
        
    # Category can be empty (None allowed), otherwise must be string
    if category is not None and not isinstance(category, str):
        raise TypeError(f"Category must be a string or None, got {type(category)}")

    # People must be a list of strings (can be empty)
    if not isinstance(people, list):
        raise TypeError(f"People involved must be a list, got {type(people)}")
    for p in people:
        if not isinstance(p, str):
            raise TypeError("All items in 'people' list must be strings")
    
    # idNum validation
    if not isinstance(idNum, int):
        raise TypeError(f"ID Number must be an integer, got {type(idNum)}")


class ToDo():
    """
    A class representing a todo item

    Attributes:
        label (string): title of the todo
        dueDate (datetime date): todo due date
        priority (string): todo completion priority
        category (string): todo category
        people (list): list of names (strings) involved
        idNum (int): todo id number, assigned in order of creation
        complete (boolean): boolean denoting if todo is complete
        status (string): either Completed or Ongoing
    """
    ###################
    # Special Methods #
    ###################
    def __init__(self, label, dueDate, priority, category, people, idNum):
        """
        Initialize a ToDo object

        Parameters:
            label (string): title of the todo
            dueDate (string): todo due date string (MM/DD/YYYY)
            priority (string): todo completion priority
            category (string): todo category
            people (list): list of strings of people involved
            idNum (int): todo id number, assigned in order of creation 
        """
        parsed_date = self._parse_date(dueDate)

        # Validate the processed data (expects date object, not string)
        validateAttributes(label, parsed_date, priority, category, people, idNum)

        # Assign attributes if validation passed
        self.label = label
        self.dueDate = parsed_date
        self.priority = priority
        self.category = category
        self.people = people
        self.idNum = idNum

        self.complete = False
        self.status = "Ongoing"

    def __str__(self):
        """Defines how todo objects are represented as strings"""
        date_display = self.dueDate.strftime("%m/%d/%Y") if self.dueDate else "N/A"
        people_str = ", ".join(self.people) if self.people else "None"
        return (
            f"Task {self.idNum}: {self.label}\n"
            f"Category: {self.category}\n"
            f"People: {people_str}\n"
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
            if isinstance(value, list): # Handle list of people
                for item in value:
                    if term in str(item).lower():
                        return True
            elif term in str(value).lower():
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
        # If it's already a date object, return it
        if isinstance(date_str, (date, datetime)):
            return date_str

        # Allow explicit empty values (None, "None", "") to be valid None dates
        if date_str is None:
            return None
            
        if isinstance(date_str, str):
            if not date_str.strip() or date_str.lower() == "none":
                return None
        
            try:
                return datetime.strptime(date_str.strip(), "%m/%d/%Y").date()
            except ValueError:
                # If string exists but isn't a date, that's an error!
                raise ValueError(f"Invalid date format: '{date_str}'. Use MM/DD/YYYY.")
        
        return None

    ###################
    # Editing Methods #
    ###################
    def editLabel(self, newVal):
        """
        Edit the label of an existing todo
        """
        validateAttributes(newVal, self.dueDate, self.priority, self.category, self.people, self.idNum)
        self.label = newVal
        print(f"Label saved as {newVal}\n")

    def editDueDate(self, newVal):
        """
        Edit the due date of an existing todo
        """
        new_date_obj = self._parse_date(newVal)
        validateAttributes(self.label, new_date_obj, self.priority, self.category, self.people, self.idNum)
        self.dueDate = new_date_obj
        date_display = new_date_obj.strftime("%m/%d/%Y") if new_date_obj else "N/A"
        print(f"Due Date saved as {date_display}\n")

    def editPriority(self, newVal):
        """
        Edit the priority of an existing todo
        """
        new_priority = PRIORITYDICT[newVal]
        validateAttributes(self.label, self.dueDate, new_priority, self.category, self.people, self.idNum)
        self.priority = new_priority
        print(f"Priority set to {new_priority}\n")

    def editCategory(self, newVal):
        """
        Edit the category of an existing todo
        """
        validateAttributes(self.label, self.dueDate, self.priority, newVal, self.people, self.idNum)
        self.category = newVal
        print(f"Category saved as {newVal}\n")

    def editPeople(self, newVal):
        """Edit the people involved in an existing todo"""
        validateAttributes(self.label, self.dueDate, self.priority, self.category, newVal, self.idNum)
        self.people = newVal
        people_str = ", ".join(newVal) if newVal else "None"
        print(f"People involved saved as: {people_str}\n")

    def toggleComplete(self, choice):
        """
        Mark an existing todo as complete or ongoing
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