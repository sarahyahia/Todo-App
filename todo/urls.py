from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home' ),
    path('create/', views.create_todo, name='create_todo' ),
    path('todo/<id>/', views.todo_details, name='todo' ),
    path('edit/<id>/', views.edit_todo, name='edit' ),
    path('delete/<id>/', views.delete_todo, name='delete' ),
]