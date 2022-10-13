from django.urls import path
from . import views


urlpatterns=[
    
    path('',views.home,name='blog-home'),
    path('accounts/login/',views.signIn,name='signin'),
    path('accounts/logout/',views.signout,name='logout'),
    path('posts/<int:pk>',views.post_detail,name='post-detail'),
    
    path('create/',views.create_post,name='post-create'),
    path('update/<int:pk>/',views.update_post,name='post-update'),
    path('delete/<int:pk>/',views.delete_post,name='post-delete'),
]