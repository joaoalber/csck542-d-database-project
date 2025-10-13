
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

THIS_DIR = Path(__file__).resolve().parent
SRC_DIR = THIS_DIR.parent
PROJECT_ROOT = SRC_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.entities.student import Student


def center_on_screen(win: tk.Tk, width: int, height: int) -> None:
    win.update_idletasks()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    x = (sw - width) // 2
    y = (sh - height) // 5
    win.geometry(f"{width}x{height}+{x}+{y}")


class StudentsApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Students")

        # Window sizing & responsiveness
        DEFAULT_W, DEFAULT_H = 900, 600
        self.minsize(720, 480)
        center_on_screen(self, DEFAULT_W, DEFAULT_H)
        # self.state("zoomed")  # <- uncomment to start maximized

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self._build_ui()
        self._load_all()

    def _build_ui(self) -> None:
        # Top search bar
        top = ttk.Frame(self, padding=(10, 10, 10, 0))
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(1, weight=1)

        ttk.Label(top, text="Search:").grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(top, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=1, sticky="ew")
        ttk.Button(top, text="Search", command=self._on_search).grid(row=0, column=2, padx=(8, 0))

        # Main area: sidebar + table
        main = ttk.Frame(self, padding=10)
        main.grid(row=1, column=0, sticky="nsew")
        main.rowconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)

        # Sidebar filters
        side = ttk.Frame(main)
        side.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        ttk.Label(side, text="Filters", style="Headline.TLabel").grid(row=0, column=0, pady=(0, 8))
        ttk.Button(side, text="All students", width=22, command=self._load_all).grid(row=1, column=0, pady=3, sticky="ew")
        ttk.Button(side, text="High-rated (completed)", width=22, command=self._load_top_students).grid(row=2, column=0, pady=3, sticky="ew")
        ttk.Button(side, text="Not enrolled yet", width=22, command=self._load_not_enrolled).grid(row=3, column=0, pady=3, sticky="ew")

        # Table
        table_frame = ttk.Frame(main)
        table_frame.grid(row=0, column=1, sticky="nsew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        cols = ("name", "contact", "extra")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        self.tree.grid(row=0, column=0, sticky="nsew")

        self.tree.heading("name", text="Name")
        self.tree.heading("contact", text="Contact")
        self.tree.heading("extra", text="Details")

        self.tree.column("name", width=300, anchor="w", stretch=True)
        self.tree.column("contact", width=320, anchor="w", stretch=True)
        self.tree.column("extra", width=220, anchor="w", stretch=False)

        yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        yscroll.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<Double-1>", self._on_open_student)

        # Style polish
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Headline.TLabel", font=("Segoe UI", 10, "bold"))

    def _clear(self) -> None:
        for iid in self.tree.get_children():
            self.tree.delete(iid)

    def _insert_rows(self, rows) -> None:
        """Rows shaped like {'name','contact','extra'}."""
        for r in rows:
            self.tree.insert("", "end", values=(r.get("name"), r.get("contact"), r.get("extra", "")))

    def _load_all(self) -> None:
        self._clear()
        data = [{"name": s.name, "contact": s.contact_info, "extra": ""} for s in Student.all()]
        self._insert_rows(data)

    def _load_top_students(self) -> None:
        self._clear()
        # expected from your entity: list of dicts with keys: name, final_grade
        data = Student.top_completed_students()
        rows = [{"name": r["name"], "contact": "", "extra": f"Final grade: {r['final_grade']}"} for r in data]
        if not rows:
            messagebox.showinfo("Top students", "No students match this filter.", parent=self)
        self._insert_rows(rows)

    def _load_not_enrolled(self) -> None:
        self._clear()
        # expected from your entity: list of dicts with key 'name'
        data = Student.not_enrolled_yet()
        rows = [{"name": r["name"], "contact": "", "extra": "Not enrolled"} for r in data]
        if not rows:
            messagebox.showinfo("Not enrolled", "No students match this filter.", parent=self)
        self._insert_rows(rows)

    def _on_search(self) -> None:
        term = (self.search_var.get() or "").strip()
        if not term:
            self._load_all()
            return
        self._clear()
        matches = Student.search(term)  # list of Student objs
        rows = [{"name": s.name, "contact": s.contact_info, "extra": ""} for s in matches]
        if not rows:
            messagebox.showinfo("Search", f"No students found for '{term}'.", parent=self)
        self._insert_rows(rows)

    def _on_open_student(self, _evt=None) -> None:
        cur = self.tree.focus()
        if not cur:
            return
        name, contact, extra = self.tree.item(cur, "values")
        messagebox.showinfo("Student", f"Name: {name}\nContact: {contact or '—'}\n{extra}", parent=self)


if __name__ == "__main__":
    app = StudentsApp()
    app.mainloop()
