import sqlite3

class Task:

    def __init__(self, id=None, title="", description="", due_date="", completed=False):

        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed

class TaskManager:

    def __init__(self):

        self.connection = sqlite3.connect("tasks.db")

        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                completed INTEGER
            )
        """)

        self.connection.commit()
    def add_task(self, task):

        self.cursor.execute("""
            INSERT INTO tasks (title, description, due_date, completed)
            VALUES (?, ?, ?, ?)
        """, (
            task.title,
            task.description,
            task.due_date,
            task.completed
        ))

        self.connection.commit() 
    def view_tasks(self):

        self.cursor.execute("SELECT * FROM tasks")

        tasks = self.cursor.fetchall()

        # Check whether there are tasks
        if len(tasks) == 0:

            print("\nNo tasks found.")

        else:

            print("\n--- YOUR TASKS ---")

            # Loop through every task
            for task in tasks:

                print(
                    f"ID: {task[0]} | "
                    f"Title: {task[1]} | "
                    f"Description: {task[2]} | "
                    f"Due Date: {task[3]} | "
                    f"Completed: {task[4]}"
                )
    def mark_task_complete(self, task_id):

        self.cursor.execute("""
            UPDATE tasks
            SET completed = 1
            WHERE id = ?
        """, (task_id,))

        self.connection.commit()

        print("Task marked as complete!")

    def delete_task(self, task_id):

        self.cursor.execute("""
            DELETE FROM tasks
            WHERE id = ?
        """, (task_id,))

        self.connection.commit()

        print("Task deleted successfully!")  

manager = TaskManager()
while True:

    print("\n--- TASK MANAGER ---")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task as Complete")
    print("4. Delete Task")
    print("5. Exit")

    choice = input("Choose an option: ")
#add task
    if choice == "1":

        title = input("Enter task title: ")
        description = input("Enter task description: ")
        due_date = input("Enter due date: ")

        new_task = Task(
            title=title,
            description=description,
            due_date=due_date
        )
#add task to database
        manager.add_task(new_task)

        print("Task added successfully!")

    elif choice == "2":
        manager.view_tasks()
    elif choice == "3":

     task_id = input("Enter the ID of the completed task: ")
     manager.mark_task_complete(task_id)
     #delete task
    elif choice == "4":
        task_id = input("Enter the ID of the task to delete: ")
        manager.delete_task(task_id)

    elif choice == "5":
        print("Goodbye!")
        manager.connection.close()
        break

    else:
        print("Invalid choice. Please choose between 1 and 5.")         





