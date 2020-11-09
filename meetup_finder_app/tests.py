from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

from django.utils import timezone
from django.urls import reverse
from .models import Event
import datetime

def create_event(organizer, desctiption, location, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Event.objects.create(event_organizer=organizer, event_desctiption=description, event_location=loaction, event_date = time)

class EventModelTests(TestCase):

    def test_coming_up_one_day_until(self):
        """
        coming_up returns true for an event one day in the future
        """
        time = timezone.now() + datetime.timedelta(days=1)
        tomorrow_event = Event(event_date=time)
        self.assertIs(tomorrow_event.coming_up(), True)

    def test_coming_up_two_days_past(self):
        """
        coming_up() returns false for event whose event_date
        is more than 2 days ago.
        """
        time = timezone.now() + datetime.timedelta(days=-2)
        tomorrow_event = Event(event_date=time)
        self.assertIs(tomorrow_event.coming_up(), False)

    def test_coming_up_seven_days_until(self):
        """
        coming_up() returns false for event whose event_date
        is more than 7 days in the future.
        """
        time = timezone.now() + datetime.timedelta(days=10)
        event = Event(event_date=time)
        self.assertIs(event.coming_up(), False)