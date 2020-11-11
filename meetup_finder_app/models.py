from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from allauth.account.forms import LoginForm
class MyCustomLoginForm(LoginForm):

    def login(self, *args, **kwargs):

        # Add your own processing here.

        # You must return the original result.
        return super(MyCustomLoginForm, self).login(*args, **kwargs)

class Event(models.Model):
    event_date = models.DateTimeField('event date')
    # need to add event name field sometime soon
    event_description = models.CharField(max_length=200)
    event_organizer = models.CharField(max_length=200)
    event_location = models.CharField(max_length=200)
    event_name = models.CharField(max_length=200)
    lat = models.FloatField(default=38.036411)
    lng = models.FloatField(default=-78.502455)
    def __str__(self):
        return self.event_description
    def coming_up(self):
        now = timezone.now()
        # maybe update this to refine including evnts that are ongoing (like a few hours past instead of a day)
        return now + datetime.timedelta(days=7) >= self.event_date >= (now - datetime.timedelta(days=1))
    coming_up.admin_order_field = 'event_date'
    coming_up.boolean = True
    coming_up.short_description = 'Coming up soon?'

