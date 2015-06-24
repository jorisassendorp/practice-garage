from testcases.base import BasicTestCase
from practice.model.garage import Garage


""" Very simple example how to use the BasicTestCase
"""
class GarageTestCase(BasicTestCase):
    
    def setUP(self):
        ''' This method can be used to import or set up some data needed for every testcase
            
            no need to call super
        '''
        BasicTestCase.setUP(self)
    
    def test_datastore(self):
        ''' start with test_ to get function started
        '''
        g = Garage()
        g.name = "test2222"
        g.brande = "Volvo"
        g.note = """ Testing note
        for multi line
        hueaah"""
        print str(g.id)
        g.put()
        self.assertEqual(1, Garage.query().count()) # yay success
        
    def test_twee(self):
        g = Garage()
        g.name = "test1"
        g.brande = "Patat"
        g.note = """ Testing note
        for multi line
        hueaah"""
        g.put()
        
        self.assertEqual(2, Garage.query().count(), "No you suck")
        
    def tearDown(self):
        """ tearDown will be called after a testcase
        """
        pass