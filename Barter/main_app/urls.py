from django.urls import path
from main_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='signin')
]