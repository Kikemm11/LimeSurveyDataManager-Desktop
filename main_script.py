import sys
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import settings
from windows.StartWindow import StartWindow


if __name__ == "__main__":
    app = StartWindow()
    app.mainloop()




# Resources and utilities

"""
def mix_columns(df, prefix, new_column):
    columns = [col for col in df.columns if col.startswith(prefix)]
    index = df.columns.get_loc(columns[0])
    df[new_column] = df[columns].bfill(axis=1).ffill(axis=1).iloc[:,0]
    df = df.drop(columns=columns)
    column_data = df.pop(new_column)
    df.insert(index,new_column,column_data)
    return df


def get_values(value, id):
    if  not isinstance(value, pd.Series):
        value = str(survey_dict.get(id).get('A').get(value)) if survey_dict.get(id).get('A').get(value) else value
        return value
    else:
        return
    
def manage_duplicates(column_name):
    
    if column_name in column_names_set:
        i = 1
        column_name = f"{column_name}_{i}"
        while column_name in column_names_set:
            i += 1
            column_name = f"{column_name.split('_')[0]}_{i}"
    column_names_set.add(column_name)
    
    return column_name

def manage_multimedia_names(column_name):
    column_name = 'Foto' if 'Foto' in column_name else column_name
    column_name = 'Ubicación' if 'ubicación' in column_name else column_name
    return column_name
    
    
# Script


if len(sys.argv) != 3:
        
        print("Usage: python script.py <path_to_txt_file> <path_to_DBResults_file>")

else:

    survey_dict = {}
    column_names_set = set()
    
    # Storage all the questions and answers details in a dict for further usage
        
    try:
        with open(sys.argv[1], mode='r') as file:
             
            lines = file.readlines()
            for line in lines:
                elements = line.split(',')

                if not survey_dict.get(elements[0]):
                     survey_dict[elements[0]] = {'Q': elements[6].rstrip(), 'A': {}}
                else:
                     survey_dict[elements[0]]['A'][elements[4]] = elements[6].rstrip()
            
    except FileNotFoundError:
        print(f"File not found: {sys.argv[1]}")
    except IOError:
        print("Error reading the file.")


    # Handle the DBResults file and create a inspection_output file
      
    db_results_df = pd.read_csv(sys.argv[2])
    db_results_df = db_results_df.drop(db_results_df.columns[:7], axis=1)
    
    columns_to_drop = [col for col in db_results_df.columns if 'file' in col]
    db_results_df = db_results_df.drop(columns=columns_to_drop)
    
    for col in db_results_df.columns:
        
        id = col.split('X')[2]
        
        if survey_dict.get(id):
            
            new_name = str(survey_dict.get(id).get('Q'))    
            new_name = manage_multimedia_names(new_name)
            new_name = manage_duplicates(new_name)    
            
            db_results_df = db_results_df.rename(columns={col: new_name})          
            db_results_df[new_name] = db_results_df[new_name].apply(lambda x: get_values(x, id))
            
    
    # Delete all the empty columns in the datafram
    db_results_df = db_results_df.dropna(axis=1, how='all')
    
    # Mix the concurrent columns in on
    db_results_df = mix_columns(db_results_df, 'Tipo_', 'Tipo')
    db_results_df = mix_columns(db_results_df, 'Tipología_', 'Tipología')
    db_results_df = mix_columns(db_results_df, 'Parroquia:_', 'Parroquia')
    db_results_df = mix_columns(db_results_df, 'UBCH:_', 'UBCH')
       
    db_results_df.to_csv('/home/kikemm11/Escritorio/test.csv',index=False)
    
"""