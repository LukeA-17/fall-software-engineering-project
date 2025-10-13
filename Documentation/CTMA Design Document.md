# CTMA Design Document
This document describes the functional requirements, architecture, and system design for the Collaborative ToDo Manager Application (CTMA). CTMA is designed for students, professionals, and teams to organize, track, and collaborate on tasks and projects.

## Table of Contents
1. [Requirements](#1-requirements)
2. [System Design](#2-system-design)
3. [Interface Design](#3-interface-design)

## 1. Requirements
### High Level Functionality 
CTMA is intended to allow users to track and manage a variety of different todo items associated with different projects and activities. This includes but is not limited to the ability to:  
- Create new tasks
- Delete tasks
- View and sort through existing tasks
- Modify existing taks
- Search existing tasks
- Save and load data between sessions

Users will have the option to interact with the program through both a command line interface (CLI) and a general user interface (GUI).

### User Stories
- As a student, I want to be able to categorize my tasks by their associated class
- As a project manager, I want to be able to give each task a specific priority and deadline
- As a user, I want to be able to quickly locate a task with a keyword

### CLI Use Cases
- User selects the create task option, enters a label, due date, priority, and category, and adds a new task with those attributes
- User selects the search options, enters a key word or phrase, and views all tasks related to that word or phrase
- User selects a task and marks it as complete
- User selects a task and marks it as incomplete
- User closes the program, then starts the program, selects the view task selection, and is able to view the tasks that existed in the previous session
- User selects the delete task option, selects the task number to be deleted, and deletes the task
- User selects the edit task option, selects the task to be edited, selects the label option, and renames the task
- User selects the search option, enters "High," and is able to see all high priority tasks
- User selects view task, then detailed view, and is presented with information on all existing tasks
- User selects edit a task, selects the task they wish to edit, selects the category attribute, enters a new category for the task, and is presented with confirmation the category was changed


## 2. System Design
CTMA utilizes layered (N-Tier) architecture for the system design. Project modules are categorized between data, logic, and presentation, with limited interdependency between these layers.

Data layer modules:  
- data.json (stores tasks between sessions)

Logic layer modules:
- todo.py (includes the ToDo Class and its methods)
- todo_handler.py (handles management of ToDo objects. Acts as the main bridge between presentation and data)
- shared.py (shared memory during runtime)

Presentation layer modules:
- cli.py (collects user input through the command line)
- gui.py (collects user input through a general user interface)

Other modules:
- main.py (program entry point)
- test_handler.py, test_todo.py (verify program works correctly)

The UML component diagram for CTMA is included in figure 1 below:

_Figure 1, CTMA component diagram:_

![CTMA Component Diagram](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Images/design_doc/component_diagram.png?raw=true)

Data flow:
- To be included at a later date

## 3. Interface Design
The GUI will be developed by building on the following wireframes.

Home Page Wireframe:  
![Home Page Wirefram](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Images/design_doc/wireframe/Home%20Page.png?raw=true)

Create Task Wireframe:  
![Create Task Wirefram](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Images/design_doc/wireframe/createTask.png?raw=true)

Edit Task Wireframe:  
![Edit Task Wireframe](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Images/design_doc/wireframe/editTask.png?raw=true)

Task View Wireframe:  
![Task View Wireframe](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Images/design_doc/wireframe/taskview.png?raw=true)

Settings Wireframe:  
![Settings Wireframe](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Images/design_doc/wireframe/settings.png?raw=true)