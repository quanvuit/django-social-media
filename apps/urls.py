from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('post',views.create_post, name='post'),
    path('post/<int:post_id>/comment/', views.comment_post, name='comment_post'),
    path('signup',views.signup, name='signup'),
    path('signin',views.signin, name='signin'),
    path('logout',views.logout_view, name='logout'),
]