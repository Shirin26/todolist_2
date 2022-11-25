from django.contrib import admin
from webapp.models import Exercise, Status, Type
# Register your models here.

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'status', 'type']
    list_filter = ['status']
    search_fields = ['title']
    exclude = []

admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Status)
admin.site.register(Type)
