from __future__ import unicode_literals

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User

# Create your tests here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from .models import Event, AppUser
from . import views
from .views import requestFriend
from . import urls
import datetime
from allauth.account.forms import LoginForm
class YourLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(YourLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()

        # You don't want the `remember` field?
        if 'remember' in self.fields.keys():
            del self.fields['remember']

        helper = FormHelper()
        helper.form_show_labels = False
        helper.layout = Layout(
            Field('login', placeholder = 'Email address'),
            Field('password', placeholder = 'Password'),
            FormActions(
                Submit('submit', 'Log me in to Cornell Forum', css_class = 'btn-primary')
            ),
        )
        self.helper = helper
def create_event(organizer, description, location, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Event.objects.create(event_organizer=organizer, event_desctiption=description, event_location=loaction, event_date = time)

class EventModelTests(TestCase):

    # def test_interested_user(self):
    #     """
    #     test interested users attribute
    #     """
    #     e = Event(event_date = timezone.now())
    #     e.save()
    #     a = User(id=1)
    #     e.interested_users.add(a)
    #     self.assertIs(a in e.interested_user.all(), True)

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

    def test_coming_up_lt_one_dat_past(self):
        """
        coming_up() returns True for event whose event_date
        is less or equal to 1 day ago.
        """
        time = timezone.now() + datetime.timedelta(days=-1, hours=1)
        tomorrow_event = Event(event_date=time)
        self.assertIs(tomorrow_event.coming_up(), True)

    def test_coming_up_one_day_past(self):
        """
        coming_up() returns false for event whose event_date
        is more than 1 day ago.
        """
        time = timezone.now() + datetime.timedelta(days=-1, hours=-1)
        tomorrow_event = Event(event_date=time)
        self.assertIs(tomorrow_event.coming_up(), False)

    def test_coming_up_seven_days_past(self):
        """
        coming_up() returns false for event whose event_date
        is more than 7 days ago.
        """
        time = timezone.now() + datetime.timedelta(days=-7)
        tomorrow_event = Event(event_date=time)
        self.assertIs(tomorrow_event.coming_up(), False)

class UserModelTests(TestCase):

    def setUp(self):
        user1 = User(email="u1@mail.com",username='user1',first_name="User1",last_name="Test")
        user2 = User(email="u2@mail.com",username='user2',first_name="User2",last_name="Test")
        user3 = User(email="u3@mail.com",username='user3',first_name="User3",last_name="Test")
        user1.save()
        user2.save()
        user3.save()
        user1 = AppUser(id=user1.id,django_user=user1)
        user2 = AppUser(id=user2.id,django_user=user2)
        user3 = AppUser(id=user3.id,django_user=user3)
        user1.save()
        user2.save()
        user3.save()

        self.user1 = user1
        self.user2 = user2
        self.user3 = user3

    def testEventsForDeletedUsers(self):
        event = Event(id=1,event_date="2020-12-30 17:00Z",event_description="none",event_organizer=self.user1.django_user, event_location='house',event_name="event",lat=10.0 ,lng=10.0)
        event.interested_users.add(self.user2.django_user)
        event.save()

        self.assertIn(event,Event.objects.all())

        User.objects.get(id=self.user1.django_user.id).delete()

        self.assertNotIn(event,Event.objects.all())
    
    def testFriendsForDeletedUsers(self):
        self.user3.friends.add(self.user2)
        
        self.assertIn(self.user2,AppUser.objects.get(id=self.user3.id).friends.all())

        AppUser.objects.get(id=self.user2.id).delete()

        self.assertNotIn(self.user2,AppUser.objects.get(id=self.user3.id).friends.all())


class AppUserTests(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='AJ', email='exmplemail@example.com', password='12345')
    

    def test_requestFriend(self):
        """
        requestFriend should add a user to another's requested friends
        """
        
        u = AppUser(id = 1)
        u.django_user = User.objects.create(username='Testuser')
        u.save()
        f = AppUser(id = 2)
        f.django_user = User.objects.create(username='Testuser2')
        f.save()
        # c = Client()
        # c.post("/requestFriend",{'Friend':f.id,'User':u.id})
        # client = Client()
        # response = client.get("/requestFriend")
        # request = response.wsgi_request 

        #request.POST({'Friend':f.id,'User':u.id})
        #response = self.client.get(reverse('meetup_finder_app:requestFriend'))
        #f.requested_friends.add(u)
        #requestFriend(request)
        data = {'Friend':f.id,'User':u.id}
        #request = self.factory.post('/a/test/path/', data, content_type='application/json')
        # request = self.factory.post('/requestFriend/', data, content_type='application/json')
        # print(request.POST['User'])
        # request.user = self.user
        # requestFriend(request)

        # poll_1 = Poll.objects.get(pk=1)
        # self.assertEqual(poll_1.choice_set.get(pk=1).votes, 1)

        resp = self.client.post('/requestFriend/', {'User': u.id, 'Friend': f.id})
        self.assertEqual(resp.status_code, 302)

        self.assertIs(u in f.requested_friends.all(), True)
    
    
    
    def test_addFriend(self):
        """
        requestFriend should add a user to another's requested friends
        """
        
        u = AppUser(id = 1)
        u.django_user = User.objects.create(username='Testuser')
        u.save()
        f = AppUser(id = 2)
        f.django_user = User.objects.create(username='Testuser2')
        f.save()
        # c = Client()
        # c.post("/requestFriend",{'Friend':f.id,'User':u.id})
        # client = Client()
        # response = client.get("/requestFriend")
        # request = response.wsgi_request 

        #request.POST({'Friend':f.id,'User':u.id})
        #response = self.client.get(reverse('meetup_finder_app:requestFriend'))
        #f.requested_friends.add(u)
        #requestFriend(request)
        data = {'Friend':f.id,'User':u.id}
        #request = self.factory.post('/a/test/path/', data, content_type='application/json')
        # request = self.factory.post('/requestFriend/', data, content_type='application/json')
        # print(request.POST['User'])
        # request.user = self.user
        # requestFriend(request)

        # poll_1 = Poll.objects.get(pk=1)
        # self.assertEqual(poll_1.choice_set.get(pk=1).votes, 1)

        resp = self.client.post('/addFriend/', {'User': u.id, 'Friend': f.id})
        self.assertEqual(resp.status_code, 302)

        self.assertIs(u in f.friends.all(), True)
    
    def test_removeFriend(self):
        """
        remove Friend should remove a user from another's friends
        """
        
        u = AppUser(id = 1)
        u.django_user = User.objects.create(username='Testuser')
        u.save()
        f = AppUser(id = 2)
        f.django_user = User.objects.create(username='Testuser2')
        f.save()
        f.friends.add(u)
        # c = Client()
        # c.post("/requestFriend",{'Friend':f.id,'User':u.id})
        # client = Client()
        # response = client.get("/requestFriend")
        # request = response.wsgi_request 

        #request.POST({'Friend':f.id,'User':u.id})
        #response = self.client.get(reverse('meetup_finder_app:requestFriend'))
        #f.requested_friends.add(u)
        #requestFriend(request)
        data = {'Friend':f.id,'User':u.id}
        #request = self.factory.post('/a/test/path/', data, content_type='application/json')
        # request = self.factory.post('/requestFriend/', data, content_type='application/json')
        # print(request.POST['User'])
        # request.user = self.user
        # requestFriend(request)

        # poll_1 = Poll.objects.get(pk=1)
        # self.assertEqual(poll_1.choice_set.get(pk=1).votes, 1)

        resp = self.client.post('/removeFriend/', {'User': u.id, 'Friend': f.id})
        self.assertEqual(resp.status_code, 302)

        self.assertIs(u not in f.friends.all(), True)
    
    def test_rejectFriend(self):
        """
        requestFriend should add a user to another's requested friends
        """
        
        u = AppUser(id = 1)
        u.django_user = User.objects.create(username='Testuser')
        u.save()
        f = AppUser(id = 2)
        f.django_user = User.objects.create(username='Testuser2')
        f.save()
        u.requested_friends.add(f)
        # c = Client()
        # c.post("/requestFriend",{'Friend':f.id,'User':u.id})
        # client = Client()
        # response = client.get("/requestFriend")
        # request = response.wsgi_request 

        #request.POST({'Friend':f.id,'User':u.id})
        #response = self.client.get(reverse('meetup_finder_app:requestFriend'))
        #f.requested_friends.add(u)
        #requestFriend(request)
        data = {'Friend':f.id,'User':u.id}
        #request = self.factory.post('/a/test/path/', data, content_type='application/json')
        # request = self.factory.post('/requestFriend/', data, content_type='application/json')
        # print(request.POST['User'])
        # request.user = self.user
        # requestFriend(request)

        # poll_1 = Poll.objects.get(pk=1)
        # self.assertEqual(poll_1.choice_set.get(pk=1).votes, 1)

        resp = self.client.post('/rejectFriend/', {'User': u.id, 'Friend': f.id})
        self.assertEqual(resp.status_code, 302)

        self.assertIs(f not in u.requested_friends.all(), True)
    
    def test_rescindRequest(self):
        """
        requestFriend should add a user to another's requested friends
        """
        
        u = AppUser(id = 1)
        u.django_user = User.objects.create(username='Testuser')
        u.save()
        f = AppUser(id = 2)
        f.django_user = User.objects.create(username='Testuser2')
        f.save()
        f.requested_friends.add(u)
        # c = Client()
        # c.post("/requestFriend",{'Friend':f.id,'User':u.id})
        # client = Client()
        # response = client.get("/requestFriend")
        # request = response.wsgi_request 

        #request.POST({'Friend':f.id,'User':u.id})
        #response = self.client.get(reverse('meetup_finder_app:requestFriend'))
        #f.requested_friends.add(u)
        #requestFriend(request)
        data = {'Friend':f.id,'User':u.id}
        #request = self.factory.post('/a/test/path/', data, content_type='application/json')
        # request = self.factory.post('/requestFriend/', data, content_type='application/json')
        # print(request.POST['User'])
        # request.user = self.user
        # requestFriend(request)

        # poll_1 = Poll.objects.get(pk=1)
        # self.assertEqual(poll_1.choice_set.get(pk=1).votes, 1)

        resp = self.client.post('/rescindRequest/', {'User': u.id, 'Friend': f.id})
        self.assertEqual(resp.status_code, 302)

        self.assertIs(u not in f.requested_friends.all(), True)
    
    
    
    
    def test_friends_symmetrical(self):
        """
        when a user is added to another user's friends it choudl be symmetrical
        """
        u = AppUser(id = 1)
        u.django_user = User.objects.create(username='Testuser')
        u.save()
        f = AppUser(id = 2)
        f.django_user = User.objects.create(username='Testuser2')
        f.save()

        u.friends.add(f)
        self.assertIs(u in f.friends.all(), True)
        self.assertIs(f in u.friends.all(), True)
    
    def test_requested_friends_asymmetrical(self):
        """
        when a user is added to another user's requested friends, it should not be symmetrical
        """
        u = AppUser(id = 1)
        u.django_user = User.objects.create(username='Testuser')
        u.save()
        f = AppUser(id = 2)
        f.django_user = User.objects.create(username='Testuser2')
        f.save()
        
        f.requested_friends.add(u)
        self.assertIs(u in f.requested_friends.all(), True)
        self.assertIs(f in u.requested_friends.all(), False)
    
    def test_remove_friends_symmetrical(self):
        """
        when a user is added to another user's friends it choudl be symmetrical
        """
        u = AppUser(id = 1)
        u.django_user = User.objects.create(username='Testuser')
        u.save()
        f = AppUser(id = 2)
        f.django_user = User.objects.create(username='Testuser2')
        f.save()

        u.friends.add(f)
        f.friends.remove(u)
        self.assertIs(u in f.friends.all(), False)
        self.assertIs(f in u.friends.all(), False)

# class UserTestCase(TestCase):

#     def setUp(self):
#         self.client = Client()

#     def testLogin(self):
#         response = self.client.get(reverse('meetup_finder_app:dashboard'))
#         self.assertEqual(int(response.status_code), 200)

# class TestPagesViews(TestCase):

#     def setUp(self):
#         # Every test needs access to the request factory.
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(
#             username='AJ', email='exmplemail@example.com', password='12345')
    
#     def test_dashboard(self):
#         url = reverse('meetup_finder_app:dashboard')
#         response = self.client.get(url)
#         self.assertContains(response, "Welcome AJ to KYSA")
    



