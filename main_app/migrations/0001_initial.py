# Generated by Django 3.2.9 on 2021-12-04 23:53

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_title', models.CharField(help_text='No more than 50 characters', max_length=50, verbose_name='Project Name')),
                ('category_description', models.TextField(blank=True, null=True, verbose_name='Project Description')),
                ('category_author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL, verbose_name='Project Author')),
            ],
            options={
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('date_posted', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('deadline_date', models.DateField(null=True, verbose_name='Deadline date (mm/dd/yyyy)')),
                ('deadline_time', models.TimeField(null=True)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('complete', models.BooleanField(default=False)),
                ('priority', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium', max_length=6)),
                ('assigned_to', models.ManyToManyField(default='', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main_app.category', verbose_name='Project')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
                'ordering': ['complete', 'deadline_date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_posted', models.DateTimeField(auto_now_add=True, null=True)),
                ('content', models.TextField(blank=True, default='', null=True)),
                ('is_published', models.BooleanField(default=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.item', verbose_name='for task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='by user')),
            ],
            options={
                'ordering': ['-date_posted'],
            },
        ),
    ]