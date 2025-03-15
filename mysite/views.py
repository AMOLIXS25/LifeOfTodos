from django.shortcuts import render, redirect, reverse

from .middlewares import clear_toast_messages

@clear_toast_messages
def home(request):
    if request.user.is_authenticated:
        return redirect(reverse('todo:todo-list'))
    return render(request, 'home.html', {})

def contact(request):
    return render(request, 'contact.html', {})