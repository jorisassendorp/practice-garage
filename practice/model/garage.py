from google.appengine.ext import ndb
from google.appengine.api import memcache
from practice.system.base.model import BaseModel


class Garage(BaseModel):

    name = ndb.StringProperty(required=True)
    brand = ndb.StringProperty()

    postal_country = ndb.StringProperty()

    note = ndb.TextProperty(indexed=False)

#     @classmethod
#     def get(cls, key):
#         return ndb.Key("Garage", int(key)).get()

    @classmethod
    def list(cls, name=None, brand=None, limit=20):
        if not name and not brand:
            """ example with caching
            """
            garages = memcache.get("garages")
            if not garages:
                q = Garage.query()
                garages = [x for x in q]
                memcache.set("garages", garages)
            if limit and len(garages) > limit:
                return garages[:limit]
            return garages
        
        """ example normal query with filter
        """
        q = Garage.query()
        if name:
            q.filter(Garage.name == name)
        elif brand:
            q.filter(Garage.brand == brand)
        if limit:
            return q.fetch(limit)
        return [x for x in q]

    def fill(self, props):
        if 'name' in props:
            self.name = props['name']
        if 'brand' in props:
            self.brand = props['brand']
        if 'note' in props:
            self.note = props['note']

    def save(self):
        self.put()
        # i changed a garage so cache list incorrect
        memcache.delete("garages")

    @classmethod
    def add(cls, props):
        g = Garage()
        g.fill(props=props)
        g.save()
        # adding garage changes list but handled in the save

    def delete(self):
        self.key.delete()
        # i removed a garages so cache list incorrect
        memcache.delete("garages")
