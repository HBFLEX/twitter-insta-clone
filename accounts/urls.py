from django.urls import path
from . import views
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
)


urlpatterns = [
    path('', views.HomeView.as_view(), name='home-page'),
    path('accounts/register/', views.RegisterUserView.as_view(), name='register-page'),
    path('accounts/login/', LoginView.as_view(template_name='accounts/login.html'), name='login-page'),
    path('accounts/logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout-page'),
    path('accounts/profile/<int:pk>/', views.ProfileView.as_view(), name='profile-page'),
    path('profile/<int:pk>/followers/add/', views.FollowView.as_view(), name='add-follower'),
    path('profile/<int:pk>/followers/remove/', views.UnFollowView.as_view(), name='remove-follower'),
    path('accounts/people/', views.PeopleView.as_view(), name='people-page'),
]