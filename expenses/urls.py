from django.urls import path
from . import views
urlpatterns=[path("",views.index,name="index"),path("transactions/",views.show_transactions,name="show_transactions"),]
