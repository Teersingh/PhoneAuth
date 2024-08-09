from django.urls import path

from . import views

from .views import LoginView,Logout,register,home

urlpatterns = [
    path('',LoginView.as_view(),name='Login'),
    path('login/',LoginView.as_view(),name='Login'),
    path('logout/',views.Logout,name="Logout"),
    path('register/',views.register,name="register"),
    path('index/',views.home,name="home"),
]