from django.shortcuts import render
from django.http import HttpResponse
from .models import Income,Outlay
import datetime
from django.utils import timezone

def index(request):
    incomes = Income.objects.all()          
    return HttpResponse(request.user)
def show_transactions(request):
    incomes = Income.objects.all()
    outlays = Outlay.objects.all()
    context = {
        'incomes': incomes,
        'outlays': outlays
    }
    return render(request, 'expenses/transactions.html', context)
def show_recent_transactions(request,days):
    start_date=timezone.now()-datetime.timedelta(days=days)
    recent_incomes=Income.objects.filter(date__gte=start_date)
    recent_outlays=Outlay.objects.filter(date__gte=start_date)
    contex={"recent_incomes":recent_incomes,"recent_outlays":recent_outlays,"days":days}
    return render(request,"expenses/recent.html",contex)

    

# Create your views here.