from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from simple_history.models import HistoricalRecords
from simple_history.utils import update_change_reason
from django.db.models.signals import m2m_changed

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return self.name


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='notes')
    tags = models.ManyToManyField(Tag, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    is_favorite = models.BooleanField(default=False)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.pk:
            original = Note.objects.get(pk=self.pk)
            change_reason = []

            if original.title != self.title:
                change_reason.append("'title' updated")
            if original.content != self.content:
                change_reason.append("'content' updated")
            if original.category_id != self.category_id:
                change_reason.append("'category' updated")
            if original.is_favorite != self.is_favorite:
                change_reason.append("'favorite' updated")

            super().save(*args, **kwargs)

            if change_reason:
                latest_history = self.history.latest('history_date')
                latest_history.history_change_reason = ', '.join(change_reason)
                latest_history.save()

        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.title