from practice.handlers import BasicHandler
from practice.model.garage import Garage


class HomePage(BasicHandler):
    """ Handler for Garage
    
        Supports up to 3 parameters
        key = always a garage id
        topic = what you want to do
        ident = Can be id of another class as child from Garage
    """
    
    def get(self):
        garages = Garage.query()
        self.render_response("/home.html", garages=garages)
