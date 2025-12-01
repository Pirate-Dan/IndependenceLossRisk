#import key libraries
import pandas as pd
import tkinter as tk
import datetime as dt
import math
import numpy as np

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
ServInfo=ServInfo.reshape(7,1)
ServInfo = np.hstack((ServInfo,np.array((ServIntens)).reshape(7,1),np.array((ServModify)).reshape(7,1)))
#convert array to dataframe
ServInfo = pd.DataFrame(ServInfo,columns = Header)
ServInfo = ServInfo.set_index("Service")

#create dataframe of key info
StatusRoute = ["Transition","Community","Hospital Discharge","Existing Service"]
StatusModify = [1.2,1.2,1.5,1]
StatusHeader = ["Entry","Modifier"]
#combine lists to array
StatusInfo = np.array((StatusRoute)).reshape(4,1)
StatusInfo = np.hstack((StatusInfo,np.array((StatusModify)).reshape(4,1)))
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

assess1 = AssessRev("789231","21/05/2025","13/07/1935","Hospital Discharge","Homecare:Low","Homecare:Mid")
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