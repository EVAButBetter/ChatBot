class Intent:
    """
    Abstract class: Intent
    """
    def __init__(self) -> None:
        pass
        
    def get_slot():
        """
        get slot value from a specific intent. provide the slot_name, return a tuple contains all the details
        
        """
        
    def fill_slot():
        """
        set value to a specific slot,provide the slot_name, slot_value
        
        """
        
    def check_value():
        """
        check whether the <slot,value> is existed in the database
        
        """
    
    def check_slot():
        """
        check whether all the required slots have already been filled
        
        """
        
    def request():
        """
        request information from user.
        
        """
        
    def confirm():
        """
        confirm the user's input
        
        """
        
    def inform():
        """
        inform the user all the information about this intent
        
        """
        
    # def release():
    #     """
    #     release the resource, prepare for the next question
        
    #     """
    
    # def remove_slot():
    #     """
    #     remove value from slot,
        
    #     """