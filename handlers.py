# -*- coding: utf-8 -*-
import datetime
import webapp2
from webapp2_extras import jinja2
from google.appengine.ext import db
from google.appengine.api import users
import geo.geomodel

from twilio.rest import TwilioRestClient
from twilio import twiml

import json

TWILIO_ACCOUNT_SID = "AC944b22c32e5665d6d2744b131689e964"
TWILIO_AUTH_TOKEN = "df78e3cc5ff61c383d8fe6dbbd0c9b0c"

VENMO_TOKEN = "R8dB25eSKth27w3UFSXNM9shXuxyBp2e"

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
    name = db.StringProperty()
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

class Payment(db.Model):
    payment_id = db.StringProperty()
    payment_amount = db.FloatProperty()
    pending = db.BooleanProperty()


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
                        address=user_address,
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
        else: #user is logged into google+ but doesnt have an account yet
            self.redirect('/register')
        
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
                            phone_number=db.PhoneNumber(business_phone),
                            location=db.GeoPt(30, -140)
                           )
        business.put()
                            
        #done adding user to database so send them to the correct main page
        self.redirect('/business')

    def feedme(self):
        user = users.get_current_user()
        if not user: 
            self.redirect('/')

        #if you are a business and try to go to /feedme        
        val = db.GqlQuery("SELECT * FROM Users " +
                "WHERE email = :1", user.email())
        val_results = val.get()       
        if val_results:
            if val_results.is_business:
                self.redirect('/business') 
        else: #user is logged into google+ but doesnt have an account yet
            self.redirect('/register')

        cust = db.GqlQuery("SELECT * FROM Customers " +
                "WHERE user_id = :1", user.user_id())
        customer = cust.get()       

        if not customer:
            self.redirect('/register')

        context = {
            'user_name' : customer.name,
            'user_address' : customer.address,
            'user_phone' : customer.phone_number
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
        else: #user is logged into google+ but doesnt have an account yet
            self.redirect('/register')

        bus = db.GqlQuery("SELECT * FROM Business " +
                "WHERE user_id = :1", user.user_id())
        business = bus.get()       

        if not business:
            self.redirect('/register')

        context = {
            'business_name' : business.name,
            'business_address' : business.address,
            'business_phone' : business.phone_number
        }               
                
        return self.render_template('business.html', context)
    
    def populate(self):
        context = {}
        bus = Business(location=db.GeoPt(39.95, -75.17),
                        name="Pat's King of Steaks",
                        address="1237 E Passyunk Ave, Philadelphia, PA 19147",
                        boo=0,
                        user_id="32023",
                        phone_number=db.PhoneNumber("+12154681546")
                        )
        bus.update_location()
        bus.put()
        
        #menu = Menu(user_id="32023",
        #            dish_name="Philly CheeseSteak",
        #            price=6.34,
        #            photo_link="http://www3.gazette.com/bots/sites/default/files/m3rmh6-m3rmgwphillycheesesteaksandwich.jpg",
        #            restriction_list=["Meat", "Dairy"]
        #                )
        #menu.put()
        return self.render_string('loaded the business data', context)

    def locate(self):
        context = {}

        pt = db.GeoPt(self.request.get("lat"), self.request.get("long"))
        
        print(self.request.get("lat"));
        print(self.request.get("long"));
        print(pt);

        result = Business.proximity_fetch(
                        Business.all().filter("boo =", 0),
                        pt,
                        max_results = 5,
                        max_distance = 160934);
        
        if len(result) != 0 :
            q = db.GqlQuery("SELECT * FROM Menu " +
                            "WHERE user_id = '" + result[0].user_id + "'");
        
            image_value = ""
            dish_name = ""
            price = 0
            for p in q.run(limit=1):
                image_value = p["photo_link"]
                dish_name = p["dish_name"]
                price = p["price"]

            obj = {
                'business' : result[0].name,
                'image_name' : image_value,
                'dish_name' : dish_name,
                'price' : price
            }
            self.response.out.write(json.dumps(obj))
        else:
            self.response.out.write(json.dumps({}))
        
    def pay(self):
        context = {}

        return self.render_string("testing", context);

    def contact(self):
        context = {}
        #message = twilio_client.sms.messages.create(to="+17138540345", 
         #       from_= "+13474721941", body="Herro Prease");
        call = twilio_client.calls.create(to="+17138540345", 
                from_= "+13474721941", 
                url="http://food-roulette.appspot.com/orderML");
        # issue here with a problematic url.

    def orderML(self):
        resp = twiml.Response()
        resp.say("how is everything going?")
        self.response.out.write(resp)

    def chargepayment(self):
        context = {}
        email = self.request.get("email");
        note = self.request.get("note");
        amount = -0.01                   # initial amount fixed
        payment_id = self.request.get("payment_id")
        # now we need to make the venmo api call.
        # charge payment to user.
        
        payment = Payment(payment_amount=amount,
                        payment_id=payment_id,
                        pending=True
                       )
        payment.put()

        return self.render_string("payment made", context)

    # function to make payment to business after authentication
    def webhook(self):
        context = {}
        data = self.request.get("data")
        payment_id = data["id"]
        payment_status = data["status"]

        if status == "settled":
            # then settled.
            q = db.GqlQuery("SELECT * FROM Payment " +
                            "WHERE payment_id = " + payment_id)
            for p in q.run(limit=1):
                    vals = {"access_token" : VENMO_TOKEN, 
                                   "email" : "csjhin@gmail.com",
                                    "note" : "FoodRoulette",
                                  "amount" : 0.01}
                    requests.post("https://api.venmo.com/payments", vals)
        return self.render_string("request for payment processed", context)


