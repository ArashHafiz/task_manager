import time
import tkinter as tk
from tkinter import messagebox, Toplevel
from task_manager import Task_Manager

current_time = time.localtime(time.time())

class Task_GUI():
    def __init__(self):
        """Initializes windows"""
        self.task_manager = Task_Manager()

        self.root = tk.Tk()
        self.root.title("To-Do List Manager")
        self.root.geometry("500x700")
        self.root.resizable(0, 0)

        self.init_ui()
        self.refresh_task_list()
        self.root.mainloop()

    def init_ui(self):
        """Initializes user interface"""
        # -- LABELS AND LISTBOX --
        # Main title
        self.main_label = tk.Label(self.root, text="To-Do List Manager", font=("Arial", 16))
        self.main_label.grid(row=0, column=0, columnspan=2, sticky="n", padx=10, pady=5)

        # Listbox title
        self.list_title = tk.Label(self.root, text="List of Tasks", font=("Arial", 14))
        self.list_title.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Listbox
        self.task_listbox = tk.Listbox(self.root, width=20, height=15)  
        self.task_listbox.grid(row=2, column=0, rowspan=1, padx=10, pady=5, sticky="nsew")

        # Task information panel title
        self.info_title = tk.Label(self.root, text="Task Information", font=("Arial", 14))
        self.info_title.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        # Task information panel
        self.task_info_panel = tk.Listbox(self.root, width=20, height=10)
        self.task_info_panel.grid(row=4, column=0, rowspan=2, padx=10, pady=5, sticky="nsew")
        self.task_listbox.bind("<<ListboxSelect>>", lambda event: self.update_info_panel())

        # -- BUTTONS --
        # Button frame
        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=2, column=1, rowspan=3, padx=5, pady=5, sticky="n")
        self.button_width = 15 

        # Add task button
        self.add_task_button = tk.Button(self.button_frame, text="Add Task", width=self.button_width, command=self.open_new_task_window)
        self.add_task_button.pack(pady=2)

        # Modify bask button
        self.modify_task_button = tk.Button(self.button_frame, text="Modify Task", width=self.button_width, command=self.open_edit_task_window)
        self.modify_task_button.pack(pady=2)

        # Delete task button
        self.delete_task_button = tk.Button(self.button_frame, text="Delete Task", width=self.button_width, command=lambda: self.remove_task(complete=False))
        self.delete_task_button.pack(pady=2)

        # Mark as complete button
        self.mark_as_complete_button = tk.Button(self.button_frame, text="Mark Complete", width=self.button_width, command=self.mark_as_complete)
        self.mark_as_complete_button.pack(pady=2)

        # View completed tasks button
        self.view_completed_tasks_button = tk.Button(self.button_frame, text="View Completed", width=self.button_width, command=self.open_completed_task_window)
        self.view_completed_tasks_button.pack(pady=2)

        # Search for tasks button
        self.search_task_button = tk.Button(self.button_frame, text="Search Task", width=self.button_width, command=self.open_search_task_window)
        self.search_task_button.pack(pady=2)

        self.root.grid_columnconfigure(0, weight=2) # Listbox horizontal expansion
        self.root.grid_columnconfigure(1, weight=0) # Button frame horizontal expansion
        self.root.grid_rowconfigure(2, weight=1) # Bottom space vertical expansion

    def open_new_task_window(self):
        """Opens window for task addition"""
        # Set has added task to false upon opening window (thus user will encounter error if trying to add details to a task they didn't add yet)
        self.has_added_task = False

        # Initialize add task window
        self.add_task_window = tk.Toplevel(self.root)
        self.add_task_window.title("Adding Task")
        self.add_task_window.geometry("500x300")
        self.add_task_window.resizable(0, 0)

        # Window labels
        self.add_task_label = tk.Label(self.add_task_window, text="Add Task", font=("Arial", 14))
        self.add_task_label.grid(row=0, column=0, columnspan=2, sticky="n", padx=10, pady=5)
        self.deadline_disclaimer_label = tk.Label(self.add_task_window, text="*For deadline, please enter in minutes from now.", font=("Arial", 11), fg="gray")
        self.deadline_disclaimer_label.grid(row=4, column=0, padx=5, pady=(0, 10), sticky="sw")

        # Entry box
        self.add_task_entry = tk.Entry(self.add_task_window, width=43, font=("Arial", 14))
        self.add_task_entry.grid(row=1, column=0, padx=10, pady=5, sticky="n")

        # -- BUTTONS --
        # Button frame
        self.add_task_button_frame = tk.Frame(self.add_task_window)
        self.add_task_button_frame.grid(row=2, column=0, rowspan=2, padx=5, pady=5, sticky="n")

        # Add task button
        self.add_task_button2 = tk.Button(self.add_task_button_frame, text="Add Task", width=self.button_width, command=self.add_task)
        self.add_task_button2.pack(pady=2)

        # Add note button
        self.add_note_button = tk.Button(self.add_task_button_frame, text="Add Note", width=self.button_width, command=lambda: self.add_note(edit=False))
        self.add_note_button.pack(pady=2)

        # Add time button
        self.add_time_button = tk.Button(self.add_task_button_frame, text="Add Deadline", width=self.button_width, command=lambda: self.add_time(edit=False))
        self.add_time_button.pack(pady=2)

        # Add tag button
        self.add_tag_button = tk.Button(self.add_task_button_frame, text="Add Tag", width=self.button_width, command=lambda: self.add_tag(edit=False))
        self.add_tag_button.pack(pady=2)

        self.add_task_window.grab_set()

    def open_edit_task_window(self):
        """Opens window for task modification"""
        self.has_added_task = False
        self.selected_task = self.task_listbox.curselection()
        if not self.selected_task:
            messagebox.showerror(title="Error!", message="Must select task to edit.")
            return
        self.selected_task_idx = self.selected_task[0]
        
        # Initialize add task window
        self.edit_task_window = tk.Toplevel(self.root)
        self.edit_task_window.title("Modifying Task")
        self.edit_task_window.geometry("500x300")
        self.edit_task_window.resizable(0, 0)

        # Window labels
        self.edit_task_label = tk.Label(self.edit_task_window, text="Edit Task", font=("Arial", 14))
        self.edit_task_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="n")

        self.deadline_disclaimer_label = tk.Label(self.edit_task_window, text="*For deadline, please enter in minutes from now.", font=("Arial", 11), fg="gray")
        self.deadline_disclaimer_label.grid(row=5, column=0, padx=5, pady=(0, 10), sticky="sw")

        self.task_name_label = tk.Label(self.edit_task_window, text=f"'{self.task_manager.task_list[self.selected_task_idx]['task']}'", font=("Arial", 14))
        self.task_name_label.grid(row=1, column=0, columnspan=2, sticky="n", padx=10, pady=5)

        # Entry box
        self.edit_task_entry = tk.Entry(self.edit_task_window, width=43, font=("Arial", 14))
        self.edit_task_entry.grid(row=2, column=0, padx=10, pady=5, sticky="n")

        # -- BUTTONS --
        # Button frame
        self.edit_task_button_frame = tk.Frame(self.edit_task_window)
        self.edit_task_button_frame.grid(row=3, column=0, rowspan=2, padx=5, pady=5, sticky="n")

        # Rename task button
        self.rename_task_button = tk.Button(self.edit_task_button_frame, text="Rename Task", width=self.button_width, command=self.rename_task)
        self.rename_task_button.pack(pady=2)

        # Edit note button
        self.edit_note_button = tk.Button(self.edit_task_button_frame, text="Edit Note", width=self.button_width, command=lambda: self.add_note(edit=True))
        self.edit_note_button.pack(pady=2)

        # Edit time button
        self.edit_time_button = tk.Button(self.edit_task_button_frame, text="Edit Deadline", width=self.button_width, command=lambda: self.add_time(edit=True))
        self.edit_time_button.pack(pady=2)

        # Edit tag button
        self.edit_tag_button = tk.Button(self.edit_task_button_frame, text="Edit Tag", width=self.button_width, command=lambda: self.add_tag(edit=True))
        self.edit_tag_button.pack(pady=2)

        self.edit_task_window.grab_set()

    def open_completed_task_window(self):
        """Opens window containing list of completed tasks"""
        # Initialize window
        self.completed_task_window = tk.Toplevel(self.root)
        self.completed_task_window.title("Completed Tasks")
        self.completed_task_window.geometry("500x400")
        self.completed_task_window.resizable(0, 0)

        # Window labels
        self.completed_task_label = tk.Label(self.completed_task_window, text="Completed Tasks", font=("Arial", 14))
        self.completed_task_label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="n")

        self.completed_list_label = tk.Label(self.completed_task_window, text="List of Completed Tasks", font=("Arial", 14))
        self.completed_list_label.grid(row=1, column=0, columnspan=3, sticky="nw", padx=10, pady=5)

        # Listboxes
        self.completed_listbox = tk.Listbox(self.completed_task_window, width=43)
        self.completed_listbox.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="nw")
        self.refresh_completed_task_list()

        self.completed_task_info_panel = tk.Listbox(self.completed_task_window, width=43)
        self.completed_task_info_panel.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="nw")
        self.completed_listbox.bind("<<ListboxSelect>>", lambda event: self.update_completed_task_info_panel())

        # -- BUTTONS --
        # Button frame
        self.completed_task_button_frame = tk.Frame(self.completed_task_window)
        self.completed_task_button_frame.grid(row=2, column=2, columnspan=3, rowspan=2, padx=5, pady=5, sticky="n")

        # Unmark complete button
        self.unmark_complete_button = tk.Button(self.completed_task_button_frame, text="Unmark Complete", width=self.button_width, command=self.unmark_as_complete)
        self.unmark_complete_button.pack(pady=2)

        # Delete task button
        self.delete_completed_task_button = tk.Button(self.completed_task_button_frame, text="Delete Task", width=self.button_width, command=lambda: self.remove_task(complete=True))
        self.delete_completed_task_button.pack(pady=2)

        # Configurations (for centre-alignment)
        self.completed_task_window.columnconfigure(0, weight=1)
        self.completed_task_window.columnconfigure(1, weight=1)
        self.completed_task_window.columnconfigure(2, weight=1)

        self.completed_task_window.grab_set()

    def open_search_task_window(self):
        """Opens search task window"""
        # Initialize window
        self.search_task_window = tk.Toplevel(self.root)
        self.search_task_window.title("Search for Task")
        self.search_task_window.geometry("500x200")
        self.search_task_window.resizable(0, 0)

        # Window labels
        self.search_task_label = tk.Label(self.search_task_window, text="Search for Task", font=("Arial", 16))
        self.search_task_label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="n")

        # Entry box
        self.search_task_entry = tk.Entry(self.search_task_window, width=43, font=("Arial", 14))
        self.search_task_entry.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="n")

        # Search task button
        self.search_task_button2 = tk.Button(self.search_task_window, text="Search Task", width=self.button_width, command=self.search_task)
        self.search_task_button2.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="n")

    def update_info_panel(self):
        """Updates information panel in root window"""
        selected_task = self.task_listbox.curselection()
        self.task_info_panel.delete(0, tk.END)
        # If task selected display task information in info panel
        if selected_task:
            selected_task_idx = selected_task[0]
            task = self.task_manager.task_list[selected_task_idx]
            # Display task information
            self.task_info_panel.insert(tk.END, f"Task: {task['task']}" if task['task'] != "EMPTY" else "Task: -")
            self.task_info_panel.insert(tk.END, f"Due: {task['time']}" if task['time'] != "EMPTY" else "Due: -")
            self.task_info_panel.insert(tk.END, f"Notes: {task['notes']}" if task['notes'] != "EMPTY" else "Notes: -")
            self.task_info_panel.insert(tk.END, f"Tag: {task['tag']}" if task['tag'] != "NO TAG" else "Tag: -")
            self.task_info_panel.insert(tk.END, f"{self.task_manager.return_time_to_deadline(selected_task_idx)}" if self.task_manager.return_time_to_deadline(selected_task_idx) != None else "")
        else:
            self.task_info_panel.insert(tk.END, "Select a task to see details.")

    def update_completed_task_info_panel(self):
        """Updates information panel in completed task window"""
        selected_task = self.completed_listbox.curselection()
        self.completed_task_info_panel.delete(0, tk.END)
        # If task selected display task information in completed info panel
        if selected_task:
            selected_task_idx = selected_task[0]
            task = self.task_manager.completed_task_list[selected_task_idx]
            # Display task information
            self.completed_task_info_panel.insert(tk.END, f"Task: {task['task']}" if task['task'] != "EMPTY" else "Task: -")
            self.completed_task_info_panel.insert(tk.END, f"Due: {task['time']}" if task['time'] != "EMPTY" else "Due: -")
            self.completed_task_info_panel.insert(tk.END, f"Notes: {task['notes']}" if task['notes'] != "EMPTY" else "Notes: -")
            self.completed_task_info_panel.insert(tk.END, f"Tag: {task['tag']}" if task['tag'] != "NO TAG" else "Tag: -")
            # If task has completed key display time of completion
            if 'completed' in task:
                self.completed_task_info_panel.insert(tk.END, f"Completed: {task['completed']}")
            # Otherwise display 'unknown'
            else:
                self.completed_task_info_panel.insert(tk.END, "Completed: Unknown")
        else:
            self.completed_task_info_panel.insert(tk.END, "Select a task to see details.")

    def refresh_task_list(self):
        """Refreshes listbox."""
        self.task_listbox.delete(0, tk.END)
        for idx, task in enumerate(self.task_manager.task_list):
            self.task_listbox.insert(tk.END, f"{idx+1}. {task['task']}")

    def refresh_completed_task_list(self):
        """Refreshes listbox of completed tasks."""
        self.completed_listbox.delete(0, tk.END)
        for idx, task in enumerate(self.task_manager.completed_task_list):
            self.completed_listbox.insert(tk.END, f"{task['task']}")

    def search_task(self):
        """Searches for task"""
        query = self.search_task_entry.get()
        # Show error if search term has nothing
        if not query:
            messagebox.showerror(title="Error!", message="Must enter something for search query.")
            return
        # If search yields no results display 'No results found'
        if not self.task_manager.search_task(query):
            messagebox.showinfo(title="Search Results", message="No results found.")
            return
        # If tasks found concatenate to string and output string
        output_message = ""
        for task in self.task_manager.search_task(query):
            output_message+=f"\n{task}"
        messagebox.showinfo(title="Search Results", message=f"Results found:\n{output_message}")

    def add_task(self):
        """Adds new task"""
        new_task = self.add_task_entry.get()
        # If no task selected display error message
        if not new_task:
            messagebox.showerror(title="Error!", message="Cannot add nothing as task.")
            return 

        # Otherwise insert task into listbox and array, refresh and output receipt of confirmation
        self.task_listbox.insert(tk.END, new_task)
        self.task_manager.add_task(new_task)
        self.refresh_task_list()
        # Set has_added_task to true (so user may begin adding details in the Add Task menu)
        self.has_added_task = True
        messagebox.showinfo(title="Task Added", message=f"'{new_task}' successfully added.")
    
    def remove_task(self, complete=False):
        """Deletes task"""
        # If task is not completed, selected task is from task listbox
        if not complete:
            self.selected_task = self.task_listbox.curselection()
        # If task is completed, selected task is from completed task listbox
        else:
            self.selected_task = self.completed_listbox.curselection()
        # If nothing is selected show error message
        if not self.selected_task:
            messagebox.showerror(title="Error!", message="Must select task to delete.")
            return
        # Otherwise retrieve selected task (from regular task listbox if not complete and from completed task listbox otherwise)
        self.selected_task_idx = self.selected_task[0]
        task_name = self.task_manager.task_list[self.selected_task_idx]['task'] if not complete else self.task_manager.completed_task_list[self.selected_task_idx]['task']
        # Show confirmation message before deleted
        self.remove_task_confirmation = messagebox.askquestion(title="Are you sure?" ,message=f"Are you sure you want to delete '{task_name}'?")
        # If user presses no return
        if self.remove_task_confirmation == "no":
            return
        # Otherwise delete task, refresh listbox and output receipt of confirmation
        self.task_manager.remove_task(self.selected_task_idx) if not complete else self.task_manager.remove_complete_task(self.selected_task_idx)
        self.refresh_task_list() if not complete else self.refresh_completed_task_list()
        messagebox.showinfo(title="Task Deleted", message="Successfully deleted task.")
    
    def add_note(self, edit=False):
        """Adds note to task"""
        # If task list is empty show error message
        if not self.task_manager.task_list:
            messagebox.showerror(title="Error!", message="No tasks to add note to.")
            return
        # If user has not added a task yet show error message
        if not self.has_added_task and not edit:
            messagebox.showerror(title="Error!", message="Must add task first before adding note.")
            return
        # If user is not in Edit Task menu, retrieve information Add Task menu
        if not edit:
            new_note = self.add_task_entry.get()
            task_idx = len(self.task_manager.task_list) - 1
        # Otherwise retrieve information from Edit Task menu
        else:
            new_note = self.edit_task_entry.get()
            task_idx = self.selected_task_idx
        # If user doesn't put anything for note show error message
        if not new_note:
            messagebox.showerror(title="Error!", message="Cannot add nothing as note.")
            return
        # Adds notes, refreshes task listbox and outputs receipt of confirmation
        self.task_manager.add_notes(task_idx, new_note)
        self.refresh_task_list()
        messagebox.showinfo(title="Note Added", message = f"Successfully added note '{new_note}' to '{self.task_manager.task_list[task_idx]['task']}'")

    def add_time(self, edit=False):
        """Adds deadline to task"""
        # If task list is empty show error message
        if not self.task_manager.task_list:
            messagebox.showerror(title="Error!", message="No tasks to add deadline to.")
            return
        # If task not added yet and user is not on Edit Task menu show error message
        if not self.has_added_task and edit == False:
            messagebox.showerror(title="Error!", message="Must add task first before adding note.")
            return
        # If user is not on Edit Task menu retrieve information from Add Task menu
        if not edit:
            new_time = self.add_task_entry.get().strip()
            task_idx = len(self.task_manager.task_list) - 1
        # Otherwise retrieve information from Edit Task menu
        else:
            new_time = self.edit_task_entry.get().strip()
            task_idx = self.selected_task_idx
        # If minutes to be added is not in digits show error message
        if not new_time.isdigit():
            messagebox.showerror(title="Error!", message="Please enter valid number for minutes to deadline.")
            return
        new_time = int(new_time)
        # Adds time to ask, refreshes task list and outputs receipt of confirmation
        self.task_manager.add_time(task_idx, new_time)
        self.refresh_task_list()
        messagebox.showinfo(title="Time Added", message = f"Successfully added deadline {self.task_manager.task_list[task_idx]['time']} to '{self.task_manager.task_list[-1]['task']}'")

    def add_tag(self, edit=False):
        """Adds tag to task"""
        # If task list empty show error message
        if not self.task_manager.task_list:
            messagebox.showerror(title="Error!", message="No tasks to add tag to.")
            return
        # If task not added yet and user is not on Edit Task menu show error message
        if not self.has_added_task and edit == False:
            messagebox.showerror(title="Error!", message="Must add task first before adding tag.")
            return
        # If user is not on Edit Task menu retrieve information from Add Task menu
        if not edit:
            new_tag = self.add_task_entry.get()
            task_idx = len(self.task_manager.task_list) - 1
        # Otherwise retrieve information from Edit Task menu
        else:
            new_tag = self.edit_task_entry.get()
            task_idx = self.selected_task_idx
        # If user has put nothing for new tag show error message
        if not new_tag:
            messagebox.showerror(title="Error!", message="Cannot add nothing as tag.")
            return
        # Adds tag, refreshes task list and displays receipt of confirmation
        self.task_manager.add_tag(task_idx, new_tag)
        self.refresh_task_list
        messagebox.showinfo(title="Tag Added", message = f"Successfully added tag '{self.task_manager.task_list[task_idx]['tag']}' to '{self.task_manager.task_list[-1]['task']}'.")
    
    def rename_task(self):
        """Renames task"""
        new_task_name = self.edit_task_entry.get()
        # If user puts nothing show error message
        if not new_task_name:
            messagebox.showerror(title="Error!", message="Cannot rename task to nothing.")
            return 
        # Renames task, refreshes task list and displays receipt of confirmation
        self.task_manager.rename_task(self.selected_task_idx, new_task_name)
        self.refresh_task_list()
        messagebox.showinfo(title="Task Renamed", message=f"Successfully renamed task to '{new_task_name}'.")
    
    def mark_as_complete(self):
        """Marks task as complete"""
        selected_task = self.task_listbox.curselection()
        # If task selected mark task as complete
        if selected_task:
            selected_task_idx = selected_task[0]
            task = self.task_manager.task_list[selected_task_idx]['task']
            self.task_manager.mark_as_complete(selected_task_idx)
            self.refresh_task_list()
            messagebox.showinfo(title="Marked as Complete", message=f"Successfully marked '{task}' as complete.")
        # Otherwise display error message
        else:
            messagebox.showerror(title="Error!", message="Must select task to mark as complete.")

    def unmark_as_complete(self):
        """Unmarks task as complete"""
        selected_task = self.completed_listbox.curselection()
        # If task selected mark task as complete
        if selected_task:
            selected_task_idx = selected_task[0]
            task = self.task_manager.completed_task_list[selected_task_idx]['task']
            self.task_manager.unmark_as_complete(selected_task_idx)
            self.refresh_completed_task_list()
            self.refresh_task_list()
            messagebox.showinfo(title="Unmarked as Complete", message=f"Successfully unmarked '{task}' as complete.")
        # Otherwise display error message
        else:
            messagebox.showerror(title="Error!", message="Must select task to unmark as complete.")

if __name__ == "__main__":
    task_gui = Task_GUI()