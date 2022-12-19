from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='Электронная почта', required=True)
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1',
                  'password2', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get(
            'first_name')
        last_name = cleaned_data.get(
            'last_name')
        if not last_name and not first_name:
            raise forms.ValidationError(
                "Заполните одно из полей: First name или Last name!")
        return cleaned_data


