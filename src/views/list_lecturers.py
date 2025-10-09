import tkinter as tk

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.entities.lecturer import Lecturer

def search():
    query = entry.get().strip()
    listbox.delete(0, tk.END)

    if not query:
        listbox.insert("end", "Please enter a search term.")
        return []

    lecturers = Lecturer.search(query)

    if not lecturers:
        listbox.insert("end", f"No lecturers found for '{query}'.")
        return []

    for lecturer in lecturers:
        display_text = f"{lecturer.lecturer_id} - {lecturer.name}"
        listbox.insert("end", display_text)

def filter_lecturers_with_no_courses():
    lecturers = Lecturer.with_no_courses_yet()
    listbox.delete(0, tk.END)

    if not lecturers:
        listbox.insert("end", "No lecturers found with the given criteria.")
        return []

    for lecturer in lecturers:
        display_text = f"{lecturer['lecturer_id']} - {lecturer['lecturer_name']}"
        listbox.insert("end", display_text)

    return lecturers

def filter_courses_by_advised_students():
    lecturers = Lecturer.with_advised_students()
    listbox.delete(0, tk.END)

    if not lecturers:
        listbox.insert("end", "No lecturers found with the given criteria.")
        return []

    for lecturer in lecturers:
        student_names = [s["student_name"] for s in lecturer["students"]]
        display_text = f"{lecturer['lecturer_name']} — Students: {', '.join(student_names)}"
        listbox.insert("end", display_text)

    return lecturers

def all_lecturers():
    lecturers = Lecturer.all()
    listbox.delete(0, tk.END)

    if not lecturers:
        listbox.insert("end", "No lecturers found with the given criteria.")
        return []

    for lecturer in lecturers:
        listbox.insert("end", lecturer.name)

root = tk.Tk()
root.title("Lecturers")
root.geometry("600x400")

frame_top = tk.Frame(root)
frame_top.pack(side="top", fill="x", pady=5)

entry = tk.Entry(frame_top, width=40)
entry.pack(side="left", padx=5, fill='x', expand=True)

btn_search = tk.Button(frame_top, text="Search", command=search)
btn_search.pack(side="left", padx=5)

frame_left = tk.Frame(root, width=150)
frame_left.pack(side="left", fill="y")

tk.Button(frame_left, text="Lecturers with no course", command=filter_lecturers_with_no_courses).pack(pady=5, padx=5, fill='x')
tk.Button(frame_left, text="Lecturers with advised students", command=filter_courses_by_advised_students).pack(pady=5, padx=5, fill='x')
tk.Button(frame_left, text="All lecturers", command=all_lecturers).pack(pady=5, padx=5, fill='x')

frame_main = tk.Frame(root)
frame_main.pack(side="left", fill="both", expand=True)

listbox = tk.Listbox(frame_main)
listbox.pack(fill="both", expand=True, padx=5, pady=5)

all_lecturers()

root.mainloop()
