from django.urls import path 
from .views import *
urlpatterns = [
    path('' , index, name="tbot_index"),  
    path('add/' , add, name="tbot_add"),   
    path('<int:tbot_id>/delete/', delete, name='tbot_delete'),  
]
