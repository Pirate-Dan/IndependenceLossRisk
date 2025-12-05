#import key libraries
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk,Tk,Label,Button,Entry,OptionMenu
from tkcalendar import DateEntry
import datetime as dt
import math
import numpy as np
import csv

#set essential formatting code
dateformat = "%m/%d/%Y"

#create a dataframe of each service variety, intensity level and risk factor modifier
#create lists
ServType = ["None","Equipment","Day Support","Direct Payment","Homecare:Low","Homecare:Mid","Homecare:High"]
ServIntens = [1,2,3,4,5,6,7]
ServModify = [0.2,0.6,0.8,1,1.1,1.3,1.5]
Header = ["Service","Intensity","RiskModifier"]
#combine lists to array
ServInfo = np.array((ServType))
servLen = len(ServInfo)
ServInfo=ServInfo.reshape(servLen,1)
ServInfo = np.hstack((ServInfo,np.array((ServIntens)).reshape(servLen,1),np.array((ServModify)).reshape(servLen,1)))
#convert array to dataframe
ServInfo = pd.DataFrame(ServInfo,columns = Header)
ServInfo = ServInfo.set_index("Service")

#create dataframe of key info
StatusRoute = ["Transition","Community","Hospital Discharge","Existing Service"]
StatusModify = [1.2,1.2,1.5,1]
StatusHeader = ["Entry","Modifier"]
#combine lists to array
StatusLen = len(StatusRoute)
StatusInfo = np.array((StatusRoute)).reshape(StatusLen,1)
StatusInfo = np.hstack((StatusInfo,np.array((StatusModify)).reshape(StatusLen,1)))
#convert to dataframe
StatusInfo = pd.DataFrame(StatusInfo,columns = StatusHeader).set_index("Entry")


#Create a new class for entering person info and generating RAG
class AssessRev:
    """
    This contains details of individuals at the point of a review or assessment that underpin the creation of a non-independent care risk rating

    Methods:
        update_AgeFac() - allows the default AgeFac created at initiation to be replaced with a calculated version
        update_ServFac()
        update_ServChange()
        update_Rag()

    Attributes:
        PersonId - This is the unique identification number for the person recieving the assessment or review. Required to be an integer
        ContactDate - The date that the review or assessment was completed
        BirthDate - The person recieving the reviews date of birth
        CurrentServ - This is the service currently in place; defined list of options
        NewServ - This is the service that will be in place following the review; defined list, shared with CurrentServ
        AgeFac - The risk modification factor associated with the persons age band.  Default = 1
        ServFac - The risk modification factor associated with the service type in NewServ. Default = 1
        ServChange - The risk modification factor associated with the direction of chnage between CurrentServ and NewServ.  Default = 1
        Rag - The combined risk score of the person entering non-independent care within the next 12 months, Default = 1
    """  
    #add validation lists for service type and status
    SERV_TYPES = ServType
    STATUS_TYPES = StatusRoute

    #create initialisation method to include key details at initialisation
    def __init__(self,PersonId,ContactDate,BirthDate,Status,CurrentServ,NewServ,AgeFac=1,ServFac=1,ServChange=1,StatusFac=1,Rag=1):
        self.PersonId = PersonId
        self.ContactDate = pd.to_datetime(ContactDate,dayfirst=True)
        self.BirthDate = pd.to_datetime(BirthDate,dayfirst=True)
        if not (Status in AssessRev.STATUS_TYPES):
            raise ValueError(f"{Status} not a valid status.")
        else:
            self.Status = Status
        if not (CurrentServ in AssessRev.SERV_TYPES):
            raise ValueError(f"{CurrentServ} is not a valid service type.")
        else:
            self.CurrentServ = CurrentServ
        if not(NewServ in AssessRev.SERV_TYPES):
            raise ValueError(f"{NewServ} is not a valid service type.")
        else:
            self.NewServ = NewServ
        self.AgeFac = AgeFac
        self.ServFac = ServFac
        self.ServChange=ServChange
        self.StatusFac = StatusFac
        self.Rag = Rag

    #create method to update AgeFac
    def update_AgeFac(self):
        """
        This method allows the replacement of the default AgeFac with a calculated value based on ageband
        No additional attributes are required
        """
        dob = pd.to_datetime(self.BirthDate)
        doc = pd.to_datetime(self.ContactDate)
        ageCalc = (doc-dob).days
        ageCalc = math.floor(ageCalc/365)
        if ageCalc >85:
            newAgeFac = 1.5
        elif ageCalc >75:
            newAgeFac = 1.2
        elif ageCalc >65:
            newAgeFac = 1
        else:
            newAgeFac = 0.8
        self.AgeFac=newAgeFac
    
    #create method to update ServFac
    def update_ServFac(self):
        """
        This method allows the replacement of the existing ServFac of an AssessRev instance with a new value
        No additional attributes are required
        """
        newServFac = ServInfo.at[self.NewServ,"RiskModifier"]
        self.ServFac = newServFac

    #create method to update ServChange
    def update_ServChange(self):
        """
        This method allows the replacement of the existing ServChange of an AssessRev instance with a new value
        No additional attributes are required
        """
        currVal = ServInfo.at[self.CurrentServ,"Intensity"]
        newVal = ServInfo.at[self.NewServ,"Intensity"]
        change = int(newVal)-int(currVal)
        if change > 2:
            changeFac = 2
        elif change > 1:
            changeFac = 1.75
        elif change > 0:
            changeFac = 1.5
        elif change == 0:
            changeFac = 1
        elif change < -2:
            changeFac = 0.25
        elif change < -1:
            changeFac = 0.5
        else:
            changeFac = 0.75
        self.ServChange = changeFac

    #add a new function to update the modification factor associated with entry route
    def update_StatusFac(self):
        StatusMod = StatusInfo.at[self.Status,"Modifier"]
        self.StatusFac = StatusMod

    #add function to recalculate RAG based on risk factors
    def update_Rag(self):
        newRag = float(self.Rag)*float(self.ServFac)*float(self.AgeFac)*float(self.ServChange)*float(self.StatusFac)
        self.Rag = newRag
    
    #add class methods to provide details of valid Service and Status types
    @classmethod
    def get_SERV_TYPES(cls):
        return cls.SERV_TYPES
    
    @classmethod
    def get_STATUS_TYPES(cls):
        return cls.STATUS_TYPES
    
    pass

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

        #commands to extract the relevant data
        def curr_serv():
            txt_curr=cb_curr.get()            
        
        def new_serv():
            txt_new = cb_new.get()

        def status():
            txt_status = cb_status.get()         
        
        def person():
            txt_person = pers_val.get()        

        def birth_date():
            bd = dob.get_date()

        def contact_date():
            cd = con_date.get_date()
        
        def age_calc():
            dob_val = pd.to_datetime(dob.get_date(),dayfirst=True)
            doc_val = pd.to_datetime(con_date.get_date(),dayfirst=True)
            age = (doc_val - dob_val).days
            age = math.floor(age/365)
            lbl_age.config(text = age)
        
        #method to run full RAG calculation
        def rag_calc():
            #create AssessRev instance from data entry
            contactData = [pers_val.get(),con_date.get(),dob.get(),cb_status.get(),cb_curr.get(),cb_new.get()]
            contact=AssessRev(contactData[0],contactData[1],contactData[2],contactData[3],contactData[4],contactData[5])
            #run the core methods from AssessRev class
            contact.update_AgeFac()
            contact.update_StatusFac()
            contact.update_ServFac()
            contact.update_ServChange()
            #run the update RAG method from AssessRev class
            contact.update_Rag()
            if contact.Rag <=1:
                txt_rag = "Green"
            elif contact.Rag >2:
                txt_rag = "Red"
            else:
                txt_rag = "Amber"
            #create confirmation label
            rag_info=(f"Person ID: {contact.PersonId} Contact Date: {contact.ContactDate.strftime("%d/%m/%Y")} Date of Birth: {contact.BirthDate.strftime("%d/%m/%Y")} Status: {contact.Status} Current Service: {contact.CurrentServ} Recommended Service: {contact.NewServ} RAG: {txt_rag}")
            lbl_rag.config(text=txt_rag)
            lbl_facs.config(text=rag_info)
        
        def export_rag():
            e_rag=lbl_facs.cget("text")
            fName=(f"{per_lbl.get()}-{con_date.get_date()}.txt")
            #write to text file
            with open(fName,"w",encoding="utf-8") as f:
                f.write(e_rag)
            with open(fName,"r",encoding="utf-8") as f:
                print(f.read())


            
        #Instructions box


        #Entry box - Person ID
        per_lbl = Label(main, text="Person ID)")
        per_lbl.pack()
        pers_val = tk.StringVar()
        pers_id = Entry(main,textvariable=pers_val,font=('calibre',12,'normal'))
        pers_id.pack()
        
        #Entry box - Birth date
        dob_lbl = Label(main,text="Date of Birth")
        dob_lbl.pack()
        dob = DateEntry(main,width=12,date_pattern = 'dd/mm/yyyy')
        dob.pack()

        #Entry box - Contact Date
        doc_lbl=Label(main, text="Date of Contact")
        doc_lbl.pack()
        con_date = DateEntry(main,width = 12,date_pattern = 'dd/mm/yyyy')
        con_date.pack()

        #Entry box - Current Service
            #create combobox
        cb_curr =ttk.Combobox(main,values=ServType,width=36)
        cb_curr.set("Please the persons current service")
        cb_curr.pack()

        #Entry box - New Service
            #create combobox
        cb_new=ttk.Combobox(main,values=ServType,width=36)
        cb_new.set("Please select the recommended service")
        cb_new.pack()

        #Entry Box - status
        cb_status = ttk.Combobox(main,values=StatusRoute,width=36)
        cb_status.set("Please select the persons current status")
        cb_status.pack()

        #Output - Age
        lbl_age = Label(main,text=" ")
        lbl_age.pack()

        #Button - calculate RAG
        self.Rag_button = Button(main,text="Calculate RAG",command=rag_calc)
        self.Rag_button.pack()

        #label to display calculated rag
        #Button - Export RAG
        self.export_button = Button(main,text="Export RAG",command=export_rag)
        self.export_button.pack()

        #Button - clear data
        self.clear_button = Button(main,text="Clear data")
        self.clear_button.pack()

        lbl_rag = Label(main,text=" ")
        lbl_rag.pack()

        lbl_facs=Label(main,text=" ")
        lbl_facs.pack()

    pass

root=Tk()
my_gui = InputGUI(root)
root.mainloop()


#assess1 = AssessRev("789231","21/05/2025","13/07/1935","Hospital Discharge","Homecare:Low","Homecare:Mid")

#assess1.update_ServChange()
#assess1.update_AgeFac()
#assess1.update_ServFac()
#assess1.update_StatusFac()
#assess1.update_Rag()
#print("Rag:",assess1.Rag,"ServFac:",assess1.ServFac,"ServChange:",assess1.ServChange,"AgeFac:",assess1.AgeFac,"StatusFac:",assess1.StatusFac)
#print(ServInfo)
#services = AssessRev.get_SERV_TYPES()
#print(services)
#print(AssessRev.get_STATUS_TYPES())