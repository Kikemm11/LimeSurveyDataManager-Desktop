# LimeSurvey Data Manager
![Project Screenshot](assets/limesurvey_data_manager_logo.png)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contact](#contact)

## Introduction

This project is a tiny and simple desktop-application which helps to manage the data provided by the responses of LimeSurveys along with the mobile application OfflineSurveysApp in order to make them presentable and readable for common users trought out .csv files and a more complete .html file.

## Features

- Analysis and interpretation of generic LimeSurvey surveys
- Simple and easy to use desktop application
- Dynamic rendering of pie charts based on user-selected data.
- Responsive design that works on all screen sizes.
- Ability to download charts as images.
- Interactive UI with smooth transitions and animations.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Kikemm11/LimeSurveyDataManager-Desktop.git
    cd LimeSurveyDataManager-Desktop
    ```
2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the app.py main file (Linux):
    ```bash
    python3 app.py
    ```
3. Run the app.py main file (Windows):
    ```bash
    python app.py
    ```

## Usage

1. Gather the survey and responses information inside a directory (limesurvey_survey_XXX.txt, DBResults.csv files, .jpg files if any)
2. Run the application and select the desire directory to process
3. Select between save a .csv file or generate a .html file after process
4. You can also select between the available options if you want to generate a piechart for any of the survey questions (Optional)

## Technologies Used

- **Application**: Python, Tkinter, Jinja2, Pandas
- **Frontend**: HTML, CSS, JavaScript
- **Charts**: Chart.js
- **Version Control**: Git

## Contact

Created by [Iván Maldonado](https://github.com/Kikemm11) - feel free to contact me at Kikemaldonado11@gmail.com for any inquiries.