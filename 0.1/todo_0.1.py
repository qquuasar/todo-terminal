#!/usr/bin/env python3

import argparse
import json
import os
from pathlib import Path

DATA_FILE = Path.home() / '.todo.json'

def load_tasks():
    if DATA_FILE.exists():
        with open(DATA_FILE,'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE,'w') as f:
        json.dump(tasks, f, indent=2)

def add_task(text):
    tasks = load_tasks()
    tasks.append({'text':text,'done':False})
    save_tasks(tasks)
    print(f"[V] Added task: {text}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks for now!")
        return
    for i, task in enumerate(tasks, 1):
        status = '✓' if task['done'] else ' '
        print(f"{i:2}, [{status}] {task['text']}")

def mark_done(index):
    tasks = load_tasks()
    try:
        tasks[index - 1]['done'] = True
        save_tasks(tasks)
        print(f"[✓] Done: {tasks[index-1]['text']}")
    except IndexError:
        print("No entries for this task")

def main():
    parser = argparse.ArgumentParser(description="TODO in terminal")
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('list', help='Show task list')

    add = subparsers.add_parser('add', help='Add task')
    add.add_argument('text',nargs='+')

    done = subparsers.add_parser('done',help="Mark as done")
    done.add_argument('id',type=int)

    rm = subparsers.add_parser('rm', help='Remove task')
    rm.add_argument('id',type=int)

    args = parser.parse_args()

    if args.command == 'add':
        add_task(' '.join(args.text))
    elif args.command == 'list':
        list_tasks()
    elif args.command == 'done':
        mark_done(args.id)
    elif args.command == 'rm':
        remove_task(args.id)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
