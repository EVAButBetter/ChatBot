import requests
import pandas as pd


response = requests.get("https://dtic-recepcionist.upf.edu/api/people/names").json()
f = open("upf-scgpt.txt", "w")
data = []
for i, professor in enumerate(response):
    request_text = "professor_info{ request ( professor_name = ? )} & sure, could you tell me the name of the professor you want to know?\n"
    inform_text = (
        "professor_info{ inform ( professor_name = "
        + professor["name"]
        + " ; location = "
        + professor["office"]
        + " ; )} & sure, the professor  "
        + professor["name"]
        + " works in office "
        + professor["office"]
        + "\n"
    )
    confirm_text = (
        "professor_info{ confirm ( professor_name = "
        + professor["name"]
        + " )} & ok, please let me confirm, you want to know the information about professor"
        + professor["name"]
        + "?\n"
    )
    deny_text = (
        "professor_info { deny ( professor_name = ? )} & sorry, I cannot get any information about the provided professor name.\n"
    )
    data.append(inform_text)
    data.append(request_text)
    data.append(confirm_text)
    data.append(deny_text)


epoch = 8
response = pd.read_csv("../../data/database/DEPARTMENT.csv",sep=";")
for i, department in enumerate(response):
    request_text = "department_info{ request ( department_name = ? )} & sure, could you tell me the name of the department you want to know?\n"
    inform_text = (
        "department_info{ inform ( department_name = "
        + department["NAME"]
        + " ; information = "
        + department["INFO"]
        + " ; )} & sure, the department  "
        + department["NAME"]
        + "'s information is "
        + department["INFO"]
        + "\n"
    )
    confirm_text = (
        "department_info{ confirm ( department_name = "
        + department["NAME"]
        + " )} & ok, please let me confirm, you want to know the information about department"
        + department["NAME"]
        + "?\n"
    )
    deny_text = (
        "department_info { deny ( department_name = ? )} & sorry, I cannot get any information about the provided department name.\n"
    )
    for i in range(epoch):
        data.append(inform_text)
        data.append(request_text)
        data.append(confirm_text)
        data.append(deny_text)

epoch = 20
response = pd.read_csv("../../data/database/OPENING_CLOSE_HOURS.csv",sep=";")
for index, item in response.iterrows():
    request_text = "opening_close_hour_info{ request ( facility_name = ? )} & sure, could you tell me the name of the facility you want to know?\n"
    inform_text = (
        "opening_close_hour_info{ inform ( facility_name = "
        + item["NAME"]
        + " ; information = "
        + item["OPENING_CLOSE_HOURS"]
        + " ; )} & sure, the timetable of the  "
        + item["NAME"]
        + " is "
        + item["OPENING_CLOSE_HOURS"]
        + "\n"
    )
    confirm_text = (
        "opening_close_hour_info{ confirm ( facility_name = "
        + item["NAME"]
        + " )} & ok, please let me confirm, you want to know the timetable about "
        + item["NAME"]
        + "?\n"
    )
    deny_text = (
        "opening_close_hour_info { deny ( facility_name = ? )} & sorry, I cannot get any information about the provided facility name, please choose from Secretary, Library and Campus.\n"
    )
    for i in range(epoch):
        data.append(inform_text)
        data.append(request_text)
        data.append(confirm_text)
        data.append(deny_text)
    
epoch = 8   
response = pd.read_csv("../../data/database/SCHEDULE.csv",sep=";")
for index, item in response.iterrows():
    request_text = "schedule_info{ request ( course_name = ? )} & sure, could you tell me the name of the course you want to know?\n"
    inform_text = (
        "schedule_info{ inform ( course_name = "
        + item["NAME"]
        + " ; information = "
        + item["THEORY"]
        + " ; )} & sure, the "
        + item["NAME"]
        + " class begins on "
        + item["THEORY"]
        + "\n"
    )
    confirm_text = (
        "schedule_info{ confirm ( course_name = "
        + item["NAME"]
        + " )} & ok, please let me confirm, you want to know the information about "
        + item["NAME"]
        + "?\n"
    )
    deny_text = (
        "schedule_info { deny ( facility_name = ? )} & sorry, I cannot get any information about the provided course name.\n"
    )
    for i in range(epoch):
        data.append(inform_text)
        data.append(request_text)
        data.append(confirm_text)
        data.append(deny_text)

epoch = 8   
response = pd.read_csv("../../data/database/COURSE.csv",sep=";")
for index, item in response.iterrows():
    request_text = "course_info{ request ( course_name = ? )} & sure, could you tell me the name of the course you want to know?\n"
    inform_text = (
        "course_info{ inform ( course_name = "
        + item["NAME"]
        + " ; information = "
        + item["DESCRIPTION"]
        + " ; )} & sure, the "
        + item["NAME"]
        + " is "
        + item["DESCRIPTION"]
        + "\n"
    )
    confirm_text = (
        "course_info{ confirm ( course_name = "
        + item["NAME"]
        + " )} & ok, please let me confirm, you want to know the information about "
        + item["NAME"]
        + "?\n"
    )
    deny_text = (
        "course_info { deny ( facility_name = ? )} & sorry, I cannot get any information about the provided course name.\n"
    )
    for i in range(epoch):
        data.append(inform_text)
        data.append(request_text)
        data.append(confirm_text)
        data.append(deny_text)

f.writelines(data)


f.close()
