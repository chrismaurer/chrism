__author__ = 'cmaurer'

# Add CaptainTestSuite and OrderContext to the items imported from tt.captain
from tt.captain import scenario, CaptainTestSuite, OrderContext
from tt.captain.lib import *      # import the entire Captain standard library

@scenario
def my_first_scenario():
    # These Actions comes from tt.captain.lib
    Root()
    with GenerateConfigFiles():
        LoadLbmConfig()

    CreateRiskOrderSender(1, 7)
    SendNewOrderSingle()


# User defined test suite class that subclasses CaptainTestSuite
class TestTutorial(CaptainTestSuite):

    def context(self):
        return OrderContext()

    def create_test(self):
        my_first_scenario()
