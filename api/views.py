from rest_framework import viewsets
from expenses.models import Income, Expense
from .serializers import IncomeSerializer, ExpenseSerializer, Userserializer
from django.contrib.auth.models import User

class IncomeViewSet(viewsets.ModelViewSet):
    queryset=Income.objects.all()
    serializer_class=IncomeSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset=Expense.objects.all()
    serializer_class=ExpenseSerializer
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=User.objects.all()
    serializer_class=Userserializer


