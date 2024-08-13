import sys
import tkinter as tk

from windows.StartWindow import StartWindow
from windows.ProcessWindow import ProcessWindow
from windows.EndWindow import EndWindow

if __name__ == "__main__":
    
    start_window = StartWindow()
    process_window = ProcessWindow(start_window.survey_dict, start_window.exported_files, start_window.survey_id)
    end_window = EndWindow(process_window.output_df)
    
