from django import forms
from django.forms import widgets, ValidationError
from webapp.models import Exercise, Project

bad_words = ['shit', 'fuck', 'bitch', 'asshole']

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['title', 'description',
                  'status', 'types']
        widgets = {'types':
                       widgets.CheckboxSelectMultiple}


    def clean_title(self):
        title = self.cleaned_data['title']
        if title != title.capitalize():
          self.add_error('title',
                           ValidationError('Title must start with a capitalize!'))
        return title

    def clean_description(self):
        description = self.cleaned_data[
            'description']
        for bad in bad_words:
            if bad in description:
                self.add_error('description',
                           ValidationError(
                               "Please don't use bad words"))
        return description
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['is_deleted']
            # fields = ['start_date', 'end_date',
            #           'name', 'project_description']



class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=50,
                             required=False,
                             label='Найти')