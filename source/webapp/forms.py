from django import forms
from django.forms import widgets
from webapp.models import Type, Status
class ExerciseForm(forms.Form):
    title = forms.CharField(max_length=100, required=True, label='Title')
    description = forms.CharField(max_length=3000, required=False, label='Description', widget=widgets.Textarea)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=True, label='Status')
    types = forms.ModelMultipleChoiceField(
        queryset=Type.objects.all(),
        required=False, label='Типы')
