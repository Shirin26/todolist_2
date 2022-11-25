# Generated by Django 4.1.3 on 2022-11-25 09:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_exercise_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Тип')),
            ],
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='todo_date',
        ),
        migrations.AddField(
            model_name='exercise',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Время создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exercise',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Время редактирования'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='exercises', to='webapp.type', verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='exercises', to='webapp.status', verbose_name='Статус'),
        ),
    ]
