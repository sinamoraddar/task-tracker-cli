"""A command-line interface for managing tasks with basic CRUD operations and status tracking."""

import argparse
import json
from datetime import datetime
from typing import List, Dict, Optional

# Constants
TASK_FILE = "tasks.json"
VALID_STATUSES = ["todo", "in-progress", "done"]

# ANSI color codes for terminal output
COLORS = {
    "GREEN": "\033[1m\033[92m",
    "RED": "\033[1m\033[91m",
    "YELLOW": "\033[1m\033[93m",
    "RESET": "\033[0m"
}

def read_json() -> List[Dict]:
    """Read tasks from the JSON file.
    
    Returns:
        List[Dict]: List of task dictionaries. Returns empty list if file doesn't exist.
    """
    try:
        with open(TASK_FILE, "r") as file:
            data = json.load(file)
            return data.get("tasks", [])
    except FileNotFoundError:
        print(f"{COLORS['YELLOW']}File not found. Creating new file.{COLORS['RESET']}")
        with open(TASK_FILE, "w") as file:
            json.dump({"tasks": []}, file)
        return []

def save_json(data: List[Dict]) -> None:
    """Save tasks to the JSON file.
    
    Args:
        data (List[Dict]): List of task dictionaries to save.
    """
    with open(TASK_FILE, "w") as file:
        json.dump({"tasks": data}, file)

def list_tasks(status: Optional[str] = None) -> None:
    """List tasks, optionally filtered by status.
    
    Args:
        status (Optional[str]): If provided, only show tasks with this status.
    """
    data = read_json()
    found = False
    
    if not data:
        print(f"{COLORS['YELLOW']}No tasks found.{COLORS['RESET']}")
        return
        
    for task in data:
        if status is None or task["status"] == status:
            print(
                f"ID: {task['id']}, Description: {task['description']}, "
                f"Status: {task['status']}, Created At: {task['createdAt']}, "
                f"Updated At: {task['updatedAt']}"
            )
            found = True
            
    if not found and status:
        print(f"{COLORS['RED']}No tasks found with status {status}.{COLORS['RESET']}")
    elif found:
        print(f"{COLORS['GREEN']}Tasks listed.{COLORS['RESET']}")

def add_task(description: str) -> None:
    """Add a new task.
    
    Args:
        description (str): Description of the task to add.
    """
    data = read_json()
    new_id = data[-1]["id"] + 1 if data else 1
    current_time = datetime.now().isoformat()
    
    data.append({
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": current_time,
        "updatedAt": current_time,
    })
    
    save_json(data)
    print(f"{COLORS['GREEN']}Task added successfully.{COLORS['RESET']}")

def update_task(task_id: int, description: str) -> None:
    """Update a task's description.
    
    Args:
        task_id (int): ID of the task to update.
        description (str): New description for the task.
    """
    data = read_json()
    found = False
    
    for task in data:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = datetime.now().isoformat()
            found = True
            break
            
    if found:
        save_json(data)
        print(f"{COLORS['GREEN']}Task with ID {task_id} updated.{COLORS['RESET']}")
    else:
        print(f"{COLORS['RED']}Task with ID {task_id} not found.{COLORS['RESET']}")

def delete_task(task_id: int) -> None:
    """Delete a task.
    
    Args:
        task_id (int): ID of the task to delete.
    """
    data = read_json()
    found = False
    
    for task in data:
        if task["id"] == task_id:
            data.remove(task)
            found = True
            break
            
    if found:
        save_json(data)
        print(f"{COLORS['GREEN']}Task with ID {task_id} deleted.{COLORS['RESET']}")
    else:
        print(f"{COLORS['RED']}Task with ID {task_id} not found.{COLORS['RESET']}")

def clear_tasks() -> None:
    """Clear all tasks from the task list."""
    save_json([])
    print(f"{COLORS['GREEN']}All tasks cleared.{COLORS['RESET']}")

def update_task_status(task_id: int, new_status: str) -> None:
    """Update a task's status.
    
    Args:
        task_id (int): ID of the task to update.
        new_status (str): New status for the task.
    """
    if new_status not in VALID_STATUSES:
        print(f"{COLORS['RED']}Invalid status: {new_status}{COLORS['RESET']}")
        return
        
    data = read_json()
    found = False
    
    for task in data:
        if task["id"] == task_id:
            task["status"] = new_status
            task["updatedAt"] = datetime.now().isoformat()
            found = True
            break
            
    if found:
        save_json(data)
        print(f"{COLORS['GREEN']}Task with ID {task_id} marked as {new_status}.{COLORS['RESET']}")
    else:
        print(f"{COLORS['RED']}Task with ID {task_id} not found.{COLORS['RESET']}")

def main():
    """Main entry point for the Task Tracker CLI."""
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add Task
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", type=str, help="Task description")

    # List Tasks
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "status", type=str, nargs="?", help="Task status (optional)"
    )

    # Update Task
    update_parser = subparsers.add_parser("update", help="Update a task description")
    update_parser.add_argument("task_id", type=int, help="Task ID")
    update_parser.add_argument("description", type=str, help="New description")

    # Delete Task
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="Task ID to delete")

    # Clear Tasks
    subparsers.add_parser("clear", help="Clear all tasks")

    # Status commands
    for status in ["mark-in-progress", "mark-done", "mark-todo"]:
        status_parser = subparsers.add_parser(status, help=f"Mark a task as {status.replace('mark-', '')}")
        status_parser.add_argument("task_id", type=int, help=f"Task ID to {status}")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        list_tasks(args.status)
    elif args.command == "update":
        update_task(args.task_id, args.description)
    elif args.command == "delete":
        delete_task(args.task_id)
    elif args.command == "clear":
        clear_tasks()
    elif args.command == "mark-in-progress":
        update_task_status(args.task_id, "in-progress")
    elif args.command == "mark-done":
        update_task_status(args.task_id, "done")
    elif args.command == "mark-todo":
        update_task_status(args.task_id, "todo")
    else:
        print(f"{COLORS['YELLOW']}Please specify a command. Use -h for help.{COLORS['RESET']}")

if __name__ == "__main__":
    main()
