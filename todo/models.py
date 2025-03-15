from django.db import models

from django.utils.text import slugify

from django.shortcuts import reverse

from django.contrib.auth.models import User

from django.conf import settings


class TODOO(models.Model):
    title = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(unique_for_date='created_at')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(TODOO, self).save(*args, **kwargs)

    def get_absolute_edit_todo_url(self):
        return reverse('todo:edit-todo', kwargs={
            'year': self.created_at.year,
            'month': self.created_at.month,
            'day': self.created_at.day,
            'slug': self.slug
        })

    def __str__(self):
        return self.title


class Reminder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task = models.ForeignKey(TODOO, on_delete=models.CASCADE, related_name='reminders')
    reminder_at = models.DateTimeField(db_index=True)
    sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['reminder_at']