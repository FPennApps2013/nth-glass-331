# -*- coding: utf-8 -*-
import datetime
import webapp2
from webapp2_extras import jinja2
from google.appengine.ext import db
from google.appengine.api import users

# data model
class Business(db.Model):
    address = db.StringProperty(required=True)
    location = db.GeoPtProperty(required=True)
    menu = db.StringListProperty(required=True)

class Customers(db.Model):
    user_id = db.UserProperty()
    restrictions = db.StringListProperty()

class Users(db.Model):
    user_id = db.UserProperty()
    is_business = db.BooleanProperty()
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



