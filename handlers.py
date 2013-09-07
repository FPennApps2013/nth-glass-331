# -*- coding: utf-8 -*-
import datetime
import webapp2
from webapp2_extras import jinja2
from google.appengine.ext import db
from google.appengine.api import users
import geo.geomodel

# data model
class Business(geo.geomodel.GeoModel):
    address = db.StringProperty(required=True)
    menu = db.StringListProperty(required=True)
    name = db.StringProperty(required=True)

class Customers(db.Model):
    user_id = db.UserProperty()
    restrictions = db.StringListProperty()

class Users(db.Model):
    user_id = db.UserProperty()
    is_business = db.BooleanProperty()

class Menu(db.Model):
    restriction_list = db.StringListProperty()

class Restrictions(db.Model):
    restriction_id = db.StringProperty();

# end data model

class BaseHandler(webapp2.RequestHandler):
    """
        BaseHandler for all requests all other handlers will
        extend this handler

    """
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(self, template_name, template_values):
        self.response.write(self.jinja2.render_template(
            template_name, **template_values))

    def render_string(self, template_string, template_values):
        self.response.write(self.jinja2.environment.from_string(
            template_string).render(**template_values))


class PageHandler(BaseHandler):
    def root(self):
        now = datetime.datetime.now()
        ten_min_ago = now - datetime.timedelta(minutes=10)
        context = {
            'now': now,
            'ten_min_ago': ten_min_ago
        }
        return self.render_template('login.html', context)

    def register(self):
        context = {
            'now': datetime.datetime.now(),
        }
        return self.render_string('register', context)

    def feedme(self):
        context = {
            'now': datetime.datetime.now(),
        }
        return self.render_string('feedme', context)

    def business(self):
        context = {
            'now': datetime.datetime.now(),
        }
        return self.render_string('business', context)
    
    def populate(self):
        context = {}
        add = "test address"
        menu = ['fish', 'tacos', 'pizza']
        location = db.GeoPt(30, -140)
        
        bus = Business(address=add, 
                        menu=menu,
                        location=db.GeoPt(30, -140),
                        name="Test Restaurant")
        bus.location = location
        bus.update_location()
        bus.put()
        return self.render_string('loaded the business data', context)

    def locate(self):
        context = {}
        result = Business.proximity_fetch(
                        Business.all(),
                        geo.geotypes.Point(30, -140),
                        max_results = 5,
                        max_distance = 160934);

        rendering = result[0].address;
        return self.render_string(rendering, context); 

