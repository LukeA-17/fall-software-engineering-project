# Software Requirements Specification (SRS)

*Based on ISO/IEC/IEEE 29148:2018*

---

## 1. Introduction

### 1.1 Purpose

Specify the software requirements for the Collaborative ToDo Manager Application (CTMA) for the transition from a prototype command-line interface (CLI) to a graphical user interface (GUI).

### 1.2 Scope

This software product is a task management tool for organizing, prioritizing, and tracking tasks. The objective is to replace the CLI with a GUI while maintaining the core functionality. The benefits of this are ease of use, and clearer visual presentation.

### 1.3 Definitions, Acronyms, and Abbreviations

- CTMA: Collaborative ToDo Manager Application
- GUI: Graphical User Interface
- CLI: Command-line interface
- CRUD: Create, Read, Update, Delete. The four basic functions for task management
- ToDo Object: Data structure representing a task
- Tkinter: Tk interface. A Python package to implement a GUI.

### 1.4 References

- `data.json`: Application data storage file.
- `todo.py`: Core `ToDo` object class.
- `handler.py`: Application logic and CLI interface.
- `gui.py`: Module for GUI implementation using Tkinter.

### 1.5 Overview

Section 1 serves as an introduction to the document. Section 2 describes the product. Section 3 lists specific requirements of the project.

---

## 2. Overall Description

### 2.1 Product Perspective

This CTMA is a standalone application, but it can be used for a wide variety of workflows. 

### 2.2 Product Functions

This software allows for all the basic operations (CRUD)

### 2.3 User Classes and Characteristics

- Standard User: Intuitive, simple interface
- Project Manager: Needs categories and sorting to keep track of multiple streams of tasks.

### 2.4 Operating Environment

This application is designed to run on a locam machine running Python 3.10 or greater with the Tkinter library for the GUI.

### 2.5 Design and Implementation Constraints

- Language: Python
- GUI Toolkit: Tkinter
- Data format: Task data persists in `data.json` file

### 2.6 Assumptions and Dependencies

The user has a compatible Python environment installed with tkinter.

---

## 3. Specific Requirements

### 3.1 Functional Requirements

1. A Home Page should provide an overview of tasks with easy navigation options for the application.

2. The number of tasks should be displayed on the Home Page view

3. Clicking on a view button (e.g., 'All', 'Completed') should take you to the corresponding task view page.

4. The task view page should display a scrollable list of tasks that match the current filter.

5. Each task in the list should have a checkbox to toggle the task's completion status. 

6. A completed task should be displayed as grayed out.

7. Each task should indicate it's priority level based on the background color. (High=red, Medium=orange, Low=yellow).

8. A task that is past due should be indicated as such when it is not complete.

9. The view page should have a sort dropdown menu with different options to sort the list of tasks.

10. Clicking on the 'Add Task' button takes you to a new page to create a task.

11. The 'Create Task' page should have form input fields for the task label, due date, priority, and category.

12. The system should validate that the task label is not empty.

13. The system should validate that the due date is in the correct format (MM/DD/YYYY).

14. Clicking on the "..." next to a task take's you to that task's edit page.

15. The edit task page should have a delete option that has you confirm before removing it.

### 3.2 Non-Functional Requirements

1. The GUI should function and display properly across a wide range of screen sizes and resolutions.

2. The GUI should be responsive when loading a long list of tasks.

3. The code should be modular and organized, with interactions with the logic of the program occuring with the `todo_handler.py`
