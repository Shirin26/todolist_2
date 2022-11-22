from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import Exercise, STATUS_CHOICES
from django.urls import reverse

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
        return render(request, 'create.html', {'statuses': STATUS_CHOICES})
    elif request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status')
        description = request.POST.get('description')
        todo_date = request.POST.get('todo_date')

        if not todo_date:
            todo_date = None

        new_ex = Exercise.objects.create(title=title, status=status, todo_date=todo_date, description=description)
        return redirect('exercise_view', pk=new_ex.pk)

def exercise_update_view(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'GET':
        return render(request, 'exercise_update.html', {'exercise': exercise})
    elif request.method == 'POST':
        exercise.title = request.POST.get('title')
        exercise.status = request.POST.get('status')
        exercise.description = request.POST.get('description')
        exercise.todo_date = request.POST.get('todo_date')
        exercise.save()
        return redirect('exercise_view', pk=exercise.pk)

def exercise_delete_view(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'GET':
        return render(request, 'exercise_delete.html', {'exercise': exercise})
    elif request.method == 'POST':
        exercise.delete()
        return redirect('index')

