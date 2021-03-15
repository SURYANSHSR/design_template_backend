from django.urls import path
from . import views

urlpatterns = [
    path('save_result', views.save_result, name='save_result'),
    path('check', views.check, name='check'),
    path('reportdetails/', views.reportdetails, name='reportdetails'),
    path('sqlquery/', views.sqlquery, name='sqlquery'),
    path('allreports/', views.allreports, name='allreports'),
]
