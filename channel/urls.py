from django.urls import path 
from .views import *
urlpatterns = [
    path('' , index, name="channel_index"),  
    path('add/' , add, name="channel_add"),   
    path('<int:channel_id>/delete/', delete, name='channel_delete'),  
    path('<int:channel_id>/detail/', detail, name='channel_detail'),  
    path('<int:channel_id>/update/', update, name='channel_update'),  
    path('<int:channel_id>/add_post/', add_post, name='channel_add_post'),  
    path('<int:channel_id>/update_post/<int:post_id>/', update_post, name='channel_update_post'),  
    path('post/<int:post_id>/' , index_post , name="post_detail"),
    path('post/<int:post_id>/run' , post_run , name="post_run"),
    path('post/<int:post_id>/stop' , post_stop , name="post_stop"),
    path('post/<int:post_id>/delete' , post_delete , name="post_delete"),


]
