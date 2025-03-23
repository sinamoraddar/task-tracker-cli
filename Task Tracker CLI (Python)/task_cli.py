import argparse
import json
import uuid
from dataclasses import dataclass
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Task sdsdTracker CLI")

    # Define subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add Task
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", type=str, help="Task description")

    # List Tasks
    list_parser = subparsers.add_parser("list", help="List all tasks")

    # Update Task
    update_parser = subparsers.add_parser("update", help="Update a task description")
    update_parser.add_argument("task_id", type=int, help="Task ID")
    update_parser.add_argument("description", type=str, help="New description")

    # Delete Task
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="Task ID to delete")

    # Clear Tasks
    clear_parser = subparsers.add_parser("clear", help="Clear all tasks")

    # Parse arguments
    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        read_json()
    elif args.command == "update":
        update_task(args.task_id, args.description)
        pass
    elif args.command == "delete":
        delete_task(args.task_id)
        pass
    elif args.command == "clear":
        clear_tasks()
    else:
        print("Please specify a command. Use -h for help.")


def read_json():
    # Open and read the JSON file
    try:
        with open("tasks.json", "r") as file:
            data = json.load(file)
            return data.get("tasks", [])
    except FileNotFoundError:
        print("File not found. Creating new file.")
        return []


def add_task(description):
    data = read_json()
    new_id = data[-1]["id"] + 1 if data else 1
    data.append(
        {
            "id": new_id,
            "description": description,
            "status": "todo",
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat(),
        }
    )
    with open("tasks.json", "w") as file:
        json.dump({"tasks": data}, file)


@dataclass
class Task:
    id: int
    description: str
    status: str
    createdAt: str
    updatedAt: str


new_task = Task(
    id=1,
    description="Go to the gym",
    status="todo",
    createdAt=datetime.now().isoformat(),
    updatedAt=datetime.now().isoformat(),
)
print(new_task)  # Task(id=1, description='Go to the gym', status='todo', ...)


def update_task(task_id, description):
    data = read_json()
    found = False
    for task in data:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = datetime.now().isoformat()
            found = True
            break
    if found:
        with open("tasks.json", "w") as file:
            json.dump({"tasks": data}, file)
        print(f"\033[1m\033[92mTask with ID {task_id} updated.\033[0m")
    else:
        print(f"\033[1m\033[91mTask with ID {task_id} not found.\033[0m")


def delete_task(task_id):
    data = read_json()
    found = False
    for task in data:
        if task["id"] == task_id:
            data.remove(task)
            found = True
            break
    if found:
        with open("tasks.json", "w") as file:
            json.dump({"tasks": data}, file)
        print(f"\033[1m\033[92mTask with ID {task_id} deleted.\033[0m")
    else:
        print(f"\033[1m\033[91mTask with ID {task_id} not found.\033[0m")


def clear_tasks():
    with open("tasks.json", "w") as file:
        json.dump({"tasks": []}, file)
    print("\033[1m\033[92mAll tasks cleared.\033[0m")


if __name__ == "__main__":
    main()
