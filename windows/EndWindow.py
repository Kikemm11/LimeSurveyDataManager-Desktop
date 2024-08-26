"""
This file contains all the logic related to the End Window of the application

Author: Ivan Maldonado (Kikemaldonado11@gmail.com)
Developed at: August, 2024
"""

import os

import tkinter as tk
from tkinter import filedialog

from jinja2 import Template, Environment, FileSystemLoader

import settings

from views import output_html


class EndWindow(tk.Tk):
    
    def __init__(self, _output_df, _img_dict, _select_questions):
        super().__init__()
        self.title("LimeSurvey Data Manager")
        self.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}")
        self.configure(bg=settings.BACKGROUND_COLOR)
        self.resizable(False, False)
        
        
        # Window grid configurations
        
        for i in range(4):  
            self.grid_rowconfigure(i, weight=1)

        for j in range(5):
              
            self.grid_columnconfigure(j, weight=1)
            

        self.output_df = _output_df
        self.img_dict = _img_dict
        self.select_questions = _select_questions
        self.selected_options = None
        self.pie_chart_data = {}
        
    
        # Window images
    
        csv_img_path = self.get_image_path('csv_file.png')
        self.csv_photo = tk.PhotoImage(file=csv_img_path)
        
        self.csv_img = tk.Label(self, image=self.csv_photo, background=settings.BACKGROUND_COLOR)
        self.csv_img.grid(row=1, column=0, sticky="nsew", pady=20, padx=0)
        
        html_img_path = self.get_image_path('html_file.png')
        self.html_photo = tk.PhotoImage(file=html_img_path)
        
        self.html_img = tk.Label(self, image=self.html_photo, background=settings.BACKGROUND_COLOR)
        self.html_img.grid(row=1, column=4, sticky="nsew", pady=20, padx=75)


        # Window buttons

        save_csv_button = tk.Button(self, text="Save .csv", command=self._save_csv_file, font=(settings.FONT, 14), bg=settings.BACKGROUND_BUTTON_COLOR, fg='black', padx=10, pady=5)
        save_csv_button.grid(row=2, column=0, sticky="nsew", pady=50, padx=80)
        
        statistics_button = tk.Button(self, text="Generate statistics", command=self.pop_up_window, font=(settings.FONT, 14), bg=settings.BACKGROUND_BUTTON_COLOR, fg='black', padx=10, pady=5)
        statistics_button.grid(row=2, column=4, sticky="nsew", pady=50, padx=80)
        
        save_html_button = tk.Button(self, text="Save .html", command=self._save_html_file, font=(settings.FONT, 14), bg=settings.BACKGROUND_BUTTON_COLOR, fg='black', padx=10, pady=5)
        save_html_button.grid(row=3, column=4, sticky="n", pady=0, padx=80)
        
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()

         
    def _save_csv_file(self):
        file_path = filedialog.asksaveasfilename(title="Save File", defaultextension=".csv", filetypes=[(".csv Files", "*.csv")])
        if file_path:
            self.output_df.to_csv(file_path,index=False)
            settings.info_message("CSV file successfully saved!")
            
    def _save_html_file(self):
        file_path = filedialog.asksaveasfilename(title="Save File", defaultextension=".html", filetypes=[(".html Files", "*.html")])
        
        if file_path:
            self.generate_html(file_path)
            settings.info_message("HTML file successfully saved!")
            
               
    def get_image_path(self, img_name):
        current_dir = os.path.dirname(__file__)  
        parent_dir = os.path.dirname(current_dir)  
        image_path = os.path.join(parent_dir, 'assets', img_name)
        return image_path
    
    
    # Set up a dictionary with all the data based on the options selected by the user
    
    def get_piechart_data(self):
        
        for name in self.selected_options:
            dic = {}
            values = self.output_df[name].value_counts()
            for option, count in values.items():
                dic[option] = count
            self.pie_chart_data[name] = dic
    
    
    # Get all the information required by the data to render the .html file 

    def generate_html(self, file_path):
        
        if self.selected_options:
            self.get_piechart_data()
        
        data = {
                'output_df': self.output_df,
                'column_names': self.output_df.columns,
                'df_lenght': len(self.output_df),
                'img_dict': self.img_dict,
                'img_path': self.get_image_path('limesurvey_data_manager_logo.svg'), 
                'piechart_data': self.pie_chart_data,
                'piechart_options': [key for key in self.pie_chart_data],
                'piechart_len': len([key for key in self.pie_chart_data]),
                }   
        
        #env = Environment(loader=FileSystemLoader('views'))
        #template = env.get_template('template.html')
        #html_content = template.render(data)

        template = Template(output_html.template_html)
        html_content = template.render(data)
        
        with open(file_path, "w") as file:
            file.write(html_content)
            

    # Pop up window to select from the available choices the ones wich will have piecharts statistics
            
    def pop_up_window(self):
        
        
        def get_options():
            self.selected_options = [option for option, var in options.items() if  var.get()]
            pop_up.destroy()
        
        # Set up the window
        
        pop_up = tk.Toplevel(self)
        pop_up.title("Select one or more options to generate charts")
        pop_up.configure(bg=settings.BACKGROUND_COLOR)
        pop_up.resizable(False, False)
        
        # Set up the scroll bar
        
        canvas = tk.Canvas(pop_up, bg=settings.BACKGROUND_COLOR, borderwidth=0, highlightbackground=settings.BACKGROUND_COLOR, highlightthickness=2)
        scrollbar = tk.Scrollbar(pop_up, orient="vertical", command=canvas.yview, highlightbackground=settings.BACKGROUND_COLOR, highlightthickness=2)
        scrollable_frame = tk.Frame(canvas, bg=settings.BACKGROUND_COLOR, highlightbackground=settings.BACKGROUND_COLOR, highlightthickness=2)
        
        scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Get the possible options to display in the window based on the question criteria
        
        options = {option: tk.BooleanVar() for option in self.select_questions}
        
        for idx, (option, var) in enumerate(options.items()):
            chk = tk.Checkbutton(scrollable_frame, text=option, variable=var, background=settings.BACKGROUND_COLOR, highlightbackground=settings.BACKGROUND_COLOR, highlightthickness=2)
            chk.grid(row=idx, column=0, sticky='w', padx=5, pady=2)
            
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        btn_show = tk.Button(pop_up, text="Done", command=get_options, font=(settings.FONT, 14), bg=settings.BACKGROUND_BUTTON_COLOR, fg='black', padx=10, pady=5)
        btn_show.pack(pady=10)
        pop_up.update_idletasks()


    def on_closing(self):
        self.destroy()
        exit()