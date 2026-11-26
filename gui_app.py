import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from itertools import combinations

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.join(BASE_DIR, "data", "timetable.csv")
CLASH_CSV = os.path.join(BASE_DIR, "data", "clashes.csv")
FIELDS = ["course", "teacher", "room", "group", "day", "start", "end"]


def to_minutes(value):
    parsed = datetime.strptime(value.strip(), "%H:%M")
    return parsed.hour * 60 + parsed.minute


def format_time(value):
    return f"{value // 60:02d}:{value % 60:02d}"


def load_classes(filename):
    classes = []
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        missing = [field for field in FIELDS if field not in (reader.fieldnames or [])]
        if missing:
            raise ValueError("CSV is missing columns: " + ", ".join(missing))
        for line_no, row in enumerate(reader, start=2):
            start = to_minutes(row["start"])
            end = to_minutes(row["end"])
            if end <= start:
                raise ValueError(f"Line {line_no}: end time must be after start time.")
            classes.append({
                "course": row["course"].strip(),
                "teacher": row["teacher"].strip(),
                "room": row["room"].strip(),
                "group": row["group"].strip(),
                "day": row["day"].strip(),
                "start": start,
                "end": end,
            })
    return classes


def save_classes(classes, filename):
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        for item in classes:
            row = item.copy()
            row["start"] = format_time(row["start"])
            row["end"] = format_time(row["end"])
            writer.writerow(row)


def find_clashes(classes):
    clashes = []
    for first, second in combinations(classes, 2):
        if first["day"].lower() != second["day"].lower():
            continue
        start = max(first["start"], second["start"])
        end = min(first["end"], second["end"])
        if start >= end:
            continue

        reasons = []
        if first["group"].lower() == second["group"].lower():
            reasons.append("Same student group")
        if first["teacher"].lower() == second["teacher"].lower():
            reasons.append("Same teacher")
        if first["room"].lower() == second["room"].lower():
            reasons.append("Same room")

        if reasons:
            clashes.append({
                "day": first["day"],
                "overlap": f"{format_time(start)} - {format_time(end)}",
                "reason": ", ".join(reasons),
                "class_1": first["course"],
                "class_2": second["course"],
            })
    return clashes


def save_clashes(clashes, filename=CLASH_CSV):
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as file:
        fields = ["day", "overlap", "reason", "class_1", "class_2"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(clashes)


class TimetableClashDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("University Timetable Clash Detector")
        self.root.geometry("1100x680")
        self.root.minsize(900, 580)
        self.classes = []
        self.clashes = []

        self.setup_style()
        self.build_interface()
        self.load_default_data()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=27, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("Title.TLabel", font=("Segoe UI", 19, "bold"))
        style.configure("TButton", padding=6)

    def build_interface(self):
        main = ttk.Frame(self.root, padding=15)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="University Timetable Clash Detector",
                  style="Title.TLabel").pack(anchor="w")
        ttk.Label(main, text="Manage class sessions and find room, teacher and student-group conflicts."
                  ).pack(anchor="w", pady=(2, 12))

        form = ttk.LabelFrame(main, text="Add a class session", padding=10)
        form.pack(fill="x", pady=(0, 12))

        self.inputs = {}
        labels = [
            ("Course", "course"), ("Teacher", "teacher"), ("Room", "room"),
            ("Student Group", "group"), ("Day", "day"),
            ("Start (HH:MM)", "start"), ("End (HH:MM)", "end")
        ]
        defaults = {"day": "Monday", "start": "09:00", "end": "10:00"}
        for column, (label, key) in enumerate(labels):
            cell = ttk.Frame(form)
            cell.grid(row=0, column=column, padx=5, sticky="ew")
            ttk.Label(cell, text=label).pack(anchor="w")
            if key == "day":
                widget = ttk.Combobox(
                    cell, values=["Monday", "Tuesday", "Wednesday", "Thursday",
                                  "Friday", "Saturday"], state="readonly", width=13
                )
                widget.set(defaults[key])
            else:
                widget = ttk.Entry(cell, width=15)
                if key in defaults:
                    widget.insert(0, defaults[key])
            widget.pack(fill="x", pady=(3, 0))
            self.inputs[key] = widget
            form.columnconfigure(column, weight=1)

        buttons = ttk.Frame(main)
        buttons.pack(fill="x", pady=(0, 10))
        ttk.Button(buttons, text="Add Session", command=self.add_class).pack(side="left", padx=(0, 6))
        ttk.Button(buttons, text="Delete Selected", command=self.delete_class).pack(side="left", padx=6)
        ttk.Button(buttons, text="Load CSV", command=self.load_csv_dialog).pack(side="left", padx=6)
        ttk.Button(buttons, text="Save Timetable", command=self.save_timetable_dialog).pack(side="left", padx=6)
        ttk.Button(buttons, text="Export Clash Report", command=self.export_report).pack(side="left", padx=6)

        self.summary = ttk.Label(main, text="Classes: 0    |    Clashes: 0")
        self.summary.pack(anchor="w", pady=(0, 7))

        notebook = ttk.Notebook(main)
        notebook.pack(fill="both", expand=True)
        timetable_tab = ttk.Frame(notebook, padding=8)
        clash_tab = ttk.Frame(notebook, padding=8)
        notebook.add(timetable_tab, text="Master Timetable")
        notebook.add(clash_tab, text="Clash Report")

        self.schedule_tree = self.make_tree(
            timetable_tab,
            ("course", "teacher", "room", "group", "day", "time"),
            ("Course", "Teacher", "Room", "Student Group", "Day", "Time")
        )
        self.clash_tree = self.make_tree(
            clash_tab,
            ("day", "overlap", "reason", "class_1", "class_2"),
            ("Day", "Overlap", "Conflict", "Class 1", "Class 2")
        )

    def make_tree(self, parent, columns, headings):
        wrapper = ttk.Frame(parent)
        wrapper.pack(fill="both", expand=True)
        tree = ttk.Treeview(wrapper, columns=columns, show="headings")
        for column, heading in zip(columns, headings):
            tree.heading(column, text=heading)
            tree.column(column, width=145, anchor="w")
        scroll = ttk.Scrollbar(wrapper, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return tree

    def load_default_data(self):
        if os.path.exists(DEFAULT_CSV):
            try:
                self.classes = load_classes(DEFAULT_CSV)
            except Exception as error:
                messagebox.showerror("CSV Error", str(error))
        self.refresh()

    def read_form(self):
        values = {key: widget.get().strip() for key, widget in self.inputs.items()}
        if not all(values.values()):
            raise ValueError("Please fill in all seven fields.")
        start = to_minutes(values["start"])
        end = to_minutes(values["end"])
        if end <= start:
            raise ValueError("End time must be later than start time.")
        return {
            "course": values["course"], "teacher": values["teacher"],
            "room": values["room"], "group": values["group"],
            "day": values["day"], "start": start, "end": end
        }

    def add_class(self):
        try:
            self.classes.append(self.read_form())
            self.refresh()
            messagebox.showinfo("Added", "Class session added successfully.")
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error))

    def delete_class(self):
        selected = self.schedule_tree.selection()
        if not selected:
            messagebox.showwarning("Select a row", "Select a class from the timetable first.")
            return
        index = int(selected[0])
        self.classes.pop(index)
        self.refresh()

    def load_csv_dialog(self):
        filename = filedialog.askopenfilename(
            title="Select timetable CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.classes = load_classes(filename)
                self.refresh()
                messagebox.showinfo("Loaded", f"Loaded {len(self.classes)} classes.")
            except Exception as error:
                messagebox.showerror("CSV Error", str(error))

    def save_timetable_dialog(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")],
            initialfile="timetable.csv"
        )
        if filename:
            try:
                save_classes(self.classes, filename)
                messagebox.showinfo("Saved", "Timetable saved successfully.")
            except Exception as error:
                messagebox.showerror("Save Error", str(error))

    def export_report(self):
        if not self.clashes:
            messagebox.showinfo("No clashes", "There are no clashes to export.")
            return
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")],
            initialfile="clashes.csv"
        )
        if filename:
            try:
                save_clashes(self.clashes, filename)
                messagebox.showinfo("Exported", "Clash report exported successfully.")
            except Exception as error:
                messagebox.showerror("Export Error", str(error))

    def refresh(self):
        self.clashes = find_clashes(self.classes)
        for tree in (self.schedule_tree, self.clash_tree):
            for item in tree.get_children():
                tree.delete(item)

        for index, item in enumerate(self.classes):
            time_slot = f"{format_time(item['start'])} - {format_time(item['end'])}"
            self.schedule_tree.insert(
                "", "end", iid=str(index),
                values=(item["course"], item["teacher"], item["room"],
                        item["group"], item["day"], time_slot)
            )

        for clash in self.clashes:
            self.clash_tree.insert(
                "", "end",
                values=(clash["day"], clash["overlap"], clash["reason"],
                        clash["class_1"], clash["class_2"])
            )

        self.summary.config(
            text=f"Classes: {len(self.classes)}    |    Clashes: {len(self.clashes)}"
        )


if __name__ == "__main__":
    window = tk.Tk()
    app = TimetableClashDetectorApp(window)
    window.mainloop()
