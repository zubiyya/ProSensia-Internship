# To-Do List Manager – CLI Tool

This is a simple, reusable command-line tool built with Python that helps you manage your daily tasks from the terminal.

Built for **#ProSensiaInternship Day 16 Task**

## 💡 Features
- Add, view, and delete tasks from your to-do list
- Colored terminal output using colorama
- Task data stored in `todo_data.json`
- Action logs saved in `logs.txt`
- Modular code structure (`cli_tool.py` and `todo_utils.py`)
- Usage help messages built with argparse

## 📦 How to Run
Make sure you have Python 3.6+ installed.

### Install Requirements:
\`\`\`
pip install colorama
\`\`\`

### Run from terminal:
\`\`\`
python cli_tool.py add "Buy milk"
python cli_tool.py view
python cli_tool.py delete 1
\`\`\`
