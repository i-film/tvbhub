from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('<int:pk>/like_videos/', views.LikeListView.as_view(), name='like_videos'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password_done/', views.reset_password_done, name='reset_password_done'),
]
