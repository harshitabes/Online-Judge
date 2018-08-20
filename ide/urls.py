
from django.urls import path
from . import views

urlpatterns = [

    path('result/', views.process, name= 'process'),
    path('submit/', views.submit, name='submit'),
    path('', views.home, name='home'),
    ]