from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='user_login'),
    path('logout/' , views.logout_v , name='user_logout'),
    path('reset_password/' , views.reset_password , name='reset_password'),
    path('/' , views.index, name= 'user_index'),
]

