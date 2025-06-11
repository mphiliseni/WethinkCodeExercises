import argparse
from task_manager import TaskManager

def main():
    parser = argparse.ArgumentParser(description="Task Management CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create
    create_parser = subparsers.add_parser("create", help="Create a new task")
    create_parser.add_argument("title")
    create_parser.add_argument("--description", default="")
    create_parser.add_argument("--priority", type=int, default=2)
    create_parser.add_argument("--due", default=None)
    create_parser.add_argument("--tags", default="")

    # List
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--status", choices=["todo", "in_progress", "review", "done"])
    list_parser.add_argument("--priority", type=int, choices=[1,2,3,4])
    list_parser.add_argument("--overdue", action="store_true")

    # Stats
    subparsers.add_parser("stats", help="Show task statistics")

    # Update status
    update_status_parser = subparsers.add_parser("update-status", help="Update task status")
    update_status_parser.add_argument("task_id")
    update_status_parser.add_argument("new_status", choices=["todo", "in_progress", "review", "done"])

    # Update priority
    update_priority_parser = subparsers.add_parser("update-priority", help="Update task priority")
    update_priority_parser.add_argument("task_id")
    update_priority_parser.add_argument("new_priority", type=int, choices=[1,2,3,4])

    # Update due date
    update_due_parser = subparsers.add_parser("update-due-date", help="Update task due date")
    update_due_parser.add_argument("task_id")
    update_due_parser.add_argument("new_due_date")

    # Add tag
    add_tag_parser = subparsers.add_parser("add-tag", help="Add a tag to a task")
    add_tag_parser.add_argument("task_id")
    add_tag_parser.add_argument("tag")

    # Remove tag
    remove_tag_parser = subparsers.add_parser("remove-tag", help="Remove a tag from a task")
    remove_tag_parser.add_argument("task_id")
    remove_tag_parser.add_argument("tag")

    # Show task details
    show_parser = subparsers.add_parser("show", help="Show task details")
    show_parser.add_argument("task_id")

    args = parser.parse_args()
    manager = TaskManager()

    if args.command == "create":
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        task = manager.add_task(args.title, args.description, args.priority, args.due, tags)
        print(f"Task created successfully: ID {task['id']}, Title: {task['title']}")

    elif args.command == "list":
        tasks = manager.list_tasks(args.status, args.priority, args.overdue)
        if not tasks:
            print("No tasks found.")
        else:
            for t in tasks:
                print(f"ID: {t['id']}, Title: {t['title']}, Status: {t['status']}, Priority: {t['priority']}, Due: {t['due']}")

    elif args.command == "stats":
        stats = manager.get_statistics()
        print("Task Statistics:")
        for key, value in stats.items():
            print(f"{key.capitalize()}: {value}")

    elif args.command == "update-status":
        task = manager.update_status(args.task_id, args.new_status)
        if task:
            print(f"Task {args.task_id} status updated to {args.new_status}.")
        else:
            print(f"Task {args.task_id} not found.")

    elif args.command == "update-priority":
        task = manager.update_priority(args.task_id, args.new_priority)
        if task:
            print(f"Task {args.task_id} priority updated to {args.new_priority}.")
        else:
            print(f"Task {args.task_id} not found.")

    elif args.command == "update-due-date":
        task = manager.update_due_date(args.task_id, args.new_due_date)
        if task:
            print(f"Task {args.task_id} due date updated to {args.new_due_date}.")
        else:
            print(f"Task {args.task_id} not found.")

    elif args.command == "add-tag":
        task = manager.add_tag(args.task_id, args.tag)
        if task:
            print(f"Tag '{args.tag}' added to task {args.task_id}.")
        else:
            print(f"Task {args.task_id} not found.")

    elif args.command == "remove-tag":
        task = manager.remove_tag(args.task_id, args.tag)
        if task:
            print(f"Tag '{args.tag}' removed from task {args.task_id}.")
        else:
            print(f"Task {args.task_id} not found.")

    elif args.command == "show":
        task = manager.get_task(args.task_id)
        if task:
            print("Task Details:")
            for k, v in task.items():
                print(f"{k.capitalize()}: {v}")
        else:
            print(f"Task {args.task_id} not found.")

if __name__ == "__main__":
    main()
