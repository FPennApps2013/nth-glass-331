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
    boo = db.IntegerProperty()

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
        user = users.get_current_user()
        if user:
            self.redirect('/authenticate')
        context = {
            'login_url': users.create_login_url(self.request.uri),
        }
        return self.render_template('login.html', context)

    def authenticate(self):
        user = users.get_current_user()
        if not user: 
            self.redirect('/')
        
        #check if google plus user is in database 
        #to get user datapoints should be user.nickname() user.user_id() user.email()

        # we need back 
            # bool in_database
            # bool customer (false if business)

        if in_database:
            if customer:
                self.redirect('/feedme')
            else:
                self.redirect('/business') 
        else: #if not in database, send to register
            self.redirect('/register')

    def register(self):
        user = users.get_current_user()
        if not user: 
            self.redirect('/')

        #add the user to the database using the same user datapoints
        #user.nickname() user.user_id() user.email()

        context = {
        }
        return self.render_string('register', context)

    def feedme(self):
        user = users.get_current_user()
        if not user: 
            self.redirect('/')
        context = {
        }
        return self.render_string('feedme', context)

    def business(self):
        user = users.get_current_user()
        if not user: 
            self.redirect('/')
        context = {
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
                        name="Test Restaurant",
                        boo=0)
        bus.location = location
        bus.update_location()
        bus.put()
        return self.render_string('loaded the business data', context)

    def locate(self):
        context = {}
        result = Business.proximity_fetch(
                        Business.all().filter("boo =", 0),
                        db.GeoPt(30, -140),
                        max_results = 5,
                        max_distance = 160934);

        rendering = result[0].address;
        return self.render_string(rendering, context); 

