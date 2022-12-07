from django.contrib import admin
from webapp.models import Exercise, Status, \
    Type, Project

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'status']
    list_filter = ['status']
    search_fields = ['title']
    exclude = []

admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Project)
