from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'incomes',views.IncomeViewSet,basename='incomes')
router.register(r'expenses',views.ExpenseViewSet,basename='expenses')
router.register(r'users',views.UserViewSet,basename='users')
urlpatterns=[
    path('',include(router.urls))
]