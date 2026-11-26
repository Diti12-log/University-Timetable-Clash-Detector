# Project Report
## University Timetable Clash Detector Using Python

**Submitted by:** Anindita Mukherjee  
**Student Code:** BWU/BCA/25/159  
**Programme:** Bachelor of Computer Applications (BCA)  
**Department:** Computational Sciences (CSS)  
**Institution:** Brainware University  
**Project Guide:** Jayanta Aich

---

## Certificate / Declaration

I, Anindita Mukherjee, student of Bachelor of Computer Applications (BCA), Brainware University, declare that this project titled **“University Timetable Clash Detector Using Python”** has been prepared by me as an academic project. The project demonstrates timetable conflict detection using Python and CSV data, with a Jupyter Notebook demonstration and a Tkinter graphical user interface.

**Student Signature:** ____________________  
**Date:** ____________________

## Acknowledgement

I express my sincere gratitude to my project guide, Jayanta Aich, and the Department of Computational Sciences, Brainware University, for their guidance and support. I also thank my teachers and everyone who helped me understand and complete this project.

## Abstract

Preparing a university timetable involves assigning courses, teachers, classrooms, student groups, days, and time slots. When two sessions overlap and share the same teacher, room, or student group, a scheduling conflict occurs. Checking these conflicts manually can be time-consuming.

The University Timetable Clash Detector is a Python-based project that reads class-session data and identifies overlapping schedules. It checks conflicts involving student groups, instructors, and rooms. The project includes a Jupyter Notebook to demonstrate the algorithm and its tests, along with a Tkinter desktop interface for managing timetable entries and exporting clash reports as CSV files.

## 1. Introduction

A timetable is an important part of academic administration. A valid timetable should avoid assigning the same student group, instructor, or classroom to two different classes at the same time. This project provides a simple way to detect such conflicts using Python.

## 2. Problem Statement

Manual timetable checking may fail to identify overlapping sessions, especially when many courses and rooms are involved. The project aims to automate the identification of time overlaps and resource conflicts.

## 3. Objectives

- Store class-session information in CSV format.
- Accept course, teacher, room, student group, day, start time, and end time.
- Detect overlapping sessions scheduled on the same day.
- Identify whether the conflict involves a student group, teacher, or room.
- Display timetable and clash information in a desktop GUI.
- Save timetable data and export clash reports.

## 4. Scope

The project is intended as a small academic demonstration. It works with locally stored CSV data and supports timetable entry, viewing, deletion, loading, saving, and clash-report export. It does not connect to a live university database.

## 5. Software and Hardware Requirements

### Software
- Python 3
- Windows, Linux, or macOS with a graphical desktop
- Tkinter (included with many standard Python installations)
- Jupyter Notebook or VS Code (for the notebook)

### Hardware
- A computer capable of running Python 3
- Keyboard, display, and sufficient storage for the project files

## 6. Technologies Used

- **Python:** main programming language.
- **CSV module:** reads and writes timetable and clash-report data.
- **Tkinter/ttk:** creates the graphical user interface.
- **Jupyter Notebook:** presents the algorithm, sample data, output, and tests.
- **GitHub:** stores and versions the project files.

## 7. System Design and Working

Each class session contains:
- Course
- Teacher
- Room
- Student group
- Day
- Start time
- End time

The program converts a time such as 09:30 into minutes after midnight. This makes it easier to compare time intervals.

For two sessions A and B, their time intervals overlap when:

`start_A < end_B and start_B < end_A`

The sessions are compared only when they occur on the same day. If their intervals overlap, the program checks whether the teacher, room, or student group is the same. Every matching resource is recorded as a reason for the clash.

## 8. Modules

### 8.1 CSV Data Handling
Reads timetable entries from a CSV file and writes timetable or clash information to CSV files.

### 8.2 Time Conversion
Converts 24-hour time strings into minute values for comparison and formats minute values back into readable time.

### 8.3 Clash Detection
Compares pairs of sessions, checks day and time overlap, and identifies shared teachers, rooms, or student groups.

### 8.4 Tkinter GUI
Provides fields for entering class details, buttons for adding/deleting sessions and loading/saving CSV files, and separate timetable and clash-report views.

### 8.5 Notebook Demonstration
Shows the core algorithm, sample timetable data, detected clashes, and five assertion-based tests.

## 9. How to Execute

### GUI
1. Install Python 3.
2. Download the project repository.
3. Open a terminal in the project folder.
4. Execute `python gui_app.py`.
5. Add a class session or use the loaded sample timetable.
6. Review the Master Timetable and Clash Report tabs.
7. Use the CSV controls to load, save, or export data.

### Notebook
1. Open `Timetable_Clash_Detector.ipynb` in Jupyter or VS Code.
2. Run the cells from top to bottom.
3. Review the sample output and test results.

## 10. Sample Data and Expected Result

The repository includes sample timetable entries in `data/timetable.csv`. The notebook also contains a sample demonstration where two conflicts are reported:
- Maths and Physics: same student group.
- Maths and Python: same room.

The notebook's test cell displays **“All 5 tests passed”**.

## 11. Testing

The notebook includes five assertion-based checks for:
1. Overlapping sessions.
2. Non-overlapping sessions that meet at an endpoint.
3. Sessions scheduled on different days.
4. Sessions with identical time slots.
5. A shared-teacher conflict.

The notebook output records that all five checks passed. The GUI should be launched and manually checked on the computer used for final demonstration.

## 12. Advantages

- Reduces manual timetable checking.
- Identifies multiple types of scheduling conflict.
- Uses simple CSV files for data storage.
- Provides both notebook-based demonstration and a desktop interface.
- Exports clash details for later review.

## 13. Limitations and Future Scope

Current limitations:
- Overnight sessions are not handled.
- Data is stored locally and is not synchronized between users.
- The project uses sample data rather than a live university timetable.

Possible future improvements:
- Database integration.
- User login and role-based access.
- Automatic timetable generation.
- More detailed reports and print support.
- Web-based access for multiple departments.

## 14. Conclusion

The University Timetable Clash Detector demonstrates the use of Python programming, CSV file handling, time-interval comparison, and Tkinter GUI development to identify common university timetable conflicts. The project meets its demonstration objective by identifying overlapping sessions that share a student group, teacher, or room.

## References

1. Python Software Foundation, *Python 3 Documentation* — https://docs.python.org/3/
2. Python Software Foundation, *tkinter — Python interface to Tcl/Tk* — https://docs.python.org/3/library/tkinter.html
3. Python Software Foundation, *csv — CSV File Reading and Writing* — https://docs.python.org/3/library/csv.html
4. Project source code and notebook maintained in the project GitHub repository.

---

**Submitted by:** Anindita Mukherjee  
**Student Code:** BWU/BCA/25/159  
**Brainware University**
