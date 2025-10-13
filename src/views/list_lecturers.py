
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

THIS_DIR = Path(__file__).resolve().parent
SRC_DIR = THIS_DIR.parent
PROJECT_ROOT = SRC_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.entities.lecturer import Lecturer


def center_on_screen(win: tk.Tk, width: int, height: int) -> None:
    win.update_idletasks()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    x = (sw - width) // 2
    y = (sh - height) // 5
    win.geometry(f"{width}x{height}+{x}+{y}")


class LecturersApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Lecturers")

        # window sizing (responsive)
        DEFAULT_W, DEFAULT_H = 900, 600
        self.minsize(720, 480)
        center_on_screen(self, DEFAULT_W, DEFAULT_H)
        

        # grid weights for resize
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self._build_ui()
        self._load_all()

    def _build_ui(self) -> None:
        # top bar: search
        top = ttk.Frame(self, padding=(10, 10, 10, 0))
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(1, weight=1)

        ttk.Label(top, text="Search:").grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(top, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=1, sticky="ew")
        ttk.Button(top, text="Search", command=self._on_search).grid(row=0, column=2, padx=(8, 0))

        # main area: sidebar + table
        main = ttk.Frame(self, padding=10)
        main.grid(row=1, column=0, sticky="nsew")
        main.rowconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)  # table expands

        # sidebar
        side = ttk.Frame(main)
        side.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        ttk.Label(side, text="Filters", style="Headline.TLabel").grid(row=0, column=0, pady=(0, 8))
        ttk.Button(side, text="All lecturers", width=22, command=self._load_all).grid(row=1, column=0, pady=3, sticky="ew")
        ttk.Button(side, text="With no courses", width=22, command=self._load_no_courses).grid(row=2, column=0, pady=3, sticky="ew")
        ttk.Button(side, text="With advised students", width=22, command=self._load_advised).grid(row=3, column=0, pady=3, sticky="ew")

        # table
        table_frame = ttk.Frame(main)
        table_frame.grid(row=0, column=1, sticky="nsew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        cols = ("lecturer_id", "name", "extra")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # headings
        self.tree.heading("lecturer_id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("extra", text="Details")

        # columns: id fixed, name stretches, extra fixed-ish
        self.tree.column("lecturer_id", width=90, anchor="w", stretch=False)
        self.tree.column("name", width=380, anchor="w", stretch=True)
        self.tree.column("extra", width=340, anchor="w", stretch=False)

        # scrollbar
        yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        yscroll.grid(row=0, column=1, sticky="ns")

        # double-click info
        self.tree.bind("<Double-1>", self._on_open_details)

        # style polish
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Headline.TLabel", font=("Segoe UI", 10, "bold"))

    def _clear(self) -> None:
        for iid in self.tree.get_children():
            self.tree.delete(iid)

    def _insert_simple(self, rows) -> None:
        """Insert rows shaped like {'lecturer_id','name'}."""
        for r in rows:
            self.tree.insert("", "end", values=(r.get("lecturer_id"), r.get("name"), ""))

    def _load_all(self) -> None:
        self._clear()
        rows = [{"lecturer_id": l.lecturer_id, "name": l.name} for l in Lecturer.all()]
        self._insert_simple(rows)

    def _load_no_courses(self) -> None:
        self._clear()
        data = Lecturer.with_no_courses_yet()  # [{'lecturer_id', 'lecturer_name'}...]
        for r in data:
            self.tree.insert(
                "", "end",
                values=(r.get("lecturer_id"), r.get("lecturer_name"), "No courses")
            )

    def _load_advised(self) -> None:
        self._clear()
        data = Lecturer.with_advised_students()  # [{'lecturer_name', 'students':[{'student_name'}...]}]
        for r in data:
            names = ", ".join(s.get("student_name") for s in r.get("students", [])) or "—"
            self.tree.insert(
                "", "end",
                values=(None, r.get("lecturer_name"), f"Students: {names}")
            )

    def _on_search(self) -> None:
        term = (self.search_var.get() or "").strip()
        if not term:
            self._load_all()
            return
        self._clear()
        matches = Lecturer.search(term)  # list of Lecturer
        rows = [{"lecturer_id": l.lecturer_id, "name": l.name} for l in matches]
        if not rows:
            messagebox.showinfo("Search", f"No lecturers found for '{term}'.", parent=self)
        self._insert_simple(rows)

    def _on_open_details(self, _evt=None) -> None:
        cur = self.tree.focus()
        if not cur:
            return
        lid, name, extra = self.tree.item(cur, "values")
        messagebox.showinfo("Lecturer", f"Name: {name}\nID: {lid or '—'}\n{extra}", parent=self)


if __name__ == "__main__":
    app = LecturersApp()
    app.mainloop()
