#Import the libraries and formats
import pandas as pd
from tkinter import Tk,Label,Button
import datetime as dt
import math
import numpy as np

#set essential formatting code
dateformat = "%m/%d/%Y"
#import the class and methods from logic model
#create the class for the TkInter GUI
class InputGUI:
    """
    The GUI that will provide the front end capability to generate a RAG on behalf of the user.

    To provide data entry boxes for the key attibutes (Person ID, Birth Date, Contact Date, current service, new service, status).

    Data entry in these cases will be limited to defined values:
                Current Service - SERV_TYPES
                New Service - SERV_TYPES
                Status - STATUS TYPES

    To also provide a generate RAG button that will produce the risk score for the individual.

    Contact Date and Birth date need to be entered as parsable date formats, or an error message will be generated
       """
    def __init__(self,main):

        #main window with title
        self.main = main
        main.title("Loss of Independence Risk Tool")

        #Instructions box

        #Entry box - Person ID

        #Entry box - Birth date

        #Entry box - Contact Date

        #Entry box - Current Service

        #Entry box - New Service

        #Entry Box - status

        #Output - Age

        #Button - calculate RAG

        #Button - Export RAG

    pass

root=Tk()
my_gui = InputGUI(root)
root.mainloop()