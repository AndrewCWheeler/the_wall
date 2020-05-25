from django.urls import path
from . import views

urlpatterns = [
    # path('', views.register),
    # path('login', views.login),
    path('wall', views.wall),
    path('process_message', views.process_message),
    path('process_comment', views.process_comment),
    path('logout', views.logout),
    path('destroy/<int:message_id>', views.destroy)
]