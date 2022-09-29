from django.contrib import admin
from django.urls import path, include
from app.api.views import *
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('owner', FlatOwnerAV.as_view(),name='owners'),
    path('owners/<int:pk>/', FlatOwnerDetailsAV.as_view(),name='ownerDetails'),
    # path('employee',EmployeesAV.as_view(),name='employees'),
    path('login', UserLogin.as_view(),name='signin'),
    path('register', Register.as_view(),name='register'),
]
urlpatterns = format_suffix_patterns(urlpatterns)