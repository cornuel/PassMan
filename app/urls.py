from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login_page'),
    path('register', views.register, name='register_page'),
    path('main', views.main, name='main_page'),
    path('get_pass', views.get_password, name='get_pass'),
    path('save_pass', views.save_password, name='save_pass')
]