from django.shortcuts import render
from webapp.models import Exercise

# Create your views here.
def index_view(request):
    exercises = Exercise.objects.all()
    return render(request, 'index.html', {'exercises': exercises})