"""
SMART STUDENT RESULT & ACADEMIC PERFORMANCE MANAGEMENT SYSTEM
A single-file Python desktop project using Tkinter/ttk and SQLite3.

Run:
    python3 main.py

The database (student_result.db) is created automatically beside this file.
"""

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

DB_PATH = Path(__file__).with_name("student_result.db")


# ----------------------------- DATABASE ---------------------------------

class Database:
    def __init__(self, path=DB_PATH):
        self.conn = sqlite3.connect(path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.create_tables()
        self.add_default_subjects()

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS STUDENTS (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_no TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                branch TEXT NOT NULL,
                section TEXT NOT NULL,
                semester TEXT NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS SUBJECTS (
                subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_code TEXT NOT NULL UNIQUE,
                subject_name TEXT NOT NULL,
                max_marks REAL NOT NULL CHECK(max_marks > 0)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS MARKS (
                mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                marks REAL NOT NULL CHECK(marks >= 0),
                UNIQUE(student_id, subject_id),
                FOREIGN KEY(student_id) REFERENCES STUDENTS(student_id)
                    ON DELETE CASCADE,
                FOREIGN KEY(subject_id) REFERENCES SUBJECTS(subject_id)
                    ON DELETE CASCADE
            )
        """)
        self.conn.commit()

    def add_default_subjects(self):
        defaults = [
            ("CS101", "Python Programming", 100),
            ("CS102", "Data Structures", 100),
            ("CS103", "Software Engineering", 100),
            ("CS104", "Digital Electronics", 100),
            ("CS105", "Mathematics", 100),
        ]
        self.conn.executemany(
            "INSERT OR IGNORE INTO SUBJECTS(subject_code, subject_name, max_marks) VALUES (?, ?, ?)",
            defaults
        )
        self.conn.commit()

    def close(self):
        self.conn.close()


# ----------------------------- MAIN APP ----------------------------------

class StudentResultApp:
    BG = "#f3f6fb"
    NAVY = "#172554"
    BLUE = "#2563eb"
    WHITE = "#ffffff"
    TEXT = "#172033"
    MUTED = "#64748b"

    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.root.title("Smart Student Result & Academic Performance Management System")
        self.root.geometry("1180x740")
        self.root.minsize(980, 640)
        self.root.configure(bg=self.BG)
        self.selected_student_id = None
        self.selected_subject_id = None
        self.setup_style()
        self.build_shell()
        self.show_dashboard()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=29, font=("Arial", 10),
                        background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"),
                        background="#e8eef8", foreground=self.TEXT)
        style.map("Treeview", background=[("selected", "#dbeafe")],
                  foreground=[("selected", self.TEXT)])
        style.configure("TCombobox", padding=6)
        style.configure("TEntry", padding=7)

    def build_shell(self):
        sidebar = tk.Frame(self.root, bg=self.NAVY, width=225)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="SMART RESULT", bg=self.NAVY, fg="white",
                 font=("Arial", 17, "bold")).pack(anchor="w", padx=20, pady=(28, 2))
        tk.Label(sidebar, text="ACADEMIC MANAGEMENT", bg=self.NAVY, fg="#bfdbfe",
                 font=("Arial", 8, "bold")).pack(anchor="w", padx=21, pady=(0, 28))

        self.content = tk.Frame(self.root, bg=self.BG)
        self.content.pack(side="right", fill="both", expand=True)

        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Student Management", self.show_students),
            ("Subject Catalog", self.show_subjects),
            ("Marks Entry", self.show_marks),
            ("Result Generator", self.show_results),
        ]
        for label, command in nav_items:
            btn = tk.Button(
                sidebar, text="   " + label, command=command,
                bg=self.NAVY, fg="white", activebackground="#1e40af",
                activeforeground="white", relief="flat", bd=0,
                anchor="w", padx=12, pady=13, font=("Arial", 10, "bold"),
                cursor="hand2"
            )
            btn.pack(fill="x", padx=10, pady=3)

        tk.Frame(sidebar, bg="#334477", height=1).pack(fill="x", padx=18, pady=22)
        tk.Label(sidebar, text="Python  •  Tkinter  •  SQLite",
                 bg=self.NAVY, fg="#cbd5e1", font=("Arial", 8)).pack(side="bottom", pady=20)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def page_header(self, title, subtitle):
        header = tk.Frame(self.content, bg=self.BG)
        header.pack(fill="x", padx=28, pady=(24, 16))
        tk.Label(header, text=title, bg=self.BG, fg=self.TEXT,
                 font=("Arial", 22, "bold")).pack(anchor="w")
        tk.Label(header, text=subtitle, bg=self.BG, fg=self.MUTED,
                 font=("Arial", 10)).pack(anchor="w", pady=(5, 0))

    def card(self, parent, title, value, color):
        box = tk.Frame(parent, bg="white", highlightbackground="#e2e8f0",
                       highlightthickness=1, padx=18, pady=15)
        box.pack(side="left", fill="both", expand=True, padx=(0, 12))
        tk.Label(box, text=title.upper(), bg="white", fg=self.MUTED,
                 font=("Arial", 9, "bold")).pack(anchor="w")
        tk.Label(box, text=str(value), bg="white", fg=color,
                 font=("Arial", 25, "bold")).pack(anchor="w", pady=(8, 0))
        return box

    def make_table(self, parent, columns, headings=None, widths=None):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="both", expand=True, padx=28, pady=(8, 24))
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for i, col in enumerate(columns):
            tree.heading(col, text=(headings[i] if headings else col.replace("_", " ").title()))
            tree.column(col, width=(widths[i] if widths else 130), anchor="w")
        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return tree

    def show_dashboard(self):
        self.clear_content()
        self.page_header("Dashboard", "Overview of student academic performance")
        cur = self.db.conn.cursor()
        students = cur.execute("SELECT COUNT(*) FROM STUDENTS").fetchone()[0]
        subjects = cur.execute("SELECT COUNT(*) FROM SUBJECTS").fetchone()[0]
        result_rows = self.get_result_rows()
        passed = sum(1 for row in result_rows if row["status"] == "PASS")
        avg = (sum(row["percentage"] for row in result_rows) / len(result_rows)) if result_rows else 0

        cards = tk.Frame(self.content, bg=self.BG)
        cards.pack(fill="x", padx=28, pady=4)
        self.card(cards, "Total Students", students, self.BLUE)
        self.card(cards, "Total Subjects", subjects, "#7c3aed")
        self.card(cards, "Pass Results", passed, "#059669")
        self.card(cards, "Average Percentage", f"{avg:.1f}%", "#d97706")

        tk.Label(self.content, text="Recent Student Records", bg=self.BG,
                 fg=self.TEXT, font=("Arial", 14, "bold")).pack(anchor="w", padx=28, pady=(24, 4))
        tree = self.make_table(self.content,
            ("roll", "name", "branch", "semester"),
            ("University Roll Number", "Student Name", "Branch", "Semester"),
            (190, 260, 160, 130))
        rows = cur.execute("""
            SELECT roll_no, name, branch, semester FROM STUDENTS
            ORDER BY student_id DESC LIMIT 10
        """).fetchall()
        for row in rows:
            tree.insert("", "end", values=row)

    # -------------------------- STUDENTS ---------------------------------

    def show_students(self):
        self.clear_content()
        self.page_header("Student Management", "Register, update, search and delete student records")

        form = tk.Frame(self.content, bg="white", padx=18, pady=15,
                        highlightbackground="#e2e8f0", highlightthickness=1)
        form.pack(fill="x", padx=28, pady=5)

        self.stu_vars = {k: tk.StringVar() for k in
                         ("roll", "name", "branch", "section", "semester")}
        labels = [("roll", "University Roll No."), ("name", "Student Name"),
                  ("branch", "Branch"), ("section", "Section"), ("semester", "Semester")]
        for i, (key, label) in enumerate(labels):
            r, c = divmod(i, 3)
            cell = tk.Frame(form, bg="white")
            cell.grid(row=r, column=c, sticky="ew", padx=8, pady=7)
            tk.Label(cell, text=label, bg="white", fg=self.MUTED,
                     font=("Arial", 9, "bold")).pack(anchor="w")
            ttk.Entry(cell, textvariable=self.stu_vars[key], width=28).pack(fill="x", pady=4)
            form.grid_columnconfigure(c, weight=1)

        actions = tk.Frame(form, bg="white")
        actions.grid(row=2, column=0, columnspan=3, sticky="w", padx=8, pady=8)
        self.action_button(actions, "Add Student", self.add_student)
        self.action_button(actions, "Update Selected", self.update_student, "#0f766e")
        self.action_button(actions, "Delete Selected", self.delete_student, "#dc2626")
        self.action_button(actions, "Clear", self.clear_student_form, "#64748b")

        searchrow = tk.Frame(self.content, bg=self.BG)
        searchrow.pack(fill="x", padx=28, pady=(14, 0))
        tk.Label(searchrow, text="Search by roll number or name:", bg=self.BG,
                 fg=self.TEXT).pack(side="left")
        self.student_search = tk.StringVar()
        entry = ttk.Entry(searchrow, textvariable=self.student_search, width=30)
        entry.pack(side="left", padx=8)
        self.action_button(searchrow, "Search", self.refresh_students)
        self.action_button(searchrow, "Show All", lambda: (self.student_search.set(""), self.refresh_students()), "#64748b")

        self.student_tree = self.make_table(self.content,
            ("id", "roll", "name", "branch", "section", "semester"),
            ("ID", "Roll Number", "Name", "Branch", "Section", "Semester"),
            (55, 160, 220, 120, 100, 100))
        self.student_tree.bind("<<TreeviewSelect>>", self.select_student)
        self.refresh_students()

    def action_button(self, parent, text, command, color=None):
        color = color or self.BLUE
        tk.Button(parent, text=text, command=command, bg=color, fg="white",
                  activebackground=color, activeforeground="white",
                  relief="flat", padx=13, pady=8, font=("Arial", 9, "bold"),
                  cursor="hand2").pack(side="left", padx=(0, 7))

    def student_values(self):
        return [self.stu_vars[k].get().strip()
                for k in ("roll", "name", "branch", "section", "semester")]

    def clear_student_form(self):
        self.selected_student_id = None
        for var in self.stu_vars.values():
            var.set("")
        if hasattr(self, "student_tree"):
            self.student_tree.selection_remove(self.student_tree.selection())

    def add_student(self):
        values = self.student_values()
        if not all(values):
            messagebox.showwarning("Missing information", "Please fill in all student fields.")
            return
        try:
            self.db.conn.execute("""
                INSERT INTO STUDENTS(roll_no, name, branch, section, semester)
                VALUES (?, ?, ?, ?, ?)
            """, values)
            self.db.conn.commit()
            self.refresh_students()
            self.clear_student_form()
            messagebox.showinfo("Success", "Student registered successfully.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate roll number", "This university roll number already exists.")

    def select_student(self, _event=None):
        selected = self.student_tree.selection()
        if not selected:
            return
        values = self.student_tree.item(selected[0], "values")
        self.selected_student_id = int(values[0])
        for key, value in zip(("roll", "name", "branch", "section", "semester"), values[1:]):
            self.stu_vars[key].set(value)

    def update_student(self):
        if not self.selected_student_id:
            messagebox.showwarning("Select student", "Select a student from the table first.")
            return
        values = self.student_values()
        if not all(values):
            messagebox.showwarning("Missing information", "Please fill in all student fields.")
            return
        try:
            self.db.conn.execute("""
                UPDATE STUDENTS SET roll_no=?, name=?, branch=?, section=?, semester=?
                WHERE student_id=?
            """, (*values, self.selected_student_id))
            self.db.conn.commit()
            self.refresh_students()
            self.clear_student_form()
            messagebox.showinfo("Success", "Student record updated.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate roll number", "This roll number is already assigned.")

    def delete_student(self):
        if not self.selected_student_id:
            messagebox.showwarning("Select student", "Select a student from the table first.")
            return
        if messagebox.askyesno("Confirm deletion", "Delete this student and their marks?"):
            self.db.conn.execute("DELETE FROM STUDENTS WHERE student_id=?", (self.selected_student_id,))
            self.db.conn.commit()
            self.refresh_students()
            self.clear_student_form()

    def refresh_students(self):
        if not hasattr(self, "student_tree"):
            return
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        term = self.student_search.get().strip()
        rows = self.db.conn.execute("""
            SELECT student_id, roll_no, name, branch, section, semester
            FROM STUDENTS
            WHERE roll_no LIKE ? OR name LIKE ?
            ORDER BY name
        """, (f"%{term}%", f"%{term}%")).fetchall()
        for row in rows:
            self.student_tree.insert("", "end", values=row)

    # --------------------------- SUBJECTS --------------------------------

    def show_subjects(self):
        self.clear_content()
        self.page_header("Subject Catalog", "Manage subject codes, titles and maximum marks")
        form = tk.Frame(self.content, bg="white", padx=18, pady=16,
                        highlightbackground="#e2e8f0", highlightthickness=1)
        form.pack(fill="x", padx=28, pady=5)
        self.sub_vars = {k: tk.StringVar() for k in ("code", "name", "max")}
        for i, (key, label) in enumerate((("code", "Subject Code"),
                                          ("name", "Subject Name"),
                                          ("max", "Maximum Marks"))):
            cell = tk.Frame(form, bg="white")
            cell.grid(row=0, column=i, sticky="ew", padx=8)
            tk.Label(cell, text=label, bg="white", fg=self.MUTED,
                     font=("Arial", 9, "bold")).pack(anchor="w")
            ttk.Entry(cell, textvariable=self.sub_vars[key], width=30).pack(fill="x", pady=5)
            form.grid_columnconfigure(i, weight=1)
        actions = tk.Frame(form, bg="white")
        actions.grid(row=1, column=0, columnspan=3, sticky="w", padx=8, pady=10)
        self.action_button(actions, "Add Subject", self.add_subject)
        self.action_button(actions, "Update Selected", self.update_subject, "#0f766e")
        self.action_button(actions, "Delete Selected", self.delete_subject, "#dc2626")
        self.action_button(actions, "Clear", self.clear_subject_form, "#64748b")

        self.subject_tree = self.make_table(self.content,
            ("id", "code", "name", "max"),
            ("ID", "Subject Code", "Subject Name", "Maximum Marks"),
            (60, 170, 350, 150))
        self.subject_tree.bind("<<TreeviewSelect>>", self.select_subject)
        self.refresh_subjects()

    def clear_subject_form(self):
        self.selected_subject_id = None
        for var in self.sub_vars.values():
            var.set("")
        if hasattr(self, "subject_tree"):
            self.subject_tree.selection_remove(self.subject_tree.selection())

    def add_subject(self):
        code, name, maximum = (self.sub_vars[k].get().strip() for k in ("code", "name", "max"))
        if not code or not name or not maximum:
            messagebox.showwarning("Missing information", "Fill in all subject fields.")
            return
        try:
            maximum = float(maximum)
            if maximum <= 0:
                raise ValueError
            self.db.conn.execute(
                "INSERT INTO SUBJECTS(subject_code, subject_name, max_marks) VALUES (?, ?, ?)",
                (code, name, maximum))
            self.db.conn.commit()
            self.refresh_subjects()
            self.clear_subject_form()
            messagebox.showinfo("Success", "Subject added successfully.")
        except ValueError:
            messagebox.showerror("Invalid marks", "Maximum marks must be a positive number.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate code", "This subject code already exists.")

    def select_subject(self, _event=None):
        selected = self.subject_tree.selection()
        if not selected:
            return
        values = self.subject_tree.item(selected[0], "values")
        self.selected_subject_id = int(values[0])
        for key, value in zip(("code", "name", "max"), values[1:]):
            self.sub_vars[key].set(value)

    def update_subject(self):
        if not self.selected_subject_id:
            messagebox.showwarning("Select subject", "Select a subject from the table first.")
            return
        code, name, maximum = (self.sub_vars[k].get().strip() for k in ("code", "name", "max"))
        try:
            maximum = float(maximum)
            if not code or not name or maximum <= 0:
                raise ValueError
            self.db.conn.execute("""
                UPDATE SUBJECTS SET subject_code=?, subject_name=?, max_marks=?
                WHERE subject_id=?
            """, (code, name, maximum, self.selected_subject_id))
            self.db.conn.commit()
            self.refresh_subjects()
            self.clear_subject_form()
            messagebox.showinfo("Success", "Subject updated.")
        except ValueError:
            messagebox.showerror("Invalid information", "Enter a code, name and positive maximum marks.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate code", "This subject code already exists.")

    def delete_subject(self):
        if not self.selected_subject_id:
            messagebox.showwarning("Select subject", "Select a subject from the table first.")
            return
        if messagebox.askyesno("Confirm deletion", "Delete this subject and its marks?"):
            self.db.conn.execute("DELETE FROM SUBJECTS WHERE subject_id=?", (self.selected_subject_id,))
            self.db.conn.commit()
            self.refresh_subjects()
            self.clear_subject_form()

    def refresh_subjects(self):
        if not hasattr(self, "subject_tree"):
            return
        for item in self.subject_tree.get_children():
            self.subject_tree.delete(item)
        rows = self.db.conn.execute("""
            SELECT subject_id, subject_code, subject_name, max_marks
            FROM SUBJECTS ORDER BY subject_name
        """).fetchall()
        for row in rows:
            self.subject_tree.insert("", "end", values=row)

    # ----------------------------- MARKS ---------------------------------

    def show_marks(self):
        self.clear_content()
        self.page_header("Marks Entry", "Enter marks for registered students and subjects")
        form = tk.Frame(self.content, bg="white", padx=20, pady=18,
                        highlightbackground="#e2e8f0", highlightthickness=1)
        form.pack(fill="x", padx=28, pady=5)

        students = self.db.conn.execute(
            "SELECT student_id, roll_no, name FROM STUDENTS ORDER BY roll_no").fetchall()
        subjects = self.db.conn.execute(
            "SELECT subject_id, subject_code, subject_name, max_marks FROM SUBJECTS ORDER BY subject_name").fetchall()
        self.student_choices = {f"{r[1]} - {r[2]}": r[0] for r in students}
        self.subject_choices = {f"{r[1]} - {r[2]} (Max {r[3]:g})": (r[0], r[3]) for r in subjects}

        tk.Label(form, text="Student", bg="white", fg=self.MUTED,
                 font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w", padx=8)
        self.mark_student = tk.StringVar()
        student_box = ttk.Combobox(form, textvariable=self.mark_student,
                                   values=list(self.student_choices), state="readonly", width=38)
        student_box.grid(row=1, column=0, padx=8, pady=7, sticky="ew")

        tk.Label(form, text="Subject", bg="white", fg=self.MUTED,
                 font=("Arial", 9, "bold")).grid(row=0, column=1, sticky="w", padx=8)
        self.mark_subject = tk.StringVar()
        subject_box = ttk.Combobox(form, textvariable=self.mark_subject,
                                   values=list(self.subject_choices), state="readonly", width=38)
        subject_box.grid(row=1, column=1, padx=8, pady=7, sticky="ew")

        tk.Label(form, text="Obtained Marks", bg="white", fg=self.MUTED,
                 font=("Arial", 9, "bold")).grid(row=0, column=2, sticky="w", padx=8)
        self.mark_value = tk.StringVar()
        ttk.Entry(form, textvariable=self.mark_value, width=18).grid(row=1, column=2, padx=8, pady=7)
        form.grid_columnconfigure(0, weight=2)
        form.grid_columnconfigure(1, weight=2)

        actions = tk.Frame(form, bg="white")
        actions.grid(row=2, column=0, columnspan=3, sticky="w", padx=8, pady=10)
        self.action_button(actions, "Save Marks", self.save_marks)
        self.action_button(actions, "Clear", self.clear_marks, "#64748b")

        self.marks_tree = self.make_table(self.content,
            ("roll", "student", "subject", "marks", "maximum"),
            ("Roll Number", "Student", "Subject", "Obtained Marks", "Maximum Marks"),
            (150, 220, 250, 140, 140))
        self.refresh_marks()

    def clear_marks(self):
        self.mark_student.set("")
        self.mark_subject.set("")
        self.mark_value.set("")

    def save_marks(self):
        student_key = self.mark_student.get()
        subject_key = self.mark_subject.get()
        raw_marks = self.mark_value.get().strip()
        if student_key not in self.student_choices or subject_key not in self.subject_choices or not raw_marks:
            messagebox.showwarning("Missing information", "Select a student, subject and enter marks.")
            return
        try:
            marks = float(raw_marks)
            subject_id, maximum = self.subject_choices[subject_key]
            if marks < 0 or marks > maximum:
                messagebox.showerror("Invalid marks", f"Marks must be between 0 and {maximum:g}.")
                return
            student_id = self.student_choices[student_key]
            self.db.conn.execute("""
                INSERT INTO MARKS(student_id, subject_id, marks) VALUES (?, ?, ?)
                ON CONFLICT(student_id, subject_id) DO UPDATE SET marks=excluded.marks
            """, (student_id, subject_id, marks))
            self.db.conn.commit()
            self.refresh_marks()
            self.clear_marks()
            messagebox.showinfo("Success", "Marks saved successfully.")
        except ValueError:
            messagebox.showerror("Invalid marks", "Enter marks as a valid number.")

    def refresh_marks(self):
        if not hasattr(self, "marks_tree"):
            return
        for item in self.marks_tree.get_children():
            self.marks_tree.delete(item)
        rows = self.db.conn.execute("""
            SELECT s.roll_no, s.name, sub.subject_name, m.marks, sub.max_marks
            FROM MARKS m
            JOIN STUDENTS s ON s.student_id=m.student_id
            JOIN SUBJECTS sub ON sub.subject_id=m.subject_id
            ORDER BY s.roll_no, sub.subject_name
        """).fetchall()
        for row in rows:
            self.marks_tree.insert("", "end", values=(row[0], row[1], row[2],
                                                       f"{row[3]:g}", f"{row[4]:g}"))

    # ----------------------------- RESULTS --------------------------------

    @staticmethod
    def grade_for(percentage):
        if percentage >= 90:
            return "A+"
        if percentage >= 80:
            return "A"
        if percentage >= 70:
            return "B+"
        if percentage >= 60:
            return "B"
        if percentage >= 50:
            return "C"
        if percentage >= 40:
            return "D"
        return "F"

    def get_result_rows(self):
        students = self.db.conn.execute("""
            SELECT student_id, roll_no, name, branch, section, semester
            FROM STUDENTS ORDER BY roll_no
        """).fetchall()
        results = []
        for student in students:
            totals = self.db.conn.execute("""
                SELECT COALESCE(SUM(m.marks), 0), COALESCE(SUM(sub.max_marks), 0),
                       COUNT(m.mark_id), COUNT(sub.subject_id)
                FROM SUBJECTS sub
                LEFT JOIN MARKS m ON m.subject_id=sub.subject_id
                    AND m.student_id=?
            """, (student[0],)).fetchone()
            obtained, maximum, entered, subject_count = totals
            percentage = (obtained / maximum * 100) if maximum else 0
            # A result is PASS only when all subjects have marks and percentage >= 40.
            status = "PASS" if subject_count > 0 and entered == subject_count and percentage >= 40 else "FAIL"
            results.append({
                "id": student[0], "roll": student[1], "name": student[2],
                "branch": student[3], "section": student[4], "semester": student[5],
                "obtained": obtained, "maximum": maximum, "percentage": percentage,
                "grade": self.grade_for(percentage), "status": status,
                "entered": entered, "subjects": subject_count
            })
        return results

    def show_results(self):
        self.clear_content()
        self.page_header("Result Generator", "Automatic totals, percentage, letter grades and pass/fail status")
        note = tk.Label(self.content,
            text="Grading: 90+ A+  |  80+ A  |  70+ B+  |  60+ B  |  50+ C  |  40+ D  |  Below 40 F",
            bg="#eaf1ff", fg="#1e40af", font=("Arial", 9, "bold"), padx=12, pady=11)
        note.pack(fill="x", padx=28, pady=(0, 8))
        self.result_tree = self.make_table(self.content,
            ("roll", "name", "obtained", "maximum", "percentage", "grade", "status"),
            ("Roll Number", "Student Name", "Total Marks", "Maximum", "Percentage", "Grade", "Status"),
            (145, 210, 115, 115, 120, 80, 90))
        self.refresh_results()
        bottom = tk.Frame(self.content, bg=self.BG)
        bottom.pack(fill="x", padx=28, pady=(0, 18))
        self.action_button(bottom, "Refresh Results", self.refresh_results)
        self.action_button(bottom, "Search Roll Number", self.search_result, "#0f766e")

    def refresh_results(self):
        if not hasattr(self, "result_tree"):
            return
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        for row in self.get_result_rows():
            if row["entered"] < row["subjects"]:
                status = "PENDING"
            else:
                status = row["status"]
            self.result_tree.insert("", "end", values=(
                row["roll"], row["name"], f"{row['obtained']:g}",
                f"{row['maximum']:g}", f"{row['percentage']:.2f}%",
                row["grade"], status
            ))

    def search_result(self):
        from tkinter.simpledialog import askstring
        roll = askstring("Search Result", "Enter University Roll Number:")
        if not roll:
            return
        matches = [r for r in self.get_result_rows() if r["roll"].lower() == roll.strip().lower()]
        if not matches:
            messagebox.showinfo("Not found", "No student found with this roll number.")
            return
        r = matches[0]
        status = r["status"] if r["entered"] == r["subjects"] else "PENDING"
        messagebox.showinfo("Student Result",
            f"Name: {r['name']}\nRoll Number: {r['roll']}\n"
            f"Total Marks: {r['obtained']:g} / {r['maximum']:g}\n"
            f"Percentage: {r['percentage']:.2f}%\nGrade: {r['grade']}\nStatus: {status}")

    def on_close(self):
        self.db.close()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = StudentResultApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
