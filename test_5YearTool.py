import pytest
def testrun():
    assert True
#import class to test
import IndLoss
from IndLoss import AssessRev

#test that creation of new instance produces the correct defaults for calculated values
assess1 = AssessRev("789231","21/05/2025","13/07/1935","Hospital Discharge","Homecare:Low","Homecare:Mid")
def initial_test_ageFac():
    val=assess1.AgeFac
    assert val == 1


#test that each calculated value fucntion produces expected output
#test that final rag calculation is correct
#test that incorrect entries in NewServ,CurrentServ and Status fields are handled as expected