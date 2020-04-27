from django.urls import path
from main_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('createlisting', views.createlisting, name='createlisting'),
    path('listing/?P<pid>\w+', views.productpage, name='productpage'),
    path('update_listing/?P<pid>\w+', views.update_listing, name='update_listing'),
    path('delete_listing/?P<pid>\w+', views.delete_listing, name='delete_listing'),
    path('user/<id>', views.user_page, name='user_page')
]