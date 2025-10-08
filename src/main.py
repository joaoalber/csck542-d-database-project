import tkinter as tk
import subprocess
import sys
import os
from repository import MySQLRepository

repo = MySQLRepository()

def open_window(file_name):
    python = sys.executable
    subprocess.Popen([python, file_name])

root = tk.Tk()
root.title("Academic Database")
root.geometry("300x165")

tk.Button(root, text="Students", width=20, command=lambda: open_window("src/views/list_students.py")).pack(pady=10)
tk.Button(root, text="Lecturers", width=20, command=lambda: open_window("src/views/list_lecturers.py")).pack(pady=10)
tk.Button(root, text="Courses", width=20, command=lambda: open_window("src/views/list_courses.py")).pack(pady=10)

def on_close():
    repo.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
