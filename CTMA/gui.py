import tkinter as tk
from tkinter import ttk
import todo_handler as h
from datetime import date

def set_styles(master):
    """
    Sets up the custom styles and themes for the application.

    Args:
        master: The root Tkinter window instance.
    """
    style = ttk.Style(master)
    # define style for main view buttons on the home page
    style.configure("HomePage.TButton", font=("Arial", 10, "bold"), padding=10)

    # define styles for task row frames based on priority
    style.configure("Task.High.TFrame", background="red", borderwidth=1, relief="solid")
    style.configure("Task.Medium.TFrame", background="orange", borderwidth=1, relief="solid")
    style.configure("Task.Low.TFrame", background="yellow", borderwidth=1, relief="solid")
    style.configure("Task.None.TFrame", background="lightgray", borderwidth=1, relief="solid")


class CTMAGUI:
    """
    Main class for the CTMA GUI.

    Manages the application state, page navigation, and user interface layout.
    """
    def __init__(self, master):
        """
        Initializes the GUI, loads backend data, and displays the home page.

        Args:
            master: The root window.
        """
        self.master = master
        master.title("CTMA - Collaborative ToDo Manager")

        # application state variables for task filtering and sorting
        self.current_view_type = "All"
        self.current_category = None
        self.current_sort_key = "Priority"

        # load save data from backend
        h.loadSave()

        # apply styles
        set_styles(master)

        # main frame for all page content
        self.main_frame = ttk.Frame(master, padding="10")
        self.main_frame.pack(fill="both", expand=True)

        self.load_home_page()
    
    def clear_frame(self):
        """
        Removes all widgets from the main_frame to clear the current page view.
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
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
        top_frame.pack(fill='x', pady=(0, 20))

        # current date display
        today = date.today().strftime("%B %d, %Y")
        ttk.Label(top_frame, text=f"Current Date: {today}", font=("Arial", 12, "bold"), relief="solid", borderwidth=1, padding=5).pack(side="left", anchor="nw")

        # optional page title
        if page_title:
            ttk.Label(top_frame, text=page_title, font=("Arial", 14, "bold")).pack(side="left", padx=20, fill='x', expand=True)
        
        # add task button
        # NOTE placeholder command
        ttk.Button(top_frame, text="Add Task", command=lambda: print("Opening Create Task Page"), width=12).pack(side="right", anchor="ne")
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
        bottom_frame.pack(fill='x', side="bottom", pady=(20, 0))

        # settings button
        # NOTE placeholder command
        ttk.Label(bottom_frame, text="⚙", font=("Arial", 20)).pack(side="left", anchor="sw")

        # exit CTMA button
        ttk.Button(bottom_frame, text="Exit CTMA", command=self.exit_app, width=12).pack(side="right", anchor="se")
        return bottom_frame
    
    def load_home_page(self):
        """
        Creates and displays the home page layout.
        """
        self.clear_frame()
        self.create_top_bar(self.main_frame)
        self.create_bottom_bar(self.main_frame)


        # container for the grid of view buttons
        grid_frame = ttk.Frame(self.main_frame)
        grid_frame.pack(pady=20, fill='x')

        # configure 3 columns
        for i in range(3):
            grid_frame.grid_columnconfigure(i, weight=1, uniform="group1")


        # --- ROW 1: Main Status Views ---
    
        # due today button
        self.create_view_button(grid_frame, "Due Today", 0, 0, lambda: self.load_task_view_page("Due Today"))
       
        # all tasks button
        num_taks = len(h.todoList)
        self.create_view_button(grid_frame, f"All ({num_taks})", 0, 1, lambda: self.load_task_view_page("All"))

        # completed button
        completed_count = len([t for t in h.todoList if t.complete])
        self.create_view_button(grid_frame, f"Completed ({completed_count})", 0, 2, lambda: self.load_task_view_page("Completed"))

        # --- ROW 2: Category Views ---
        # NOTE placeholders
        self.create_view_button(grid_frame, "Category 1", 1, 0, lambda: self.load_task_view_page("Category 1"))
        self.create_view_button(grid_frame, "Category 2", 1, 1, lambda: self.load_task_view_page("Category 2"))
        self.create_view_button(grid_frame, "Category 3", 1, 2, lambda: self.load_task_view_page("Category 3"))

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
        controls_frame.pack(fill='x', pady=5)

        # sort dropdown menu
        sort_options = ["Priority", "dueDate", "label"]
        self.sort_var = tk.StringVar(value=self.current_sort_key)
        
        sort_menu = ttk.OptionMenu(
            controls_frame,
            self.sort_var,
            self.current_sort_key,
            *sort_options,
            command=self.update_task_list_sort
        )
        sort_menu.pack(side="left", anchor="w", padx=5, pady=5)

        # category/view information label
        cat_text = f"Category viewing ( {category if category else view_type} )"
        ttk.Label(controls_frame, text=cat_text, font=("Arial", 12, "bold")).pack(side="left", fill="x", expand=True, padx=20)

        # container for the scrollable list of tasks
        task_list_container = ttk.Frame(self.main_frame)
        task_list_container.pack(fill="both", expand=True, pady=10)

        # canvas for scrolling
        self.task_canvas = tk.Canvas(task_list_container)
        self.task_canvas.pack(side="left", fill="both", expand=True)

        # scrollbar for the canvas
        task_scrollbar = ttk.Scrollbar(task_list_container, orient="vertical", command=self.task_canvas.yview)
        task_scrollbar.pack(side="right", fill="y")
        self.task_canvas.configure(yscrollcommand=task_scrollbar.set)

        # frame inside the canvas where task rows are drawn
        self.task_list_frame = ttk.Frame(self.task_canvas)
        self.task_canvas.create_window((0, 0), window=self.task_list_frame, anchor="nw", width=self.task_canvas.winfo_width())

        # bind events to manage scrolling and resizing
        # update scroll region when the list frame's size changes
        self.task_list_frame.bind("<Configure>", lambda _: self.task_canvas.configure(scrollregion = self.task_canvas.bbox("all")))
        # update the inner frame's width when the canvas's size changes
        self.task_canvas.bind("<Configure>", lambda e: self.task_canvas.itemconfig(self.task_canvas.find_all()[0], width=e.width))

        self.update_task_list()

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
        tasks_to_display = h.get_tasks_for_view(
            view_type=self.current_view_type,
            category=self.current_category,
            sort_key=self.current_sort_key
        )

        if not tasks_to_display:
            ttk.Label(self.task_list_frame, text=f"No tasks found for the current view.", font=("Arial", 10, "italic")).pack(pady=20)
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
        priority_style_map = {
            "High": "Task.High.TFrame",
            "Medium": "Task.Medium.TFrame",
            "Low": "Task.Low.TFrame",
            "None": "Task.None.TFrame"
        }

        # main frame for the task row, styled by priority
        row_frame = ttk.Frame(parent, padding=10, style=priority_style_map.get(task.priority, "TFrame"))
        row_frame.pack(fill="x", pady=5, padx=5)

        # completion checkbox and toggle logic
        status_var = tk.BooleanVar(value=task.complete)
        def toggle_completion():
            new_state = status_var.get()
            # 1 for complete, 2 for ongoing
            choice = 1 if new_state else 2
            task.toggleComplete(choice)
            self.update_task_list() # reraw to reflect status/sorting changes
        
        ttk.Checkbutton(row_frame, variable=status_var, command=toggle_completion).pack(side="left", padx=(0, 10))

        # task label
        ttk.Label(row_frame, text=task.label, font=("Arial", 10, "bold")).pack(side="left", anchor="w")

        # past due indicator
        if task.dueDate and task.dueDate < date.today():
            ttk.Label(row_frame, text="Past Due", font=("Arial", 12, "bold")).pack(side="left", padx=10)

        # due date display
        date_display = task.dueDate.strftime("%m/%d") if task.dueDate else "N/A"
        ttk.Label(row_frame, text=date_display, font=("Arial", 10)).pack(side="right", padx=(10, 5), anchor="e")

        # edit button
        # NOTE placeholder command
        ttk.Button(row_frame, text="...", width=3, command=lambda: print(f"Edit Task {task.idNum}")).pack(side="right", anchor="e")

    
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

        ttk.Button(button_frame, text=text, command=command, style="HomePage.TButton").pack(fill="both", expand=True, padx=10, pady=10)

    def add_task(self):
        """
        Handles the 'Add Task' button click (Placeholder)
        """
        print("Opening Add Task screen") # placeholder
    


    def exit_app(self):
        """
        Saves all task data and closes the application window
        """
        h.saveData()
        self.master.destroy()
        print("\nThank yu for using CTMA!")


def start_gui():
    """
    Initializes and runs the main event loop
    """
    root = tk.Tk()
    app = CTMAGUI(root)
    root.mainloop()