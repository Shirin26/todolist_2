from django import forms
from django.forms import widgets, ValidationError
from webapp.models import Type, Status, Exercise

# class ExerciseForm(forms.Form):
#     title = forms.CharField(max_length=100, required=True, label='Title')
#     description = forms.CharField(max_length=3000, required=False, label='Description', widget=widgets.Textarea)
#     status = forms.ModelChoiceField(queryset=Status.objects.all(), required=True, label='Status')
#     types = forms.ModelMultipleChoiceField(
#         queryset=Type.objects.all(),
#         required=False, label='Типы',
#         widget=widgets.CheckboxSelectMultiple)

bad_words = ['shit', 'fuck', 'bitch', 'asshole']

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['title', 'description',
                  'status', 'types']
        widgets = {'types':
                       widgets.CheckboxSelectMultiple}
        # error_messages

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


