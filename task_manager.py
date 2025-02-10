import time
current_time = time.localtime(time.time())

class Task_Manager():

    def __init__(self):
        self.task_list = []
        self.completed_task_list = []

    def display_list(self):
        for idx, task in enumerate(self.task_list):
            print(f"\nTask {idx+1}: {task['task']}")
            print(f"Due: {task['time']}")
            print(f"Notes: {task['notes']}")
            print(f"Tag: {task['tag']}")
            print(f"Subtasks: {len(task['subtasks'])}")

    def display_completed_list(self):
        for idx, task in enumerate(self.completed_task_list):
            print(f"\nCompleted task {idx+1}: {task['task']}")

    def display_task(self, idx):
        task = self.task_list[idx]
        print(f"\nTask {idx+1}: {task['task']}")
        print(f"Due: {task['time']}")
        print(f"Notes: {task['notes']}")
        print(f"Tag: {task['tag']}")
        print(f"Subtasks: {len(task['subtasks'])}")

    def check_task_time(self):
        for task in self.task_list:
            if task['time'] != "EMPTY":
                deadline_timestamp = time.mktime(time.strptime(task['time'], "%H:%M %d %B %Y"))
                time_left = deadline_timestamp - time.time()
                
                if time_left <= 0:
                    print(f"\nWarning: task overdue! {task['task']} was due at {task['time']}")
                elif time_left <= 3600:
                    print(f"\nWarning: task due within an hour! {task['task']} is due at {task['time']}")
                elif time_left <= 43200:
                    print(f"\nWarning: task due within 12 hours! {task['task']} is due at {task['time']}")
                elif time_left <= 86400:
                    print(f"\nWarning: task due within a day! {task['task']} is due at {task['time']}")
    
    def add_task(self):
        print("\n== ADD TASK ==")
        while True:
            self.display_list()
            new_task = input("\nPlease enter new task (X to exit): ")
            if new_task.upper() == "X":
                print("\nReturning to menu...")
                break
            
            task_entry = {
                "task": new_task,
                "time": "EMPTY",
                "notes": "EMPTY",
                "tag": "NO TAG",
                "subtasks": []
            }
            self.task_list.append(task_entry)
    
    def remove_task(self):
        print("\n== REMOVING TASKS ==")
        while True:
            if not self.task_list:
                print("\nIt appears that your task list is empty!")
                return
            
            for idx, task in enumerate(self.task_list):
                print(f"Task {idx+1}: {task['task']}")
            
            remove_task = input("\nPlease put down number of task to be removed (X to exit): ")
            if remove_task.upper() == "X":
                print("\nReturning to menu...")
                break
            
            try:
                remove_task = int(remove_task)
                self.task_list.pop(remove_task-1)
                print("\nTask removed.")
            except (ValueError, IndexError):
                print("\nInvalid input, please try again.")
    
    def add_time(self):
        print("\n== ADDING TIME TO TASKS ==")
        while True:
            if not self.task_list:
                print("\nIt appears your task list is empty!")
                return
            
            self.display_list()
            task_time = input("\nPlease enter amount of minutes to task deadline (X to exit): ")
            if task_time.upper() == "X":
                print("\nReturning to menu...")
                break
            
            task_index = input("\nPlease enter index of task to attach timing to (X to exit): ")
            if task_index.upper() == "X":
                print("\nReturning to menu...")
                break
            
            try:
                task_index = int(task_index) - 1
                task_time = float(task_time)
                task_time_minutes = time.localtime(time.time() + 60 * task_time)
                
                if task_time_minutes <= current_time:
                    print("\nI think you might be slightly overdue for this one.\n")
                elif task_time_minutes >= time.localtime(time.time() + 60 * 525960):
                    print("\nI don't think you'll have to worry about this one for a while.\n")
                
                formatted_time = time.strftime('%H:%M %d %B %Y', task_time_minutes)
                print(f"\nTask {task_index + 1} due: {formatted_time}")
                self.task_list[task_index]['time'] = formatted_time
                
            except (ValueError, IndexError):
                print("\nInvalid input, please try again.")

    def add_notes(self):
        print("\n== ADDING NOTES TO TASKS ==")

        if not self.task_list:
                print("\nSorry, it appears you have no tasks to add notes to!")
                return
        
        while True:
            try:
                self.display_list()
                self.task_note = input("\nPlease write your note (X to exit): ")
                if self.task_note.upper() == "X":
                    print("\nReturning to menu...")
                    break

                self.task_note_idx = input("\nPlease enter index of task to add note to (X to exit): ")
                if self.task_note_idx.upper() == "X":
                    print("\nReturning to menu...")
                    break

                self.task_note_idx = int(self.task_note_idx) - 1
                self.task_list[self.task_note_idx]['notes'] = self.task_note

            except ValueError:
                print("\nInvalid value for task index, please enter a number.")
            except IndexError:
                print("\nIt appears that the index you've provided is out of the task lists' range. Please try again.\n")

    def search_task(self):
        print("\n== SEARCH FOR TASK ==")

        if not self.task_list:
            print("\nIt appears you have no impending tasks!")
            return
        results_found = False

        while True:
            self.search_query = input("\nPlease enter your search query here (X to exit): ")
            if self.search_query.upper() == "X":
                print("\nReturning to menu...")
                break

            for idx, task in enumerate(self.task_list):
                if self.search_query.upper() in task['task'].upper():
                    print(f"\nResults found in title of task {idx+1}:")
                    self.display_task(idx)
                    results_found = True
                 
                if self.search_query.upper() in task['time'].upper():
                    print(f"\nResults found in due of task {idx+1}:")
                    self.display_task(idx)
                    results_found = True
                    
                if self.search_query.upper() in task['notes'].upper():
                    print(f"\nResults found in notes of task {idx+1}:")
                    self.display_task(idx)
                    results_found = True

                if self.search_query.upper() in task['tag'].upper():
                    print(f"\nResults found in tag of task {idx+1}:")
                    self.display_task(idx)
                    results_found = True

                if self.search_query.upper() in task['subtasks'].upper():
                    print(f"\nResults found in subtasks of task {idx+1}:")
                    self.display_task(idx)
                    results_found = True
                    
            else:
                if results_found == False:
                    print("\nNo results found.")

    def add_tag(self):
        print("\n== ADD TAG TO TASK ==")

        if not self.task_list:
            print("\nIt appears you have no impending tasks!")
            return

        while True:
            try:
                self.display_list()
                self.task_tag = input("\nPlease enter tag name (X to exit): ")

                if self.task_tag.upper() == "X":
                    print("\nReturning to menu...")
                    break

                for task in self.task_list:
                    if task['tag'] == self.task_tag:
                        print("\nIt appears you already have a task with this name.")
                        return

                self.tag_idx = input("\nEnter index of task you would like to add tag to (X to exit): ")
                if self.tag_idx.upper() == "X":
                    print("\nReturning to menu...")
                    break

                self.tag_idx = int(self.tag_idx) - 1
                self.task_list[self.tag_idx]['tag'] = self.task_tag
                self.display_list()

                while True:
                    self.tag_idx = input(f"\nEnter index of other tasks you would like to assign {self.task_tag} to (X to exit): ")
                    if self.tag_idx.upper() == "X":
                        print("\nReturning to menu...")
                        break

                    self.tag_idx = int(self.tag_idx)
                    self.task_list[self.tag_idx]['tag'] = self.task_tag
                    self.display_list()
                    
            except ValueError:
                print("\nInvalid value, please enter a number.")
            except IndexError:
                print("\nYour entered index is out of bounds. Please try again.")

    def add_sub_tasks(self):
        print("\n== ADD SUB-TASKS ==")

        if not self.task_list:
            print("\nSeems like your list is empty! You can't add sub-tasks if there are no tasks.")
            return
        
        while True:
            try:
                self.display_list()
                self.sub_task_idx = input("\nPlease enter index of task you would like to add sub-tasks to (X to exit): ")
                if self.sub_task_idx.upper() == "X":
                    print("\nReturning to menu...")
                    break

                self.sub_task_idx = int(self.sub_task_idx) - 1
                self.display_task(self.sub_task_idx)

                while True:
                    self.sub_task = input("\nPlease enter sub task (X to exit): ")
                    if self.sub_task.upper() == "X":
                        print("\nReturning to menu...")
                        break

                    self.task_list[self.sub_task_idx]['subtasks'].append(self.sub_task)

            except ValueError:
                print("Invalid value for indexing!")
            except IndexError:
                print("Index value out of bounds. Please try again.")

    def mark_as_complete(self):
        print("\n== MARK TASK AS COMPLETE ==")
        print("Mark tasks as complete and view completed tasks.")

        if not self.task_list:
            print("Congrats! Looks like there's nothing to do.")
            return
        
        while True:
            try:
                if self.completed_task_list:
                    print("\n-- COMPLETED TASKS --")
                    self.display_completed_list()
                
                print("\n-- CURRENT TASKS --")
                self.display_list()

                self.check_task_idx = input("\nPlease enter index of task you would like to mark as complete (X to exit): ")
                if self.check_task_idx.upper() == "X":
                    print("\nReturning to menu...")
                    break

                self.check_task_idx = int(self.check_task_idx)

                task_to_complete = self.task_list[self.check_task_idx - 1]
                self.completed_task_list.append(task_to_complete)
                del self.task_list[self.check_task_idx - 1]

            except ValueError:
                print("Invalid value for indexing!")
            
            except IndexError:
                print("Index value out of bounds. Please try again.")

task = Task_Manager()
choice = ""

operations = {
    "A": task.add_task,
    "B": task.remove_task,
    "C": task.add_time,
    "D": task.display_list,
    "E": task.add_notes,
    "F": task.search_task,
    "G": task.add_tag,
    "H": task.add_sub_tasks,
    "I" : task.mark_as_complete,
    }

while choice != "X":

    print("\n=== ARASH'S TASK MANAGER ===")
    print("\nA: Add task")
    print("B: Remove task")
    print("C: Add timing to task")
    print("D: Display list")
    print("E: Add notes to task")
    print("F: Search for task")
    print("G: Add tag to task")
    print("H: Add sub-tasks")
    print("I: Mark task as complete")
    print(f"\nCurrent time: {time.strftime('%H:%M %d %B %Y')}")

    if task.task_list:
        task.check_task_time()

    choice = input("\nPlease enter choice: ").upper()

    if choice in operations:
        operations[choice]()
    elif choice == "X":
        print("\nExiting...")
    else:
        print("\nInvalid operation!")