#import pytest library
import pytest

#import class to test
import IndLoss
from IndLoss import AssessRev,ServType,StatusRoute

assess1 = AssessRev("789231","21/05/2025","13/07/1935","Hospital Discharge","Homecare: Low","Homecare: Mid")

#test that creation of new instance produces the correct defaults for calculated values
def test_ageFacDefault():
    age=assess1.AgeFac
    assert age == 1

def test_ServFacDefault():
    sf = assess1.ServFac
    assert sf==1

def test_servChangeDefault():
    sc=assess1.ServChange
    assert sc==1

def test_StatusFacDeafault():
    stat = assess1.StatusFac
    stat == 1

def test_RagDefault():
    rg = assess1.Rag
    rg==1

#test that each calculated value function produces expected output when converted to float (as per rag calculation)
def test_updateAgeFac():
    assess1.update_AgeFac()
    af_new = float(assess1.AgeFac)
    assert af_new==1.5

def test_updateServFac():
    assess1.update_ServFac()
    sf_new=float(assess1.ServFac)
    assert sf_new==1.3

def test_updateServChange():
    assess1.update_ServChange()
    sc_new=float(assess1.ServChange)
    assert sc_new==1.5

def test_updateStatus():
    assess1.update_StatusFac()
    stat_new=float(assess1.StatusFac)
    assert stat_new==1.5

#test that final rag calculation is correct

def test_updateRag():
    assess1.update_Rag()
    rg_new=assess1.Rag
    assert rg_new==4.3875

#test that incorrect entries in NewServ,CurrentServ and Status fields are handled as expected
def test_NewServValueError():
    with pytest.raises(ValueError):
        AssessRev("789231","21/05/2025","13/07/1935","Hospital Discharge","Homecare: Low","NotInList")



#AgeFac=1,ServFac=1,ServChange=1,StatusFac=1,Rag=1