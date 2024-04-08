from django.contrib import admin
from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="main"),
    path("<int:page>", views.main, name="root_paginate"),
    path('tag/', views.tag, name='tag'),
    path('note/', views.note, name='note'),


]