from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):

    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status=Post.Status.PUBLISHED)

    class Status(models.TextChoices):
        DRAFT = 'draft'
        PUBLISHED = 'published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish_date')
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', default=User)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    object = models.Manager()
    newmanager = NewManager()

    class Meta:
        get_latest_by = ['publish_date']
        ordering = ['-publish_date']

    def __str__(self):
        return self.title

