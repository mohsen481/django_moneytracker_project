from django.shortcuts import render
from django.http import HttpResponse
from .models import Income,Expense
import datetime
from django.utils import timezone
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def index(request):          
    return HttpResponse(request.user)
def show_transactions(request):
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
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=authenticate(request,username=username,password=password)
    if user:
        login(request,user)
        return HttpResponse(f"successfully logged in--{request.user}")
    return render(request,"expenses/accounts/login.html")


    

# Create your views here.