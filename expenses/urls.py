from django.urls import path
from . import views
urlpatterns=[
                path("",views.index,name="index"),
                path("transactions/",views.show_transactions,name="show_transactions"),
                path("accounts/login/",views.login_view,name="login"),
                path("accounts/register/",views.register_view,name="register"),
                path("dashboard/",views.dashboard,name="dashboard"),
                path("reports/",views.reports,name="reports"),
                path("accounts/logout/",views.logout_view,name="logout"),
                
             

             ]
