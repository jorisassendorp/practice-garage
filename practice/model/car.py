from google.appengine.ext import ndb
from practice.model.garage import Garage
from google.appengine.api import memcache
from practice.system.base.model import BaseModel
import datetime


class Car(BaseModel):

    name = ndb.StringProperty(required=True)
    brand = ndb.StringProperty()
    garage = ndb.KeyProperty()
    doors = ndb.IntegerProperty(default=5)
    buildyear = ndb.DateProperty()
    
    
    @classmethod
    def list(cls, name=None, brand=None, garage=None, limit=20):
        q = Car.query()
        if not name and not brand:
            cars = [x for x in q]
            if limit and len(cars) > limit:
                return cars[:limit]
            return cars
        
        if name:
            q = q.filter(Car.name == name)
        if brand:
            q = q.filter(Car.brand == brand)
        if garage:
            q = q.filter(Car.garage == garage)
        if limit:
            return q.fetch(limit)
        return [x for x in q]

    def fill(self, props):
        if 'name' in props:
            self.name = props['name']
        if 'brand' in props:
            self.brand = props['brand']
        if 'garage' in props:
            self.garage = Garage.get(props['garage']).key()
        if 'doors' in props:
            self.doors = int(props['doors'])
        if 'buildyear' in props:
            self.buildyear = datetime.datetime.strptime(props['buildyear'],'%d-%m-%Y')

    def save(self):
        self.put()

    @classmethod
    def add(cls, props):
        c = Car()
        c.fill(props=props)
        c.save()

    def delete(self):
        self.key.delete()