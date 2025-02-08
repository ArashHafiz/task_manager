import time
current_time = time.localtime(time.time())

class Task_Manager():

    def __init__(self):

        self.task_list = []
        self.time_list = []
        self.notes_list = []
        self.tag_list = []
        self.tag_name_list = []
        self.sub_tasks = dict()

    def display_list(self):
        for (idx,item) in enumerate(self.task_list):
            print(f"\nTask {idx+1}: {item}")
            print(f"Due: {self.time_list[idx]}")
            print(f"Notes: {self.notes_list[idx]}")
            print(f"Tag: {self.tag_list[idx]}")
            if idx in self.sub_tasks:
                print(f"# Subtasks: {len(self.sub_tasks[idx])}")

            else:
                print("Subtasks: 0")
        
    def add_task(self):

        print("\n== ADD TASK ==")
        print("This section allows you to add tasks and their times.")
        self.new_task = ""
        
        while True:

            self.display_list()
                
            self.new_task = input("\nPlease enter new task (X to exit): ")
            
            if self.new_task.upper() == "X":
                break
            self.task_list.append(self.new_task)
            self.time_list.append("EMPTY")
            self.notes_list.append("EMPTY")
            self.tag_list.append("NO TAG")

            self.sub_tasks[len(self.task_list) - 1] = []

    def remove_task(self):

        print("\n== REMOVING TASKS ==")
        print("This section allows you to remove tasks.")
        
        while True:
            
            try:
                if len(self.task_list) == 0:
                    print("\nIt appears that your task list is empty!")
                    return
  
                for (idx,item) in enumerate(self.task_list):
                    print(f"Task {idx+1}: {item}")
                
                self.remove_task = input("\nPlease put down number of task to be removed (x to exit): ")
                
                if self.remove_task.upper() == "X":
                    print("\nReturning to menu...")
                    break
                    
                self.remove_task = int(self.remove_task)
                self.task_list.pop(self.remove_task-1)
                print("\nTask removed.")
                
            except ValueError:
                print("\nInvalid, please put a number for the task number.")

            except IndexError:
                print("\nOops, looks like that index isn't in the list range. Try again.")

    def add_time(self):

        print("\n== ADDING TIME TO TASKS ==")
        print("This section allows you to attach times to tasks.")

        self.task_time = ""

        while True:

            try:
                if len(self.task_list) == 0:
                    print("\nIt appears your task list is empty!")
                    return

                self.display_list()

                self.task_time = input("\nPlease enter amount of minutes to task deadline (X to exit): ")
                
                
                if self.task_time.upper() == "X":
                    print("\nReturning to menu...")
                    break

                self.task_time_task = input("\nPlease enter index of task to attach timing to (X to exit): ")
                    
                if self.task_time_task.upper() == "X":
                    print("\nReturning to menu...")
                    break

                self.task_time_task = int(self.task_time_task)

                self.task_time = float(self.task_time)
                
                self.task_time_minutes = time.localtime(time.time()+ 60 * self.task_time)

                if self.task_time_minutes <= current_time:
                    print("\nI think you might be slightly overdue for this one.\n")

                elif self.task_time_minutes >= time.localtime(time.time() + 60 * 525960):
                    print("\nI don't think you'll have to worry about this one for a while.\n")
                          
                print(f"\nTask {self.task_time_task} due: {time.strftime('%H:%M %d %B %Y',self.task_time_minutes)}")
                self.time_list[self.task_time_task-1] = time.strftime('%H:%M %d %B %Y',self.task_time_minutes)
                
            except ValueError:
                print("\nInvalid value, please enter a number")

            except IndexError:
                print("\nIt appears that the index you've provided is out of the task lists' range. Please try again.\n")


    def add_notes(self):
        print("\n== ADD NOTES ==")
        print("This section allows you to add notes to your tasks.")

        if len(self.task_list) == 0:
            print("\nSorry, it appears you have no tasks to add notes to!")
            return

        while True:

            try:

                self.display_list()

                self.task_note = input("\nPlease write note (X to exit): ")

                if self.task_note.upper() == "X":
                    print("\nReturning to menu...")
                    break

                self.task_note_idx = input("\nPlease enter index of task (X to exit): ")

                if self.task_note_idx.upper() == "X":
                    print("\nReturning to menu...")
                    break

                self.task_note_idx = int(self.task_note_idx)

                self.notes_list[self.task_note_idx-1] = self.task_note

            except ValueError:
                print("\nInvalid value for task index, please enter a number.")

            except IndexError:
                print("\nIt appears that the index you've provided is out of the task lists' range. Please try again.\n")

    def search_task(self):
        print("\n== SEARCH FOR TASK ==")
        print("This section allows you to search for tasks using a search query.")

        if len(self.task_list) == 0:
            print("\nIt appears you have no impending tasks!")
            return

        results_found = False

        while True:

            self.search_query = input("\nPlease enter your search query here (X to exit): ")

            if self.search_query.upper() == "X":
                print("\nReturning to menu...")
                break

            for idx in range(len(self.task_list)):

                if self.search_query.upper() in self.task_list[idx].upper():
                    print(f"\nResults found in title of task {idx+1}:")
                    print(f"\nTask: {self.task_list[idx]}")
                    print(f"Due: {self.time_list[idx]}")
                    print(f"Notes: {self.notes_list[idx]}")
                    print(f"Tag: {self.tag_list[idx]}")
                    print(f"# Subtasks: {len(self.sub_tasks[idx])}")
                    results_found = True
                 
                if self.search_query.upper() in self.time_list[idx].upper():
                    print(f"\nResults found in due of task {idx+1}:")
                    print(f"\nTask: {self.task_list[idx]}")
                    print(f"Due: {self.time_list[idx]}")
                    print(f"Notes: {self.notes_list[idx]}")
                    print(f"Tag: {self.tag_list[idx]}")
                    print(f"# Subtasks: {len(self.sub_tasks[idx])}")
                    results_found = True
                    
                if self.search_query.upper() in self.notes_list[idx].upper():
                    print(f"\nResults found in notes of task {idx+1}:")
                    print(f"\nTask: {self.task_list[idx]}")
                    print(f"Due: {self.time_list[idx]}")
                    print(f"Notes: {self.notes_list[idx]}")
                    print(f"Tag: {self.tag_list[idx]}")
                    print(f"# Subtasks: {len(self.sub_tasks[idx])}")
                    results_found = True

                if self.search_query.upper() in self.tag_list[idx].upper():
                    print(f"\nResults found in notes of task {idx+1}:")
                    print(f"\nTask: {self.task_list[idx]}")
                    print(f"Due: {self.time_list[idx]}")
                    print(f"Notes: {self.notes_list[idx]}")
                    print(f"Tag: {self.tag_list[idx]}")
                    print(f"# Subtasks: {len(self.sub_tasks[idx])}")
                    results_found = True

                if self.search_query.upper() in (item.upper() for item in self.sub_tasks[idx]):
                    print(f"\nResults found in subtasks of task {idx+1}:")
                    print(f"\nTask: {self.task_list[idx]}")
                    print(f"Due: {self.time_list[idx]}")
                    print(f"Notes: {self.notes_list[idx]}")
                    print(f"Tag: {self.tag_list[idx]}")
                    print(f"# Subtasks: {len(self.sub_tasks[idx])}")
                    results_found = True
                    
                    

            else:
                if results_found == False:
                    print("\nNo results found.")

    def add_tag(self):
        print("\n== ADD TAG TO TASK ==")
        print("This section allows you to add tags to tasks for better organization.")

        if len(self.task_list) == 0:
            print("\nIt appears you have no impending tasks!")
            return

        while True:

            try:

                self.display_list()

                self.task_tag = input("\nPlease enter tag name (X to exit): ")

                if self.task_tag.upper() == "X":
                    print("\nReturning to menu...")
                    break

                for item in self.tag_name_list:
                    if item == self.task_tag:
                        print("\nIt appears you already have a task with this name.")
                        return

                self.tag_name_list.append(self.task_tag)

                self.tag_idx = input("\nEnter index of task you would like to add tag to (X to exit): ")

                if self.tag_idx.upper() == "X":
                    print("\nReturning to menu...")
                    break

                self.tag_idx = int(self.tag_idx)

                self.tag_list[self.tag_idx-1] = self.task_tag

                self.display_list()

                while True:

                    self.tag_idx = input(f"\nEnter index of other tasks you would like to assign {self.task_tag} to (X to exit): ")

                    if self.tag_idx.upper() == "X":
                        print("\nReturning to menu...")
                        return

                    self.tag_idx = int(self.tag_idx)
                    
                    self.tag_list[self.tag_idx-1] = self.task_tag

                    self.display_list()
                    
            except ValueError:
                print("\nInvalid value, please enter a number.")

            except IndexError:
                print("\nYour entered index is out of bounds. Please try again.")

    def display_tags(self):
        print("\n== DISPLAY TASKS BASED ON TAGS ==")
        print("This section allows you to display the tasks that go under a chosen tag.")

        while True:

            try:

                if len(self.task_list) == 0:
                    print("\nSeems like your list is empty!")
                    return

                print("\n-- LIST OF TAGS --\n")

                for (idx,item) in enumerate(self.tag_name_list):
                    print(f"{idx+1} : {item}")

                self.tag_display = input("\nPlease enter index of tag you wish to access (X to exit, and 'No tag' to display tasks with no tag): ")

                if self.tag_display.upper() == "X":
                    print("\nReturning to menu...")
                    return

                if self.tag_display.upper() == "NO TAG":
                    print("\n== Tasks with no tags ==")
                    for (idx, item) in enumerate(self.task_list):
                        if self.tag_list[idx] == "NO TAG":
                            print(f"\nTask {idx+1}: {item}")
                            print(f"Due: {self.time_list[idx]}")
                            print(f"Notes: {self.notes_list[idx]}")
                            print(f"Tag: {self.tag_list[idx]}")
                            print(f"# Subtasks: {len(self.sub_tasks[idx])}")

                    else:
                        return
                        
                
                self.tag_display = int(self.tag_display)

                print(f"\n== {self.tag_name_list[self.tag_display-1]} ==")

                for (idx, item) in enumerate(self.task_list):
                    if self.tag_list[idx] == self.tag_name_list[self.tag_display-1]:
                        print(f"\nTask {idx+1}: {item}")
                        print(f"Due: {self.time_list[idx]}")
                        print(f"Notes: {self.notes_list[idx]}")
                        print(f"Tag: {self.tag_list[idx]}")
                        print(f"# Subtasks: {len(self.sub_tasks[idx])}")

            except ValueError:
                print("\nInvalid value for tag index!")

            except IndexError:
                print("\nYour entered index is out of bounds. Please try again.")

    def add_sub_tasks(self):
        print("\n== ADD SUB-TASKS ==")
        print("This section allows you to add sub-tasks to tasks.")

        while True:

            try:

                self.display_list()

                self.sub_task_idx = input("\nPlease enter index of task you would like to add sub-tasks to (X to exit): ")

                if self.sub_task_idx.upper() == "X":
                    print("\nReturning to menu...")
                    return

                self.sub_task_idx = int(self.sub_task_idx)

                for (idx, item) in enumerate(self.task_list):
                    
                    if self.task_list[self.sub_task_idx-1] == item:

                        print(f"\nTask {idx+1}: {item}")
                        print(f"Due: {self.time_list[idx]}")
                        print(f"Notes: {self.notes_list[idx]}")
                        print(f"Tag: {self.tag_list[idx]}")
                        print(f"# Subtasks: {len(self.sub_tasks[idx])}")

                while True:

                    self.sub_task = input("\nPlease enter sub task (X to exit): ")

                    if self.sub_task.upper() == "X":
                        print("\nReturning to menu...")
                        return

                    self.sub_tasks[self.sub_task_idx-1].append(self.sub_task)

                    for key in self.sub_tasks:
                        print(f"\nTask {key+1}: {', '.join(self.sub_tasks[key])}")
                    
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
    "H": task.display_tags,
    "I": task.add_sub_tasks,
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
    print("H: Display tasks based on tags")
    print("I: Add sub-tasks")
    print(f"\nCurrent time: {time.strftime('%H:%M %d %B %Y')}")

    choice = input("\nPlease enter choice: ").upper()

    if choice in operations:
        operations[choice]()
    elif choice == "X":
        print("\nExiting...")
    else:
        print("\nInvalid operation!")