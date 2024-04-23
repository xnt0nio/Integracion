from django import views
from django.urls import path, include
from .views import *



urlpatterns = [
    path('', index, name="index"),
    path('test', test, name="test"),


]