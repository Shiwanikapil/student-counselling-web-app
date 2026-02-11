from django.contrib import admin
from django.shortcuts import render
from django.urls import path,include
from MyApp import views
from django.shortcuts import render


urlpatterns = [
    path("", views.index, name='MyApp'),
    path("home", views.home, name='home'),
    path("about", views.about, name='about'),
     path("contact", views.contact, name='contact'),
      #path("login", views.login, name='login'),
      path("login", views.login_view, name='login'),  
     path("signup", views.signup, name='signup'),
     path("dashboard", views.dashboard, name='dashboard'),
     #path('pending', lambda request: render(request, 'pending.html'), name='pending'), 
     path('pending', views.pending, name='pending'),
     path('payment/<int:student_id>/', views.make_payment, name='make_payment'),
     path('letter/<int:student_id>/', views.download_letter, name='download_letter'),


]
