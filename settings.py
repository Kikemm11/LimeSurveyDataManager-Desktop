import os

import pandas as pd
from tkinter import messagebox


# Main properties

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500

BACKGROUND_COLOR = '#CAFCB3'
BACKGROUND_BUTTON_COLOR = '#76C453'

FONT = "Poppins"


# Resources and utilities


def mix_columns(df, prefix, new_column):
        columns = [col for col in df.columns if col.startswith(prefix)]
        index = df.columns.get_loc(columns[0])
        df[new_column] = df[columns].bfill(axis=1).ffill(axis=1).iloc[:,0]
        df = df.drop(columns=columns)
        column_data = df.pop(new_column)
        df.insert(index,new_column,column_data)
        return df
    
    
def manage_duplicates(column_names_set, column_name):
        
        if column_name in column_names_set:
            i = 1
            column_name = f"{column_name}_{i}"
            while column_name in column_names_set:
                i += 1
                column_name = f"{column_name.split('_')[0]}_{i}"
        column_names_set.add(column_name)
        
        return column_name


def manage_multimedia_names(column_name):
        column_name = 'Foto' if 'CameraIMG' in column_name else column_name
        column_name = 'Ubicación' if 'LocationIMG' in column_name else column_name
        return column_name


def show_error_message(message):
        messagebox.showerror(
            title="Error",
            message=message
        )


def info_message(message):
    messagebox.showinfo(
          title="Success",
          message=message
        )