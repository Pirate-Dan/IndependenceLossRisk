#import key libraries
import pandas as pd
import tkinter as tk
import datetime as dt
import math
import numpy as np

#set essential formatting code
dateformat = "%m/%d/%Y"
#create array to store instances of AssessRev
Contact_Array = np.array(["Person_ID","BirthDate","ContactDate","CurrentServ","NewServ","RAG"])
#create a dataframe of each service variety, intensity level and risk factor modifier
#create lists
ServType = ["Equipment","Day Support","Direct Payment","Homecare:Low","Homecare:Mid","Homecare:High"]
ServIntens = [1,2,3,4,5,6]
ServModify = [0.6,0.8,1,1.1,1.3,1.5]
Header = ["Service","Intensity","RiskModifier"]
#combine lists to array
ServInfo = np.array((ServType))
ServInfo=ServInfo.reshape(6,1)
ServInfo = np.hstack((ServInfo,np.array((ServIntens)).reshape(6,1),np.array((ServModify)).reshape(6,1)))
#convert array to dataframe
ServInfo = pd.DataFrame(ServInfo,columns = Header)
ServInfo = ServInfo.set_index("Service")

#Create a new class for individual information
class AssessRev:
    """This contains details of individuals at the point of a review or assessment that underpin the creation of a non-independent care risk rating
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
    #add validation list for service types (CurrentServ and NewServ)
    ServType = ServType
    
    #create initialisation method to include key details at initialisation
    def __init__(self,PersonId,ContactDate,BirthDate,CurrentServ,NewServ,AgeFac=1,ServFac=1,ServChange=1,Rag=1):
        self.PersonId = PersonId
        self.ContactDate = pd.to_datetime(ContactDate,dayfirst=True)
        self.BirthDate = pd.to_datetime(BirthDate,dayfirst=True)
        self.CurrentServ = CurrentServ
        self.NewServ = NewServ
        self.AgeFac = AgeFac
        self.ServFac = ServFac
        self.ServChange=ServChange
        self.Rag = Rag

    #create method to update AgeFac
    def update_AgeFac(self):
        """This method allows the replacement of the default AgeFac with a calculated value based on ageband"""
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
        """This method allows the replacement of the existing ServFac of an AssessRev instance with a new value"""
        newServFac = ServInfo.at[self.NewServ,"RiskModifier"]
        self.ServFac = newServFac

    #create method to update ServChange
    def update_ServChange(self,ServChangeNew):
        """This method allows the replacement of the existing ServChange of an AssessRev instance with a new value"""
        self.ServChange = ServChangeNew

    #create method to update RAG
    def update_Rag(self,RagNew):
        """This method allows the replacement of the existing RAG of an AssessRev instance with a new value"""
        self.Rag=RagNew
      
    pass

assess1 = AssessRev("789231","21/05/2025","13/07/1935","Homecare:Low","Homecare:Mid")

currVal = ServInfo.at[assess1.CurrentServ,"Intensity"]
newVal = ServInfo.at[assess1.NewServ,"Intensity"]
if currVal>newVal:
    changeFac = 0.5
elif currVal<newVal:
    changeFac = 1.5
else:
    changeFac = 1

print(changeFac)
#assess1.update_ServFac()
#print(assess1.ServFac)

#### remove code below here (testing area)
#assess1.update_AgeFac(1.5)
#print(assess1.AgeFac)

# create function to recalculate and replace the AgeFac of a AssessRev Instance
#def calc_AgeFactor(ID):
  #  dob = pd.to_datetime(ID.BirthDate)
 #   doc = pd.to_datetime(ID.ContactDate)
 #   AgeCalc =  (doc-dob).days
  #  AgeCalc = math.floor(AgeCalc/365)
  #  if AgeCalc >85:
   #     AgeCalc = 1.5
  ##  elif AgeCalc >75:
   #     AgeCalc = 1.2
   # else:
  #      AgeCalc = 1
   # ID.update_AgeFac(AgeCalc)

#calc_AgeFactor(assess1)
#print(assess1.AgeFac)
#assess1.update_AgeFac()
#print(assess1.AgeFac)


#arr1 = np.array(["Person_ID","BirthDate","ContactDate","CurrentServ","NewServ","RAG"])
#list = ["yes","No","Why","Contact","in","Shoes"]
#arr2=np.array(list)
#arr3 = np.stack((arr1,arr2))
#df = pd.DataFrame(arr3)
#arr3 = np.vstack((arr3,arr2))
#arr4 = np.vstack((Contact_Array,arr2))

#new = create_Contact(assess1)

#create a matrix to store service information (ServFac,Intensity Score)