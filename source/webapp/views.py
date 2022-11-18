from django.shortcuts import render
from webapp.models import Exercise, STATUS_CHOICES

# Create your views here.
def index_view(request):
    exercises = Exercise.objects.all()
    return render(request, 'index.html', {'exercises': exercises})

def create_ex(request, *args, **kwargs):
    if request.method == 'GET':
        return render(request, 'create.html', {'statuses': STATUS_CHOICES})
    elif request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status')
        todo_date = request.POST.get('todo_date')
        if not todo_date:
            todo_date = None
        new_ex = Exercise.objects.create(title=title, status=status, todo_date=todo_date)
        return render(request, 'exercise.html', {'exercise': new_ex})