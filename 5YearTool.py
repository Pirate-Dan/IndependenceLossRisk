#import key libraries
import pandas as pd
import tkinter as tk
import datetime as dt
dateformat = "%m/%d/%Y"
#Create a new class for individual information
class AssessRev:
    """This contains details of individuals at the point of a review or assessment that underpin the creation of a non-independent care risk rating
    Methods:
        update_AgeFac()
        update_ServFac()
        update_ServChange()
        update_RAG()
    Attributes:
        PersonId - This is the unique identification number for the person recieving the assessment or review. Required to be an integer
        ContactDate - The date that the review or assessment was completed
        BirthDate - The person recieving the reviews date of birth
        CurrentServ - This is the service currently in place; defined list of options
        NewServ - This is the service that will be in place following the review; defined list, shared with CurrentServ
        AgeFac - The risk modification factor associated with the persons age band.  Default = 1
        ServFac - The risk modification factor associated with the service type in NewServ. Default = 1
        ServChange - The risk modification factor associated with the direction of chnage between CurrentServ and NewServ.  Default = 1
        RAG - The combined risk score of the person entering non-independent care within the next 12 months, Default = 1
    """
    #create initialisation method to include key details at initialisation
    def __init__(self,PersonId,ContactDate,BirthDate,CurrentServ,NewServ,AgeFac=1,ServFac=1,ServChange=1,RAG=1):
        self.PersonId = PersonId
        self.ContactDate = pd.to_datetime(ContactDate,dayfirst=True)
        self.BirthDate = pd.to_datetime(BirthDate,dayfirst=True)
        self.CurrentServ = CurrentServ
        self.NewServ = NewServ
        self.AgeFac = AgeFac
        self.ServFac = ServFac
        self.ServChange=ServChange
        self.RAG = RAG

    #create method to update AgeFac
    def update_AgeFac(self,AgeFacNew):
        """This method allows the replacement of the existing AgeFac of an AssessRev instance with a new value"""
        self.AgeFac = AgeFacNew
    
    #create method to update ServFac
    def update_ServFac(self,ServFacNew):
        """This method allows the replacement of the existing ServFac of an AssessRev instance with a new value"""
        self.ServFac = ServFacNew

    #create method to update ServChange
    def update_ServChange(self,ServChangeNew):
        """This method allows the replacement of the existing ServChange of an AssessRev instance with a new value"""
        self.ServChange = ServChangeNew

    #create method to update RAG
    def update_RAG(self,RagNew):
        """This method allows the replacement of the existing RAG of an AssessRev instance with a new value"""
        self.RAG=RagNew
      
    pass
assess1 = AssessRev("789231","21/05/2025","13/07/1935","Homecare:Low","Homecare:Mid")
#assess1.update_AgeFac(1.5)
print(assess1.AgeFac)



