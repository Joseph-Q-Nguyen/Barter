from django.urls import path
from main_app import views

urlpatterns = [
    path('', views.index, kwargs={"offset": 0, "limit": 10}, name='index'),
    path('login', views.login, name='signin')
]