
from django.urls import path, re_path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.home, name= 'home'),

    path('Signup/', views.Signup, name= 'Signup'),
    re_path(r'^profile/(?P<id>[0-9A-Za-z_]+)/$', views.user_detail, name= 'profileview'),
    path('loginview/', views.loginview, name= 'loginview'),
    path('logoutview/', views.logoutview, name= 'logoutview'),
    path('submit/<int:pk>/result/', views.process, name= 'process'),
    path('submit/<int:pk>/', views.submit, name='submit'),
    path('contest/', views.contest, name='contest'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),


    ]