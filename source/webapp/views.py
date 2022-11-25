from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import Exercise
from webapp.forms import ExerciseForm
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exercises'] = Exercise.objects.all()
        return context


class ExerciseView(TemplateView):
    template_name = 'exercise.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exercise'] = get_object_or_404(Exercise, pk=kwargs['pk'])
        return context


class CreateExercise(TemplateView):
    template_name = 'create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ExerciseForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ExerciseForm(data=request.POST)
        if form.is_valid():
            exercise = Exercise.objects.create(**form.cleaned_data)
            return redirect('exercise_view', pk=exercise.pk)
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


def exercise_update_view(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'GET':
        form = ExerciseForm(initial={
            'title': exercise.title,
            'status': exercise.status,
            'todo_date': exercise.todo_date,
            'description': exercise.description
        })
        return render(request, 'exercise_update.html', {'statuses': '', 'form': form})
    elif request.method == 'POST':
        if request.method == 'POST':
            form = ExerciseForm(data=request.POST)
            if form.is_valid():
                exercise.title = form.cleaned_data.get('title')
                exercise.status = form.cleaned_data.get('status')
                exercise.description = form.cleaned_data.get('description')
                exercise.todo_date = form.cleaned_data.get('todo_date')
                exercise.save()
                return redirect('exercise_view', pk=exercise.pk)
            else:
                return render(request, 'exercise_update.html', {'statuses': '', 'form': form})

def exercise_delete_view(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'GET':
        return render(request, 'exercise_delete.html', {'exercise': exercise})
    elif request.method == 'POST':
        exercise.delete()
        return redirect('index')

