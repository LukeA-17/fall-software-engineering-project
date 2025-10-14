# Software Requirements Specification (SRS)

*Based on ISO/IEC/IEEE 29148:2018*

---
## Table of Contents
1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [Specific Requirements](#3-specific-requirements)

## 1. Introduction

### 1.1 Purpose

This document describes the functional requirements, architecture, and system design for the Collaborative ToDo Manager Application (CTMA). CTMA is designed for students, professionals, and teams to organize, track, and collaborate on tasks and projects.

### 1.2 Scope

CTMA is intended to allow users to track and manage a variety of different todo items associated with different projects and activities. It's objective is to allow for comprehensive management and viewing of all todo items, benefiting the user by increasing productivity through allowing organizing, prioritizing, and tracking of tasks.

### 1.3 Definitions, Acronyms, and Abbreviations
**Definitions:**  
- CTMA: Collaborative ToDo Manager Application
- GUI: Graphical User Interface
- CLI: Command-line interface
- CRUD: Create, Read, Update, Delete. The four basic functions for task management
- ToDo Object: Data structure representing a task
- ToDo/Task Item:  Interchangeable description for something that needs to be completed. Has a label, due date, priority, and category
- Tkinter: Tk interface. A Python package to implement a GUI.

### 1.4 References
**Core Documents:**  
- [README](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/README.md)  
- [Design Document](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Core%20Documents/Design%20Document.md)  
- [Class Definition Document](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Core%20Documents/Class%20Definition.md)  
- [Project Launch Details](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Core%20Documents/Project%20Launch%20Details.md)  
- [Test Case Documentation](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Core%20Documents/Test%20Cases.md)  
- [AI Usage Log](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Core%20Documents/AI%20Usage%20Log.md)

**Useful folders:**
- [Documentation Folder](https://github.com/LukeA-17/fall-software-engineering-project/tree/main/Documentation)
- [Meeting Reports](https://github.com/LukeA-17/fall-software-engineering-project/tree/main/Documentation/Meeting%20Reports)


## 2. Overall Description

### 2.1 Product Perspective

CTMA is a standalone application, but is applicable to a wide variety of workflows. 

### 2.2 Product Functions

CTMA is designed to allow users to create and manage their tasks, following the basic operations of CRUD. This includes but is not limited to:
- Create new task
- Delete task
- View and sort through existing tasks
- Modify existing task
- Search existing tasks
- Save and load data between sessions

### 2.3 User Classes and Characteristics

CTMA users are expected to be students, professionals, teams, and individuals. Because this is a large scope of potential users, CTMA needs to be flexible to accommodate their different needs. For example:  
- Students might have a higher need for due date accessibility, because homework and exam deadlines are inflexible
- Professionals might need a greater degree of shareability of files to coordinate with others 
- Individuals might be more reliant on separating tasks by category so that they can separate their personal life from their professional life

### 2.4 Operating Environment

This application is designed to run on a local machine running Python 3.10 or greater with a working Tkinter library for GUI support.

### 2.5 Design and Implementation Constraints
- Language: Python
- GUI Toolkit: Tkinter
- Data format: Task data persists in `data.json` file

---

## 3. Specific Requirements

### 3.1 Functional Requirements
**CLI User Stories:**
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

**GUI Functional Requirements:**
- A Home Page should provide an overview of tasks with easy navigation options for the application.  
- The number of tasks should be displayed on the Home Page view
- Clicking on a view button (e.g., 'All', 'Completed') should take you to the corresponding task view page.
- The task view page should display a scrollable list of tasks that match the current filter.
- Each task in the list should have a checkbox to toggle the task's completion status. 
- A completed task should be displayed as grayed out.
- Each task should indicate it's priority level based on the background color. (High=red, Medium=orange, Low=yellow).
- A task that is past due should be indicated as such when it is not complete.
- The view page should have a sort dropdown menu with different options to sort the list of tasks.
- Clicking on the 'Add Task' button takes you to a new page to create a task.
- The 'Create Task' page should have form input fields for the task label, due date, priority, and category.
- The system should validate that the task label is not empty.
- The system should validate that the due date is in the correct format (MM/DD/YYYY).
- Clicking on the "..." next to a task takes you to that task's edit page.
- The edit task page should have a delete option that has you confirm before removing it.


### 3.2 Non-Functional Requirements

- The GUI should function and display properly across a wide range of screen sizes and resolutions.

- The GUI should be responsive when loading a long list of tasks.

- Modules should maintain high levels of separation between presentation, logic, and data layers

- Program should allow for easy transfer of data

### 3.3 External Interface Requirements

Users are expected to be able to interact with their program through both a command line interface and a general user interface, switching between the two at their leisure. Attached is the wireframe for the GUI:

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


### 3.4 Logical Database Requirements

CTMA utilizes layered (N-Tier) architecture for the system design. Project modules are categorized between data, logic, and presentation, with limited interdependency between these layers.

Data layer modules:  
- data.json (stores tasks between sessions)

Logic layer modules:
- todo.py (includes the ToDo Class and its methods)
- todo_handler.py (handles management of ToDo objects. Acts as the main bridge between presentation and data)

Presentation layer modules:
- cli.py (collects user input through the command line)
- gui.py (collects user input through a general user interface)

Other modules:
- main.py (program entry point)
- test_handler.py, test_todo.py (verify program works correctly)

The UML component diagram for CTMA is included in figure 1 below:

_Figure 1, CTMA component diagram:_

![CTMA Component Diagram](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Images/design_doc/component_diagram.png?raw=true)