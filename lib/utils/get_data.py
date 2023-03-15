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



response = requests.get("https://dtic-recepcionist.upf.edu/api/groups/names").json()
for i, group in enumerate(response):
    request_text = "group_info{ request ( group_name = ? )} & sure, could you tell me the name of the group you want to know?\n"
    inform_text = (
        "group_info{ inform ( group_name = "
        + group["name"]
        + " ; location = "
        + group["office"]
        + " ; leader = "
        + group["leader"]
        + " ; )} & sure, the group  "
        + group["name"]
        + " is in office "
        + group["office"]
        + ", the leader is "
        + group["leader"]
        + "\n"
    )
    confirm_text = (
        "group_info{ confirm ( group_name = "
        + group["name"]
        + " )} & ok, please let me confirm, you want to know the information about group"
        + group["name"]
        + "?\n"
    )
    deny_text = (
        "group_info { deny ( group_name = ? )} & sorry, I cannot get any information about the provided group name.\n"
    )
    data.append(inform_text)
    data.append(request_text)
    data.append(confirm_text)
    data.append(deny_text)


response = pd.read_csv("../data/database/OPENING_CLOSE_HOURS.csv",sep=";")
for index, item in response.iterrows():
    request_text = "opening_close_hour_info{ request ( facility_name = ? )} & sure, could you tell me the name of the facility you want to know?\n"
    inform_text = (
        "opening_close_hour_info{ inform ( facility_name = "
        + item["NAME"]
        + " ; timetable = "
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
        + " )} & ok, please let me confirm, you want to know the information about "
        + item["NAME"]
        + "?\n"
    )
    deny_text = (
        "opening_close_hour_info { deny ( facility_name = ? )} & sorry, I cannot get any information about the provided facility name, please choose from Secretary, Library and Campus.\n"
    )
    data.append(inform_text)
    data.append(request_text)
    data.append(confirm_text)
    data.append(deny_text)
    
    
response = pd.read_csv("../data/database/SCHEDULE.csv",sep=";")
for index, item in response.iterrows():
    request_text = "schedule_info{ request ( course_name = ? )} & sure, could you tell me the name of the course you want to know?\n"
    inform_text = (
        "schedule_info{ inform ( course_name = "
        + item["NAME"]
        + " ; theory = "
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
    data.append(inform_text)
    data.append(request_text)
    data.append(confirm_text)
    data.append(deny_text)

f.writelines(data)


f.close()
