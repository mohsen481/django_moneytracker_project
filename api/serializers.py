from expenses.models import Income , Expense
from rest_framework import serializers
from django.contrib.auth.models import User

class IncomeSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source='user.username')
    class Meta:
        model=Income
        fields=['user','amount','date','source']

class ExpenseSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source='user.username')
    class Meta:
        model=Expense
        fields=['user','amount','date','text']
class Userserializer(serializers.ModelSerializer):
    incomes=serializers.PrimaryKeyRelatedField(many=True,queryset=Income.objects.all())
    expenses=serializers.PrimaryKeyRelatedField(many=True,queryset=Expense.objects.all())
    class Meta:
        model=User
        fields=['id','username','incomes','expenses']



