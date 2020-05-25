from django.urls import path
from . import views

urlpatterns = [
    path('', views.register),
    path('registering', views.registering),
    path('login', views.login),
    path('logging', views.logging),
]