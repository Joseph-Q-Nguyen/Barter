from django.urls import path
from main_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('createlisting', views.createlisting, name='createlisting'),
    path('listing/?P<pid>\w+', views.productpage, name='productpage')
]