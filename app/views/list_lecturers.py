import tkinter as tk

def search():
    query = entry.get()
    print(f"Searching lecturers for: {query}")

root = tk.Tk()
root.title("Lecturers")
root.geometry("600x400")

frame_top = tk.Frame(root)
frame_top.pack(side="top", fill="x", pady=5)

entry = tk.Entry(frame_top, width=40)
entry.pack(side="left", padx=5)

btn_search = tk.Button(frame_top, text="Search", command=search)
btn_search.pack(side="left")

frame_left = tk.Frame(root, width=150)
frame_left.pack(side="left", fill="y")

tk.Button(frame_left, text="Filter A").pack(pady=5, padx=5)
tk.Button(frame_left, text="Filter B").pack(pady=5, padx=5)
tk.Button(frame_left, text="Filter C").pack(pady=5, padx=5)

frame_main = tk.Frame(root)
frame_main.pack(side="left", fill="both", expand=True)

listbox = tk.Listbox(frame_main)
listbox.pack(fill="both", expand=True, padx=5, pady=5)

for i in range(10):
    listbox.insert("end", f"Lecturer {i+1}")

root.mainloop()
