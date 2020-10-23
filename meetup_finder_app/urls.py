from django.urls import path

from . import views
from django.views.generic import TemplateView

from django.conf.urls import include


app_name = 'meetup_finder_app'
urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('', views.HomeView.as_view(), name='home'),
    path('accounts/profile/', views.WelcomeView),
]