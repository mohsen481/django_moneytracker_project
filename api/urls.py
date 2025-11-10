from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'incomes',views.IncomeViewSet,basename='incomes')
router.register(r'expenses',views.ExpenseViewSet,basename='expenses')
router.register(r'users',views.UserViewSet,basename='user')
urlpatterns=[
    path('',include(router.urls)),
    path('transactions/',views.Show_transactions.as_view(),name='show_transactions_api'),
    path('token/',views.CustomAuthToken.as_view(),name='custom_auth_token'),
    path('reports/',views.ReportView.as_view(),name='reports_api'),
    path('register/',views.RegisterUser.as_view(),name='register_user_api'),
]