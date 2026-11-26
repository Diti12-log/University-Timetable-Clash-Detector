"""Launcher for the University Timetable Clash Detector GUI."""

import tkinter as tk
from gui_app import TimetableClashDetectorApp


def main():
    root = tk.Tk()
    TimetableClashDetectorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
