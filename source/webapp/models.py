from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Project(models.Model):
    start_date = models.DateField(
        auto_now=False, verbose_name='Дата '
                                     'начала')
    end_date = models.DateField(null=True,
                                blank=True, verbose_name='Дата окончания')
    name = models.CharField(max_length=50,
                            verbose_name='Проект')
    project_description = models.TextField(
        max_length=3000,
        verbose_name='Описание проекта')
    is_deleted = models.BooleanField(
        default=False)
    users = models.ManyToManyField(
        get_user_model(),
        related_name='projects', blank=True,
        verbose_name='Пользователь')


    def get_absolute_url(self):
        return reverse('webapp:project_view',
                       kwargs={'pk': self.pk})


class Type(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тип')

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name='Статус')

    def __str__(self):
        return self.name


class Exercise(models.Model):
    title = models.CharField(max_length=100,
                             verbose_name='Заголовок')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Описание')
    status = models.ForeignKey('webapp.Status', related_name='exercises', on_delete=models.PROTECT, verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время редактирования')
    types = models.ManyToManyField(
        'webapp.Type',
        related_name='exercises', blank=True)
    project = models.ForeignKey(
        'webapp.Project',
        related_name='exercises',
        on_delete=models.PROTECT,
        verbose_name='Проект')

    def __str__(self):
        return f'{self.id}. {self.title}'

