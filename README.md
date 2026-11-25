# Student-Database-Management-System
A Python-based Student Result &amp; Academic Performance Management System built using Tkinter and SQLite. It automates marks entry, result calculations, percentage and grade generation, student record management, and class performance analysis with real-time validation through an offline desktop interface.
# Smart Student Result & Academic Performance Management System

A Python-based desktop application designed to simplify student academic record management and automate result calculations. The system uses Tkinter for its graphical interface and SQLite for secure, local data storage.

## 🚀 Features

- **Student Management:** Register, update, search and delete student records.
- **Subject Management:** Maintain subject codes, names and maximum marks.
- **Marks Entry:** Enter student marks with real-time validation.
- **Automatic Result Calculation:** Calculate total marks, percentages and grades.
- **Grade Generation:** Automatically assign grades from A+ to F.
- **Pass/Fail Evaluation:** Determine results based on the 40% passing threshold.
- **Student Search:** Retrieve academic records using University Roll Number.
- **Performance Dashboard:** View class averages, pass percentages, toppers and weak performers.
- **Offline Access:** Works locally without requiring an internet connection.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.x | Core programming language |
| Tkinter / ttk | Graphical User Interface |
| SQLite3 | Local database management |
| VS Code / PyCharm | Development environment |

## ⚙️ System Architecture

The application follows a three-layer desktop architecture:

1. **UI Layer:** Tkinter forms and views.
2. **Logic Layer:** Input validation, calculations and result processing.
3. **Database Layer:** SQLite relational database.

## 📊 Grading System

| Percentage | Grade |
|---|---|
| 90–100% | A+ |
| 80–89.99% | A |
| 70–79.99% | B+ |
| 60–69.99% | B |
| 50–59.99% | C |
| 40–49.99% | D |
| Below 40% | F (Fail) |

**Passing Criteria:** Minimum 40% overall percentage.

## 🗄️ Database Design

The system uses three normalized relational tables:

- **STUDENTS:** Student ID, Roll Number, Name, Branch, Section and Semester.
- **SUBJECTS:** Subject ID, Subject Code, Subject Name and Maximum Marks.
- **MARKS:** Marks ID, Student ID, Subject ID and Marks Obtained.

## 💻 Installation & Setup

### Prerequisites
- Python 3.x
- VS Code or PyCharm

### Steps

1. Clone this repository:

   ```bash
   git clone https://github.com/molikgupta8964-stack/Smart-Student-Result-Management-System.git
   ```

2. Navigate to the project folder:

   ```bash
   cd Smart-Student-Result-Management-System
   ```

3. Run the application:

   ```bash
   python main.py
   ```

   Replace `main.py` with your actual entry-point filename if different.

**Note:** Tkinter and SQLite3 are included with standard Python installations in most environments.

## 🎯 Project Objectives

- Reduce manual work in academic result preparation.
- Minimize calculation errors and invalid marks entries.
- Improve student record searching and management.
- Generate academic performance summaries quickly.
- Provide a simple and reliable offline solution for colleges.

## 🔮 Future Enhancements

- Export marksheets into PDF and Excel formats.
- Password-protected login for staff.
- Shared network database support.
- Enhanced academic analytics and reporting.

## 👨‍💻 Developed By

**Molik Gupta & Team**

Arya College of Engineering & IT  
Department of Computer Science & Engineering  
Academic Session: 2026–27

## 📄 License

This project is developed for academic and educational purposes.
