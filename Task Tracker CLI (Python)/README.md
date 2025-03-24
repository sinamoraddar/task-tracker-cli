# Task Tracker CLI

A simple and efficient command-line interface for managing your tasks. This CLI tool allows you to create, list, update, and manage tasks with different statuses.

## Features

- Create new tasks
- List all tasks or filter by status
- Update task descriptions
- Delete tasks
- Mark tasks as todo, in-progress, or done
- Clear all tasks
- Persistent storage using JSON
- Color-coded output for better visibility

## Installation

1. Clone this repository:
```bash
git clone git@github.com:sinamoraddar/task-tracker-cli.git
cd task-tracker-cli
```

2. Make sure you have Python 3.6 or higher installed.

3. Run the script:
```bash
python task_cli.py
```

## Usage

### Adding a Task
```bash
python task_cli.py add "Complete the project documentation"
```

### Listing Tasks
List all tasks:
```bash
python task_cli.py list
```

List tasks with a specific status:
```bash
python task_cli.py list todo
python task_cli.py list "in-progress"
python task_cli.py list done
```

### Updating a Task
```bash
python task_cli.py update 1 "Updated task description"
```

### Deleting a Task
```bash
python task_cli.py delete 1
```

### Changing Task Status
Mark a task as in progress:
```bash
python task_cli.py mark-in-progress 1
```

Mark a task as done:
```bash
python task_cli.py mark-done 1
```

Mark a task as todo:
```bash
python task_cli.py mark-todo 1
```

### Clearing All Tasks
```bash
python task_cli.py clear
```

### Getting Help
To see all available commands and their usage:
```bash
python task_cli.py -h
```

To get help for a specific command:
```bash
python task_cli.py add -h
python task_cli.py list -h
python task_cli.py update -h
```

## Task Statuses

The following statuses are available:
- `todo`: Task is pending
- `in-progress`: Task is currently being worked on
- `done`: Task has been completed

## Data Storage

Tasks are stored in a `tasks.json` file in the same directory as the script. Each task contains:
- ID (auto-incrementing)
- Description
- Status
- Creation timestamp
- Last update timestamp

## Output Format

Tasks are displayed in the following format:
```
ID: <id>, Description: <description>, Status: <status>, Created At: <timestamp>, Updated At: <timestamp>
```

## Color Coding

- 🟢 Green: Success messages
- 🔴 Red: Error messages
- 🟡 Yellow: Information messages

## Contributing

Feel free to submit issues and enhancement requests! 