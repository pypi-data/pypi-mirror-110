'''Example on how code can be distributed in multiple files
Function and object put here need second import (import implement_pypi_example.example_file)
to used'''
import numpy #remember to add package requirement in setup file if you use
#external packages like this, so that it will check and install those packages
#if needed
import random #built-in package like random shall not be added to package requirment
def no_function():
    return random.choice([True, False])
class nothing:
    def __init__(self):
        None
    def nothing_to_show(self):
        return random.choice([True,False,None])