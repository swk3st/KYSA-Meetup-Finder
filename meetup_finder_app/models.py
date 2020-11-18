from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

class AppUser(models.Model):
    id = models.IntegerField(primary_key=True)
    django_user = models.OneToOneField(User,on_delete=models.CASCADE)
    friends = models.ManyToManyField("self")
    def __str__(self):
        return str(self.id)


class Event(models.Model):
    event_date = models.DateTimeField('event date')
    # need to add event name field sometime soon
    event_description = models.CharField(max_length=200)
    event_organizer = models.CharField(max_length=200)
    event_location = models.CharField(max_length=200)
    event_name = models.CharField(max_length=200)
    lat = models.FloatField(default=38.036411)
    lng = models.FloatField(default=-78.502455)

    interested_users = models.ManyToManyField(User)

    def __str__(self):
        return self.event_description
    def coming_up(self):
        now = timezone.now()
        # maybe update this to refine including evnts that are ongoing (like a few hours past instead of a day)
        return now + datetime.timedelta(days=7) >= self.event_date >= (now - datetime.timedelta(days=1))

    def all_users(self):
        return self.interested_users.all()

    coming_up.admin_order_field = 'event_date'
    coming_up.boolean = True
    coming_up.short_description = 'Coming up soon?'

