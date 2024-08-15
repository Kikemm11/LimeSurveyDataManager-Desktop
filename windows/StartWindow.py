"""
This file contains all the logic related to the Start Window of the application

Author: Ivan Maldonado (Kikemaldonado11@gmail.com)
Developed at: August, 2024
"""

import tkinter as tk
from tkinter import filedialog

import settings
from windows.ProcessWindow import ProcessWindow

import re

class StartWindow(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("LimeSurvey Data Manager")
        self.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}")
        self.configure(bg=settings.BACKGROUND_COLOR)
        self.resizable(False, False)
        
        
        # Window grid configuration
        
        for i in range(6):  
            self.grid_rowconfigure(i, weight=1)

        for j in range(3):  
            self.grid_columnconfigure(j, weight=1)
        
        
        self.survey_dict = {}
        self.lime_survey_file = []
        self.exported_files = []
        self.survey_id = None
        
        
        # Window labels
        
        welcome_text = tk.Label(self, text="Welcome to LimeSurvey Data Manager!", background=settings.BACKGROUND_COLOR, wraplength=900, font=(settings.FONT, 20, "bold"))
        welcome_text.grid(row=0, column=1, sticky="nsew") 
        
        main_text = tk.Label(self, text="Here you can upload your LimeSurvey exported survey\nand all the responses provided by OfflineSurveysApp to manage them and obtained a finest .csv", background=settings.BACKGROUND_COLOR, width=500, wraplength=600, font=(settings.FONT, 14))
        main_text.grid(row=1, column=1, sticky="nsew")
        
        
        # Window buttons
        
        lime_survey_button = tk.Button(self, text="Select LimeSurvey file", command=self.select_survey_file, font=(settings.FONT, 14), bg=settings.BACKGROUND_BUTTON_COLOR, fg='black', padx=10, pady=5)
        lime_survey_button.grid(row=2, column=1, sticky="nsew", padx=170, pady=20)

        responses_button = tk.Button(self, text="Select the DBResults files", command=self.select_exported_files, font=(settings.FONT, 14), bg=settings.BACKGROUND_BUTTON_COLOR, fg='black', padx=10, pady=5)
        responses_button.grid(row=3, column=1, sticky="nsew", padx=170, pady=20)
         
        process_button = tk.Button(self, text="Process", command=self._change_window, font=(settings.FONT, 14), bg=settings.BACKGROUND_BUTTON_COLOR, fg='black', padx=10, pady=5)
        process_button.grid(row=5, column=1, sticky="nsew", padx=250, pady=20)
        
        
        self.mainloop()
        
        
        
    def select_survey_file(self):
        file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Text Files", "*.txt")])
        
        if file_path: 
            if 'limesurvey_survey' in file_path:
                self.survey_id = ''.join(filter(str.isdigit, file_path.split('_')[2]))
                with open(file_path, 'r') as file:
                    self.lime_survey_file = file.readlines()
                    self._get_survey_dict()
            else: 
                settings.show_error_message("The file must be an exported .txt file from LimeSurvey!")
        else:
            settings.show_error_message("You've got to select one limesurvey.txt file")
    
    
    def select_exported_files(self):
        self.exported_files = filedialog.askopenfilenames(title="Select Files", filetypes=[("CSV Files", "*.csv")])
        
    
    # Parse all the limesurvey file to get all the information related 
    
    def _get_survey_dict(self):
        for line in self.lime_survey_file:
            elements = line.split(',')
            if not self.survey_dict.get(elements[0]):
                 self.survey_dict[elements[0]] = {'Q': elements[6].rstrip(), 'A': {}}
            else:
                self.survey_dict[elements[0]]['A'][elements[4]] = elements[6].rstrip()
    
    
    def _change_window(self): 
        if self.lime_survey_file and len(self.exported_files) > 0:
            self.destroy()
        else:
            settings.show_error_message("You've got to select one or more BDResult.csv files")       