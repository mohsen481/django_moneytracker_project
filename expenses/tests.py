
import pytest
from pytest_django.asserts import assertTemplateUsed,assertRaisesMessage
from django.conf import settings
from datetime import datetime 
import datetime as dt
from .models import Income,Expense
from django.utils import timezone
from django.core.exceptions import ValidationError
pytestmark=pytest.mark.django_db
#fixtures
@pytest.fixture
def create_user(django_user_model,data):
     return django_user_model.objects.create_user(**data)
@pytest.fixture
def data():
     data={'username':'test','password':'1234'}
     return data
@pytest.fixture
def create_income(create_user):
    def _create_income(amount=None,date=None):
        if amount is None:
            amount=1
        if date is None:
            date=timezone.now().date()
        income_data={
            'amount':amount,
            'date':date,
            'source':'test',
            'user':create_user,
        }
        income=Income.objects.create(**income_data)
        return income
    return _create_income
    
@pytest.fixture
def create_expense(create_user):
    def _create_expense(amount=None,date=None):
        if amount is None:
            amount=1
        if date is None:
            date=timezone.now().date()
        expense_data={
            'amount':amount,
            'date':date,
            'text':'test',
            'user':create_user,
        }
        expense=Expense.objects.create(**expense_data)
        return expense
    return _create_expense

@pytest.fixture
def freeze_date(monkeypatch):
    fixed = datetime(2025, 3, 11, tzinfo=dt.timezone.utc)
    monkeypatch.setattr(timezone, "now", lambda: fixed)
    return fixed
#test views

class TestRegister:   

    def test_register_New_user(self,client,django_user_model,data):
        response=client.post('/accounts/register/',data,follow=True)
        assert response.status_code==200
        assert django_user_model.objects.filter(username='test').exists()
        assertTemplateUsed(response,'expenses/HomePage.html')
        assert response.redirect_chain[-1]==("/",302)
        
    def test_register_existing_user(self,client,django_user_model,data,create_user):
        response=client.post('/accounts/register/',data)
        error_message=b'Username already exists. Please choose another.'
        assertTemplateUsed(response,'expenses/accounts/register.html')
        assert response.status_code==200
        assert error_message in response.content

class TestLogin:
    def test_succesfull_login(self,client,django_user_model,create_user,data):
        response=client.post('/accounts/login/',data)
        assert response.status_code==302
        assert response.url=='/dashboard/'
    def test_failed_login(self,client):
        wrong_data={'username':'test','password':'123'}
        message=b"Invalid username or password"
        response=client.post('/accounts/login/',wrong_data)
        assert response.status_code==200
        assert message in response.content

class TestTransactions:
    URL='/transactions/'
    def test_unauthenticated_access(self,client):
        response=client.get(self.URL)
        assert response.status_code==302
        assert response.url=='/accounts/login/?next=/transactions/'
    def test_authenticated_access(self,client,create_user,data):
        client.login(**data)
        response=client.get(self.URL)
        assert response.status_code==200
        assertTemplateUsed(response,'expenses/transactions.html')
    def test_create_new_income(self,client,create_user,data):
        client.login(**data)
        post_data={
            'amount':1,
            'date':datetime.now().strftime('%Y-%m-%d'),
            'source':'test',
            'add_income':'add_income'}
        assert Income.objects.count()==0
        response=client.post(self.URL,post_data)
        new_income=Income.objects.get(pk=1)
        assert Income.objects.count()==1
        assert new_income.amount==1
        assert response.status_code==302
    def test_delete_income(self,client,data,create_income):
        client.login(**data)
        income=create_income()
        assert Income.objects.count()==1
        response=client.post(self.URL,{'income_id':income.id})
        assert Income.objects.count()==0
        assert response.status_code==302
    def test_create_new_expense(self,client,create_user,data):
        client.login(**data)
        post_data={
            'amount':1,
            'date':datetime.now().strftime('%Y-%m-%d'),
            'text':'test',
            'add_expense':'add_expense'}
        assert Expense.objects.count()==0
        response=client.post(self.URL,post_data)
        new_expense=Expense.objects.get(pk=1)
        assert Expense.objects.count()==1
        assert new_expense.amount==1
        assert response.status_code==302

    def test_delete_expense(self,client,data,create_expense):
        client.login(**data)
        expense=create_expense()
        assert Expense.objects.count()==1
        response=client.post(self.URL,{'expense_id':expense.id})
        assert Expense.objects.count()==0
        assert response.status_code==302
    
    def test_sort_incomes(self,client,data,create_income):
        client.login(**data)
        create_income()
        create_income(4)
        create_income(3)
        response=client.get(self.URL,query_params={'sort_incomes':'asc'})
        incomes=response.context['incomes']
        amounts=[income.amount for income in incomes]
        assert amounts==sorted(amounts)

    def test_sort_expenses(self,client,data,create_expense):
        client.login(**data)
        create_expense()
        create_expense(3)
        create_expense(2)
        response=client.get(self.URL,query_params={'sort_expenses':'desc'})
        expenses=response.context['expenses']
        amounts=[expense.amount for expense in expenses]
        assert amounts==sorted(amounts,reverse=True)

        
class TestReports:
    url = "/reports/"
    def test_reports_with_periods(self, client, create_income, create_expense, data, freeze_date):
        client.login(**data)
       
        date_inside_week = (freeze_date - dt.timedelta(days=5)).date()     
        date_inside_month = (freeze_date - dt.timedelta(days=20)).date() 
        date_inside_year = (freeze_date - dt.timedelta(days=200)).date()    
        date_out_of_year = (freeze_date - dt.timedelta(days=400)).date()    
        # incomes
        create_income(4, date_inside_week)
        create_income(2, date_inside_month)
        create_income(5, date_inside_year)
        create_income(9, date_out_of_year)
        # expenses
        create_expense(3, date_inside_week)
        create_expense(1, date_inside_month)
        create_expense(7, date_inside_year)
        # GET responses
        r_week  = client.get(self.url, query_params={"period": "week"})
        r_month = client.get(self.url, query_params={"period": "month"})
        r_year  = client.get(self.url, query_params={"period": "year"})
        assert r_week.context["balance"] == 1
        assert r_month.context["balance"] == 2
        assert r_year.context["balance"] == 0

    def test_reports_with_custom_date(self, client, create_income, create_expense, data, freeze_date):
        client.login(**data)
        start_date = (freeze_date - dt.timedelta(days=10)).date()  
        end_date   = freeze_date.date()            
        create_income(4, start_date + dt.timedelta(days=1))   
        create_expense(3, start_date + dt.timedelta(days=2))        
        create_income(7, start_date - dt.timedelta(days=1))
        create_expense(5, start_date - dt.timedelta(days=1))
        response = client.get(self.url, query_params={
            "start": start_date.isoformat(),
            "end": end_date.isoformat(),
        })
        assert response.context["balance"] == 1
        incomes_in = response.context["incomes"]
        expenses_in = response.context["expenses"]
        assert all(start_date <= inc.date <= end_date for inc in incomes_in)
        assert all(start_date <= exp.date <= end_date for exp in expenses_in)


#test models
def test_create_income_with_invalid_values(create_user):
    user=create_user
    with pytest.raises(ValidationError) as res:
        Income(user=user,amount=-1,date=timezone.now().date(),source='test').full_clean()
    assert 'Income amount cannot be negative' in str(res.value)
    with pytest.raises(ValidationError) as res:
        Income(user=user,amount=1,date=timezone.now().date()+dt.timedelta(days=1),source='test').full_clean()
    assert 'Income date cannot be in the future' in str(res.value)
def test_create_expense_with_invalid_values(create_user):
    user=create_user
    with pytest.raises(ValidationError) as res:
        Expense(user=user,amount=-1,date=timezone.now().date(),text='test').full_clean()
    assert 'Expense amount cannot be negative' in str(res.value)
    with pytest.raises(ValidationError) as res:
        Expense(user=user,amount=1,date=timezone.now().date()+dt.timedelta(days=1),text='test').full_clean()
    assert 'Expense date cannot be in the future' in str(res.value)