# Supporting Documentation Guide For Collaborative TODO Manager Application (CTMA)

## 1. User Manual (CLI Reference)

### A. Core Commands
The application is entirely menu-driven. The user must navigate the main menu after running the program (`python main.py`).

| Option # | Description | Functionality |
|-----------|--------------|----------------|
| 0 | Exit CTMA | Saves all data to `data.json` and closes the application. |
| 1 | Create a task | Prompts for Label, Due Date, Priority (1–4), and Category. |
| 2 | Edit a task | Prompts to select a task, then provides a sub-menu to edit Label, Due Date, Priority, Category, or Completion. |
| 3 | Delete a task | Prompts to select a task and permanently removes it from the list. |
| 4 | Change a task's completion | Prompts to select a task, then set its status to 1: Complete or 2: Ongoing. |
| 5 | View tasks | Prompts to select 0: Simple (just Task # and Label) or 1: Detailed (full task info). |
| 6 | Search tasks | Prompts for a search term and returns tasks where the term matches the Label, Category, or Priority. |

---

### Export to Sheets

### B. Priority Levels
The system uses numeric input for setting or changing priority:

- **1:** None  
- **2:** Low  
- **3:** Medium  
- **4:** High  

---

## 2. Technical Requirements (Milestone 2 Focus)

### A. Functional Requirements (Implemented)

- **FR-1.0:** The system shall support all CRUD operations on a list of ToDo objects.  
- **FR-1.1 (Persistence):** The system shall save and load task data to/from a local file named `data.json` using JSON serialization.  
- **FR-1.2 (Categorization):** Tasks shall be organizable by a user-defined category string.  
- **FR-1.3 (Completion):** Tasks shall be toggleable between "Ongoing" (False) and "Complete" (True) statuses.  
- **FR-1.4 (Search/Filter):** The system shall allow searching by a single term across the task's label, category, or priority fields.  
- **FR-1.5 (Re-indexing):** Upon deletion of a task, the system shall automatically re-index the `idNum` for all remaining tasks.  

---

### B. Data Validation and Error Handling

- **DV-1.0:** Task label must be non-empty (validated in `createTodo`).  
- **DV-2.0:** Task priority input must be a valid key (1–4) in the `PRIORITYDICT` (validated in `createTodo` and `editTodo`).  

- **EH-1.0:** All user menu choices must be valid integers within the displayed range (handled by `try-except ValueError` and range checks in menu functions).  
- **EH-2.0:** Attempting to delete or edit a non-existent task number must be handled gracefully with an error message (`IndexError` in `handler.py`).  
