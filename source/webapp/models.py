from django.db import models

STATUS_CHOICES = [('new', 'Новая'), ('in_progress', 'В процессе'),  ('done', 'Сделано')]

class Exercise(models.Model):
    title = models.CharField(max_length=100, verbose_name='Описание')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0], verbose_name='Статус')
    todo_date = models.DateField(null=True, blank=True, verbose_name='Дата выполнения')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.id}. {self.title}'