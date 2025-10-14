Modern SRS Template (md format)
# Software Requirements Specification (SRS)

*Based on ISO/IEC/IEEE 29148:2018*

---

## 1. Introduction

### 1.1 Purpose

This document describes the functional requirements, architecture, and system design for the Collaborative ToDo Manager Application (CTMA). CTMA is designed for students, professionals, and teams to organize, track, and collaborate on tasks and projects.

### 1.2 Scope

CTMA is intended to allow users to track and manage a variety of different todo items associated with different projects and activities. It's objective is to allow for comprehensive management and viewing of all todo items, benefiting the user by increasing productivity through organization.

### 1.3 Definitions, Acronyms, and Abbreviations
**Definitions:**  
- CTMA: Stands for Collaborative Todo Manager Application
- CLI: Stands for command line interface. cli.py is the module dedicated to handling command line presentation
- GUI: Stands for general user interface. gui.py is the module dedicated to handling the general user interface presentation
- ToDo/Task: Interchangeable description for an item that needs to be completed. Has a label, due date, priority, and category

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

---

## 2. Overall Description

### 2.1 Product Perspective

CTMA is a standalone application, but can be applied to any situation.

### 2.2 Product Functions

CTMA is designed to allow users to create and manage their tasks.

### 2.3 User Classes and Characteristics

Identify user types and their needs.  
*Tip: Use personas and user journey maps.*

CTMA users are expected to be students, professionals, teams, and individuals. Because this is a large scope of potential users, CTMA needs to be flexible to accommodate their different needs. Students might have a higher need for due dates, because homework and exam deadlines are inflexible. Professionals might need a greater degree of shareability of files to coordinate with others. Individuals might be more reliant on separating tasks by category so that they can separate their personal life from their professional life.

### 2.4 Operating Environment

CTMA can run on any system that supports Python 3.0 or greater. The machine must have some way to run python files.

### 2.5 Design and Implementation Constraints
CTMA is created entirely in Python.

### 2.6 Assumptions and Dependencies

CTMA is dependent on running Python.

---

## 3. Specific Requirements

### 3.1 Functional Requirements
CTMA is intended to allow users to track and manage a variety of different todo items associated with different projects and activities. This includes but is not limited to the ability to:  
- Create new tasks
- Delete tasks
- View and sort through existing tasks
- Modify existing tasks
- Search existing tasks
- Save and load data between sessions

User Stories:
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


### 3.2 Non-Functional Requirements

CTMA is expected to run without crashing, maintain high levels of separation between presentation, logic, and data layers, and allow for easy transfer of data.

### 3.3 External Interface Requirements

Describe interactions with hardware, software, and users.  
*Tip: Use interface mockups and DFDs.*

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


---