import tkinter as tk

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.entities.course import Course

def search():
    query = entry.get().lower()
    listbox.delete(0, tk.END)

    for course in all_courses:
        if query in (course.name or "").lower():
            listbox.insert("end", course.name)

root = tk.Tk()
root.title("Courses")
root.geometry("600x400")

frame_top = tk.Frame(root)
frame_top.pack(side="top", fill="x", pady=5)

entry = tk.Entry(frame_top, width=40)
entry.pack(side="left", padx=5, fill='x', expand=True)

btn_search = tk.Button(frame_top, text="Search", command=search)
btn_search.pack(side="left", padx=5)

frame_left = tk.Frame(root, width=150)
frame_left.pack(side="left", fill="y")

tk.Button(frame_left, text="Filter X").pack(pady=5, padx=5)
tk.Button(frame_left, text="Filter Y").pack(pady=5, padx=5)
tk.Button(frame_left, text="Filter Z").pack(pady=5, padx=5)

frame_main = tk.Frame(root)
frame_main.pack(side="left", fill="both", expand=True)

listbox = tk.Listbox(frame_main)
listbox.pack(fill="both", expand=True, padx=5, pady=5)

all_courses = Course.all()
for course in all_courses:
    listbox.insert("end", course.name)

root.mainloop()
