from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    # return f'photos/{instance.id}/{filename}'
    return f'photos/%Y/%m/%d'


class Category(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):

    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status=Post.Status.PUBLISHED)

    class Status(models.TextChoices):
        DRAFT = 'draft'
        PUBLISHED = 'published'

    title = models.CharField(max_length=250)
    photo = models.ImageField(upload_to=user_directory_path, default='photos/default.png')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(max_length=250, unique_for_date='publish_date')
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', default=User)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    objects = models.Manager()
    newmanager = NewManager()

    def get_absolute_url(self):
        return reverse('blog:post_single', args=[self.slug])

    class Meta:
        get_latest_by = ['publish_date']
        ordering = ['-publish_date']

    def __str__(self):
        return self.title


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('-publish_date', )

    def __str__(self):
        return f'Comment by {self.name}'
