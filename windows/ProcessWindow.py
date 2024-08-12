import sys
import time
import pandas as pd

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import settings
import json

from windows.EndWindow import EndWindow


class ProcessWindow(tk.Tk):
    
    def __init__(self, _survey_dict, _files):
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
        self.column_names_set = set()
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
        

    def _manage_data(self):

        for file in self.files:
            
            db_results_df = pd.read_csv(file)
            db_results_df = db_results_df.drop(db_results_df.columns[:7], axis=1)
            
            columns_to_drop = [col for col in db_results_df.columns if 'file' in col]
            db_results_df = db_results_df.drop(columns=columns_to_drop)
            
            for col in db_results_df.columns:
                
                id = col.split('X')[2]
                
                if self.survey_dict.get(id):
                    
                    new_name = str(self.survey_dict.get(id).get('Q'))    
                    new_name = self.manage_multimedia_names(new_name)
                    new_name = self.manage_duplicates(new_name)    
                    
                    db_results_df = db_results_df.rename(columns={col: new_name})          
                    db_results_df[new_name] = db_results_df[new_name].apply(lambda x: self.get_values(x, id))
                    
            self.column_names_set = set()
            
            # Delete all the empty columns in the dataframe
            db_results_df = db_results_df.dropna(axis=1, how='all')
            # Mix the concurrent columns in on
            db_results_df = self.mix_columns(db_results_df, 'Tipo_', 'Tipo')
            db_results_df = self.mix_columns(db_results_df, 'Tipología_', 'Tipología')
            db_results_df = self.mix_columns(db_results_df, 'Parroquia:_', 'Parroquia')
            db_results_df = self.mix_columns(db_results_df, 'UBCH:_', 'UBCH')
            
            self.DBResults_dataframes.append(db_results_df)
            self.file_counter += 1
            
            self.progress_bar["value"] = self.file_counter
            self.progress_label.config(text=f"{self.file_counter} / {len(self.files)} files")  
            self.update_idletasks()
            
            
        self.output_df = pd.concat(self.DBResults_dataframes, ignore_index=True) if len(self.DBResults_dataframes) > 1 else self.DBResults_dataframes[0] 
        self.change_window()
    
    # Resources and utilities

    def mix_columns(self, df, prefix, new_column):
        columns = [col for col in df.columns if col.startswith(prefix)]
        index = df.columns.get_loc(columns[0])
        df[new_column] = df[columns].bfill(axis=1).ffill(axis=1).iloc[:,0]
        df = df.drop(columns=columns)
        column_data = df.pop(new_column)
        df.insert(index,new_column,column_data)
        return df


    def get_values(self, value, id):
 
        if  not isinstance(value, pd.Series):
            value = str(self.survey_dict.get(id).get('A').get(value)) if self.survey_dict.get(id).get('A').get(value) else value

            if isinstance(value, str) and value.startswith('[ {'):
                value = json.loads(value)[0]["name"]

            return value
        else:
            return
        
    def manage_duplicates(self, column_name):
        
        if column_name in self.column_names_set:
            i = 1
            column_name = f"{column_name}_{i}"
            while column_name in self.column_names_set:
                i += 1
                column_name = f"{column_name.split('_')[0]}_{i}"
        self.column_names_set.add(column_name)
        
        return column_name

    def manage_multimedia_names(self, column_name):
        column_name = 'Foto' if 'Foto' in column_name else column_name
        column_name = 'Ubicación' if 'ubicación' in column_name else column_name
        return column_name
    
    def change_window(self): 
        df = self.output_df
        time.sleep(1)
        self.destroy()
        end_window = EndWindow(df)
        end_window.mainloop()
        
        
    
    