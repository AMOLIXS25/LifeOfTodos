from django.urls import path

from .views import todo_list, edit_todo, delete_todo, create_todo, list_todo_reminders

app_name = 'todo'

urlpatterns = [
    path('', todo_list, name='todo-list'),
    path('<int:todo_id>/reminders/', list_todo_reminders, name='todo-list-reminders'),
    path('create-todo/', create_todo, name='create-todo'),
    path('edit-todo/<int:year>/<int:month>/<int:day>/<slug:slug>/', edit_todo, name='edit-todo'),
    path('delete-todo/<int:todo_id>/', delete_todo, name='delete-todo'),
]