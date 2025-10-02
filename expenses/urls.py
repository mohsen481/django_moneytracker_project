from django.urls import path
from . import views
urlpatterns=[path("",views.index,name="index"),
             path("transactions/",views.show_transactions,name="show_transactions"),
             path("recent/<int:days>/",views.show_recent_transactions,name="recent"),
             path("accounts/login/",views.login_view,name="login")
             ]
