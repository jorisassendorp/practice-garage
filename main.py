import webapp2
from practice.handlers.garages import Garages
from practice.handlers.home import HomePage


class MainPage(webapp2.RequestHandler):

    def get(self):
#         self.response.headers['Content-Type'] = 'text/plain'
#         self.response.out.write('Hello, webapp World!')
        self.redirect('/home')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/home', HomePage),

    ('/garage', Garages),
    ('/garage/(.*)', Garages)
    ], debug=True)
