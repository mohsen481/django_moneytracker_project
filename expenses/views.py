from django.shortcuts import render
from django.http import HttpResponse
from .models import Income,Outlay

def index(request):
    incomes = Income.objects.all()          
    return HttpResponse(incomes)
def show_transactions(request):
    incomes = Income.objects.all()
    outlays = Outlay.objects.all()
    context = {
        'incomes': incomes,
        'outlays': outlays
    }
    return render(request, 'expenses/transactions.html', context)

# Create your views here.