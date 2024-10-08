"""
This file contains the main calls to the windows involved in the application

Author: Ivan Maldonado (Kikemaldonado11@gmail.com)
Developed at: August, 2024
"""

from windows.StartWindow import StartWindow
from windows.ProcessWindow import ProcessWindow
from windows.EndWindow import EndWindow

if __name__ == "__main__":
    
    start_window = StartWindow()
    process_window = ProcessWindow(start_window.survey_dict, start_window.csv_files, start_window.survey_id, start_window.selected_directory)
    end_window = EndWindow(process_window.output_df, process_window.img_dict, process_window.select_questions)