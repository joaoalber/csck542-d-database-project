from __future__ import annotations

import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

THIS_DIR = Path(__file__).resolve().parent
SRC_DIR = THIS_DIR.parent
PROJECT_ROOT = SRC_DIR.parent

# Ensure both repo root and src are on sys.path
for p in (str(PROJECT_ROOT), str(SRC_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from entities.course import Course
except ModuleNotFoundError:
    from src.entities.course import Course


def center_on_screen(win: tk.Tk, width: int, height: int) -> None:
    win.update_idletasks()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    x = max((sw - width) // 2, 0)
    y = max((sh - height) // 5, 0)
    win.geometry(f"{width}x{height}+{x}+{y}")


class CoursesApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Courses")

        # Window sizing
        DEFAULT_W, DEFAULT_H = 900, 600
        self.minsize(720, 480)
        center_on_screen(self, DEFAULT_W, DEFAULT_H)

        # Make main area expandable
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self._build_ui()
        self._load_all()

    def _build_ui(self) -> None:
        # Try a neutral ttk theme
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Headline.TLabel", font=("Segoe UI", 10, "bold"))

        # Top: search row
        top = ttk.Frame(self, padding=(10, 10, 10, 0))
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(1, weight=1)

        ttk.Label(top, text="Search:").grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(top, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=1, sticky="ew")
        ttk.Button(top, text="Search", command=self._on_search).grid(row=0, column=2, padx=(8, 0))
        self.bind("<Return>", lambda _e: self._on_search())

        # Main: sidebar + table
        main = ttk.Frame(self, padding=10)
        main.grid(row=1, column=0, sticky="nsew")
        main.rowconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)  # table expands

        # Sidebar filters
        side = ttk.Frame(main)
        side.grid(row=0, column=0, sticky="ns", padx=(0, 12))
        ttk.Label(side, text="Filters", style="Headline.TLabel").grid(row=0, column=0, pady=(0, 8))
        ttk.Button(side, text="All courses", width=20, command=self._load_all).grid(row=1, column=0, pady=3, sticky="ew")
        ttk.Button(side, text="No students yet", width=20, command=self._load_no_students).grid(row=2, column=0, pady=3, sticky="ew")
        ttk.Button(side, text="Lecturer expertise", width=20, command=self._load_expertise).grid(row=3, column=0, pady=3, sticky="ew")

        # Table area
        table_frame = ttk.Frame(main)
        table_frame.grid(row=0, column=1, sticky="nsew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        cols = ("course_code", "name", "status", "extra")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Headings
        self.tree.heading("course_code", text="Code")
        self.tree.heading("name", text="Name")
        self.tree.heading("status", text="Status")
        self.tree.heading("extra", text="Details")

        # Column widths / stretch
        self.tree.column("course_code", width=110, anchor="w", stretch=False)
        self.tree.column("name",        width=420, anchor="w", stretch=True)
        self.tree.column("status",      width=120, anchor="center", stretch=False)
        self.tree.column("extra",       width=220, anchor="w", stretch=True)

        # Scrollbar
        yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        yscroll.grid(row=0, column=1, sticky="ns")

        # Double-click to view details
        self.tree.bind("<Double-1>", self._on_open_row)

    def _clear(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

    def _insert_rows(self, rows) -> None:
        for r in rows:
            self.tree.insert(
                "", "end",
                values=(
                    r.get("course_code"),
                    r.get("name"),
                    r.get("status"),
                    r.get("extra", ""),
                )
            )

    def _load_all(self) -> None:
        self._clear()
        rows = []
        for c in Course.all():
            rows.append({
                "course_code": c.course_code,
                "name": c.name,
                "status": c.status,
                "extra": "",   # keep column consistent
            })
        self._insert_rows(rows)

    def _load_no_students(self) -> None:
        self._clear()
        rows = Course.with_no_students_yet()
        # Normalize to include "extra" column
        for r in rows:
            r["extra"] = "No enrollments"
        self._insert_rows(rows)

    def _load_expertise(self) -> None:
        self._clear()
        data = Course.lecturer_expertises()
        rows = []
        for r in data:
            rows.append({
                "course_code": r["course_code"],
                "name": r["course_name"],
                "status": "",  # not returned by that query
                "extra": f"{r['lecturer_name']} — {', '.join(r['lecturer_areas'])}",
            })
        self._insert_rows(rows)

    def _on_search(self) -> None:
        term = (self.search_var.get() or "").strip()
        self._clear()
        if not term:
            self._load_all()
            return

        results = Course.search(term)
        if not results:
            messagebox.showinfo("Search", f"No courses found for '{term}'.", parent=self)
            return

        rows = [{
            "course_code": c.course_code,
            "name": c.name,
            "status": c.status,
            "extra": "",
        } for c in results]
        self._insert_rows(rows)

    def _on_open_row(self, _evt=None) -> None:
        cur = self.tree.focus()
        if not cur:
            return
        code, name, status, extra = self.tree.item(cur, "values")
        messagebox.showinfo(
            "Course details",
            f"Code: {code}\nName: {name}\nStatus: {status}\nDetails: {extra}",
            parent=self,
        )


if __name__ == "__main__":
    app = CoursesApp()
    app.mainloop()
