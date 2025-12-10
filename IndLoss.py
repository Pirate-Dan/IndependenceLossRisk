#import key libraries
import pandas as pd
import datetime as dt
import math
import numpy as np


#set essential formatting code
dateformat = "%m/%d/%Y"

#create a dataframe of each service variety, intensity level and risk factor modifier
#create lists
ServType = ["None","Equipment","Day Support","Direct Payment","Homecare: Low","Homecare: Mid","Homecare: High"]
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

#create dataframe of key setting info
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

    Attributes:
        PersonId: A unique identifier for the person requiring a rag
        ContactDate: The date the contact was completed
        BirthDate: The individuals date of birth
        Status: The current setting of the person (Transition,Community,Hospital Discharge,Existing Service)
        CurrentServ: The service being reviewed.  If new to ASC, select 'None'
        NewServ: The service being recommended as a result of the review/assessment
        AgeFac: Calculated risk modifer based on age at contact. Default is 1. Overwirtten by update_AgeFac
        ServFac: Calculated risk modifier based on recommended service. Default is 1. Overwritten by update_ServFac
        ServChange: Calculated risk modifier based on the service chnage post review/assessment. Default is 1. Overwritten by update_ServChange
        StatusFac: Calculated risk modifier based on current setting. Default is 1. Overwritten by update_StatusFac
        Rag: Calculated Rag score based on AgeFac, ServFac, ServChange and StatusFac. Default is 1. Overwritten by update_Rag

     Methods:
        update_AgeFac() - allows the default AgeFac created at initiation to be replaced with a calculated version
        update_ServFac() - allows the default ServFac created at initiation to be replaced with a calculated version
        update_ServChange() - allows the default ServChange created at initiation to be replaced with a calculated version
        update_StatusFac() - allows the default StatusFac created at initiation to be replaced with a calculated version
        update_Rag() - Replaces the default RAG with one calculated from the risk factors

    Error handling:
        Entry of incorrect data types will generate a different value error depending on where the error is
    """  
    #add validation lists for service type and status
    SERV_TYPES = ServType
    STATUS_TYPES = StatusRoute

    #create initialisation method to include key details at initialisation
    def __init__(self,PersonId,ContactDate,BirthDate,Status,CurrentServ,NewServ,AgeFac=1,ServFac=1,ServChange=1,StatusFac=1,Rag=1):
        """
        Docstring for __init__
        
        :param self: Defines instance of class
        :param PersonId: A unique identifier for the person requiring a rag
        :param ContactDate: The date the contact was completed
        :param BirthDate: The individuals date of birth
        :param Status: The current setting of the person (Transition,Community,Hospital Discharge,Existing Service)
        :param CurrentServ: The service being reviewed.  If new to ASC, select 'None'
        :param NewServ: The service being recommended as a result of the review/assessment
        :param AgeFac: Calculated risk modifer based on age at contact. Default is 1. Overwirtten by update_AgeFac
        :param ServFac: Calculated risk modifier based on recommended service. Default is 1. Overwritten by update_ServFac
        :param ServChange: Calculated risk modifier based on the service chnage post review/assessment. Default is 1. Overwritten by update_ServChange
        :param StatusFac: Calculated risk modifier based on current setting. Default is 1. Overwritten by update_StatusFac
        :param Rag: Calculated Rag score based on AgeFac, ServFac, ServChange and StatusFac. Default is 1. Overwritten by update_Rag

        Data validation applies to parameters
        """
        if len(PersonId)>0:
            self.PersonId = PersonId
        else:
            raise ValueError("Please enter a person ID")
        try:
            self.ContactDate = pd.to_datetime(ContactDate,dayfirst=True)
        except:
            raise ValueError("Contact Date is not valid")
        try:
            self.BirthDate = pd.to_datetime(BirthDate,dayfirst=True)
        except:
            raise ValueError("Birth Date is not a valid date")
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
        self.ServChange = ServChange
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
        """
        This method updates the StatusFac parameter of an existing AssessRev instance
        No additional attributes required
        """
        StatusMod = StatusInfo.at[self.Status,"Modifier"]
        self.StatusFac = StatusMod

    #add function to recalculate RAG based on risk factors
    def update_Rag(self):
        """
        This method calculates the RAG based on risk factors of an existing AssessRev instance
        No additional attributes required
        """
        newRag = float(self.Rag)*float(self.ServFac)*float(self.AgeFac)*float(self.ServChange)*float(self.StatusFac)
        self.Rag = newRag
    
    #add class methods to provide details of valid Service and Status types
    @classmethod
    def get_SERV_TYPES(cls):
        """
        Returns a list of acceptable service types for the AssessRev class parameters CurrServ and NewServ
        """
        return cls.SERV_TYPES
    
    @classmethod
    def get_STATUS_TYPES(cls):
        """
        Returns a list of acceptable settings for AssessRev parameter Status
        """
        return cls.STATUS_TYPES
    
    pass
