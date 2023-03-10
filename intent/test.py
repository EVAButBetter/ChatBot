from ai_intent.AiIntent import AiIntent

#
# for testing, useless
#


if __name__ == "__main__":
    # professor = AiIntent("professor_info","PROFESSOR")
    # res = professor.fill_slot("NAME","LOBO JORGE")
    # print(res)
    
    course = AiIntent("professor_info","PROFESSOR")
    course.fill_slot("NAME","LOBO , JORGE")
    course.fill_slot("OFFICE","55110")
    course.inform()
    # if res is not True:
    #     course.request(res)
        
    # res = course.get_slot("PRICE")
