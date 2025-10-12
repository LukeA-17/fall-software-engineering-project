# CTMA - Collaborative ToDo Manager Application
CTMA is the hottest up and coming ToDo manager out there! Keep track of every task you have, including their due dates, categories, and priorities with the simplicity of a command line interface.

## Features:
- Manage todos from multiple projects
- Add, edit, and mark tasks as complete
- Persistent data storage between sessions
- Simple command-line interface

## Requirements:
- Python 3.10 or higher

## Setup
- Download the CTMA folder, and move it into your chosen python environment
- Run main.py. CLI used to interact with the program.

## File Storage Functionality
- Saved list of ToDo tasks are stored in data.json
- data.json is located in the same folder as main.py
- If data.json does not exist on startup, the program adds it to the directory

## Creating a New Task
This is the point where you can validate your save data loaded succesfully.

Upon starting the program, the following prompt appears:

![CTMA Startup Menu](Documentation\Images\readme\startup.png)

To start the task creation process, type 1 and then enter.

The program will then prompt you for each trait of the new task

Enter your answers after the prompt. It should look something like this:

![CTMA New Task](Documentation\Images\readme\new_task.png)

You may view your tasks at any time by selecting 5 in the main menu, and then the desired view, like so:

![CTMA Task View](Documentation\Images\readme\view_task.png)

When you are done using the program, enter 0 into the main menu to save and close:

![CTMA Closure](Documentation\Images\readme\exit_CTMA.png)


## Troubleshooting
If you encounter errors, please contact the developers.

This section will be developed more over time.