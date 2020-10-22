from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone


class Event(models.Model):
    event_date = models.DateTimeField('event date')
    event_description = models.CharField(max_length=200)
    event_organizer = models.CharField(max_length=200)
    event_location = models.CharField(max_length=200)