TASK MANAGEMENT & DAILY PLANNING SYSTEM (CLI)

A menu-driven, object-oriented task management system built in Python that helps users manage tasks, track deadlines, prioritize work, and generate a daily plan — all from the command line.

---

FEATURES

TASK MANAGEMENT

- Add, remove, and view tasks
- Assign priority (High / Medium / Low)
- Set deadlines with format validation
- Mark tasks as completed
- Persistent storage using a JSON file

TASK INSIGHTS

- Check if a task is overdue
- View remaining time for a task
- Automatically mark overdue tasks

PRIORITY ENGINE

- Sort tasks by deadline
- Sort tasks by priority
- View urgent tasks (High priority + not completed)

DAILY PLANNER

- Generate a daily plan based on available time
- Separate tasks into today’s plan and overflow
- Show remaining free time
- Warn if workload exceeds available time
- Suggest breaks based on workload length

MENU-DRIVEN CLI

- Organized menus for different task categories
- Input validation to prevent crashes
- Easy navigation and clean interface

---

TECH STACK

Language:

- Python 3

Concepts Used:

- Object-Oriented Programming (OOP)
- File I/O using JSON
- Dictionary comprehensions
- Sorting with custom keys
- Date and time handling

Libraries:

- datetime
- json
- os

---

PROJECT STRUCTURE

task-system/
|
|-- tasks.json
|-- main.py
|-- README.txt

---

HOW TO RUN

1. Clone the repository
2. Navigate into the project folder
3. Run: python main.py

---

AUTHOR

Built by Hamza
Student | Aspiring Software & AI Engineer
