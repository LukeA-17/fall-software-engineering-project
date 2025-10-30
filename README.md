# CTMA - Collaborative ToDo Manager Application
CTMA is the hottest up and coming ToDo manager out there! Keep track of every task you have, including their due dates, categories, and priorities with the simplicity of a command line interface.

## Table of Contents
1. [Features](#1-features)
2. [Setup](#2-setup)
3. [Command Line Usage Guide](#3-command-line-usage-guide)
4. [GUI Usage Guide](#3-gui-usage-guide)
5. [GitHub Issues Fixes](#5-github-issues-fixes)

## 1. Features
- Manage todos from multiple projects
- Add, edit, and mark tasks as complete
- Persistent data storage between sessions
- Simple command-line interface

**File Storage Functionality**
- Saved list of ToDo tasks are stored in data.json
- data.json is located in the same folder as main.py
- If data.json does not exist on startup, the program adds it to the directory

## 2. Setup
**Requires Python 3.10 or higher**
- Download the CTMA folder, and move it into your chosen python environment
- Run main.py. CLI used to interact with the program.

## 3. Command Line Usage Guide

### Creating a New Task:
This is the point where you can validate your save data loaded succesfully.

Upon starting the program, the following prompt appears:

![CTMA Startup Menu](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Images/readme/startup.png?raw=true)

To start the task creation process, type 1 and then enter.

The program will then prompt you for each trait of the new task

Enter your answers after the prompt. It should look something like this:

![CTMA New Task](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Images/readme/new_task.png?raw=true)

You may view your tasks at any time by selecting 5 in the main menu, and then the desired view, like so:

![CTMA Task View](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Images/readme/view_task.png?raw=true)

When you are done using the program, enter 0 into the main menu to save and close:

![CTMA Closure](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Images/readme/exit_CTMA.png?raw=true)

## 4. GUI Usage Guide
## 5. GitHub Issues Fixes


