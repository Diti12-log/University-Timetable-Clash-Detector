# University Timetable Clash Detector Using Python

**Student:** Anindita Mukherjee  
**Student Code:** BWU/BCA/25/159  
**Programme:** BCA, Department of Computational Sciences (CSS)  
**Institution:** Brainware University  
**Project Guide:** Jayanta Aich

## 1. Project Overview

The University Timetable Clash Detector helps identify overlapping university class sessions. It checks whether two sessions on the same day overlap in time and share a student group, instructor, or classroom.

The repository provides two ways to explore the project:
- **Jupyter Notebook:** demonstrates the clash-detection logic, sample timetable, output, and five assertion-based tests.
- **Tkinter GUI:** provides a desktop interface to add and delete sessions, load and save timetable CSV files, view clashes, and export a clash report.

## 2. Features

- Add and manage class sessions.
- Detect overlapping sessions on the same day.
- Identify student-group, teacher, and room conflicts.
- Display the master timetable and clash report.
- Load and save timetable data in CSV format.
- Export detected clashes to a CSV report.
- Validate time values in 24-hour `HH:MM` format.

## 3. Technologies Used

- Python 3
- Tkinter and ttk
- CSV module
- Jupyter Notebook
- GitHub for version control and project hosting

All Python modules used by the application are part of the Python standard library. No third-party package is required for the GUI.

## 4. Repository Structure

```text
University-Timetable-Clash-Detector/
├── data/
│   └── timetable.csv
├── Timetable_Clash_Detector.ipynb
├── gui_app.py
├── requirements.txt
├── README.md
└── docs/
    └── PROJECT_REPORT.md
```

## 5. How to Run the GUI

1. Install Python 3 on your computer. On Windows, make sure Python is added to PATH.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run:

```bash
python gui_app.py
```

The application loads `data/timetable.csv` automatically when that file is present.

## 6. How to Run the Notebook

1. Open `Timetable_Clash_Detector.ipynb` in Jupyter Notebook, JupyterLab, or VS Code.
2. Run the cells from top to bottom.
3. Review the sample timetable, detected clash output, and test results.

## 7. CSV Format

The timetable CSV uses these columns:

```csv
course,teacher,room,group,day,start,end
```

Time values must use 24-hour `HH:MM` format. The end time must be later than the start time.

## 8. Clash Detection Logic

For each pair of class sessions, the program:
1. Checks whether both sessions are scheduled on the same day.
2. Checks whether their time intervals overlap.
3. If they overlap, compares their student group, teacher, and room.
4. Records the overlap and the reason(s) for the clash.

Two intervals overlap when:

```text
start_A < end_B AND start_B < end_A
```

Sessions where one ends exactly when the other begins are not treated as overlapping.

## 9. Testing

The notebook contains five assertion-based checks covering:
- Overlapping sessions.
- Sessions that only touch at an endpoint.
- Sessions on different days.
- Sessions with identical time slots.
- Detection of a shared teacher conflict.

The notebook's displayed output reports: **All 5 tests passed**. The Tkinter desktop interface should also be launched locally to verify its behavior on the submission computer.

## 10. Limitations

- The application checks one-day time slots and does not model overnight classes.
- Timetable data is stored locally in CSV files; there is no central university database or multi-user synchronization.
- The sample timetable is demonstration data and should be replaced with actual institutional data when used in practice.

## 11. Conclusion

The project demonstrates how Python, CSV file handling, pairwise comparison, and a Tkinter interface can be used to identify common timetable conflicts. It can help reduce manual checking when preparing university class schedules.

## 12. Author

**Anindita Mukherjee**  
BCA, Brainware University  
Student Code: BWU/BCA/25/159
