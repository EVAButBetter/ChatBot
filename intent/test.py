from ai_intent import AiIntent

#
# for testing, useless
#


if __name__ == "__main__":
    # professor = AiIntent("professor_info","PROFESSOR")
    # res = professor.fill_slot("NAME","LOBO JORGE")
    # print(res)
    
    course = AiIntent("professor_info")
    print(course.fill_slot("name","LOBO , JORGE"))
    # course.fill_slot("OFFICE","55110")
    print(course.inform())
    print(course.request('name'))
    print(course.confirm())
    # if res is not True:
    #     course.request(res)
        
    # res = course.get_slot("PRICE")
