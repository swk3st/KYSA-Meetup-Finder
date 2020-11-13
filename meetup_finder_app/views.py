from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404


# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import timezone

from django.urls import reverse
from django.views import generic
from django.views.generic.base import TemplateView
from .models import Event, AppUser
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount


class HomeView(TemplateView):
    template_name = 'meetup_finder_app/home.html'


def CreateUser(user):
    print("Creating New User")
    try:
        social_account = SocialAccount.objects.filter(user_id=user.id)[0]
        new_user = AppUser(id=user.id,django_user=user)
        new_user.save()
    finally:
        pass

def WelcomeView(request):
    template_name = 'meetup_finder_app/dashboard.html'
    return render(request, template_name)
    # template_name = 'meetup_finder_app/userProfile.html'

def SingleEventView(request):
    template_name = 'meetup_finder_app/single_event_view.html'
    return render(request, template_name, context={"event":{"lat":38.028212,"lng":-78.511077}})

class IndexView(generic.ListView):
    template_name = 'meetup_finder_app/index.html'


    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Event.objects.filter(event_date__lte=timezone.now()).order_by('-event_date')[:5]


def NewEventView(request):
    template_name = 'meetup_finder_app/Updated_New_Event.html'
    return render(request,template_name)
def Sign2(request):
    template_name = 'meetup_finder_app/signin2.html'
    return render(request,template_name)
def Uprofile(request):
    template_name = 'meetup_finder_app/userProfile.html'
    if len(AppUser.objects.filter(id=request.user.id)) == 0:
        CreateUser(request.user)

    try:
        profile_picture = SocialAccount.objects.get(user_id=request.user.id).extra_data['picture']
    except:
        profile_picture = ""

    return render(request, template_name, context={"profile_picture":profile_picture})
   
    
def createEvent(request):
    newEvent = Event()
    newEvent.event_name = request.POST['event_name_text']
    newEvent.event_date = request.POST['event_time'] 
    newEvent.event_organizer = request.POST['organizer'] # request.user
    newEvent.event_description = request.POST['detail_text']
    newEvent.event_location = request.POST['address']
    newEvent.lat = request.POST['lat']
    newEvent.lng = request.POST['lng']

    #newEvent.comment_text = request.POST['commented_text']
    #newComment.comment_name = request.POST['name']
    
    
    newEvent.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('meetup_finder_app:detail',kwargs={'pk':newEvent.id}))

def showInterest(request):

    userid = request.POST['User']
    eventid = request.POST['Event']

    event = Event.objects.get(id=eventid)
    user = User.objects.get(id=userid)

    event.interested_users.add(user)

    event.save()
    return HttpResponseRedirect(reverse('meetup_finder_app:detail',kwargs={'pk':eventid}))

def revokeInterest(request):

    userid = request.POST['User']
    eventid = request.POST['Event']

    event = Event.objects.get(id=eventid)
    user = User.objects.get(id=userid)

    event.interested_users.remove(user)

    print(user.event_set.all())

    event.save()
    return HttpResponseRedirect(reverse('meetup_finder_app:detail',kwargs={'pk':eventid}))

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

    
    