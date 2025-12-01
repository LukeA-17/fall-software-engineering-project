"""
gui.py presents the GUI, allowing for user interaction

Functions:
Class Management:
- set_styles(master, theme): Sets up custom styles and themes for the application widgets.
- CTMAGUI.__init__(master): Initializes the GUI, loads backend data, and displays the home page.
- CTMAGUI.clear_frame(): Removes all widgets from the main frame to clear the current page view.
- CTMAGUI.create_top_bar(parent, page_title): Creates the consistent top navigation bar with date and home controls.
- CTMAGUI.create_bottom_bar(parent): Creates the consistent bottom control bar with settings and exit buttons.
- CTMAGUI.create_view_button(parent, text, row, col, command): Helper to create and place main view buttons on the homepage.

Page Creation:
- CTMAGUI.load_home_page(): Creates and displays the dashboard with task status and category summaries.
- CTMAGUI.load_task_view_page(view_type, category): Loads the scrollable task list, filtered by status or category.
- CTMAGUI.load_create_task_page(): Displays the form interface for creating a new task.
- CTMAGUI.load_edit_task_page(task): Displays the form interface pre-filled with existing data for editing a task.
- CTMAGUI.load_settings_page(): Loads the settings page

Task Rendering:
- CTMAGUI.update_task_list_sort(new_sort_key): Updates the current sorting key and redraws the task list.
- CTMAGUI.update_task_list(): Clears and redraws tasks based on the current filters and sort order.
- CTMAGUI.draw_task_row(parent, task): Renders a single task row with priority styling and controls.
- CTMAGUI._create_task_form_widgets(parent_frame, is_new_task, task_id): Helper to draw common form fields for creating/editing tasks.
- CTMAGUI._create_form_row(parent_frame, label_text, row_num, textvariable): Helper to create a standard label and entry layout.

Task Interaction:
- CTMAGUI._submit_new_task_creation(): Validates form data and creates a new task in the backend.
- CTMAGUI._submit_task_update(): Validates form data and updates an existing task's attributes.
- CTMAGUI._confirm_delete_task(): Prompts the user for confirmation before deleting a task.
- CTMAGUI.copy_task(task): Copies a task object to the backend clipboard.
- CTMAGUI.paste_task(): Fills the current form with data from the previously copied task.
- CTMAGUI._get_unique_categories(): Returns a sorted list of unique categories from existing tasks.

System:
- CTMAGUI.exit_app(): Saves application data and destroys the window.
- start_gui(): Initializes the main Tkinter root and starts the event loop.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import todo_handler as th
from datetime import date
import sys


def set_styles(master, theme):
    """
    Sets up the custom styles and themes for the application.

    Args:
        master: The root Tkinter window instance.
        theme: The desired color scheme
    """
    style = ttk.Style(master)
    # line needed to override some OS's using their own style
    style.theme_use("clam")

    # Theme Name, background color, foreground color
    themeMap = {
        "UVU": ("#4C721D", "#061F00"),
        "Dark": ("#000000", "#FFFFFF"),
        "Light": ("#FFFFFF", "#3C2BD4"),
    }

    bg, fg = themeMap.get(theme, themeMap["UVU"])

    style.configure("TFrame", background=bg)
    style.configure(".", foreground=fg)

    # global label style
    style.configure("TLabel", background=bg)
    style.configure("Settings.TLabel", background=bg, foreground=fg, font=("Arial", 25))

    style.configure("TButton", foreground="black")
    style.configure("TCombobox", foreground="black", background="white")
    style.configure("TOptionmenu", foreground="black", background="white")
    style.configure("TEntry", foreground="black")

    # define style for main view buttons on the home page
    style.configure(
        "HomePage.TButton", font=("Arial", 10, "bold"), padding=10, foreground="black"
    )

    # define styles for task row frames based on priority

    # high
    style.configure("Task.High.TFrame", background="red", borderwidth=1, relief="solid")
    style.configure("High.TLabel", background="red")
    style.configure("High.TCheckbutton", background="red")

    # medium
    style.configure(
        "Task.Medium.TFrame", background="orange", borderwidth=1, relief="solid"
    )
    style.configure("Medium.TLabel", background="orange")
    style.configure("Medium.TCheckbutton", background="orange")

    # low
    style.configure(
        "Task.Low.TFrame", background="yellow", borderwidth=1, relief="solid"
    )
    style.configure("Low.TLabel", background="yellow", foreground="black")
    style.configure("Low.TCheckbutton", background="yellow")

    # none
    style.configure(
        "Task.None.TFrame", background="lightgray", borderwidth=1, relief="solid"
    )
    style.configure("None.TLabel", background="lightgray")
    style.configure("None.TCheckbutton", background="lightgray")

    # style for settings icon
    style.configure("Settings.TLabel", background=bg, foreground=fg, font=("Arial", 25))


class CTMAGUI:
    """
    Main class for the CTMA GUI.

    Manages the application state, page navigation, and user interface layout.
    """

    # =========================================
    # Initialization and State
    # =========================================

    def __init__(self, master):
        """
        Initializes the GUI, loads backend data, and displays the home page.

        Args:
            master: The root window.
        """
        self.master = master
        master.title("CTMA - Collaborative ToDo Manager")

        # Set a default window size
        master.geometry("600x600")

        # application state variables for task filtering and sorting
        self.current_view_type = "All"
        self.current_category = None
        self.current_sort_key = "Priority"

        try:
            th.loadSave()
        except ValueError as e:
            messagebox.showerror("Critical Error", f"{e}\nProgram Terminating")
            self.master.destroy()
            sys.exit()

        # apply styles
        set_styles(master, th.curTheme)

        # main frame for all page content
        self.main_frame = ttk.Frame(master, padding="10")
        self.main_frame.pack(fill="both", expand=True)

        self.load_home_page()

    # =========================================
    # Frame Management
    # =========================================

    def clear_frame(self):
        """
        Removes all widgets from the main_frame to clear the current page view.
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # =========================================
    # Layout Components
    # =========================================

    def create_top_bar(self, parent, page_title=""):
        """
        Creates the consistent top navigation bar

        Args:
            parent: The parent widget (usually self.main_frame).
            page_title: Optional title to display in the center of the bar.

        Returns:
            The created top_frame widget.
        """
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill="x", pady=(0, 20))

        # current date display
        today = date.today().strftime("%B %d, %Y")

        # home button
        home_label = ttk.Label(
            top_frame,
            text="⌂",
            style="Settings.TLabel",
        )
        home_label.pack(side="left", anchor="nw", padx=(0, 10))
        home_label.bind("<Button-1>", lambda e: self.load_home_page())

        # optional page title or centered date
        if page_title:
            ttk.Label(top_frame, text=page_title, font=("Arial", 14, "bold")).pack(
                side="left", padx=20, fill="x", expand=True
            )
        else:
            lbl = ttk.Label(
                top_frame,
                text=f"Current Date: {today}",
                font=("Arial", 12, "bold"),
                relief="solid",
                borderwidth=1,
                padding=5,
                anchor="center",  # Center text inside label
            )
            # Pack it to fill available space between left and right buttons
            lbl.pack(side="left", expand=True, padx=20)

        # add task button
        ttk.Button(
            top_frame, text="Add Task", command=self.load_create_task_page, width=12
        ).pack(side="right", anchor="ne")
        return top_frame

    def create_bottom_bar(self, parent):
        """
        Creates the consistent bottom control bar.

        Args:
            parent: The parent widget (usually self.main_frame).

        Returns:
            The created bottom_frame widget.
        """
        bottom_frame = ttk.Frame(parent)
        bottom_frame.pack(fill="x", side="bottom", pady=(20, 0))

        # settings button
        settings_label = ttk.Label(
            bottom_frame,
            text="⚙",
            style="Settings.TLabel",
            cursor="hand2",
        )
        settings_label.pack(side="left", anchor="sw", padx=10)
        settings_label.bind("<Button-1>", lambda e: self.load_settings_page())

        # exit CTMA button
        ttk.Button(
            bottom_frame, text="Exit CTMA", command=self.exit_app, width=12
        ).pack(side="right", anchor="se")
        return bottom_frame

    def create_view_button(self, parent, text, row, col, command):
        """
        Helper function to create and place the main view buttons on the homepage

        Args:
            parent: The parent frame (grid_frame)
            text: The text label for the button
            row: The row index in the grid
            col: The column index in the grid
            command: The function to call when the button is clicked
        """
        # frame for visual boundary and styling
        button_frame = ttk.Frame(parent, relief="solid", borderwidth=1)
        button_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        ttk.Button(
            button_frame, text=text, command=command, style="HomePage.TButton"
        ).pack(fill="both", expand=True)

    # =========================================
    # Page Loaders
    # =========================================

    def load_home_page(self):
        """
        Creates and displays the home page layout.
        """
        self.clear_frame()
        self.create_top_bar(self.main_frame)
        self.create_bottom_bar(self.main_frame)

        # container for the grid of view buttons
        grid_frame = ttk.Frame(self.main_frame)
        grid_frame.pack(pady=20, fill="x")

        # configure 3 columns
        for i in range(3):
            grid_frame.grid_columnconfigure(i, weight=1, uniform="group1")

        # --- ROW 1: Main Status Views ---

        # due today button
        self.create_view_button(
            grid_frame, "Due Today", 0, 0, lambda: self.load_task_view_page("Due Today")
        )

        # all tasks button
        num_tasks = len(th.todoList)
        self.create_view_button(
            grid_frame,
            f"All ({num_tasks})",
            0,
            1,
            lambda: self.load_task_view_page("All"),
        )

        # completed button
        completed_count = len([t for t in th.todoList if t.complete])
        self.create_view_button(
            grid_frame,
            f"Completed ({completed_count})",
            0,
            2,
            lambda: self.load_task_view_page("Completed"),
        )

        # --- Category Views ---

        category_grid_frame = ttk.Frame(self.main_frame)
        category_grid_frame.pack(fill="x", pady=5)

        for i in range(3):
            category_grid_frame.grid_columnconfigure(i, weight=1, uniform="cat_group")

        categories = self._get_unique_categories()
        for i, cat in enumerate(categories):
            row, col = divmod(i, 3)
            count = len([t for t in th.todoList if t.category == cat])

            self.create_view_button(
                category_grid_frame,
                f"{cat} ({count})",
                row,
                col,
                lambda c=cat: self.load_task_view_page(view_type="All", category=c),
            )

    def load_task_view_page(self, view_type="All", category=None):
        """
        Loads the Task Viewing page, filtered by status (view_type) or category.

        Args:
            view_type: The task status filter ('All', 'Due Today', 'Completed').
            category: The specific category filter (e.g., 'School', 'Work').
        """
        # update current state
        self.current_view_type = view_type
        self.current_category = category

        self.clear_frame()
        self.create_top_bar(self.main_frame)
        self.create_bottom_bar(self.main_frame)

        # control frame for sorting and view information
        controls_frame = ttk.Frame(self.main_frame)
        controls_frame.pack(fill="x", pady=5)

        # sort dropdown menu
        sort_options = ["Priority", "dueDate", "label"]
        self.sort_var = tk.StringVar(value=self.current_sort_key)

        sort_menu = ttk.OptionMenu(
            controls_frame,
            self.sort_var,
            self.current_sort_key,
            *sort_options,
            command=self.update_task_list_sort,
        )
        sort_menu.pack(side="left", anchor="w", padx=5, pady=5)

        # category/view information label
        cat_text = f"Category viewing ( {category if category else view_type} )"
        ttk.Label(controls_frame, text=cat_text, font=("Arial", 12, "bold")).pack(
            side="left", fill="x", expand=True, padx=20
        )

        # container for the scrollable list of tasks
        task_list_container = ttk.Frame(self.main_frame)
        task_list_container.pack(fill="both", expand=True, pady=10)

        bg_color = ttk.Style().lookup("TFrame", "background")

        # canvas for scrolling
        self.task_canvas = tk.Canvas(
            task_list_container, bg=bg_color, highlightthickness=0
        )
        self.task_canvas.pack(side="left", fill="both", expand=True)

        # scrollbar for the canvas
        task_scrollbar = ttk.Scrollbar(
            task_list_container, orient="vertical", command=self.task_canvas.yview
        )
        task_scrollbar.pack(side="right", fill="y")
        self.task_canvas.configure(yscrollcommand=task_scrollbar.set)

        # frame inside the canvas where task rows are drawn
        self.task_list_frame = ttk.Frame(self.task_canvas)
        self.task_canvas.create_window(
            (0, 0),
            window=self.task_list_frame,
            anchor="nw",
            width=self.task_canvas.winfo_width(),
        )

        # bind events to manage scrolling and resizing
        # update scroll region when the list frame's size changes
        self.task_list_frame.bind(
            "<Configure>",
            lambda _: self.task_canvas.configure(
                scrollregion=self.task_canvas.bbox("all")
            ),
        )
        # update the inner frame's width when the canvas's size changes
        self.task_canvas.bind(
            "<Configure>",
            lambda e: self.task_canvas.itemconfig(
                self.task_canvas.find_all()[0], width=e.width
            ),
        )

        self.update_task_list()

    def load_create_task_page(self):
        """
        Creates and displays the form for creating a new task
        """
        self.clear_frame()
        self.create_top_bar(self.main_frame, page_title="Create Task")

        form_frame = ttk.Frame(self.main_frame, padding="20")
        form_frame.pack(pady=20, padx=50, fill="x")

        # form fields setup
        self.current_task_vars = {
            "label": tk.StringVar(),
            "dueDate": tk.StringVar(),
            "priority": tk.StringVar(value=th.PRIORITYDICT["1"]),  # default to None
            "category": tk.StringVar(),
            "people": tk.StringVar(),
        }

        self._create_task_form_widgets(form_frame, is_new_task=True)

        # save/discard buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill="x", pady=20)
        button_frame.grid_columnconfigure((0, 1), weight=1, uniform="button_group")

        # Paste button
        ttk.Button(
            button_frame,
            text="Paste Task",
            command=lambda: self.paste_task(),
            style="HomePage.TButton",
        ).grid(row=0, column=0, padx=10, ipadx=20, pady=20, sticky="ew")

        # Save Button
        ttk.Button(
            button_frame,
            text="Save",
            command=self._submit_new_task_creation,
            style="HomePage.TButton",
        ).grid(row=1, column=0, padx=10, ipadx=20, sticky="ew")

        # Discard Button
        ttk.Button(
            button_frame,
            text="Discard",
            command=self.load_home_page,
            style="HomePage.TButton",
        ).grid(row=1, column=1, padx=10, ipadx=20, sticky="ew")

        self.create_bottom_bar(self.main_frame)

    def load_edit_task_page(self, task):
        """
        Loads the task editing page

        Args:
            task: The ToDo object to be edited
        """
        self.clear_frame()

        self.editing_task = task

        page_title = f"Edit: {task.label}"
        self.create_top_bar(self.main_frame, page_title=page_title)

        back_command = lambda: self.load_task_view_page(
            self.current_view_type, self.current_category
        )
        ttk.Button(
            self.main_frame, text="<< Back", command=back_command, width=10
        ).pack(side="top", anchor="w", pady=(0, 10), padx=5)

        form_frame = ttk.Frame(self.main_frame, padding="20")
        form_frame.pack(pady=20, padx=50, fill="x")

        # pre-fill form variables
        date_str = task.dueDate.strftime("%m/%d/%Y") if task.dueDate else ""
        people_str = (
            ", ".join(task.people) if task.people else ""
        )  # Convert list to string for display

        self.current_task_vars = {
            "label": tk.StringVar(value=task.label),
            "dueDate": tk.StringVar(value=date_str),
            "priority": tk.StringVar(value=task.priority),
            "category": tk.StringVar(value=task.category),
            "people": tk.StringVar(value=people_str),
        }

        self._create_task_form_widgets(form_frame, is_new_task=False)

        # Add copy button
        ttk.Button(
            form_frame,
            text="Copy Task",
            command=lambda: self.copy_task(task),
            style="HomePage.TButton",
        ).grid(row=6, column=0, pady=(10, 5), sticky="w")

        # delete and save/discard
        ttk.Button(
            form_frame,
            text="Delete Task",
            command=self._confirm_delete_task,
            style="HomePage.TButton",
        ).grid(row=6, column=9, columnspan=2, pady=(10, 5))

        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill="x", pady=10)
        button_frame.grid_columnconfigure((0, 1), weight=1, uniform="button_group")

        ttk.Button(
            button_frame,
            text="Save",
            command=self._submit_task_update,
            style="HomePage.TButton",
        ).grid(row=0, column=0, padx=10, ipadx=20)
        ttk.Button(
            button_frame, text="Discard", command=back_command, style="HomePage.TButton"
        ).grid(row=0, column=1, padx=10, ipadx=20)

        self.create_bottom_bar(self.main_frame)

    def load_settings_page(self):
        """
        Loads the Settings Page
        """
        ##### Initial construction #####
        self.clear_frame()
        self.create_top_bar(self.main_frame, page_title="Settings")

        settings_frame = ttk.Frame(self.main_frame)

        ##### Theme Section #####
        # Theme Selection Label
        ttk.Label(
            settings_frame, text="Theme Selection:", font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(0, 5))

        # Theme Combobox
        self.selected_theme = tk.StringVar()

        themeCombo = ttk.Combobox(
            settings_frame,
            textvariable=self.selected_theme,
            values=["UVU", "Dark", "Light"],
            state="readonly",
        )

        themeCombo.pack(anchor="w", pady=(0, 10), fill="x")
        self.selected_theme.set(th.curTheme)

        ##### Profile Management #####
        # Profile Label
        ttk.Label(settings_frame, text="Profiles:", font=("Arial", 11, "bold")).pack(
            anchor="w", pady=(10, 5)
        )

        # Profile Combobox
        self.selected_profile = tk.StringVar()

        profileCombo = ttk.Combobox(
            settings_frame,
            textvariable=self.selected_profile,
            values=list(th.fileDict.keys()),
            state="readonly",
        )
        profileCombo.pack(anchor="w", pady=(0, 5), fill="x")
        self.selected_profile.set("Default")

        # Profile Logic Functions
        def add_profile_logic():
            # Select File Path
            file_path = filedialog.askopenfilename(title="Select Profile File")

            if not file_path:
                return
            if not file_path.lower().endswith(".json"):
                messagebox.showerror(
                    "Invalid File", "Please select a valid .json file."
                )
                return

            # Name Profile
            profile_name = simpledialog.askstring(
                "Profile Name", "Enter a name for this profile:"
            )

            if profile_name:
                if profile_name in th.fileDict:
                    messagebox.showwarning(
                        "Error", "A profile with this name already exists."
                    )
                    return

                # Save to backend and update UI
                th.fileDict[profile_name] = file_path
                profileCombo["values"] = list(th.fileDict.keys())
                self.selected_profile.set(profile_name)
                messagebox.showinfo("Success", f"Profile '{profile_name}' added.")

        def delete_profile_logic():
            target = self.selected_profile.get()
            if not target:
                messagebox.showwarning(
                    "Selection Error", "Please select a profile to delete."
                )
                return

            confirm = messagebox.askyesno(
                "Confirm Delete", f"Are you sure you want to delete profile '{target}'?"
            )

            if confirm:
                if target == "Default":
                    messagebox.showinfo(
                        "Error", "You may not remove the default profile."
                    )
                    return

                del th.fileDict[target]
                profileCombo["values"] = list(th.fileDict.keys())
                self.selected_profile.set("")  # Clear selection
                messagebox.showinfo("Deleted", "Profile deleted successfully.")
                self.load_home_page()

        def apply_profile_logic():
            target = self.selected_profile.get()
            if not target:
                return
            try:
                th.changeProfile(target)
                messagebox.showinfo("Success", f"Profile switched to {target}")
                self.load_home_page()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        # Profile Buttons Frame
        # Create a sub-frame to hold the three buttons side-by-side
        btn_frame = ttk.Frame(settings_frame)
        btn_frame.pack(fill="x", pady=(0, 5))

        # Add Profile Button
        ttk.Button(btn_frame, text="Add Profile", command=add_profile_logic).pack(
            side="left", expand=True, fill="x", padx=(0, 5)
        )

        # Delete Profile Button
        ttk.Button(btn_frame, text="Delete Profile", command=delete_profile_logic).pack(
            side="left", expand=True, fill="x", padx=(0, 5)
        )

        # Apply Profile Button
        ttk.Button(btn_frame, text="Apply Profile", command=apply_profile_logic).pack(
            side="left", expand=True, fill="x", padx=(0, 0)
        )

        ##### Save Settings Logic #####
        def on_save():
            new_theme = self.selected_theme.get()

            # Save theme
            th.curTheme = new_theme
            set_styles(self.master, new_theme)

            messagebox.showinfo("Info Alert", "Settings Saved Successfully!")

        ##### Main Save Button #####
        ttk.Button(settings_frame, text="Save Settings", command=on_save).pack(
            pady=(10, 0), fill="x"
        )

        ##### Bottom bar #####
        self.create_bottom_bar(self.main_frame)

        ##### Render Frame #####
        settings_frame.pack(fill="x", padx=50)

    # =========================================
    # Task List Display
    # =========================================

    def update_task_list_sort(self, new_sort_key):
        """
        Updates the sorting key and redraws the task list.

        Args:
            new_sort_key: The new attribute to sort tasks by ('Priority', 'dueDate', 'label').
        """
        self.current_sort_key = new_sort_key
        self.update_task_list()

    def update_task_list(self):
        """
        Clears the task list frame and redraws tasks based on the current filters and sort order.
        """
        # clear existing task rows
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        # get filtered and sorted tasks from the handler
        tasks_to_display = th.get_tasks_for_view(
            view_type=self.current_view_type,
            category=self.current_category,
            sort_key=self.current_sort_key,
        )

        if not tasks_to_display:
            ttk.Label(
                self.task_list_frame,
                text=f"No tasks found for the current view.",
                font=("Arial", 10, "italic"),
            ).pack(pady=20)
            return

        # draw each task row
        for task in tasks_to_display:
            self.draw_task_row(self.task_list_frame, task)

        # ensure scroll region is updated
        self.task_list_frame.update_idletasks()
        self.task_canvas.config(scrollregion=self.task_canvas.bbox("all"))

    def draw_task_row(self, parent, task):
        """
        Draws a single task row item on the task view page.

        Args:
            parent: The frame to draw the tsk row in
            task: The ToDo object to display
        """
        # map priority string to a defined style
        priorityKey = (
            task.priority
            if task.priority in ["High", "Medium", "Low", "None"]
            else "None"
        )

        frameStyle = f"Task.{priorityKey}.TFrame"
        labelStyle = f"{priorityKey}.TLabel"
        checkStyle = f"{priorityKey}.TCheckbutton"

        # main frame for the task row, styled by priority
        row_frame = ttk.Frame(parent, padding=10, style=frameStyle)
        row_frame.pack(fill="x", pady=5, padx=5)

        # completion checkbox and toggle logic
        status_var = tk.BooleanVar(value=task.complete)

        def toggle_completion():
            new_state = status_var.get()
            # 1 for complete, 2 for ongoing
            choice = 1 if new_state else 2
            task.toggleComplete(choice)
            self.update_task_list()  # reraw to reflect status/sorting changes

        ttk.Checkbutton(
            row_frame, variable=status_var, command=toggle_completion, style=checkStyle
        ).pack(side="left", padx=(0, 10))

        # task label
        ttk.Label(
            row_frame, text=task.label, font=("Arial", 10, "bold"), style=labelStyle
        ).pack(side="left", anchor="w")

        # past due indicator
        if task.dueDate and task.dueDate < date.today():
            ttk.Label(
                row_frame, text="Past Due", font=("Arial", 12, "bold"), style=labelStyle
            ).pack(side="left", padx=10)

        # due date display
        date_display = task.dueDate.strftime("%m/%d") if task.dueDate else "N/A"
        ttk.Label(
            row_frame, text=date_display, font=("Arial", 10), style=labelStyle
        ).pack(side="right", padx=(10, 5), anchor="e")

        # edit button
        ttk.Button(
            row_frame,
            text="···",
            width=3,
            command=lambda t=task: self.load_edit_task_page(t),
        ).pack(side="right", anchor="e")

    # =========================================
    # Form Helpers
    # =========================================

    def _create_task_form_widgets(self, parent_frame, is_new_task, task_id=None):
        """
        Helper to draw the common Task and Edit Task form fields.
        """
        # label entry
        self._create_form_row(
            parent_frame, "Task Label:", 0, self.current_task_vars["label"]
        )

        self._create_form_row(
            parent_frame, "Due Date (MM/DD/YYYY):", 1, self.current_task_vars["dueDate"]
        )

        self._create_form_row(
            parent_frame, "Category:", 3, self.current_task_vars["category"]
        )

        self._create_form_row(
            parent_frame,
            "People Involved (comma separated):",
            4,
            self.current_task_vars["people"],
        )

        priority_options = list(th.PRIORITYDICT.values())
        ttk.Label(parent_frame, text="Priority:").grid(
            row=2, column=0, sticky="w", pady=5, padx=5
        )

        priority_menu = ttk.OptionMenu(
            parent_frame,
            self.current_task_vars["priority"],
            self.current_task_vars["priority"].get(),
            *priority_options,
        )
        priority_menu.grid(row=2, column=1, sticky="ew", pady=5, padx=5)

        parent_frame.grid_columnconfigure(1, weight=1)

    def _create_form_row(self, parent_frame, label_text, row_num, textvariable):
        """
        Helper to create a label and an entry field in the form.
        """
        ttk.Label(parent_frame, text=label_text).grid(
            row=row_num, column=0, sticky="w", pady=5, padx=5
        )
        ttk.Entry(parent_frame, textvariable=textvariable).grid(
            row=row_num, column=1, sticky="ew", pady=5, padx=5
        )

    # =========================================
    # Form Submission Logic
    # =========================================

    def _submit_new_task_creation(self):
        """
        Gathers form data, validates, and creates the task in the handler.
        """
        data = {k: v.get().strip() for k, v in self.current_task_vars.items()}

        # Process people string into list
        people_list = [p.strip() for p in data["people"].split(",") if p.strip()]

        # The ToDo class handles parsing and validation internally when instantiated.
        try:
            idNum = len(th.todoList) + 1
            new_task = th.todo.ToDo(
                data["label"],
                data["dueDate"],
                data["priority"],
                data["category"],
                people_list,  # Pass people list
                idNum,
            )

            # If no exception was raised, the task is valid
            th.todoList.append(new_task)
            messagebox.showinfo(
                "Success", f"Task '{data['label']}' created successfully!"
            )
            self.load_home_page()

        except (ValueError, TypeError) as e:
            # Catch the error message from validateAttributes and show a popup
            messagebox.showerror("Validation Error", str(e))
            return

    def _submit_task_update(self):
        """
        Gathers form data, validates, and updates the task
        """
        data = {k: v.get().strip() for k, v in self.current_task_vars.items()}
        task = self.editing_task

        # Process people string into list
        people_list = [p.strip() for p in data["people"].split(",") if p.strip()]

        try:
            priority_key = next(
                (k for k, v in th.PRIORITYDICT.items() if v == data["priority"]), "1"
            )

            th.update_task_attributes(
                task.idNum,
                data["label"],
                data["dueDate"],
                priority_key,
                data["category"],
                people_list,  # Pass people list
            )

            messagebox.showinfo(
                "Success", f"Task '{data['label']}' updated successfully!"
            )
            self.load_task_view_page(self.current_view_type, self.current_category)

        except (ValueError, TypeError) as e:
            # Catch the error and show the user the specific problem
            messagebox.showerror("Validation Error", str(e))
            return

    def _confirm_delete_task(self):
        """
        Asks the user to confirm task deletion
        """
        task = self.editing_task
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to permanently delete task: '{task.label}'?",
        )

        if confirm:
            try:
                # task num is 1 indexed
                deletedTask = th.todoList.pop(task.idNum - 1)
                print(f"Task {task.idNum}: {deletedTask.label} deleted successfully.\n")

                # re-index tasks
                for i, t in enumerate(th.todoList):
                    t.idNum = i + 1
            except IndexError:
                print("Error: Task not found with that number.\n")
            except Exception as e:
                print(f"An error occurred during deletion: {e}\n")

            messagebox.showinfo("Deleted", f"Task '{task.label}' has been deleted.")
            self.load_home_page()

    def copy_task(self, task):
        th.copyTask(task)
        messagebox.showinfo("Info Alert", f"{task.label} copied")

    def paste_task(self):
        copied_task = th.copiedTask

        if not copied_task:
            messagebox.showinfo("Paste Error", "No task has been copied yet.")
            return

        date_str = (
            copied_task.dueDate.strftime("%m/%d/%Y") if copied_task.dueDate else ""
        )
        # Added handling for people list paste
        people_str = ", ".join(copied_task.people) if copied_task.people else ""

        self.current_task_vars["label"].set(f"COPY: {copied_task.label}")
        self.current_task_vars["dueDate"].set(date_str)
        self.current_task_vars["priority"].set(copied_task.priority)
        self.current_task_vars["category"].set(copied_task.category)
        self.current_task_vars["people"].set(people_str)

        messagebox.showinfo("Success", f"Task data copied from '{copied_task.label}'.")

    # =========================================
    # Helper Data Methods
    # =========================================
    def _get_unique_categories(self):
        """
        Extracts a set of all unique, non-empty categories from the todoList
        """
        categories = set()
        for t in th.todoList:
            if t.category and t.category.strip():
                categories.add(t.category.strip())
        return sorted(list(categories))

    # =========================================
    # Application Control
    # =========================================

    def exit_app(self):
        """
        Saves all task data and closes the application window
        """
        # th.saveData() now raises OSError if saving fails.
        try:
            th.saveData()
        except OSError as e:
            messagebox.showerror("Save Error", f"Could not save data: {e}")

        self.master.destroy()
        print("\nThank you for using CTMA!")


def start_gui():
    """
    Initializes and runs the main event loop
    """
    root = tk.Tk()
    app = CTMAGUI(root)
    root.mainloop()
