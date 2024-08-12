import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import settings
from windows.ProcessWindow import ProcessWindow

class StartWindow(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("LimeSurvey Data Manager")
        self.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}")
        self.configure(bg=settings.BACKGROUND_COLOR)
        self.resizable(False, False)
        
        for i in range(6):  
            self.grid_rowconfigure(i, weight=1)

        for j in range(3):  
            self.grid_columnconfigure(j, weight=1)
        
        self.survey_dict = {}
        self.lime_survey_file = []
        self.exported_files = []
        
        
        welcome_text = tk.Label(self, 
                        text="Welcome to LimeSurvey Data Manager!",
                        background=settings.BACKGROUND_COLOR,
                        wraplength=900,
                        font=(settings.FONT, 20, "bold"),
                        )
        
        welcome_text.grid(row=0, column=1, sticky="nsew") 
        
        
        main_text = tk.Label(self, 
                        text="Here you can upload your LimeSurvey exported survey\nand all the responses provided by OfflineSurveysApp to manage them and obtained a finest .csv",
                        background=settings.BACKGROUND_COLOR,
                        width=500,
                        wraplength=600,
                        font=(settings.FONT, 14)
                        )
        
        main_text.grid(row=1, column=1, sticky="nsew")
        
        
        lime_survey_button = tk.Button(self, 
                        text="Select LimeSurvey file", 
                        command=self.select_survey_file,
                        font=(settings.FONT, 14),
                        bg=settings.BACKGROUND_BUTTON_COLOR,  
                        fg='black',    
                        padx=10,       
                        pady=5
                    )
        
        lime_survey_button.grid(row=2, column=1, sticky="nsew", padx=170, pady=20)


        responses_button = tk.Button(self, 
                        text="Select the DBResults files", 
                        command=self.select_exported_files,
                        font=(settings.FONT, 14),
                        bg=settings.BACKGROUND_BUTTON_COLOR,  
                        fg='black',    
                        padx=10,       
                        pady=5
                    )

        responses_button.grid(row=3, column=1, sticky="nsew", padx=170, pady=20)
        
        
        process_button = tk.Button(self, 
                        text="Process", 
                        command=self.change_window,
                        font=(settings.FONT, 14),
                        bg=settings.BACKGROUND_BUTTON_COLOR,  
                        fg='black',    
                        padx=10,       
                        pady=5
                    )

        process_button.grid(row=5, column=1, sticky="nsew", padx=250, pady=20)
    
    
    def change_window(self): 
        
        if self.lime_survey_file and len(self.exported_files) > 0:
            s_dict = self.survey_dict
            e_files = self.exported_files
            self.destroy()
            process_window = ProcessWindow(s_dict, e_files)
            process_window.mainloop()
        else:
            message = "You've got to select one or more BDResult.csv files"
            self.show_error_message(message)
                
    def _get_survey_dict(self):
        
        for line in self.lime_survey_file:
            elements = line.split(',')
            if not self.survey_dict.get(elements[0]):
                 self.survey_dict[elements[0]] = {'Q': elements[6].rstrip(), 'A': {}}
            else:
                self.survey_dict[elements[0]]['A'][elements[4]] = elements[6].rstrip()
    
    def select_survey_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[("Text Files", "*.txt")]
        )
        
        if file_path: 
            with open(file_path, 'r') as file:
                self.lime_survey_file = file.readlines()
                self._get_survey_dict()
        else:
            message = "You've got to select one limesurvey.txt file"
            self.show_error_message(message)
     
        
    def select_exported_files(self):
        
        self.exported_files = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=[("CSV Files", "*.csv")]
        )
        
        
    def show_error_message(self, message):
        messagebox.showerror(
            title="Error",
            message=message
        )