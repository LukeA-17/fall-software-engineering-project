"""
shared.py stores the variables that more than one module needs access to
"""
#############
# Constants #
#############
# mapping of numbers to priorities
PRIORITYDICT = {
    "1": "None",
    "2": "Low",
    "3": "Medium",
    "4": "High"  
}

############
# Dynamics #
############
todoList = [] # stores todo objects during runtime