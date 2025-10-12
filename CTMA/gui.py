import tkinter as tk
from tkinter import ttk
import handler as h
from datetime import date

def set_styles(master):
    style = ttk.Style(master)
    style.configure("HomePage.TButton", font=("Arial", 10, "bold"), padding=10)
    style.configure("Task.High.TFrame", background="red", borderwidth=1, relief="solid")
    style.configure("Task.Medium.TFrame", background="orange", borderwidth=1, relief="solid")
    style.configure("Task.Low.TFrame", background="yellow", borderwidth=1, relief="solid")
    style.configure("Task.None.TFrame", background="lightgray", borderwidth=1, relief="solid")


class CTMAGUI:
    def __init__(self, master):
        self.master = master
        master.title("CTMA - Collaborative ToDo Manager")

        self.current_view_type = "All"
        self.current_category = None
        self.current_sort_key = "Priority"

        h.loadSave()
        set_styles(master)

        # frame for all page content
        self.main_frame = ttk.Frame(master, padding="10")
        self.main_frame.pack(fill="both", expand=True)

        self.load_home_page()
    
    def clear_frame(self):
        """
        Removes all widgets from the frame.
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def create_top_bar(self, parent, page_title=""):
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill='x', pady=(0, 20))

        today = date.today().strftime("%B %d, %Y")
        ttk.Label(top_frame, text=f"Current Date: {today}", font=("Arial", 12, "bold"), relief="solid", borderwidth=1, padding=5).pack(side="left", anchor="nw")

        if page_title:
            ttk.Label(top_frame, text=page_title, font=("Arial", 14, "bold")).pack(side="left", padx=20, fill='x', expand=True)
        
        # NOTE placeholder command
        ttk.Button(top_frame, text="Add Task", command=lambda: print("Opening Create Task Page"), width=12).pack(side="right", anchor="ne")
        return top_frame
    
    def create_bottom_bar(self, parent):
        bottom_frame = ttk.Frame(parent)
        bottom_frame.pack(fill='x', side="bottom", pady=(20, 0))

        # NOTE placeholder command
        ttk.Label(bottom_frame, text="⚙", font=("Arial", 20)).pack(side="left", anchor="sw")

        ttk.Button(bottom_frame, text="Exit CTMA", command=self.exit_app, width=12).pack(side="right", anchor="se")
        return bottom_frame
    
    def load_home_page(self):
        """
        Creates and displays the home page layout
        """
        self.clear_frame()
        self.create_top_bar(self.main_frame)
        self.create_bottom_bar(self.main_frame)


        # view buttons
        grid_frame = ttk.Frame(self.main_frame)
        grid_frame.pack(pady=20, fill='x')

        # configure 3 columns
        for i in range(3):
            grid_frame.grid_columnconfigure(i, weight=1, uniform="group1")


        # --- ROW 1 ---
        # due today
        self.create_view_button(grid_frame, "Due Today", 0, 0, lambda: self.load_task_view_page("Due Today"))
       
        # all tasks
        num_taks = len(h.todoList)
        self.create_view_button(grid_frame, f"All ({num_taks})", 0, 1, lambda: self.load_task_view_page("All"))

        # completed
        completed_count = len([t for t in h.todoList if t.complete])
        self.create_view_button(grid_frame, f"Completed ({completed_count})", 0, 2, lambda: self.load_task_view_page("Completed"))

        # --- ROW 2 ---
        self.create_view_button(grid_frame, "Category 1", 1, 0, lambda: self.load_task_view_page("Category 1"))
        self.create_view_button(grid_frame, "Category 2", 1, 1, lambda: self.load_task_view_page("Category 2"))
        self.create_view_button(grid_frame, "Category 3", 1, 2, lambda: self.load_task_view_page("Category 3"))

    
    def create_view_button(self, parent, text, row, col, command):
        button_frame = ttk.Frame(parent, relief="solid", borderwidth=1)
        button_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        ttk.Button(button_frame, text=text, command=command, style="HomePage.TButton").pack(fill="both", expand=True, padx=10, pady=10)

    def add_task(self):
        """Handles the 'Add Task' button"""
        print("Opening Add Task screen") # placeholder
    
    def load_task_view_page(self, view_type):
        print(f"Viewing {view_type} tasks") # placeholder

    def exit_app(self):
        h.saveData()
        self.master.destroy()
        print("\nThank yu for using CTMA!")


def start_gui():
    root = tk.Tk()
    app = CTMAGUI(root)
    root.mainloop()