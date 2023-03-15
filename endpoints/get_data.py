import requests


response = requests.get("https://dtic-recepcionist.upf.edu/api/people/names").json()
f = open("upf-scgpt.txt", "w")
data = []
for i, professor in enumerate(response):
    request_text = "professor_info{ request ( professor_name = ? ) & sure, could you tell me the name of the professor you want to know? }\n"
    inform_text = (
        "professor_info{ inform ( professor_name = "
        + professor["name"]
        + " ; location = "
        + professor["office"]
        + " ; ) & sure, the professor  "
        + professor["name"]
        + " works in office "
        + professor["office"]
        + "  }\n"
    )
    confirm_text = (
        "professor_info{ confirm ( professor_name = "
        + professor["name"]
        + " ) & ok, please let me confirm, you want to know the information about professor"
        + professor["name"]
        + "? }\n"
    )
    deny_text = (
        "professor_info { deny ( professor_name = ? & sorry, I cannot get any information about the provided professor name. }\n"
    )
    data.append(inform_text)
    data.append(request_text)
    data.append(confirm_text)
    data.append(deny_text)

f.writelines(data)


response = requests.get("https://dtic-recepcionist.upf.edu/api/groups/names").json()
data = []
for i, group in enumerate(response):
    request_text = "group_info{ request ( group_name = ? ) & sure, could you tell me the name of the group you want to know? }\n"
    inform_text = (
        "group_info{ inform ( group_name = "
        + group["name"]
        + " ; location = "
        + group["office"]
        + " ; leader = "
        + group["leader"]
        + " ; ) & sure, the group  "
        + group["name"]
        + " is in office "
        + group["office"]
        + ", the leader is "
        + group["leader"]
        + " }\n"
    )
    confirm_text = (
        "group_info{ confirm ( group_name = "
        + group["name"]
        + " ) & ok, please let me confirm, you want to know the information about group"
        + group["name"]
        + "? }\n"
    )
    deny_text = (
        "group_info { deny ( group_name = ?) & sorry, I cannot get any information about the provided group name. }\n"
    )
    data.append(inform_text)
    data.append(request_text)
    data.append(confirm_text)
    data.append(deny_text)

f.writelines(data)

f.close()
