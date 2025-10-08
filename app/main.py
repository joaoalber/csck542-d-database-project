import tkinter as tk
import subprocess
import sys
import os

def open_window(file_name):
    python = sys.executable
    subprocess.Popen([python, file_name])

root = tk.Tk()
root.title("Academic Database")
root.geometry("300x165")

tk.Button(root, text="Students", width=20, command=lambda: open_window("app/views/list_students.py")).pack(pady=10)
tk.Button(root, text="Lecturers", width=20, command=lambda: open_window("app/views/list_lecturers.py")).pack(pady=10)
tk.Button(root, text="Courses", width=20, command=lambda: open_window("app/views/list_courses.py")).pack(pady=10)

root.mainloop()
