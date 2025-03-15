from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from .views import signup, profile, account_settings, logout_account, stats_reset, delete_account, change_display_mode, register, ranking_list

app_name = 'account'

urlpatterns = [
    # Retrieve password
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='account/registration/password_reset_form.html', 
        email_template_name='account/registration/password_reset_email.html',
        success_url=reverse_lazy('account:password_reset_done')
    ),  
    name='password_reset'),

    path('password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='account/registration/password_reset_done.html',
        ), 
        name='password_reset_done'
    ),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/registration/password_reset_confirm.html',
        success_url=reverse_lazy('account:password_reset_complete')
    ), 
    name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/registration/password_reset_complete.html'
        
    ), 
    name='password_reset_complete'),

    path('signup/', signup, name='signup'),
    path('register/', register, name='register'),
    path('change-display-mode/', change_display_mode, name='change-display-mode'),
    path('logout/', logout_account, name='logout'),
    path('profile/', profile, name='profile'),
    path('delete/', delete_account, name='delete'),
    path('settings/', account_settings, name='account-settings'),
    path('stats-reset/', stats_reset, name='stats-reset'),
    path('ranking-list/', ranking_list, name='ranking-list')
] 