# CTMA - Collaborative ToDo Manager Application
CTMA is the hottest up and coming ToDo manager out there! Keep track of every task you have, including their due dates, categories, and priorities with the simplicity of a command line interface.

## Table of Contents
1. [Features](#1-features)
2. [Setup](#2-setup)
3. [Command Line Usage Guide](#3-command-line-usage-guide)
4. [GUI Usage Guide](#4-gui-usage-guide)
5. [GitHub Issues Fixes](#5-github-issues-fixes)

## 1. Features
- Manage todos from multiple projects
- Add, edit, and mark tasks as complete
- Simple command-line interface
- Intuitive graphical user interface
- Multi-profile support
- Customizable themes
- Auto-saves settings and tasks on exit

**File Storage Functionality**
- settings.json: Stores your theme preference and a list of profiles.
- tasks.json: The default profile file where tasks are stored.
- Custom profiles: You may create additional `.json` files anywhere on your computer and link them via the Settings menu

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
### Home Dashboard
![Home Page](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Images/readme/home_page.png?raw=true)

This is the screen you are presented with upon launch.

* **Top Bar:** Displays the current date, the **Add Task** button, and the **Home** button. The home button will return you to this screen at any time.
* **Main Views:** Buttons to quickly filter tasks by "Due Today", "All" or "Completed".
* **Category Views:** Automatically generates buttons for every unique category (e.g., "School", "Work") found in your task list.
* **Bottom Bar:** Contains the **Settings** button and the **Exit CTMA** button.

### Creating and Editing Tasks
#### To Create a Task:
![Create Page](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Images/readme/create_page.png?raw=true)

1. Click **Add Task** in the top right corner.
2. Fill in the **Label**, **Due Date** (MM/DD/YYYY), **Category**, and **People Involved**.
3. Select a **Priority** (None, Low, Medium, High) from the dropdown.
4. Click **Save** to commit the task or **Paste Task** to fill fields from a copied task.

#### To Edit a Task:
![Edit Page](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Images/readme/edit_page.png?raw=true)

1. In the Task View, click the "..." button next to a task.
2. Update the desired fields.
3. You may also **Copy Task** to the clipboard or **Delete Task** from this menu.

### Viewing Tasks
![View Page](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Images/readme/view_page.png?raw=true)

* **Sorting:** Use the dropdown menu at the top to sort by **Priority**, **Due Date**, or **Label**.
* **Color Coding:** Tasks are color-coded by priority:
    * **Red:** High Priority
    * **Orange:** Medium Priority
    * **Yellow:** Low Priority
    * **Gray:** No Priority
* **Completion:** Click the checkbox on the left of a task to toggle it between Complete and Ongoing.
* **Past Due:** Tasks with due dates before the current day are marked as "Past Due".

### Settings
![Settings Page](https://github.com/LukeA-17/fall-software-engineering-project/blob/main/Documentation/Images/readme/settings_page.png?raw=true)

Click the **Gear** icon on the home page to access settings.
* **Theme Selection:** Choose between different visual themes.
* **Profile Management:** Switch between different save files (profiles), add new profiles, or delete existing ones.



## 5. GitHub Issues Fixes
### 1. 🟢 [Set up weekly meeting with instructor](https://github.com/LukeA-17/fall-software-engineering-project/issues/1)
- Weekly meeting scheduled for Mondays at 10:15 am

### 2. 🟢 [Milestone 2 Progress Report Status Section](https://github.com/LukeA-17/fall-software-engineering-project/issues/2)
- Addressed in commit [28cce9f](https://github.com/LukeA-17/fall-software-engineering-project/commit/28cce9f37ede544f4f717e122aa4378509c742e8)

### 3. 🟢 [Missing Docstrings](https://github.com/LukeA-17/fall-software-engineering-project/issues/3)
- Addressed in commit [073371b](https://github.com/LukeA-17/fall-software-engineering-project/commit/073371b66788189898ad80a14f5b652409c5dd0d)

### 4. 🟢 [todo module](https://github.com/LukeA-17/fall-software-engineering-project/issues/4)
- Addressed via issue [reply](https://github.com/LukeA-17/fall-software-engineering-project/issues/4#issuecomment-3399052808)

### 5. 🟢 [Snake case vs Camel Case](https://github.com/LukeA-17/fall-software-engineering-project/issues/5)
- Addressed via issue [reply](https://github.com/LukeA-17/fall-software-engineering-project/issues/5#issuecomment-3399048354)

### 6. 🟢 [if statements in user_flow.py](https://github.com/LukeA-17/fall-software-engineering-project/issues/6)
- Code has been restructured and user_flow.py no longer exists

### 7. 🟢 [No design document](https://github.com/LukeA-17/fall-software-engineering-project/issues/7)
- Initially addressed in commit [9cdd384](https://github.com/LukeA-17/fall-software-engineering-project/commit/9cdd3845a66e294be5ed38f0a42f5fb788d1262d)
- Further addressed in commit [7e050cf](https://github.com/LukeA-17/fall-software-engineering-project/commit/7e050cf463f9ed5683e4eebe5973e92367e0caff)

### 8. 🟢 [Missing Design Doc](https://github.com/LukeA-17/fall-software-engineering-project/issues/8)
- Initially addressed in commit [9cdd384](https://github.com/LukeA-17/fall-software-engineering-project/commit/9cdd3845a66e294be5ed38f0a42f5fb788d1262d)
- Further addressed in commit [7e050cf](https://github.com/LukeA-17/fall-software-engineering-project/commit/7e050cf463f9ed5683e4eebe5973e92367e0caff)

### 9. 🟢 [Missing test_cases.md document](https://github.com/LukeA-17/fall-software-engineering-project/issues/9)
- Addressed in commit [fd319b7](https://github.com/LukeA-17/fall-software-engineering-project/commit/fd319b7e1ca30ad2ca42e58c7d6016fdae3e322b)

### 10. 🟡 [Missing team video](https://github.com/LukeA-17/fall-software-engineering-project/issues/10)
- In progress

### 11. 🟢 [Missing AI log](https://github.com/LukeA-17/fall-software-engineering-project/issues/11)
- Addressed in commit [149115c](https://github.com/LukeA-17/fall-software-engineering-project/commit/149115c3e06d53f89c0cdfaeebfe581576873fc3) and [e352e0f](https://github.com/LukeA-17/fall-software-engineering-project/commit/e352e0fc74602a07ac4155cd9238262ecfe50c8b)

### 12. 🟢 [How many test cases do you have?](https://github.com/LukeA-17/fall-software-engineering-project/issues/12)
- Addressed in commit [f6ab7e0](https://github.com/LukeA-17/fall-software-engineering-project/commit/f6ab7e0163bb3d6ceb6d6a1dd05cbfc678129f53)

### 13. 🟢 [Incomplete README file](https://github.com/LukeA-17/fall-software-engineering-project/issues/13)
- Addressed in commits [feefc35](https://github.com/LukeA-17/fall-software-engineering-project/commit/feefc35a2dd2a885a128f64f8bd5adf242e46c91), [6bc2b02](https://github.com/LukeA-17/fall-software-engineering-project/commit/6bc2b02cc055311d6e23e9a003de698b6b5bc823), and [3beb20e](https://github.com/LukeA-17/fall-software-engineering-project/commit/3beb20e76be3840e46e6b7bd4e8f26d84c652275)

### 14. 🟢 [Missing file input loading option](https://github.com/LukeA-17/fall-software-engineering-project/issues/14)
- Addressed in commit [6bc2b02](https://github.com/LukeA-17/fall-software-engineering-project/commit/6bc2b02cc055311d6e23e9a003de698b6b5bc823) by adding a description of file storage to the README

### 15. 🟢 [M2 Results and Score](https://github.com/LukeA-17/fall-software-engineering-project/issues/15)
- Score feedback, no action needed

### 16. 🟡 [Commits](https://github.com/LukeA-17/fall-software-engineering-project/issues/16)
- In progress

### 17. 🟢 [No Class Diagram](https://github.com/LukeA-17/fall-software-engineering-project/issues/17)
- Addressed in commit [4e56ed6](https://github.com/LukeA-17/fall-software-engineering-project/commit/4e56ed6eb47a11367403479baf454b9672524508)

### 18. 🟢 [No Use Case Diagram](https://github.com/LukeA-17/fall-software-engineering-project/issues/18)
- Addressed in commit [202fdb5](https://github.com/LukeA-17/fall-software-engineering-project/commit/202fdb51407d11e1fa6586fc45adab84b0bd564d)

### 19. 🟢 [CLI usage example in README; GUI screenshots?](https://github.com/LukeA-17/fall-software-engineering-project/issues/19)
- Addressed in commit [59692c5](https://github.com/LukeA-17/fall-software-engineering-project/commit/59692c582f2babe1b42d160ac23cf1270f1f5dcb)

### 20. 🟡 [Issues from Milestone 2 some not closed](https://github.com/LukeA-17/fall-software-engineering-project/issues/20)
- In progress

### 21. 🟢 [Test Case Doc exists but is empty](https://github.com/LukeA-17/fall-software-engineering-project/issues/21)
- Addressed in commit [fd319b7](https://github.com/LukeA-17/fall-software-engineering-project/commit/fd319b7e1ca30ad2ca42e58c7d6016fdae3e322b)

### 22. 🟡 [Modifications from Previous Milestone](https://github.com/LukeA-17/fall-software-engineering-project/issues/22)
- In progress

### 23. 🟡 [GUI Design](https://github.com/LukeA-17/fall-software-engineering-project/issues/23)
- In progress

### 24. 🟡 [Recommendations for code improvements](https://github.com/LukeA-17/fall-software-engineering-project/issues/24)
- In progress

### 25. 🟡 [Long methods in Code](https://github.com/LukeA-17/fall-software-engineering-project/issues/25)
- In progress

### 26. 🟡 [Code Changes + GUI Implementation](https://github.com/LukeA-17/fall-software-engineering-project/issues/26)
- In progress

### 27. 🟡 [Class Definition & Documentation needs improvement](https://github.com/LukeA-17/fall-software-engineering-project/issues/27)
- In progress

### 28. 🟡 [SRS Doc](https://github.com/LukeA-17/fall-software-engineering-project/issues/28)
- In progress

### 29. 🟡 [Supporting Doc](https://github.com/LukeA-17/fall-software-engineering-project/issues/29)
- In progress

### 30. 🟡 [AI-Assisted Architecture Review Bonus Points](https://github.com/LukeA-17/fall-software-engineering-project/issues/30)
- In progress

### 31. 🟢 [General Observations](https://github.com/LukeA-17/fall-software-engineering-project/issues/31)
- Feedback - no action needed. The team will continue to use this as a reference for further improvements

### 32. 🟢 [Results](https://github.com/LukeA-17/fall-software-engineering-project/issues/32)
- Score feedback, no action needed

### 34. 🟢 [File Path Support for Different Platforms](https://github.com/LukeA-17/fall-software-engineering-project/issues/34)
- Addressed in commit [dee7a1c](https://github.com/LukeA-17/fall-software-engineering-project/commit/dee7a1ca61ca9bf95d5247367384e274645aef98)