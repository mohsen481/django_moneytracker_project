from django.test import TestCase
from .models import Income,Expense
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from .views import login_view
from django.contrib.auth import login
#from django.urls import reverse
from django.conf import settings
class Show_recent_transactions_test(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='test_name',password='test')
    def test_url_with_unauthenticated_user(self):
        response=self.client.get('/expenses/recent/10/')
        self.assertNotEqual(response.status_code,200)
        self.assertRedirects(response,f"{settings.LOGIN_URL}?next=/expenses/recent/10/")
        
    def test_url_with_authenticated_user(self):
        self.client.login(username='test_name',password='test')
        response=self.client.get('/expenses/recent/10/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'expenses/recent.html')