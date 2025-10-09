import tkinter as tk

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.entities.student import Student

def search():
    query = entry.get().strip()
    listbox.delete(0, tk.END)

    if not query:
        listbox.insert("end", "Please enter a search term.")
        return []

    students = Student.search(query)

    if not students:
        listbox.insert("end", f"No students found for '{query}'.")
        return []

    for student in students:
        display_text = f"{student.name} ({student.contact_info})"
        listbox.insert("end", display_text)

    return students

def filter_top_students():
    students = Student.top_completed_students()
    listbox.delete(0, tk.END)

    if not students:
        listbox.insert("end", "No students found with the given criteria.")
        return []

    for student in students:
        display_text = f"{student['name']} - Final Grade: {student['final_grade']}"
        listbox.insert("end", display_text)

    return students

def filter_not_enrolled_students():
    students = Student.not_enrolled_yet()
    listbox.delete(0, tk.END)

    if not students:
        listbox.insert("end", "No students found with the given criteria.")
        return []

    for student in students:
        display_text = f"{student['name']}"
        listbox.insert("end", display_text)

    return students

def all_students():
    students = Student.all()
    listbox.delete(0, tk.END)

    if not students:
        listbox.insert("end", "No students found with the given criteria.")
        return []

    for student in students:
        display_text = f"{student.name} ({student.contact_info})"
        listbox.insert("end", display_text)

    return students

root = tk.Tk()
root.title("Students")
root.geometry("600x400")

frame_top = tk.Frame(root)
frame_top.pack(side="top", fill="x", pady=5)

entry = tk.Entry(frame_top, width=40)
entry.pack(side="left", padx=5, fill='x', expand=True)

btn_search = tk.Button(frame_top, text="Search", command=search)
btn_search.pack(side="left", padx=5)

frame_left = tk.Frame(root, width=150)
frame_left.pack(side="left", fill="y")

tk.Button(frame_left, text="High-rated students", command=filter_top_students).pack(pady=5, padx=5, fill='x')
tk.Button(frame_left, text="Not enrolled yet", command=filter_not_enrolled_students).pack(pady=5, padx=5, fill='x')
tk.Button(frame_left, text="All students", command=all_students).pack(pady=5, padx=5, fill='x')

frame_main = tk.Frame(root)
frame_main.pack(side="left", fill="both", expand=True)

listbox = tk.Listbox(frame_main)
listbox.pack(fill="both", expand=True, padx=5, pady=5)

all_students()

root.mainloop()
