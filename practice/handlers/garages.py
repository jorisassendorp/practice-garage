from practice.handlers import BasicHandler
from practice.model.garage import Garage


class Garages(BasicHandler):
    """ Handler for Garage
    
        Supports up to 3 parameters
        key = always a garage id
        topic = what you want to do
        ident = Can be id of another class as child from Garage
    """
    
    def get(self, key="", topic="", ident=""):
        if not key:
            garages = Garage.query()
            self.render_response("/detail/garage-list.html", garages=garages)
        else:
            garage = Garage.get(key)
            import logging
            logging.warning("Got garage " + garage.name)
            pass