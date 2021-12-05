import datetime
from django.utils import timezone

from django.db import models
from django.contrib.auth import get_user_model as user_model
from ckeditor_uploader.fields import RichTextUploadingField

User = user_model()


class Category(models.Model):
    category_title = models.CharField('Project Name', max_length=50, help_text='No more than 50 characters')
    category_description = models.TextField('Project Description', blank=True, null=True)
    category_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories',
                                        verbose_name='Project Author',
                                        blank=True,
                                        null=True)

    def __str__(self):
        return self.category_title

    class Meta:
        verbose_name_plural = 'Projects'


# aka Task
class Item(models.Model):
    User = user_model()
    category_list = Category.objects.all()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='', verbose_name="Project")
    title = models.CharField(max_length=200)
    description = RichTextUploadingField()
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE, default='')
    assigned_to = models.ManyToManyField(User, default='')
    date_posted = models.DateTimeField(null=True, blank=True, default=timezone.now)  # to make field editable in admin
    deadline_date = models.DateField(null=True, verbose_name='Deadline date (mm/dd/yyyy)')
    deadline_time = models.TimeField(null=True)
    deadline = models.DateTimeField(null=True, blank=True)  # deprecated in this project
    complete = models.BooleanField(default=False)

    # in templates: item.deadline_date_time
    def deadline_date_time(self):
        return datetime.datetime.combine(self.deadline_date, self.deadline_time)

    def __str__(self):
        return f'{self.title}'

    @property
    def monthposted(self):
        return int(self.date_posted.strftime('%m'))

    class Priority(models.TextChoices):
        low = 'Low'
        medium = 'Medium'
        high = 'High'

    priority = models.CharField(
        max_length=6,
        choices=Priority.choices,
        default=Priority.medium,
    )

    class Meta:
        ordering = ['complete', 'deadline_date']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


#  Comments
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='by user')
    date_posted = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='for task')
    content = models.TextField(null=True, blank=True, default='')
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f'Comment by {self.user}'
