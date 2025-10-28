from rest_framework import viewsets
from expenses.models import Income, Expense
from api.serializers import IncomeSerializer, ExpenseSerializer, Userserializer
from django.contrib.auth.models import User
from rest_framework import permissions

class IncomeViewSet(viewsets.ModelViewSet):
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    serializer_class=IncomeSerializer
    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class ExpenseViewSet(viewsets.ModelViewSet):
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    serializer_class=ExpenseSerializer
    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=User.objects.all()
    serializer_class=Userserializer


