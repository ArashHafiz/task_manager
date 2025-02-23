import time, json
current_time = time.localtime(time.time())

class Task_Manager():
    """A simple task manager that can create, delete, edit, and add other features to tasks."""
    def __init__(self):
        """Initializes lists and loads saved tasks"""
        self.task_list = []
        self.completed_task_list = []

        # Load file unless file doesn't exist or is corrupted
        try:
            with open("tasks.json", "r") as file:
                data = json.load(file)
                if isinstance(data, list): 
                    # Loads old format without completed task list 
                    self.task_list = data  
                    self.completed_task_list = []  
                elif isinstance(data, dict):  
                    # Loads new format with completed task list
                    self.task_list = data.get("tasks", [])
                    self.completed_task_list = data.get("completed", [])
        except (FileNotFoundError, json.JSONDecodeError):
            # New task lists if file is not found or corrupted
            self.task_list = [] 
            self.completed_task_list = []

    def display_list(self):
        """Displays list of pending tasks"""
        for idx, task in enumerate(self.task_list):
            print(f"\nTask {idx+1}: {task['task']}")
            print(f"Due: {task['time']}")
            print(f"Notes: {task['notes']}")
            print(f"Tag: {task['tag']}")
            print(f"Subtasks: {len(task['subtasks'])}")

    def add_task(self, task_name):
        """Adds a new task to the list"""
        task_entry = {
            "task": task_name,
            "time": "EMPTY",
            "notes": "EMPTY",
            "tag": "NO TAG",
            "subtasks": []
        }
        self.task_list.append(task_entry)
        self.save_tasks()

    def rename_task(self, task_idx, task_name):
        """Renames a task by index"""
        if isinstance(task_idx, str):
            try:
                task_idx = int(task_idx)
            except ValueError:
                return False
        if 0 <= task_idx < len(self.task_list):
            self.task_list[task_idx]['task'] = task_name
            self.save_tasks()
            return True
        return False
    
    def remove_task(self, task_idx):
        """Removes a task by index"""
        if isinstance(task_idx, str):
            try:
                task_idx = int(task_idx)  
            except ValueError:
                return False  
        if 0 <= task_idx < len(self.task_list):
            del self.task_list[task_idx]
            self.save_tasks()
            return True
        return False

    def add_time(self, task_idx, minutes):
        """Adds a deadline to a task"""
        if isinstance(task_idx, str):
            try:
                task_idx = int(task_idx)  
            except ValueError:
                return False
        if 0 <= task_idx < len(self.task_list):
            task_time = time.localtime(time.time() + 60 * minutes)
            self.task_list[task_idx]["time"] = time.strftime('%H:%M %d %B %Y', task_time)
            self.save_tasks()
            return True
        return False

    def add_notes(self, task_idx, note):
        """Adds a note to a task"""
        if isinstance(task_idx, str):
            try:
                task_idx = int(task_idx)  
            except ValueError:
                return False
        if 0 <= task_idx < len(self.task_list):
            self.task_list[task_idx]["notes"] = note
            self.save_tasks()
            return True
        return False

    def search_task(self, query):
        """Search for tasks based on a query"""
        return [task['task'] for task in self.task_list if query.upper() in task["task"].upper()]

    def add_tag(self, task_idx, tag):
        """Adds a tag to a task"""
        if isinstance(task_idx, str):
            try:
                task_idx = int(task_idx)  
            except ValueError:
                return False
        if 0 <= task_idx < len(self.task_list):
            self.task_list[task_idx]["tag"] = tag
            self.save_tasks()
            return True
        return False

    def add_sub_tasks(self, task_idx, subtask):
        """Adds a subtask to a task"""
        if isinstance(task_idx, str):
            try:
                task_idx = int(task_idx)  
            except ValueError:
                return False
        if 0 <= task_idx < len(self.task_list):
            self.task_list[task_idx]["subtasks"].append(subtask)
            self.save_tasks()
            return True
        return False

    def mark_as_complete(self, task_idx):
        """Marks a task as completed"""
        if isinstance(task_idx, str):
            try:
                task_idx = int(task_idx)  
            except ValueError:
                return False
        if 0 <= task_idx < len(self.task_list):
            self.completed_task_list.append(self.task_list[task_idx])
            self.completed_task_list[-1]['completed'] = time.strftime('%H:%M %d %B %Y', current_time)
            del self.task_list[task_idx]
            self.save_tasks()
            return True
        return False
    
    def unmark_as_complete(self, task_idx):
        """Unmarks task as complete"""
        if isinstance(task_idx, str):
            try:
                task_idx = int(task_idx)
            except ValueError:
                return False
        if 0 <= task_idx < len(self.completed_task_list):
            if 'completed' in self.completed_task_list[task_idx]:
                self.completed_task_list[task_idx].pop('completed')
            self.task_list.append(self.completed_task_list[task_idx])
            del self.completed_task_list[task_idx]
            self.save_tasks()
            return True
        return False
    
    def remove_complete_task(self, task_idx):
        """Removes a task by index"""
        if isinstance(task_idx, str):
            try:
                task_idx = int(task_idx)  
            except ValueError:
                return False  
        if 0 <= task_idx < len(self.completed_task_list):
            del self.completed_task_list[task_idx]
            self.save_tasks()
            return True
        return False

    def return_time_to_deadline(self, task_idx):
        """Returns amount of time left until task deadline"""
        task = self.task_list[task_idx]
        if task['time'] != "EMPTY":
            deadline_timestamp = time.mktime(time.strptime(task['time'], "%H:%M %d %B %Y"))
            time_left = deadline_timestamp - time.time()
            days = abs(time_left) // 86400
            hours = (abs(time_left) % 86400) // 3600
            minutes = (abs(time_left) % 3600) // 60
            if time_left <= 0:
                return f"Overdue {int(days)} days {int(hours)} hours {int(minutes)} minutes ago!"
            else:
                return f"Due in {int(days)} days {int(hours)} hours {int(minutes)} minutes"

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump({"tasks": self.task_list, "completed": self.completed_task_list}, file, indent=4)