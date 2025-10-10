from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Income,Expense
import datetime
from django.utils import timezone
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.db import models 
from django.utils.dateparse import parse_datetime

def index(request):          
    return render(request,'expenses/HomePage.html')
@login_required
def show_transactions(request):
    if request.method=="POST":
        #Delete selected income
        if 'income_id' in request.POST:
            income_id=request.POST.get('income_id')
            try:
                income=Income.objects.get(id=income_id)
                income.delete()
                return redirect('show_transactions')
            except Income.DoesNotExist:
                return HttpResponse("Income not found!")
        #Delete selected expense
        elif 'expense_id' in request.POST:
            expense_id=request.POST.get('expense_id')
            try:
                expense=Expense.objects.get(id=expense_id)
                expense.delete()
                return redirect('show_transactions')
            except Expense.DoesNotExist:
                return HttpResponse("Expense not found!")
        #Add income 
        elif 'add_income' in request.POST:
            amount=int(request.POST.get('amount'))
            date=parse_datetime(request.POST.get('date'))
            source=request.POST.get('source')
            if timezone.is_naive(date):
                date=timezone.make_aware(date,timezone.get_current_timezone())
            if amount<0 or date>timezone.now():
                return HttpResponse("Invalid data: amount cannot be negative and date cannot be in future")
            Income.objects.create(amount=amount,date=date,source=source,user=request.user)
            return redirect('show_transactions')
        #Add expense
        else:
            amount=int(request.POST.get('amount'))
            date=parse_datetime(request.POST.get('date'))
            text=request.POST.get('text')
            if timezone.is_naive(date):
                date=timezone.make_aware(date,timezone.get_current_timezone())
            if amount<0 or date>timezone.now():
                return HttpResponse("Invalid data: amount cannot be negative and date cannot be in future")
            Expense.objects.create(amount=amount,date=date,text=text,user=request.user)
            return redirect('show_transactions')
    else:
        incomes = Income.objects.all()
        expenses = Expense.objects.all()
        context = {
            'incomes': incomes,
            'expenses': expenses
        }
        return render(request, 'expenses/transactions.html', context)
    
@login_required
def show_recent_transactions(request,days):
    start_date=timezone.now()-datetime.timedelta(days=days)
    recent_incomes=Income.objects.filter(date__gte=start_date)
    recent_expenses=Expense.objects.filter(date__gte=start_date)
    contex={"recent_incomes":recent_incomes,"recent_outlays":recent_expenses,"days":days}
    return render(request,"expenses/recent.html",contex)
def login_view(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('dashboard')
        else:
            msg="Invalid username or password"
            return render(request,"expenses/accounts/login.html",{"msg":msg})
    return render(request,"expenses/accounts/login.html")
def logout_view(request):
    logout(request)
    return redirect('index')
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            error = "Username already exists. Please choose another."
            return render(request, "expenses/accounts/register.html", {"error": error})
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect("index")
    return render(request,"expenses/accounts/register.html")
@login_required
def dashboard(request):
    username=request.user
    return render(request,"expenses/dashboard.html",{"username":username})
@login_required
@require_GET
def reports(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    now = timezone.now()
    period_label = "Custom Period"

    if start and end:
        try:
            start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end, "%Y-%m-%d") + datetime.timedelta(days=1)
        except ValueError:
            start_date = now - datetime.timedelta(days=7)
            end_date = now + datetime.timedelta(days=1)
            period_label = "Invalid date, showing last week"
        else:
            period_label = f"{start} to {end}"
    else:
        period = request.GET.get('period', 'week')
        if period == 'week':
            start_date = now - datetime.timedelta(days=7)
            period_label = "Last Week"
        elif period == 'month':
            start_date = now - datetime.timedelta(days=30)
            period_label = "Last Month"
        elif period == 'year':
            start_date = now - datetime.timedelta(days=365)
            period_label = "Last Year"
        else:
            start_date = now - datetime.timedelta(days=7)
            period_label = "Last Week"
        end_date = now + datetime.timedelta(days=1)

    incomes = Income.objects.filter(date__gte=start_date, date__lt=end_date, user=request.user)
    expenses = Expense.objects.filter(date__gte=start_date, date__lt=end_date, user=request.user)

    total_income = incomes.aggregate(total=models.Sum('amount'))['total'] or 0
    total_expense = expenses.aggregate(total=models.Sum('amount'))['total'] or 0
    balance = total_income - total_expense

    context = {
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'period_label': period_label,
        'period': request.GET.get('period', 'week'),
        'request': request,
    }
    return render(request, "expenses/reports.html", context)


    

    

# Create your views here.