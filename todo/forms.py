from django import forms

from .models import TODOO

class TodoForm(forms.ModelForm):
    class Meta:
        model = TODOO
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input-custom', 'placeholder': 'titre'})
        }