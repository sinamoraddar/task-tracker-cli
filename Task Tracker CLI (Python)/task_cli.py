import argparse
import json
import uuid
from dataclasses import dataclass
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")

    # Define subcommands
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
    clear_parser = subparsers.add_parser("clear", help="Clear all tasks")

    # Mark in progress
    markinprogress_parser = subparsers.add_parser(
        "mark-in-progress", help="Mark a task in progress"
    )
    markinprogress_parser.add_argument(
        "task_id", type=int, help="Task ID to mark in progress"
    )

    # Mark done
    markdone_parser = subparsers.add_parser("mark-done", help="Mark a task done")
    markdone_parser.add_argument("task_id", type=int, help="Task ID to mark done")

    # Mark todo
    marktodo_parser = subparsers.add_parser("mark-todo", help="Mark a task todo")
    marktodo_parser.add_argument("task_id", type=int, help="Task ID to mark todo")

    # Parse arguments
    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        list_tasks(args.status)
    elif args.command == "update":
        update_task(args.task_id, args.description)
    elif args.command == "delete":
        delete_task(args.task_id)
    elif args.command == "mark-in-progress":
        markinprogress(args.task_id)
    elif args.command == "mark-done":
        markdone(args.task_id)
    elif args.command == "mark-todo":
        marktodo(args.task_id)
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
        with open("tasks.json", "w") as file:
            json.dump({"tasks": []}, file)
        return []


def list_tasks(status=None):
    data = read_json()
    found = False
    if not data:
        print("\033[1m\033[93mNo tasks found.\033[0m")
    else:
        for task in data:
            if status is None or task["status"] == status:
                print(
                    f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created At: {task['createdAt']}, Updated At: {task['updatedAt']}"
                )
                found = True
    if not found:
        print(f"\033[1m\033[91mNo tasks found with status {status}.\033[0m")
    else:
        print("\033[1m\033[92mTasks listed.\033[0m")


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


# @dataclass
# class Task:
#     id: int
#     description: str
#     status: str
#     createdAt: str
#     updatedAt: str


# new_task = Task(
#     id=1,
#     description="Go to the gym",
#     status="todo",
#     createdAt=datetime.now().isoformat(),
#     updatedAt=datetime.now().isoformat(),
# )
# print(new_task)  # Task(id=1, description='Go to the gym', status='todo', ...)


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


def markinprogress(task_id):
    data = read_json()
    found = False
    for task in data:
        if task["id"] == task_id:
            task["status"] = "in-progress"
            task["updatedAt"] = datetime.now().isoformat()
            found = True
            break
    if found:
        with open("tasks.json", "w") as file:
            json.dump({"tasks": data}, file)
        print(f"\033[1m\033[92mTask with ID {task_id} updated.\033[0m")
    else:
        print(f"\033[1m\033[91mTask with ID {task_id} not found.\033[0m")


def markdone(task_id):
    data = read_json()
    found = False
    for task in data:
        if task["id"] == task_id:
            task["status"] = "done"
            task["updatedAt"] = datetime.now().isoformat()
            found = True
            break
    if found:
        with open("tasks.json", "w") as file:
            json.dump({"tasks": data}, file)
        print(f"\033[1m\033[92mTask with ID {task_id} updated.\033[0m")
    else:
        print(f"\033[1m\033[91mTask with ID {task_id} not found.\033[0m")


def marktodo(task_id):
    data = read_json()
    found = False
    for task in data:
        if task["id"] == task_id:
            task["status"] = "todo"
            task["updatedAt"] = datetime.now().isoformat()
            found = True
            break
    if found:
        with open("tasks.json", "w") as file:
            json.dump({"tasks": data}, file)
        print(f"\033[1m\033[92mTask with ID {task_id} updated.\033[0m")
    else:
        print(f"\033[1m\033[91mTask with ID {task_id} not found.\033[0m")


def list_done_tasks():
    data = read_json()
    if not data:
        print("\033[1m\033[93mNo tasks found.\033[0m")
    else:
        for task in data:
            if task["status"] == "done":
                print(
                    f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created At: {task['createdAt']}, Updated At: {task['updatedAt']}"
                )


def list_not_done_tasks():
    data = read_json()
    if not data:
        print("\033[1m\033[93mNo tasks found.\033[0m")
    else:
        for task in data:
            if task["status"] != "done":
                print(
                    f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created At: {task['createdAt']}, Updated At: {task['updatedAt']}"
                )


def list_in_progress_tasks():
    data = read_json()
    if not data:
        print("\033[1m\033[93mNo tasks found.\033[0m")
    else:
        for task in data:
            if task["status"] == "in-progress":
                print(
                    f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created At: {task['createdAt']}, Updated At: {task['updatedAt']}"
                )


def list_todo_tasks():
    data = read_json()
    if not data:
        print("\033[1m\033[93mNo tasks found.\033[0m")
    else:
        for task in data:
            if task["status"] == "todo":
                print(
                    f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created At: {task['createdAt']}, Updated At: {task['updatedAt']}"
                )


if __name__ == "__main__":
    main()
