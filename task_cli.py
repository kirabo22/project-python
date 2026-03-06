import json
import sys
import os
from datetime import datetime

FILE_NAME = "tasks.json"

# create json file if it doesn't exist
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w") as file:
        json.dump([], file)

def load_tasks():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
        
    except FileNotFoundError:
        return []
    
    except json.JSONDecodeError:
        print("Error: tasks.json is corrupted.")
        return []

def save_tasks(tasks):
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(description):
    tasks = load_tasks()

    new_id = 1 if not tasks else tasks[-1]["id"] + 1
    
    task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
        
    }

    tasks.append(task)
    save_tasks(tasks)

    print(f"Task added successfully.")

def list_tasks():
    tasks = load_tasks()

    if not tasks:
        print("No tasks found.")
        return
    
    for task in tasks:
        status = "✓" if task.get("status") == "done" else "✗"
        print(f'{task["id"]}. [{status}] {task["description"]}')

# Mark a task as done
def mark_done(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            save_tasks(tasks)
            print("Task marked as done.")
            return
        
def delete_task(task_id):
    tasks = load_tasks()

    new_tasks = [task for task in tasks if task["id"] != task_id]

    if len(tasks) == len(new_tasks):
        print("Task not found.")
        return

    save_tasks(new_tasks)
    print("Task deleted.")

def update_task(task_id, new_description):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()

            save_tasks(tasks)

            print(f"Task {task_id} updated successfully.")
            break

    else:
        print("Task not found.")

def mark_task(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}.")
            return
    print("Task not found.")

def show_help():
    print("""
Task CLI - Commands
         python task_cli.py add "task description"   Add a new task
python task_cli.py list                     List all tasks
python task_cli.py done <id>                Mark task as done
python task_cli.py delete <id>              Delete a task
python task_cli.py help                     Show this help menu
""") 
    
def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit()

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Please provide a task description.")
        else:
            add_task(sys.argv[2])

    elif command == "list":
        list_tasks()

    elif command == "done":
        if len(sys.argv) < 3:
            print("Please provide task ID.")
        else:
            mark_done(int(sys.argv[2]))

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Please provide the task ID to delete.")
        else:
                delete_task(int(sys.argv[2]))

    elif command == "help":
        show_help()

    elif command == "update":
        if len(sys.argv) < 4:
            print("Error: Please provide task ID and new description.")
        else:
            try:
                update_task(int(sys.argv[2]), sys.argv[3])
            except ValueError:
                print("Task ID must be a number.")

    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print("Provide task ID.")
        else:
            mark_task(int(sys.argv[2]), "in-progress")

    elif command == "mark-done":
        if len(sys.argv) < 3:
            print("Provide task ID.")
        else:
            mark_task(int(sys.argv[2]), "done")

    else:
        print("Unknown command")

if __name__ == "__main__":
    main()