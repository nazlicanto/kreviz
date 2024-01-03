from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'matcher'


# matcher/urls.py
urlpatterns = [
    path('manage_interests/', views.manage_interests, name='manage_interests'),
]
