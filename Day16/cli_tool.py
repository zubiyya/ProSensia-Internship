
import argparse
from colorama import init, Fore
from todo_utils import load_tasks, save_tasks, log_action

init(autoreset=True)

def add_task(description):
    tasks = load_tasks()
    tasks.append({"desc": description})
    save_tasks(tasks)
    log_action(f"Added: {description}")
    print(Fore.GREEN + "✅ Task added.")

def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print(Fore.YELLOW + "📭 No tasks found.")
        return
    print(Fore.CYAN + "--- Your To-Do List ---")
    for idx, task in enumerate(tasks, 1):
        print(Fore.WHITE + f"{idx}. {task['desc']}")

def delete_task(index):
    tasks = load_tasks()
    if 0 < index <= len(tasks):
        removed = tasks.pop(index - 1)
        save_tasks(tasks)
        log_action(f"Deleted: {removed['desc']}")
        print(Fore.RED + f"🗑️ Deleted: {removed['desc']}")
    else:
        print(Fore.YELLOW + "⚠️ Invalid task number.")

def main():
    parser = argparse.ArgumentParser(
        description="📝 A simple command-line To-Do List Manager"
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("view", help="View all saved tasks")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("desc", type=str, help="Task description")

    del_parser = subparsers.add_parser("delete", help="Delete a task by number")
    del_parser.add_argument("index", type=int, help="Task number to delete")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.desc)
    elif args.command == "view":
        view_tasks()
    elif args.command == "delete":
        delete_task(args.index)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
