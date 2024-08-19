"""
This file contains all the logic related to the Start Window of the application

Author: Ivan Maldonado (Kikemaldonado11@gmail.com)
Developed at: August, 2024
"""

import os
import csv

import tkinter as tk
from tkinter import filedialog

import settings


class StartWindow(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("LimeSurvey Data Manager")
        self.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}")
        self.configure(bg=settings.BACKGROUND_COLOR)
        self.resizable(False, False)
        
        
        # Window grid configurations
        
        for i in range(7):  
            self.grid_rowconfigure(i, weight=1)

        for j in range(3):  
            self.grid_columnconfigure(j, weight=1)
            
        
        self.survey_dict = {}
        self.selected_directory = None
        self.txt_files = None
        self.csv_files = None
        self.survey_id = None
        
        
        # Window Labels
        
        welcome_text = tk.Label(self, text="Welcome to LimeSurvey Data Manager!", background=settings.BACKGROUND_COLOR, wraplength=900, font=(settings.FONT, 20, "bold"),)
        welcome_text.grid(row=0, column=1, sticky="nsew") 
         
        main_text = tk.Label(self, text="Here you can upload your LimeSurvey exported survey\nand all the responses provided by OfflineSurveysApp to manage them and obtained a finest .csv", background=settings.BACKGROUND_COLOR, width=500, wraplength=600, font=(settings.FONT, 14))
        main_text.grid(row=1, column=1, sticky="nsew")
        
        # Window buttons
        
        directory_button = tk.Button(self, text="Select Directory", command=self.select_directory, font=(settings.FONT, 14), bg=settings.BACKGROUND_BUTTON_COLOR, fg='black', padx=10, pady=5)
        directory_button.grid(row=3, column=1, sticky="nsew", padx=170, pady=20)

        process_button = tk.Button(self, text="Process", command=self._change_window, font=(settings.FONT, 14), bg=settings.BACKGROUND_BUTTON_COLOR, fg='black', padx=10, pady=5)
        process_button.grid(row=6, column=1, sticky="nsew", padx=250, pady=20)
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()



    def select_directory(self):
        self.selected_directory = filedialog.askdirectory(title="Select a Directory")
        
        if self.selected_directory:
            
            # Storage all .txt and .csv files in list for further usage along with the survey id 
            
            self.txt_files = [os.path.join(self.selected_directory, file) for file in os.listdir(self.selected_directory) if os.path.join(self.selected_directory, file).endswith('.txt')]
            self.survey_id = [''.join(filter(str.isdigit, file.split('_')[2])) for file in os.listdir(self.selected_directory) if os.path.join(self.selected_directory, file).endswith('.txt')]
            self.csv_files = [os.path.join(self.selected_directory, file) for file in os.listdir(self.selected_directory) if os.path.join(self.selected_directory,file).endswith('.csv')]
    
    
    def _validate_survey(self):
        if self.txt_files:
            if len(self.txt_files) > 1:
                settings.show_error_message("It looks like you've got more than one limesurvey.txt file inside your directory")
                exit()
            else:
                with open(self.txt_files[0], 'r') as survey_file:
                    if survey_file.readline() in 'id,related_id,class,typscale,name,relevance,text,help,language,validation,mandatory,encrypted,other,default,same_default,same_script,allowed_filetypes,alphasort,answer_order,answer_width,answer_width_bycolumn,array_filter,array_filter_exclude,array_filter_style,assessment_value,category_separator,choice_input_columns,choice_title,commented_checkbox,commented_checkbox_auto,cssclass,date_format,date_max,date_min,display_columns,display_rows,display_type,dropdown_dates,dropdown_dates_minute_step,dropdown_dates_month_style,dropdown_prefix,dropdown_prepostfix,dropdown_separators,dropdown_size,dualscale_headerA,dualscale_headerB,em_validation_q,em_validation_q_tip,em_validation_sq,em_validation_sq_tip,equals_num_value,equation,exclude_all_others,exclude_all_others_auto,hidden,hide_tip,input_boxes,input_size,label_input_columns,location_city,location_country,location_defaultcoordinates,location_mapheight,location_mapservice,location_mapwidth,location_mapzoom,location_nodefaultfromip,location_postal,location_state,max_answers,max_filesize,max_num_of_files,max_num_value,max_num_value_n,max_subquestions,maximum_chars,min_answers,min_num_of_files,min_num_value,min_num_value_n,multiflexible_checkbox,multiflexible_max,multiflexible_min,multiflexible_step,num_value_int_only,numbers_only,other_comment_mandatory,other_numbers_only,other_replace_text,page_break,parent_order,placeholder,prefix,printable_help,public_statistics,random_group,random_order,rank_title,repeat_headings,reverse,samechoiceheight,samelistheight,scale_export,show_comment,show_grand_total,show_title,show_totals,showpopups,slider_accuracy,slider_custom_handle,slider_default,slider_default_set,slider_handle,slider_layout,slider_max,slider_middlestart,slider_min,slider_orientation,slider_rating,slider_reset,slider_reversed,slider_separator,slider_showminmax,statistics_graphtype,statistics_showgraph,statistics_showmap,suffix,text_input_columns,text_input_width,time_limit,time_limit_action,time_limit_countdown_message,time_limit_disable_next,time_limit_disable_prev,time_limit_message,time_limit_message_delay,time_limit_message_style,time_limit_timer_style,time_limit_warning,time_limit_warning_2,time_limit_warning_2_display_time,time_limit_warning_2_message,time_limit_warning_2_style,time_limit_warning_display_time,time_limit_warning_message,time_limit_warning_style,use_dropdown,value_range_allows_missing':
                        settings.show_error_message("Incorrect limesurvey file")
                        exit()
                    else:
                        self.survey_id = self.survey_id[0]
                        self._get_survey_dict(survey_file.readlines())
                        return True
        else:
            settings.show_error_message("It looks like you've got no limesurvey.txt file inside your directory. Please provide one")
            exit()


    # Check if every DBResults file belongs to the selected limesurvey.txt

    def _validate_csv_files(self):

        if len(self.csv_files) > 0:
        
            for file in self.csv_files:

                with open(file, newline='', encoding='UTF-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        for i in range(7, len(row)):
                            if 'filecount' not in row[i]:
                                code = row[i].split('X')
                                if  not (code[0] == self.survey_id and self.survey_dict.get(code[1]) and self.survey_dict.get(code[2])):
                                    settings.show_error_message("Ups, one of your DBResults file does not belong to the same survey you're trying to process")
                                    exit()
                        break        
            return True
        
        else:
            settings.show_error_message("Ups, you've got no DBResults files in this directory")
            exit() 
            
            
    # Parse all the limesurvey.txt to get all the related information into a dict        
                
    def _get_survey_dict(self, limesurvey_file):
        
        for line in limesurvey_file:
            elements = line.split(',')
            if not self.survey_dict.get(elements[0]):
                 self.survey_dict[elements[0]] = {'Q': elements[6].rstrip(), 'A': {}}
            else:
                self.survey_dict[elements[0]]['A'][elements[4]] = elements[6].rstrip()
    

    def _change_window(self): 
        if self._validate_survey() and self._validate_csv_files():
            self.destroy()
            
    def on_closing(self):
        exit()
