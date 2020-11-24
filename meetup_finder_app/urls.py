from django.urls import path

from . import views
from django.views.generic import TemplateView

from django.urls import reverse
from django.views import generic
from django.conf.urls import include


app_name = 'meetup_finder_app'
urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('newevent/', views.NewEventView, name="newevent"),
    path('createEvent/', views.createEvent, name = 'createEvent'),
    path('accounts/profile/', views.WelcomeView, name="dashboard"),
    path('dashboard/', views.WelcomeView, name="dashboard"),
    path('upcoming/', views.UpcomingView.as_view(), name="upcoming"),
    path('<int:pk>', views.DetailView.as_view(), name = "detail"),
    path('single_map_vew/', views.SingleEventView, name="eventView"),
    path('signin2/',views.Sign2, name="signin2"),
    path('profile/',views.Uprofile, name="uProfile"),
    path('showInterest/', views.showInterest, name="show_interest"),
    path('revokeInterest/', views.revokeInterest, name="revoke_interest"),
    path('profiles/<int:user_id>',views.singleProfileView, name="singleProfile"),
    path('addFriend/',views.addFriend, name = 'addFriend'),
    path('removeFriend/',views.removeFriend, name = 'removeFriend'),
    path('requestFriend/',views.requestFriend, name = 'requestFriend'),
    path('rejectFriend/',views.rejectFriend, name = 'rejectFriend'),
    path('rescindRequest/',views.rescindRequest, name = 'rescindRequest'),
    path('friends/', views.FriendsView, name = 'FriendsView'),
    path('deleteEvent/', views.deleteEvent, name="delete_event"),
    path('', views.HomeView.as_view(), name='home'),
]