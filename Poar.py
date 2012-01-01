##  Sebastian Perez Vasseur 2012
##  This is a WSGI app that provides a RESTful interface for your CRUD apps


Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

import cgi
import logging
import time
import datetime

from urlparse import urlparse
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from django.utils import simplejson

class DictModel(db.Model):
    def to_dict(self):
        temp = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
        temp["id"] = unicode(self.key().id())
        return temp

class Store(DictModel):
	name = db.StringProperty()
        content = db.TextProperty()
        typeo = db.StringProperty()
	date = db.DateTimeProperty()
	owner = db.UserProperty()

class login(webapp.RequestHandler):
	def get(self):
		self.redirect(users.create_login_url("/"))

class logout(webapp.RequestHandler):
	def get(self):
		self.redirect(users.create_logout_url("/"))
			
class listcreate(webapp.RequestHandler):
	def get(self,resource):
		user = users.get_current_user()
                if user:
                      	data = db.GqlQuery("SELECT * FROM Store WHERE owner=:1 AND typeo=:2",user,resource)
		    	self.response.headers['Content-Type'] = 'text/plain'
		    	self.response.out.write(simplejson.dumps([p.to_dict() for p in data]))
		else:
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write('Please Login')

	def post(self,resource):
		user = users.get_current_user()
        	if user:
			name = cgi.escape(self.request.get('name'))
			content = cgi.escape(self.request.get('content'))
			typeo = resource
			data = Store()
	
			data.name = name
			data.owner = user
			data.content = content
                        data.typeo = typeo
			data.date = datetime.datetime.now()
			data.put()

			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write(data.key().id())
        	else:
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write('Please Login')

class checkdeleteupdate(webapp.RequestHandler):
        def get(self,resource,ids):
		user = users.get_current_user()
                if user:
                      	data = Store.get_by_id(int(ids))
		    	self.response.headers['Content-Type'] = 'text/plain'
		    	if data:
				self.response.out.write(simplejson.dumps(data.to_dict()))
			else:
				self.response.out.write("[]")
		else:
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write('Please Login')

	def post(self,resource,ids):
		user = users.get_current_user()
        	if user:
			data = Store.get_by_id(int(ids))
			
			name = cgi.escape(self.request.get('name'))
			content = cgi.escape(self.request.get('content'))
                        logging.info(content)
			typeo = resource

			data.name = name
			data.owner = user
			data.content = content
                        data.typeo = typeo
			data.date = datetime.datetime.now()

			data.put()

			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write(data.key().id())
        	else:
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write('Please Login')

	def delete(self,resource,ids):
		user = users.get_current_user()
        	if user:
			data = Store.get_by_id(int(ids))
			data.delete()

			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write("Deleted")
        	else:
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write('Please Login')	
		
class main(webapp.RequestHandler):		
	def get(self):
		user = users.get_current_user()
                if user:
                      	data = db.GqlQuery("SELECT * FROM Store WHERE owner=:1",user)
		    	self.response.headers['Content-Type'] = 'text/plain'
		    	self.response.out.write(simplejson.dumps([p.to_dict() for p in data]))
		else:
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write('Please Login')

class test(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			data = Store()
			data.typeo = "testt"
			data.name = "testing"
			data.content = "[]"
			data.owner = user
			data.put()
			self.response.out.write('Added')
	

application = webapp.WSGIApplication([('/data', main),('/data/(.*)/(.*)', checkdeleteupdate),('/data/(.*)', listcreate)])

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
