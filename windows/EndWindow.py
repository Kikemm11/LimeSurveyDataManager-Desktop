import os

import tkinter as tk
from tkinter import filedialog

from jinja2 import Template

import settings
from views import output_html


class EndWindow(tk.Tk):
    
    def __init__(self, _output_df):
        super().__init__()
        self.title("LimeSurvey Data Manager")
        self.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}")
        self.configure(bg=settings.BACKGROUND_COLOR)
        self.resizable(False, False)
        
        for i in range(5):  
            self.grid_rowconfigure(i, weight=1)

        for j in range(3):  
            self.grid_columnconfigure(j, weight=1)

        self.output_df = _output_df

        label = tk.Label(self, 
                        text="CSV file ready",
                        background=settings.BACKGROUND_COLOR,
                        wraplength=300,
                        font=(settings.FONT, 20, "bold"),
                        height=3
                        )

        label.grid(row=1, column=1, sticky="nsew")


        img_path = self.get_image_path('csv_file.png')

        self.photo = tk.PhotoImage(file=img_path)
        self.csv_img = tk.Label(self,
                                image=self.photo,
                                background=settings.BACKGROUND_COLOR
                                )

        self.csv_img.grid(row=2, column=1, sticky="nsew", pady=20)


        save_button = tk.Button(self, 
                            text="Save", 
                            command=self._save_file,
                            font=(settings.FONT, 14),
                            bg=settings.BACKGROUND_BUTTON_COLOR,  
                            fg='black',    
                            padx=10,       
                            pady=5
                        )

        save_button.grid(row=3, column=1, sticky="nsew", pady=20, padx=70)
        
        self.mainloop()

         
    def _save_file(self):
        file_path = filedialog.asksaveasfilename(
            title="Save File",
            defaultextension=".csv",  
            filetypes=[(".csv Files", "*.csv")]  
        )
        
        if file_path:
            self.output_df.to_csv(file_path,index=False)
            self.generate_html(file_path)
            self.destroy()
            
            
    def get_image_path(self, img_name):
        current_dir = os.path.dirname(__file__)  
        parent_dir = os.path.dirname(current_dir)  
        image_path = os.path.join(parent_dir, 'assets', img_name)
        return image_path
    

    def generate_html(self, file_path):
        data = {
                    "output_df": self.output_df,
                    "column_names": self.output_df.columns,
                    "df_lenght": len(self.output_df)

                    }   
            
        template = Template(output_html.html_template)
        html_content = template.render(data)
        with open(file_path.replace('.csv', '.html'), "w") as file:
            file.write(html_content)
