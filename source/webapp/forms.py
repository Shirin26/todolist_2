from django import forms
from django.forms import widgets
class ExerciseForm(forms.Form):
    title = forms.CharField(max_length=100, required=True, label='Title')
    status = forms.CharField(max_length=50, required=True, label='Status')
    todo_date = forms.DateField(required=False, label='Todo_date')
    description = forms.CharField(max_length=3000, required=False, label='Description', widget=widgets.Textarea)