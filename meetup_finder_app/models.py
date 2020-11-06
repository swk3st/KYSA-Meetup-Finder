from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Event(models.Model):
    event_date = models.DateTimeField('event date')
    # need to add event name field sometime soon
    event_description = models.CharField(max_length=200)
    event_organizer = models.CharField(max_length=200)
    event_location = models.CharField(max_length=200)
    event_name = models.CharField(max_length=200)
    def __str__(self):
        return self.event_description
    def coming_up(self):
        now = timezone.now()
        # maybe update this to refine including evnts that are ongoing (like a few hours past instead of a day)
        return now + datetime.timedelta(days=7) >= self.event_date >= (now - datetime.timedelta(days=1))
    coming_up.admin_order_field = 'event_date'
    coming_up.boolean = True
    coming_up.short_description = 'Coming up soon?'


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200, null = True)
    phone = models.CharField(max_length = 200, null = True)
    email = models.CharField(max_length = 200, null = True)
    date_create = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
            return self.name 