import pandas as pd
import requests
data = []
f = open("nlu1.txt", "w")
# response = pd.read_csv("../../data/database/COURSE.csv",sep=";")
# for index, item in response.iterrows():
#     name = item["NAME"]
#     data.append("What is the price of the course [" + name + "](COURSE)?\n")
#     data.append("How many credits is the course [" + name + "](COURSE) worth?\n")
#     data.append("Which faculty is offering the course [" + name + "](COURSE)?\n")
#     data.append("What is the description of the course [" + name + "](COURSE)?\n")
#     data.append("How many available spots are there for the course [" + name + "](COURSE)?\n")
#     data.append("What is the schedule for the course [" + name + "](COURSE)?\n")
#     data.append("Where is the course [" + name + "](COURSE) being held?\n")
#     data.append("What is the price of the course [" + name + "](COURSE)?\n")
#     data.append("How many credits is the course [" + name + "](COURSE) worth?\n")
#     data.append("What is the schedule for the course [" + name + "](COURSE)?\n")
#     data.append("What can you tell me about the course [" + name + "](COURSE)?\n")
#     data.append("How does the course [" + name + "](COURSE) fit into the curriculum?\n")
#     data.append("What are the prerequisites for the course [" + name + "](COURSE)?\n")
#     data.append("How is the course [" + name + "](COURSE) graded?\n")
#     data.append("Who is the instructor for the course [" + name + "](COURSE)?\n")
#     data.append("What textbooks are used in the course [" + name + "](COURSE)?\n")
#     data.append("Are there any special requirements for the course [" + name + "](COURSE) (e.g. group projects, presentations, etc.)?\n")
#     data.append("What kind of career opportunities can graduates of the course [" + name + "](COURSE) expect?\n")
#     data.append("Can you provide more information about the faculty offering the course [" + name + "](COURSE)?\n")
#     data.append("What sets the course [" + name + "](COURSE) apart from other similar  courses offered at the university?\n")
    
    
# response = pd.read_csv("../../data/database/OPENING_CLOSE_HOURS.csv",sep=";")
# for index, item in response.iterrows():
#     name = item["NAME"]
#     data.append("What time does the [" + name + "](FAC) open and close each day?\n")
#     data.append("Can you tell me the opening and closing hours for the [" + name + "](FAC)?\n")
#     data.append("When does the [" + name + "](FAC) start and end its daily operations?\n")
#     data.append("What are the operating hours for the [" + name + "](FAC) on weekdays and weekends?\n")
#     data.append("Could you provide me with the schedule for the [" + name + "](FAC) opening and closing times?\n")
#     data.append("What time does the [" + name + "](FAC) usually open its doors and what time does it close for the day?\n")
#     data.append("I was wondering what the daily hours of operation are for the [" + name + "](FAC)?\n")
#     data.append("At what time does the [" + name + "](FAC) open for business and at what time does it close?\n")
#     data.append("What time does the [" + name + "](FAC) usually start its operations in the morning and when does it shut down at night?\n")
#     data.append("Could you give me the hours of operation for the [" + name + "](FAC) during the week and on weekends?\n")
#     data.append("What time does the [" + name + "](FAC) open each day?\n")
#     data.append("Could you tell me when the [" + name + "](FAC) doors typically open?\n")
#     data.append("At what time does the [" + name + "](FAC) begin its operations for the day?\n")
#     data.append("I was wondering when the [" + name + "](FAC) usually opens to the public?\n")
#     data.append("What are the usual opening hours for the [" + name + "](FAC) during weekdays and weekends?\n")
#     data.append("What time does the [" + name + "](FAC) close each day?\n")
#     data.append("Could you tell me when the [" + name + "](FAC) typically shuts down for the day?\n")
#     data.append("At what time does the [" + name + "](FAC) end its daily operations?\n")
#     data.append("I was wondering when the [" + name + "](FAC) usually closes its doors to the public?\n")
#     data.append("What are the usual closing hours for the [" + name + "](FAC) during weekdays and weekends?\n")

response = requests.get("https://dtic-recepcionist.upf.edu/api/people/names").json()
f = open("nlu3.txt", "w")
data = []
for i, professor in enumerate(response):
    names = professor["name"]
    seq = names.split(" ")
    name = ""
    for i in seq:
        i = i[0] + i[1:].lower()
        name = name + i + " "
    # name = " ".join(seq)
    name = name.strip()
    data.append("where is professor [" + name + "](PERSON)\n")
    data.append("Has anyone seen Professor [" + name + "](PERSON)\n")
    data.append("Where could Professor [" + name + "](PERSON) be\n")
    data.append("Do you know the whereabouts of Professor [" + name + "](PERSON)\n")
    data.append("I can't seem to find Professor [" + name + "](PERSON), have you seen him\n")
    data.append("Is Professor [" + name + "](PERSON) around\n")
    data.append("Can someone tell me where Professor [" + name + "](PERSON) is\n")
    data.append("I'm looking for Professor [" + name + "](PERSON), have you seen him\n")
    data.append("Professor [" + name + "](PERSON), have you seen him\n")
    data.append("I heard Professor [" + name + "](PERSON) is here, do you know where\n")
    data.append("Have you come across Professor [" + name + "](PERSON)\n")
    data.append("Have you seen Professor [" + name + "](PERSON)\n")
    data.append("Can you tell me if Professor [" + name + "](PERSON) is around\n")
    data.append("I need to speak with Professor [" + name + "](PERSON), have you seen him\n")
    data.append("Where might Professor [" + name + "](PERSON) be\n")
    data.append("Is Professor [" + name + "](PERSON) in the building\n")
    data.append("Who is professor [" + name + "](PERSON)\n")
    data.append("Can you tell me who professor [" + name + "](PERSON) is\n")
    data.append("I'm not familiar with professor [" + name + "](PERSON). can you introduce them?\n")
    data.append("Could you explain who professor [" + name + "](PERSON) is\n")
    data.append("Who is the professor named professor [" + name + "](PERSON)\n")
    data.append("Can you provide more information on professor [" + name + "](PERSON)\n")
    data.append("Who exactly is professor [" + name + "](PERSON)\n")
    data.append("Can you give me a brief background on professor [" + name + "](PERSON)\n")
    data.append("Who is the individual known as professor [" + name + "](PERSON)\n")
    data.append("[" + name + "](PERSON)\n")

    
    
f.writelines(data)
f.close()
