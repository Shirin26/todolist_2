from django.contrib import admin
from webapp.models import Exercise
# Register your models here.

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'status', 'todo_date']
    list_filter = ['status']
    search_fields = ['title']
    exclude = []

admin.site.register(Exercise, ExerciseAdmin)