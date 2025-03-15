from django.shortcuts import render, redirect, reverse

from django.contrib.auth import logout, authenticate, login


from .models import Profile, CustomUser
from .forms import UserForm, DisplayModeForm, LoginForm, RegisterForm
from mysite.middlewares import clear_toast_messages
from mysite.utils import define_toast_message


@clear_toast_messages
def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.set_password(register_form.cleaned_data['password1']) 
            new_user.save() 
            login(request, new_user, backend="django.contrib.auth.backends.ModelBackend")
            define_toast_message(request, f'Bienvenue {new_user} !', False, True)
            return redirect(reverse('todo:todo-list'))
    else:
        register_form = RegisterForm()
    return render(request, 'account/register.html', {'register_form': register_form})


@clear_toast_messages
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'account/profile.html', {'profile': profile})


@clear_toast_messages
def signup(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(request, username=cd.get('username'), password=cd.get('password'))
            if user is not None:
                if user.is_active:
                    login(request, user)
                    define_toast_message(request, f'Content de te revoir {request.user} !', False, True)
                    return redirect(reverse('todo:todo-list'))
                else:
                    define_toast_message(request, 'Votre compte a été désactivé !', True, False)
            else:
                define_toast_message(request, 'Compte introuvable !', True, False)
    else:
        login_form = LoginForm()
    return render(request, 'account/signup.html', {'login_form': login_form})


@clear_toast_messages
def account_settings(request):
    display_mode_form = DisplayModeForm(initial={'my_select': request.user.profil.get_display_mode_display()})
    if request.method == 'POST' and request.POST['username']:
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            define_toast_message(request, "Votre nom d'utilisateur à été mis à jours !", False, False)
    else:
        user_form = UserForm(instance=request.user) 
    return render(request, 'account/settings.html', {'user_form': user_form, 'display_mode_form': display_mode_form})

def change_display_mode(request):
    if request.method == 'POST':
        display_mode_form = DisplayModeForm(request.POST)
        if display_mode_form.is_valid():
            print('ok')
            selected_option = display_mode_form.cleaned_data['my_select']
            print(selected_option)
            request.user.profil.update_display_mode(selected_option)
    return redirect(reverse('account:account-settings'))


@clear_toast_messages
def stats_reset(request):
    if request.method == 'POST':
        request.user.profil.reset_stats()
        define_toast_message(request, 'Vos stats on correctement été reset !', False, True)
        return redirect(reverse('account:profile'))
    return render(request, 'account/stats_reset.html', {})

def logout_account(request):
    logout(request)
    return redirect(reverse('home'))


@clear_toast_messages
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        if username == user.username:
            logout(request)
            user.delete()       
            define_toast_message(request, 'Ton compte à correctement été supprimé !', False, True)
    return redirect(reverse('home'))

def ranking_list(request):
    users = CustomUser.objects.order_by('-profil__points')
    return render(request, 'account/ranking-list.html', {'users': users})