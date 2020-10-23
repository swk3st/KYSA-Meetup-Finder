from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404


# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import timezone

from django.urls import reverse
from django.views import generic
from django.views.generic.base import TemplateView

class HomeView(TemplateView):
    template_name = 'meetup_finder_app/home.html'

def WelcomeView(request):
    template_name = 'meetup_finder_app/welcome.html'
    return render(request, template_name)

def testView(request):
    return HttpResponse("hello")