from ai_intent.AiIntent import AiIntent

#
# for testing, useless
#


if __name__ == "__main__":
    # professor = AiIntent("professor_info","PROFESSOR")
    # res = professor.fill_slot("NAME","LOBO JORGE")
    # print(res)
    
    course = AiIntent("course_info","COURSE")
    res = course.get_slot("PRICE")
    res = course.get_slot("PRICE")
    print(res)
