__author__ = 'josh'

class held_errors:

    def __init__(self):
        self.errors_in_string = ''

    def held_errors(self, error_string):
        # hold errors/mis-match info until the end then dump it
        self.errors_in_string += error_string + ('\n')

    def dump_held_errors(self):
        print('\n ----DUMPING ERRORS AND WARNINGS::: ', end='\n')
        print (self.errors_in_string)


        
    
        
    