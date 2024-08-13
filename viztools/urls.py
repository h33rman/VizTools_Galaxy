# viztools/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload'),
    path('upload/success/', views.upload_success, name='upload_success'),
    path('select_galaxy/', views.select_galaxy, name='select_galaxy'),
    path('visualize_galaxy/', views.visualize_galaxy, name='visualize_galaxy'),
]
