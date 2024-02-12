from django.urls import path
from . import views

urlpatterns = [
        path('reading-list/', views.reading_material_view, name='reading-list'),
        path('timer/', views.pomodoro_timer, name='timer'),
        path('', views.home, name='home'),
]