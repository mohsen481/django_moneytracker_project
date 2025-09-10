from django.shortcuts import render
from django.http import HttpResponse
from .models import Income,Outlay

def index(request):
    incomes = Income.objects.all()
    return HttpResponse(incomes)

# Create your views here.
