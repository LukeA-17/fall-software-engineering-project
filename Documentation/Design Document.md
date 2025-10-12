## 1. Introduction and Overview
### 1.1 Purpose and Scope
This document includes the engineering description and architectural design of the first prototype of the Command-Line Interface (CLI) of the Collaborative TODO Manager Application (CTMA), written in Python. Specifically, it addresses the fundamental CRUD (Create, Read, Update, Delete) functionality created during Milestone 2 and provides the framework on which the subsequent Graphical User Interface (GUI) and collaboration among multiple users features are to be built.

### 1.2 Architectural Pattern: Layered CLI (MVC-Style)
The existing architecture follows a Layered Design Pattern, with strict separation of presentation, business logic and data modeling, to provide high modularity and testability.

| **Layer**                 | **Component/File**                         | **Responsibility** |
|----------------------------|--------------------------------------------|--------------------|
| **Presentation (CLI)**     | `main.py`, `user_flow.py` (Menus)          | Handles program entry, displays the main menu, validates user navigation choices, and manages program exit/persistence calls. |
| **Business/Application Logic** | `handler.py` / `user_flow.py` (Functional Methods) | Manages the application state (`todoList`), orchestrates task manipulation, implements search/filtering, and enforces business rules. |
| **Data/Model Logic**       | `todo.py` (the ToDo class)                 | Defines the data structure and provides object-specific mutation methods. This layer is central to the Milestone 2 “No-AI Zone.” |
| **Configuration/Testing**  | `context.py`, `constants.py`, `test_*` files | Stores static configurations (Priority Map) and houses all unit and integration testing logic (Pytest). |
| **Persistence**            | `handler.py` (`loadSave`, `saveData`)      | Manages robust file I/O using JSON serialization to persist the in-memory `todoList` state. |

_Table 1 Layered Architecture and Component Responsibilities_

## Data Model and Core Logic (No-AI Zone)
### 2.1 Core Data Model: ToDo Class Specification (todo.py)

The ToDo class encapsulates all task data and internal mutation methods, ensuring data integrity is controlled at the object level.

| **Attribute** | **Data Type** | **Description** |
|----------------|----------------|-----------------|
| `label` | String | Task title/name. Must be non-empty upon creation. |
| `dueDate` | String | Task deadline (currently accepts unvalidated string input). |
| `priority` | String | Task priority (Mapped from keys in `PRIORITYDICT` in `context.py`). |
| `category` | String | Used for organizational filtering. |
| `idNum` | Integer | 1-indexed identifier used for user selection in the CLI. Automatically re-indexed upon task deletion. |
| `complete` | Boolean | Internal status tracking (`True = Complete`, `False = Ongoing`). |
| `status` | String | Display status ("Ongoing" or "Complete"). |

_Table 2 Class Data Model Specification_

### 2.2 Data Persistence and I/O (handler.py)

- Mechanism: The tasks are kept in the memory in the form of handler.todoList. The list is serialize to dictionary format and dumped to data.json.
- As shown, loading (loadSave) reads the JSON dictionary and recreates the list of ToDo objects, restoring the state of the application.
- Error Handling: try... except FileNotFoundError: This provides a clean boot to new users, loading a blank data.json so that all can begin with empty data.json... Input validation in the handlers acts as a safeguard against catastrophic failure.

### 2.3 Core CRUD Implementation Details (handler.py)

The functions below represent the primary implementation of the No-AI Zone business logic:

| **Operation** | **Method(s)** | **Key Implementation Details** |
|----------------|----------------|--------------------------------|
| **Create (C)** | `createTodo` | Validates label is non-empty. Maps user input (1–4) to string priority levels (`PRIORITYDICT`). |
| **Read (R)** | `viewTodos`, `viewTodosInfoed`, `search` | `viewTodos` (simple list) supports task selection; `viewTodosInfoed` provides full task detail (`ToDo.__str__`). `search` performs a case-insensitive match on Label, Category, and Priority. |
| **Update (U)** | `editTodo`, `changeCompletion` | Uses a declarative dictionary of lambda functions to map CLI menu choices to specific `ToDo` object mutation calls. |
| **Delete (D)** | `deleteTodo` | Removes the task via `todoList.pop(selection - 1)`. Crucially, it re-indexes all remaining tasks by iterating and resetting the `idNum` attribute to maintain sequence integrity (`NFR-1.1`). |

_Table 3 Core CRUD Implementation Details and No-AI Zone Logic_

![View of visual studio code running CTMA](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Images/design_doc/visual_studio_view.png?raw=true)

_Figure 2 A screenshot of the console showing the output of View Tasks (Detailed) to demonstrate the ToDo.__str__ formatting_

## 3. Testing and Quality Assurance
### 3.1 Testing Strategy

Strict testing is enforced on the Pytest framework in two levels: unit and integration testing.

#### Unit Tests (test_todo.py)
These tests focus exclusively on the Data Model Layer (todo.py), confirming object reliability:
- Validation of object initialization and data integrity.
- Verification of the __str__ and printLabel output formats.
- Confirmation of correct data mutation via editLabel, editPriority, and toggleComplete.

#### Integration/Handler Tests (test_handler.py)
These tests focus on the Application Logic Layer and system flow:

- Persistence: test_loadsave and test_savedata check the proper reading/writing of data to/from the mocked data.json.
- Data integrity: test_delete_todo has an explicit assertion that the re-indexing logic is followed correctly when a task is deleted.
- Input Handling: Tests are used to check that the application can process invalid numeric data (test_invalid_selection) and that a required field exists (test_invalid_create).

![Screenshot of test cases](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Images/design_doc/tests_running.png?raw=true)

_Figure 3 A screenshot of the console showing Pytest running, verifying all tests (test_handler.py and test_todo.py) have successfully passed_