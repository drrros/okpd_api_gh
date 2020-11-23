
from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('<slug:pk>/', views.DetailRecord.as_view()),
    path('', views.ListRecord.as_view()),
]
