
import time

class MethodTimer:
    '''Helper class for timing method execution'''
    def __init__(self):
        self.start_time = time.time()
        
    def print_duration(self):
        print("\nThis took %s seconds." % (time.time() - self.start_time))
        print('-' * 40)
        
        
def get_user_input(prompt, allowed_values, name):
    '''
    Prompts a user to input a value
    
    Args:
        (str) prompt - the string value to be displayed as prompt
        (str) allowed_values - list of valid values that a user can enter
        (str) name - the name that represents the type of data
    Returns:
        (str) selected_value - the valid value that the user entered
    '''
    while True:
        selected_value = input("%s\n" % prompt).lower()

        if selected_value not in [value.lower() for value in allowed_values]:
            print("You entered an incorrect value for '%s'!" % name)
        else:
            break
                
    return selected_value