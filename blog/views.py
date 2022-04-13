from django.shortcuts import render, get_object_or_404

from . import models


def home(request):
    context = {
        'posts': models.Post.newmanager.all(),
    }
    return render(request, 'blog/home.html', context)
    # return render(request, 'blog/home.html')


def post_single(request, post_slug):
    context = {
        'post': get_object_or_404(models.Post, slug=post_slug, status=models.Post.Status.PUBLISHED)
    }
    return render(request, 'blog/post_single.html', context)
