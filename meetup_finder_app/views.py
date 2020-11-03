from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404


# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import timezone

from django.urls import reverse
from django.views import generic
from django.views.generic.base import TemplateView
from .models import Event

class HomeView(TemplateView):
    template_name = 'meetup_finder_app/home.html'

def WelcomeView(request):
    template_name = 'meetup_finder_app/welcome.html'
    return render(request, template_name)
class IndexView(generic.ListView):
    template_name = 'meetup_finder_app/index.html'
    #context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Event.objects.filter(event_date__lte=timezone.now()).order_by('-event_date')[:5]


class NewEventView(TemplateView):
    template_name = 'polls/NewEvent.html'

def createEvent(request):
    newEvent = Event()
    newEvent.event_name = request.POST['event_name_text']
    newEvent.event_date = request.POST['event_time']
    newEvent.event_organizer = request.POST['organizer']
    newEvent.event_description = request.POST['detail_text']
    newEvent.event_location = request.POST['address']

    #newEvent.comment_text = request.POST['commented_text']
    #newComment.comment_name = request.POST['name']
    
    
    newEvent.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('meetup_finder_app:home'))


class UpcomingView(generic.ListView):
    template_name = 'meetup_finder_app/upcoming.html'
    #context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the closest 5 events.
        """
        return Event.objects.filter(event_date__gte=timezone.now()).order_by('event_date')[:5]

class DetailView(generic.DetailView):
    model = Event
    template_name = 'meetup_finder_app/detail.html'
    