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
    delete_parser = subparsers.add_parser("delettte", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="Task ID to delete")

    # Parse arguments
    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        read_json()
    elif args.command == "update":
        # TODO: Implement update functionality
        pass
    elif args.command == "delettte":
        # TODO: Implement delete functionality
        pass
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
    data.append(
        {
            "id": len(data) + 1,
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


if __name__ == "__main__":
    main()
