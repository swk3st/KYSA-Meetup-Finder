from django.urls import path

from . import views
from django.views.generic import TemplateView

from django.urls import reverse
from django.views import generic
from django.conf.urls import include


app_name = 'meetup_finder_app'
urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('newevent/', TemplateView.as_view(template_name="meetup_finder_app/newEvent.html"), name="newevent"),
    path('createEvent/', views.createEvent, name = 'createEvent'),
    path('accounts/profile/', views.WelcomeView),
    path('upcoming/', views.UpcomingView.as_view(), name="upcoming"),
    path('<int:pk>', views.DetailView.as_view(), name = "detail"),
    path('', views.HomeView.as_view(), name='home'),
]