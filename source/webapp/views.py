from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import Exercise, STATUS_CHOICES
from webapp.forms import ExerciseForm

# Create your views here.
def index_view(request):
    if request.method == 'POST':
        exercise_id = request.GET.get('id')
        exercise = Exercise.objects.get(id=exercise_id)
        exercise.delete()
        return redirect('index')

    exercises = Exercise.objects.all()
    return render(request, 'index.html', {'exercises': exercises})

def exercise_view(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    return render(request, 'exercise.html', {'exercise': exercise})

def create_ex(request, *args, **kwargs):
    if request.method == 'GET':
        form = ExerciseForm()
        return render(request, 'create.html', {'statuses': STATUS_CHOICES, 'form': form})
    elif request.method == 'POST':
        form = ExerciseForm(data=request.POST)
        if form.is_valid():
            new_exercise = Exercise.objects.create(
                title=form.cleaned_data['title'],
                status=form.cleaned_data['status'],
                todo_date=form.cleaned_data['todo_date'],
                description=form.cleaned_data['description']
            )
            return redirect('exercise_view', pk=new_exercise.pk)
        else:
            return render(request, 'create.html', {'statuses': STATUS_CHOICES, 'form': form})


def exercise_update_view(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'GET':
        form = ExerciseForm(initial={
            'title': exercise.title,
            'status': exercise.status,
            'todo_date': exercise.todo_date,
            'description': exercise.description
        })
        return render(request, 'exercise_update.html', {'statuses': STATUS_CHOICES, 'form': form})
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
                return render(request, 'exercise_update.html', {'statuses': STATUS_CHOICES, 'form': form})

def exercise_delete_view(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'GET':
        return render(request, 'exercise_delete.html', {'exercise': exercise})
    elif request.method == 'POST':
        exercise.delete()
        return redirect('index')

