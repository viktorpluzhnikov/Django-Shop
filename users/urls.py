from django.urls import path

from users.templates.users.views import UserLoginView, UserRegistrationView, UserLogoutView, UserProfileView, verify
from django.contrib.auth.decorators import login_required

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('veryfy/<str:email>/<str:activate_key>/', verify, name='verify'),
]