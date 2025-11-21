from django.test import TestCase
from .models import Income,Expense
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from .views import login_view
from django.contrib.auth import login
#from django.urls import reverse
from django.conf import settings
class DashboardViewTest(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='test_name',password='test')
    def test_url_with_unauthenticated_user(self):
        response=self.client.get('/dashboard/')
        self.assertNotEqual(response.status_code,200)
        self.assertRedirects(response,f"{settings.LOGIN_URL}?next=/dashboard/")
    def test_url_with_authenticated_user(self):
        self.client.login(username='test_name',password='test')
        response=self.client.get('/dashboard/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'expenses/dashboard.html')