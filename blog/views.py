from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.template.defaulttags import register

from . import models
from . import forms


def home(request):
    context = {
        'posts': models.Post.newmanager.all(),
        'categories': models.Category.objects.all()
    }
    return render(request, 'blog/home.html', context)
    # return render(request, 'blog/home.html')


def post_single(request, post_slug):

    post = get_object_or_404(models.Post, slug=post_slug, status=models.Post.Status.PUBLISHED)

    comments = post.comments.filter(status=True)

    user_comment = None

    if request.method == 'POST':
        comment_form = forms.NewComment(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.save()
            return HttpResponseRedirect('/' + post_slug)
    else:
        comment_form = forms.NewComment()

    context = {
        'post': post,
        # 'comments': user_comment,
        'comments': comments,
        'comments_form': comment_form,
    }
    return render(request, 'blog/post_single.html', context)


class CategoryListView(ListView):

    template_name = 'blog/category.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {
            'current_category': self.kwargs['category_slug'],
            'posts': models.Post.objects.filter(category__slug=self.kwargs['category_slug']).filter(status=models.Post.Status.PUBLISHED),
            'categories': models.Category.objects.all()
        }
        return content
