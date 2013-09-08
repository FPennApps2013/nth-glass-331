# -*- coding: utf-8 -*-
import datetime
import webapp2
from webapp2_extras import jinja2
from google.appengine.ext import db
from google.appengine.api import users
import geo.geomodel

from twilio.rest import TwilioRestClient
from twilio import twiml


TWILIO_ACCOUNT_SID = "AC944b22c32e5665d6d2744b131689e964"
TWILIO_AUTH_TOKEN = "df78e3cc5ff61c383d8fe6dbbd0c9b0c"

###### set up twilio client ######

twilio_client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)



###### end twilio client #########

# data model
class Business(geo.geomodel.GeoModel):
    user_id = db.StringProperty(required=True)
    address = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    phone_number = db.PhoneNumberProperty()
    boo = db.IntegerProperty()
    open_time = db.TimeProperty()
    close_time = db.TimeProperty()

class Customers(db.Model):
    address = db.StringProperty()
    user_id = db.StringProperty()
    phone_number = db.PhoneNumberProperty()
    restrictions = db.StringListProperty()

class Users(db.Model):
    user_id = db.StringProperty(required=True)
    is_business = db.BooleanProperty()
    email = db.StringProperty()

class Orders(db.Model):
    customer_id = db.StringProperty()
    business_id = db.StringProperty()
    order_time = db.DateProperty()

class Menu(db.Model):
    user_id = db.StringProperty(required=True)
    dish_name = db.StringProperty()
    price = db.FloatProperty()
    photo_link = db.LinkProperty()
    restriction_list = db.StringListProperty()

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
        val = Users.all().filter('email=', user.email()).get();
        
        # print user.email()
        if val:
            if val[0].is_business:
                self.redirect('/business') 
            else:
                self.redirect('/feedme')
        else: #user didn't exist so register
           self.redirect('/register')

    def register(self):
        user = users.get_current_user()
        if not user: 
            self.redirect('/')
        
        val = db.GqlQuery("SELECT * FROM Users " +
                "WHERE email = :1", user.email())
        val_results = val.get()       
        if val_results:
            if val_results.is_business:
                self.redirect('/business') 
            else:
                self.redirect('/feedme')
        
        context = {
            'hide_overflow': 'hide_overflow',
        }
        return self.render_template('register.html', context)

    def adduser(self):
        user = users.get_current_user()
        if not user: 
            self.redirect('/')
        
        val = db.GqlQuery("SELECT * FROM Users " +
                "WHERE email = :1", user.email())
        val_results = val.get()       
        if val_results:
            if val_results.is_business:
                self.redirect('/business') 
            else:
                self.redirect('/feedme')
        
        user_name = self.request.get("name");        
        user_address = self.request.get("address");        
        user_phone = self.request.get("phone");        
        user_dietary = self.request.get("diet", allow_multiple=True);        


        #add the user to the database using the same user datapoints
        new_customer = Customers(
                        user_id=user.user_id(),
                        email=user.email(),
                        name=user_name,
                        phone_number=db.PhoneNumber(user_phone),
                        restrictions=user_dietary
                        );
        new_customer.put()
        new_user = Users(
                        user_id=user.user_id(),
                        email=user.email(),
                        is_business=False
                        );
        new_user.put()
        #done adding user to database so send them to the correct main page
        self.redirect('/feedme')

    def addbusiness(self):
        user = users.get_current_user()
        if not user:
            self.redirect('/')
        
        val = db.GqlQuery("SELECT * FROM Users " +
                "WHERE email = :1", user.email())
        val_results = val.get()       
        if val_results:
            if val_results.is_business:
                self.redirect('/business') 
            else:
                self.redirect('/feedme')
        
        #add the user to the database using the same user datapoints
        entry = Users(user_id=user.user_id(),
                        is_business=True,
                        email=user.email())
        entry.put()
        
        business_name = self.request.get("name");        
        business_address = self.request.get("address");        
        business_phone = self.request.get("phone");
        business = Business(user_id=user.user_id(),
                            address=business_address,
                            name=business_name,
                            phone_number=db.PhoneNumber(business_phone))
        business.put()
                            
        #done adding user to database so send them to the correct main page
        self.redirect('/business')

    def feedme(self):
        user = users.get_current_user()
        if not user: 
            self.redirect('/')
        
        val = db.GqlQuery("SELECT * FROM Users " +
                "WHERE email = :1", user.email())
        val_results = val.get()       
        if val_results:
            if val_results.is_business:
                self.redirect('/business') 
        
        context = {
        }
        return self.render_template('feedme.html', context)

    def business(self):
        user = users.get_current_user()
        if not user: 
            self.redirect('/')
        
        val = db.GqlQuery("SELECT * FROM Users " +
                "WHERE email = :1", user.email())
        val_results = val.get()       
        if val_results:
            if not val_results.is_business:
                self.redirect('/feedme') 
                
                
        context = {
            'gray' : 'gray',
        }
        return self.render_template('restaurant.html', context)
    
    def populate(self):
        context = {}
        add = "yo momma's house"
        menu = ['fish', 'tacos', 'pizza']
        location = db.GeoPt(30, -140)
        
        bus = Business(address=add, 
                        menu=menu,
                        location=db.GeoPt(29, -139),
                        name="Chez Chas",
                        boo=0)
        bus.location = location
        bus.update_location()
        bus.put()
        return self.render_string('loaded the business data', context)

    def locate(self):
        context = {}
        result = Business.proximity_fetch(
                        Business.all().filter("boo =", 0),
                        db.GeoPt(29, -139),
                        max_results = 5,
                        max_distance = 160934);
        rendering = result[0].address;
        return self.render_string(rendering, context);

    def pay(self):
        request










    def contact(self):
        context = {}
        #message = twilio_client.sms.messages.create(to="+17138540345", 
         #       from_= "+13474721941", body="Herro Prease");
        call = twilio_client.calls.create(to="+17138540345", 
                from_= "+13474721941", 
                url="http://localhost:8080/orderML");
        # issue here with a problematic url.
        return self.render_string("helloworld", context)

    def orderML(self):
        context = {}
        resp = twilio.twiml.Response()
        resp.say("how is everything going?")
        return self.render_string(str(resp), context)


