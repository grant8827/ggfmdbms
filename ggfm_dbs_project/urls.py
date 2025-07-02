"""
URL configuration for ggfm_dbs_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView # For a simple home page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # Django's built-in auth URLs
    path('', TemplateView.as_view(template_name='home.html'), name='home'), # Simple home page
    path('ggfm/', include('ggfm_dbs.urls')), # Include your app's URLs
]
