from google.appengine.ext import ndb
import logging

class BaseModel(ndb.Model):
    
    @property
    def id(self):
        """
        """
        if self.key:
            return self.key.integer_id()
        logging.error("Model %s instance not stored yet!" % self.__class__.__name__)
        return None
    
    @classmethod
    def get(cls, key, parent=None):
        """
        """
        return cls.get_by_id(int(key), parent)

    def update(self, props):
        """
        """
        self.fill(props=props)
        return self.save()
    
    def save(self):
        """
        """
        self.put()
        return self