from django.urls import path

from . import views

urlpatterns = [
    path('register', views.registration, name='register'),
    path('auth', views.CustomAuthToken.as_view()),
    path('online', views.online_list),
    path('ping', views.ping_me),
    path('online_list', views.OnlineView.as_view())
]
