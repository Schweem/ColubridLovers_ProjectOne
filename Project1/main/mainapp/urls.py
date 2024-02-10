from django.urls import path
from . import views

urlpatterns = [
    path('todo/', views.todo_list, name='todo_list'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('mark_completed/<int:todo_id>/', views.mark_todo_completed, name='mark_todo_completed'),
    path('calendar/', views.calendar, name='calendar'),

]