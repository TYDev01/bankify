from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib.auth.decorators import login_required

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name="dashboard-home"),
    path('deposit/', views.deposit, name="deposit"),
    path('logout/', views.logout_user, name='logout'),
    path('approve-deposit/<int:deposit_id>/', views.approve_deposit, name='approve_deposit'),

]