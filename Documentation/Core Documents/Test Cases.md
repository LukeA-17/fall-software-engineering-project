# CTMA Unit Test Documentation

**Testing Framework:** Pytest  
**Module:** `test_ctma.py`  
**Coverage:** Core logic in `todo.py` and `todo_handler.py`.

---

## Use Case 1: Create New Task

### Test 1.1: `test_handler_create_task_success`
* **Description:** Verifies adding a new task to the global todoList.
* **Use Case:** User creates a new task with all attributes.
* **Inputs:**
    * Initial State: List of 3 mock tasks.
    * Action: `todo.ToDo` object initialized with valid data.
* **Expected Outputs:** The global `todoList` size increases to 4. The new task is assigned ID #4.
* **Pass Criteria:** `len(th.todoList) == 4` AND `th.todoList[3].idNum == 4`.

### Test 1.2: `test_handler_create_task_failure_invalid_date`
* **Description:** Checks that creating a task with an invalid date string raises a ValueError.
* **Use Case:** User attempts to create a task with an invalid date format.
* **Inputs:**
    * Action: `todo.ToDo` object initialized with Date String `"12-01-2025"` (Incorrect format).
* **Expected Outputs:** The system raises a `ValueError`.
* **Pass Criteria:** `pytest.raises(ValueError)` catches the exception.

---

## Use Case 2: Search Tasks (Keyword)

### Test 2.1: `test_search_by_keyword_success`
* **Description:** Verifies the search function returns all tasks whose label or category contains the keyword.
* **Use Case:** User searches for a key word or phrase.
* **Inputs:**
    * Search Term: `"Project"`
* **Expected Outputs:** A list containing the specific task labeled "Group Project Milestone 03".
* **Pass Criteria:** Result list length is 1 AND result item label matches "Group Project Milestone 03".

### Test 2.2: `test_search_by_keyword_failure_no_match`
* **Description:** Verifies the search function correctly returns an empty list when no tasks match the keyword.
* **Use Case:** User searches for a non-existent word.
* **Inputs:**
    * Search Term: `"Zyxwv"`
* **Expected Outputs:** An empty list `[]`.
* **Pass Criteria:** Result list length is 0.

---

## Use Case 3: Mark Task Complete/Incomplete

### Test 3.1: `test_toggle_complete_success_complete`
* **Description:** Verifies the task is correctly marked as complete.
* **Use Case:** User selects a task and marks it as complete.
* **Inputs:**
    * Initial State: `complete=False`
    * Action: Toggle with choice `1`.
* **Expected Outputs:** Task attribute `complete` is `True` and `status` is `"Complete"`.
* **Pass Criteria:** `task.complete is True` AND `task.status == "Complete"`.

### Test 3.2: `test_toggle_complete_success_incomplete`
* **Description:** Verifies the task is correctly marked as incomplete from a completed state.
* **Use Case:** User selects a task and marks it as incomplete.
* **Inputs:**
    * Initial State: `complete=True`
    * Action: Toggle with choice `2`.
* **Expected Outputs:** Task attribute `complete` is `False` and `status` is `"Ongoing"`.
* **Pass Criteria:** `task.complete is False` AND `task.status == "Ongoing"`.

---

## Use Case 4: Save and Load Data (Persistence)

### Test 4.1: `test_save_data_success`
* **Description:** Verifies `th.saveData` creates the correct JSON structure for tasks and settings.
* **Use Case:** User closes the program (triggering save).
* **Inputs:**
    * State: 3 mock tasks loaded in memory.
    * Action: `th.saveData()` called with mocked file I/O.
* **Expected Outputs:** Valid JSON string written to file handle matching the properties of the mock tasks.
* **Pass Criteria:** The JSON data written to the mock file contains "Group Project Milestone 03".

### Test 4.2: `test_load_data_success`
* **Description:** Verifies `th.loadSave` successfully restores tasks from a file.
* **Use Case:** User starts the program (triggering load).
* **Inputs:**
    * File System: Mocked `tasks.json` containing 2 valid task definitions.
* **Expected Outputs:** `th.todoList` is populated with 2 `ToDo` objects matching the file data.
* **Pass Criteria:** `len(th.todoList) == 2` AND first task label matches "Loaded Task A".

---

## Use Case 5: Delete Task

### Test 5.1: `test_delete_task_success_reindex`
* **Description:** Verifies a task is deleted and the remaining tasks are correctly re-indexed.
* **Use Case:** User selects the delete task option and confirms deletion.
* **Inputs:**
    * Initial State: Tasks [1, 2, 3].
    * Action: Delete Task ID 1.
* **Expected Outputs:** List size reduces to 2. The task originally at ID 2 is re-assigned ID 1.
* **Pass Criteria:** `len(th.todoList) == 2` AND `th.todoList[0].idNum == 1`.

### Test 5.2: `test_delete_task_failure_invalid_id`
* **Description:** Verifies that deleting a non-existent ID fails gracefully and preserves the list.
* **Use Case:** User attempts to delete a task with a non-existent ID.
* **Inputs:**
    * Action: Delete Task ID 999.
* **Expected Outputs:** List size remains unchanged. Error message printed to standard out.
* **Pass Criteria:** `len(th.todoList)` equals initial length AND "Error: Task not found" in captured output.

---

## Use Case 6: Edit Task Label

### Test 6.1: `test_edit_label_success`
* **Description:** Verifies the task's label attribute can be successfully changed.
* **Use Case:** User selects edit task, selects label, and renames the task.
* **Inputs:**
    * New Label: `"Submit Quarterly Report"`
* **Expected Outputs:** The task object's label attribute is updated.
* **Pass Criteria:** `task.label == "Submit Quarterly Report"`.

### Test 6.2: `test_edit_label_failure_empty_string`
* **Description:** Verifies the task's label attribute cannot be changed to an empty string.
* **Use Case:** User attempts to clear the label.
* **Inputs:**
    * New Label: `""` (Empty string).
* **Expected Outputs:** System raises `ValueError`.
* **Pass Criteria:** `pytest.raises(ValueError)` catches the exception.

---

## Use Case 7: Search by Priority

### Test 7.1: `test_search_by_priority_success`
* **Description:** Verifies the search function returns all tasks matching a specific priority level.
* **Use Case:** User selects search option and enters "High".
* **Inputs:**
    * Search Term: `"High"`
* **Expected Outputs:** A list containing only the tasks with "High" priority.
* **Pass Criteria:** `len(found_tasks) == 2` AND all items in list have `priority == "High"`.

### Test 7.2: `test_search_by_priority_failure_none`
* **Description:** Verifies the search function returns an empty list when searching for a priority level that has no matching tasks.
* **Use Case:** User searches for an unused priority level.
* **Inputs:**
    * Search Term: `"None"`
* **Expected Outputs:** An empty list `[]`.
* **Pass Criteria:** `len(found_tasks) == 0`.

---

## Use Case 8: View Tasks (Detailed)

### Test 8.1: `test_detailed_view_success_multiple_tasks`
* **Description:** Verifies all tasks are present and accessible in the handler list for viewing.
* **Use Case:** User selects view task, then detailed view.
* **Inputs:**
    * State: 3 mock tasks loaded.
* **Expected Outputs:** The list contains 3 objects, and their string representations contain the correct data.
* **Pass Criteria:** `len(th.todoList) == 3` AND string representation contains "Priority: High".

### Test 8.2: `test_detailed_view_success_empty_list`
* **Description:** Verifies the list is empty when no tasks have been created or loaded.
* **Use Case:** User selects view task in a fresh session.
* **Inputs:**
    * State: Empty list.
* **Expected Outputs:** List length is 0.
* **Pass Criteria:** `len(th.todoList) == 0`.

---

## Use Case 9: Edit Task Category

### Test 9.1: `test_edit_task_category_handler_success`
* **Description:** Verifies the handler function successfully updates a task's category.
* **Use Case:** User selects edit task, selects category, and enters new category.
* **Inputs:**
    * Task ID: 2
    * New Category: `"Trip Planning"`
* **Expected Outputs:** The specific task in the handler list is updated.
* **Pass Criteria:** `th.update_task_attributes` returns `True` AND `th.todoList[1].category == "Trip Planning"`.

### Test 9.2: `test_edit_task_attribute_failure_invalid_id`
* **Description:** Verifies an attribute update attempt on a non-existent task fails.
* **Use Case:** User attempts to edit a task with a non-existent ID.
* **Inputs:**
    * Task ID: 999
* **Expected Outputs:** The update function returns `False` and no data changes.
* **Pass Criteria:** `th.update_task_attributes` returns `False`.