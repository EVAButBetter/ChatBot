import requests
import pandas as pd
from fuzzywuzzy import fuzz

COURSE_PATH = "data/database/COURSE.csv"
DEPARTMENT_PATH = "data/database/DEPARTMENT.csv"
FACULTY_PATH = "data/database/CAMPUS.csv"
SCHEDULE_PATH = "data/database/SCHEDULE.csv"
OPENING_CLOSE_HOURS = "data/database/OPENING_CLOSE_HOURS.csv"


def get_most_similar_value_df(df, column, value, threshold):
    max_score = -1
    best_match = None

    for name in df[column]:
        score = fuzz.ratio(name.lower(), value.lower())
        if score > max_score and score >= threshold:
            max_score = score
            best_match = name

    return best_match


def get_most_similar_value_json_list(json_list, column_name, value, threshold):
    max_score = -1
    best_match = None

    for i, json_element in enumerate(json_list):
        score = fuzz.ratio(json_element[column_name].lower(), value.lower())
        if score > max_score and score >= threshold:
            max_score = score
            best_match = json_element[column_name]

    return best_match


class ActionsSlots:

    def __init__(self):

        self.faculty_csv = None
        self.course_csv = None
        self.department_csv = None
        self.opening_close_csv = None
        self.schedule_csv = None

        self.load_databases()

    def load_databases(self):
        self.course_csv = pd.read_csv(COURSE_PATH, sep=";")
        self.department_csv = pd.read_csv(DEPARTMENT_PATH, sep=";")
        self.faculty_csv = pd.read_csv(FACULTY_PATH, sep=";")
        self.schedule_csv = pd.read_csv(SCHEDULE_PATH, sep=";")
        self.opening_close_csv = pd.read_csv(OPENING_CLOSE_HOURS, sep=";")

    def find_professor_names(self, location):
        professors_json = requests.get("https://dtic-recepcionist.upf.edu/api/people/names").json()
        professors = []
        for professor in professors_json:
            if professor["office"] == location:
                professors.append(professor["name"])
        return professors

    def find_location_info(self, professor_name):
        professors_json = requests.get("https://dtic-recepcionist.upf.edu/api/people/names").json()
        best_match = get_most_similar_value_json_list(professors_json, "name", professor_name, 0.8)
        if best_match is None:
            return None
        else:
            for professor in professors_json:
                if professor["name"] == best_match:
                    return professor['office']

    def find_course_info(self, course_name):
        self.course_csv = pd.read_csv(COURSE_PATH, sep=";")
        best_match = get_most_similar_value_df(self.course_csv, "NAME", course_name, 0.8)
        if best_match is None:
            return None
        else:
            return self.course_csv[self.course_csv["NAME"] == best_match]["DESCRIPTION"].iloc[0]

    def find_department_info(self, department_name):
        self.department_csv = pd.read_csv(DEPARTMENT_PATH, sep=";")
        best_match = get_most_similar_value_df(self.department_csv, "NAME", department_name, 0.8)
        if best_match is None:
            return None
        else:
            return self.department_csv[self.department_csv["NAME"] == best_match]["INFO"].iloc[0]

    def find_faculty_info(self, faculty_info):
        self.faculty_csv = pd.read_csv(FACULTY_PATH, sep=";")
        best_match = get_most_similar_value_df(self.faculty_csv, "NAME", faculty_info, 0.8)
        if best_match is None:
            return None
        else:
            campus_row = self.faculty_csv[self.faculty_csv["NAME"] == best_match]
            return campus_row["LOCATION"].iloc[0] + ";\n" + campus_row["CONTACT"].iloc[0] + ";\n" + \
                campus_row["BUILDINGS"].iloc[0] + ";\n" + \
                campus_row["OPENING_CLOSE_HOURS"].iloc[0]

    def find_schedule_info(self, course_name):
        self.schedule_csv = pd.read_csv(SCHEDULE_PATH, sep=";")
        best_match = get_most_similar_value_df(self.schedule_csv, "NAME", course_name, 0.8)
        if best_match is None:
            return None
        else:
            schedule_row = self.schedule_csv[self.schedule_csv["NAME"] == best_match]
            return "Theory class: " + str(schedule_row["THEORY"].iloc[0]) + ";\n" + \
                "Practice class: " + str(schedule_row["PRACTICE"].iloc[0]) + ";\n" + \
                "Seminar class: " + str(schedule_row["SEMINAR"].iloc[0])

    def find_close_open_time_info(self, service_name):
        self.opening_close_csv = pd.read_csv(OPENING_CLOSE_HOURS, sep=";")
        best_match = get_most_similar_value_df(self.opening_close_csv, "NAME", service_name, 0.8)
        if best_match is None:
            return None
        else:
            return self.opening_close_csv[self.opening_close_csv["NAME"] == best_match]["OPENING_CLOSE_HOURS"].iloc[0]
