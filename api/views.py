from rest_framework.views import APIView
from expenses.models import Income, Expense
from api.serializers import IncomeSerializer, ExpenseSerializer, Userserializer
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from django.db.models import Sum
from django.utils import timezone
# Override ObtainAuthToken to allow CSRF exemption.
@method_decorator(csrf_exempt, name='dispatch')
class CustomAuthToken(ObtainAuthToken):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token_key = response.data['token']
        try:
            token_object = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
             return Response({'error': 'Token not found after authentication.'}, status=500)
        return Response({'token': token_object.key, 'user_id': token_object.user_id})

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

#add endpoint for expenses views
class Show_transactions(APIView):
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    def get(self,request):
        sort_incomes=request.query_params.get('sort_incomes','')
        sort_expenses=request.query_params.get('sort_expenses','')
        if sort_incomes=='asc':
            incomes=Income.objects.filter(user=request.user).order_by('amount')
        elif sort_incomes=='desc':
            incomes=Income.objects.filter(user=request.user).order_by('-amount')
        else:
            incomes = Income.objects.filter(user=request.user)
        if sort_expenses=='asc':
            expenses=Expense.objects.filter(user=request.user).order_by('amount')
        elif sort_expenses=='desc':
            expenses=Expense.objects.filter(user=request.user).order_by('-amount')
        else:
            expenses = Expense.objects.filter(user=request.user)
        expenses_serializer=ExpenseSerializer(expenses,many=True,context={'request': request})            
        incomes_serializer=IncomeSerializer(incomes,many=True,context={'request': request})
        return Response({'incomes': incomes_serializer.data, 'expenses': expenses_serializer.data})
class ReportView(APIView):
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    def get(self,request):
        period=request.query_params.get('period','week')
        today=timezone.now().date()
        if period=='week':
            start_date=today - timezone.timedelta(days=7)
        elif period=='month':
            start_date=today - timezone.timedelta(days=30)
        elif period=='year':
            start_date=today - timezone.timedelta(days=365)
        else:
            return Response({'error': 'Invalid period specified.'}, status=400)
        total_income=Income.objects.filter(user=request.user,date__gte=start_date,date__lte=today).aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense=Expense.objects.filter(user=request.user,date__gte=start_date,date__lte=today).aggregate(Sum('amount'))['amount__sum'] or 0
        net_balance=total_income - total_expense
        return Response({
            'total_income': total_income,
            'total_expense': total_expense,
            'net_balance': net_balance,
            'period': period
        })
class RegisterUser(APIView):
    permission_classes=[AllowAny]
    authentication_classes=[]
    def post(self,request):
        serializer=Userserializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            token,created=Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id}, status=201)
        return Response(serializer.errors,status=400)