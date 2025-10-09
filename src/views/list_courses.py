import tkinter as tk

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.entities.course import Course

def search():
    query = entry.get().strip()
    listbox.delete(0, tk.END)

    if not query:
        listbox.insert("end", "Please enter a search term.")
        return []

    courses = Course.search(query)

    if not courses:
        listbox.insert("end", f"No courses found for '{query}'.")
        return []

    for course in courses:
        display_text = f"{course.course_code} - {course.name} ({course.status})"
        listbox.insert("end", display_text)

    return courses

def filter_courses_with_no_students():
    courses = Course.with_no_students_yet()
    listbox.delete(0, tk.END)

    if not courses:
        listbox.insert("end", "No courses found with the given criteria.")
        return []

    for course in courses:
        display_text = f"{course['course_code']} - {course['name']} ({course['status']})"
        listbox.insert("end", display_text)

    return courses

def filter_courses_by_lecturer_expertises():
    courses = Course.lecturer_expertises()
    listbox.delete(0, tk.END)

    if not courses:
        listbox.insert("end", "No courses found with the given criteria.")
        return []

    for course in courses:
        display_text = f"{course['course_code']} - {course['course_name']} - Lecturer: {course['lecturer_name']} [{', '.join(course['lecturer_areas'])}]"
        listbox.insert("end", display_text)

    return courses

def all_courses():
    courses = Course.all()
    listbox.delete(0, tk.END)

    if not courses:
        listbox.insert("end", "No courses found with the given criteria.")
        return []

    for course in courses:
        display_text = f"{course.course_code} - {course.name} ({course.status})"
        listbox.insert("end", display_text)

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

tk.Button(frame_left, text="No students yet", command=filter_courses_with_no_students).pack(pady=5, padx=5, fill='x')
tk.Button(frame_left, text="Lecturer expertise for each course", command=filter_courses_by_lecturer_expertises).pack(pady=5, padx=5, fill='x')
tk.Button(frame_left, text="All courses", command=all_courses).pack(pady=5, padx=5, fill='x')

frame_main = tk.Frame(root)
frame_main.pack(side="left", fill="both", expand=True)

listbox = tk.Listbox(frame_main)
listbox.pack(fill="both", expand=True, padx=5, pady=5)

all_courses()

root.mainloop()
