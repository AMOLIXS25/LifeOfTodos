from django import forms

from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input-custom mb-3', 'placeholder': "Nom d'utilisateur"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input-custom mb-3', 'placeholder': 'Mot de passe'}))

class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input-custom mb-3', 'placeholder': "Nom d'utilsateur"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input-custom mb-3', 'placeholder': "Mot de passe"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input-custom mb-3', 'placeholder': "Confirmer le mot de passe"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-input-custom mb-3', 'placeholder': 'Email'}))
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email']
    

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input-custom'})
        }


CHOICES = [
    ('dark', 'Sombre'),
    ('light', 'Clair'),
]

class DisplayModeForm(forms.Form):
    my_select = forms.ChoiceField(choices=CHOICES, label="", widget=forms.Select(attrs={'class': 'form-input-custom'}))