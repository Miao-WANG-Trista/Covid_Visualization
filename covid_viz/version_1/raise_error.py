"""to define customized error messages"""

import datetime

class DateError_total(Exception):
    """ Verify whether the input fits into data range
    
    Attributes:
    redefined passed method __init__ from parent class Exception by setting a default value for 'message' attribute'
    """
    def __init__(self,start_date,message='Date entered is earlier than provided, 2020/03/20'):
        self.start_date = start_date
        self.message = message
        super().__init__(self.message) # __init__ method inherited from parent class 'Exception' 



def invalid_input(start_date):
    """Verify if the data value users input is in correct format
    
    :param start_date: a string entered by users, retrieved by input() function
    :raises ValueError if the format doesn't coincide
    """
    try:
        datetime.datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")



class out_of_range_error(ValueError):
    pass
