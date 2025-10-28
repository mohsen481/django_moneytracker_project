from expenses.models import Income , Expense
from rest_framework import serializers
from django.contrib.auth.models import User

class IncomeSerializer(serializers.HyperlinkedModelSerializer):
    user=serializers.ReadOnlyField(source='user.username')
    url=serializers.HyperlinkedIdentityField(view_name='incomes-detail')
    class Meta:
        model=Income
        fields=['id','user','amount','date','source','url']

class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    user=serializers.ReadOnlyField(source='user.username')
    url=serializers.HyperlinkedIdentityField(view_name='expenses-detail')
    class Meta:
        model=Expense
        fields=['id','user','amount','date','text','url']
class Userserializer(serializers.HyperlinkedModelSerializer):
    incomes=serializers.HyperlinkedRelatedField(many=True,view_name='incomes-detail',read_only=True)
    expenses=serializers.HyperlinkedRelatedField(many=True,view_name='expenses-detail',read_only=True)
    class Meta:
        model=User
        fields=['id','username','incomes','expenses','url']



