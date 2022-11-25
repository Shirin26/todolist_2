from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тип')

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name='Статус')

    def __str__(self):
        return self.name


class Exercise(models.Model):
    title = models.CharField(max_length=100, verbose_name='Описание')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Описание')
    status = models.ForeignKey('webapp.Status', related_name='exercises', on_delete=models.PROTECT, verbose_name='Статус')
    type = models.ForeignKey('webapp.Type', related_name='exercises', on_delete=models.PROTECT, verbose_name='Тип')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время редактирования')


    def __str__(self):
        return f'{self.id}. {self.title}'

