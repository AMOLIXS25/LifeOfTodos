import time

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from django.contrib import messages

from mysite.utils import define_toast_message
from mysite.middlewares import clear_toast_messages

from .models import TODOO
from accounts.models import Profile
from .forms import TodoForm


@clear_toast_messages
def create_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        try:
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            define_toast_message(request, 'Todo Créer avec Succes !', False, True)
            return redirect(reverse('todo:todo-list'))
        except ValueError:
            define_toast_message(request, 'Impossible de créer deux même todo !', True)
    else:
        form = TodoForm()
    return render(request, 'todo/todo_create.html', {'form': form})


@clear_toast_messages
def todo_list(request):
    q = None
    if request.GET.get('q'):
        q = request.GET.get('q')
        todos = TODOO.objects.filter(title__contains=q, user=request.user)
    else:
        todos = TODOO.objects.filter(user=request.user)
    paginator = Paginator(todos, 3)
    page_number = request.GET.get('page', 1)
    page_obj = None
    try:
        page_obj = paginator.page(page_number)        
    except:
        return redirect(reverse('todo:todo-list'))

    return render(request, 'todo/todo_list.html', {'page_obj': page_obj, 'q': q})


@clear_toast_messages
def edit_todo(request, year, month, day, slug):
    todo = get_object_or_404(
        TODOO,
        created_at__year=year,
        created_at__month=month,
        created_at__day=day,
        slug=slug,
        user=request.user
    )

    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        try:
            form.save()
            define_toast_message(request, 'La todo a correctement été modifiée !', False, True)
            return redirect(reverse('todo:todo-list'))
        except ValueError:
            define_toast_message(request, 'Une todo porte déjà ce nom !', True, False)
    else:
        form = TodoForm(initial={'title': todo.title})
    return render(request, 'todo/edit_todo.html', {'todo': todo, 'form': form})


@clear_toast_messages
def delete_todo(request, todo_id):
    todo_to_delete = get_object_or_404(
        TODOO,
        id=todo_id,
        user=request.user
    )
    if request.method == 'POST':
        todo_to_delete.delete()
        request.user.profil.complete_task()
        define_toast_message(request, 'Todo completée ! + 7 points', False, True)
        return redirect(reverse('todo:todo-list'))
    else:
        return render(request, 'todo/delete_todo.html', {'todo': todo_to_delete})


def list_todo_reminders(request, todo_id):
    todo = get_object_or_404(
        TODOO, 
        id=todo_id,
        user=request.user
    )
    reminders = todo.reminders.filter(sent=False)

    return render(request, 'todo/todo_reminders_list.html', {'reminders': reminders})
    