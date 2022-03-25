# from django.conf.urls import url

import authapp.views as authapp
from django.urls import re_path, path

app_name = "authapp"

urlpatterns = [
    path('login/', authapp.login, name='login'),
    re_path(r'^logout/$', authapp.logout, name='logout'),
    re_path(r'^register/$', authapp.UserRegisterView.as_view(), name='register'),
    re_path(r'^edit/$', authapp.edit, name='edit'),

    path('veryfy/<str:email>/<str:activate_key>/', authapp.verify, name='verify')
]

