from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('post',views.create_post, name='post'),
    path('setting',views.member_setting, name='setting'),
    path('post/<int:post_id>/comment/', views.comment_post, name='comment_post'),
    path('signup',views.signup, name='signup'),
    path('signin',views.signin, name='signin'),
    path('logout',views.logout_view, name='logout'),
]