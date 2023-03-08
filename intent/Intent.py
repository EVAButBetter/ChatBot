class Intent:
    """
    Abstract class: Intent
    """
    def __init__(self) -> None:
        pass
        
    def get_slot(self):
        """
        get slot value from a specific intent. provide the slot_name, return a tuple contains all the details
        
        """
        
    
    def fill_slot(self):
        """
        set value to a specific slot,provide the slot_name, slot_value
        
        """
        
    # def remove_slot():
    #     """
    #     remove value from slot,
        
    #     """
        
    def check_value(self):
        """
        check whether the <slot,value> is existed in the database
        
        """
    
    def check_slot(self):
        """
        check whether all the required slots have already been filled
        
        """
        
    def request(self):
        """
        request information from user.
        
        """
        
    def confirm(self):
        """
        confirm the user's input
        
        """
        
    def inform(self):
        """
        inform the user all the information about this intent
        
        """
        
    def release(self):
        """
        release the resource, prepare for the next question
        
        """