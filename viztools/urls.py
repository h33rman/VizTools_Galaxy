# viztools/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('select_galaxy/', views.select_galaxy, name='select_galaxy'),
    path('result/', views.visualization_result, name='visualization_result'),  # Assuming a separate result view
]
