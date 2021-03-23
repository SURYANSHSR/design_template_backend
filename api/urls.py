from django.urls import path
from . import views

urlpatterns = [
    path('allrecords1', views.allrecords1, name='allrecords1'),
    path('check', views.check, name='check'),
    path('recorddetails', views.recorddetails, name='recorddetails'),
    path('createrecord/', views.createrecord, name='createrecord'),
    path('updaterecord/', views.updaterecord, name='updaterecord'),
    path('export_excel', views.export_excel, name='export_excel'),
]
