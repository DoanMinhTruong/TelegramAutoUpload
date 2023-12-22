from django.urls import path 
from .views import *
urlpatterns = [
    path('' , index, name="forward_index"),  
    path('add/' , add, name="forward_add"),   
    # path('<int:channel_id>/delete/', delete, name='channel_delete'),  
    # path('<int:channel_id>/detail/', detail, name='channel_detail'),  
    path('<int:forward_id>/update', update, name='forward_update'),  
    # path('<int:channel_id>/add_post/', add_post, name='channel_add_post'),  
    # path('<int:channel_id>/update_post/<int:post_id>/', update_post, name='channel_update_post'),  
    # path('post/<int:post_id>/' , index_post , name="forward_detail"),
    path('<int:forward_id>/run' , run , name="forward_run"),
    path('<int:forward_id>/stop' , stop , name="forward_stop"),
    path('<int:forward_id>/delete' , delete , name="forward_delete"),


]
