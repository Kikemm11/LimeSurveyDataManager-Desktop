import time
import pandas as pd

import tkinter as tk
from tkinter import ttk

import settings


class ProcessWindow(tk.Tk):
    
    def __init__(self, _survey_dict, _files, _survey_id):
        super().__init__()
        self.title("LimeSurvey Data Manager")
        self.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}")
        self.configure(bg=settings.BACKGROUND_COLOR)
        self.resizable(False, False)
        
        for i in range(4):  
            self.grid_rowconfigure(i, weight=1)

        for j in range(3): 
            self.grid_columnconfigure(j, weight=1)
        
        self.survey_dict = _survey_dict
        self.files = _files
        self.survey_id = _survey_id
        self.DBResults_dataframes = []
        self.output_df = None
        self.file_counter = 0
        
        label = tk.Label(self, 
                        text="Processing Data",
                        background=settings.BACKGROUND_COLOR,
                        wraplength=300,
                        font=(settings.FONT, 20, "bold"),
                        )
        
        label.grid(row=0, column=1, sticky="nsew")
        
        self.progress_label = tk.Label(self,
                                text=f"{self.file_counter} / {len(self.files)} files",
                                background=settings.BACKGROUND_COLOR,
                                wraplength=300,
                                font=(settings.FONT, 16),
                                  )
        
        self.progress_label.grid(row=1, column=1, pady=10)
        
    
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.progress_bar.grid(row=2, column=1, sticky="nsew", padx=20, pady=70)
            
        self.progress_bar["maximum"] = len(self.files)
        self.progress_bar["value"] = 0
        
        self._manage_data()
        
        self.mainloop()



    def _manage_data(self):

        for file in self.files:
            
            self.duplicated_names = []
            self.column_names_set = set()
            
            db_results_df = pd.read_csv(file)
            db_results_df = db_results_df.drop(db_results_df.columns[:7], axis=1)
            
            columns_to_drop = [col for col in db_results_df.columns if 'file' in col]
            db_results_df = db_results_df.drop(columns=columns_to_drop)
            
            for col in db_results_df.columns:

                id = col.split('X')[2]
            
                new_name = str(self.survey_dict.get(id).get('Q'))    
                new_name = settings.manage_multimedia_names(new_name)
                self.duplicated_names.append(new_name)
                new_name = settings.manage_duplicates(self.column_names_set, new_name)
                    
                db_results_df = db_results_df.rename(columns={col: new_name})          
                db_results_df[new_name] = db_results_df[new_name].apply(lambda x: settings.get_values(x, self.survey_dict, id))
                    
                    
            self.duplicated_names = set([name for name in self.duplicated_names if self.duplicated_names.count(name) > 1 and (name != 'Foto' and name != 'Ubicación')])
            
            # Delete all the empty columns in the dataframe
            
            db_results_df = db_results_df.dropna(axis=1, how='all')
            
            # Mix the concurrent columns in one
            
            for column in self.duplicated_names:
                db_results_df = settings.mix_columns(db_results_df, column+'_', column)
        
            self.DBResults_dataframes.append(db_results_df)
            self.file_counter += 1
            
            self.progress_bar["value"] = self.file_counter
            self.progress_label.config(text=f"{self.file_counter} / {len(self.files)} files")  
            self.update_idletasks()
            
            
        self.output_df = pd.concat(self.DBResults_dataframes, ignore_index=True) if len(self.DBResults_dataframes) > 1 else self.DBResults_dataframes[0] 
        self._change_window()
    


    def _change_window(self): 
        time.sleep(1)
        self.destroy()    