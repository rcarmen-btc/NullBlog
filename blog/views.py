from django.utils import timezone

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.template.defaulttags import register

from . import models
from . import forms


def home(request):
    context = {
        'posts': models.Post.newmanager.all(),
        'categories': models.Category.objects.all(),
        'tags': models.Tag.objects.all()
    }
    # print(context['posts'])
    return render(request, 'blog/home.html', context)


class PostDetailView(DetailView):

    model = models.Post
    template_name = 'blog/post_detail_view.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'post_slug'

    def get_queryset(self):
        return models.Post.objects.filter(slug=self.kwargs['post_slug'])

    def get_context_data(self, **kwargs):
        post = get_object_or_404(models.Post, slug=self.kwargs['post_slug'], status=models.Post.Status.PUBLISHED)
        context = super().get_context_data(**kwargs)
        context['comments'] = post.comments.filter(status=True)
        context['comments_form'] = forms.NewComment()
        return context

    def post(self, request, **kwargs):
        post = get_object_or_404(models.Post, slug=self.kwargs['post_slug'], status=models.Post.Status.PUBLISHED)
        comments = post.comments.filter(status=True)
        user_comment = None
        comment_form = forms.NewComment(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.save()
        return HttpResponseRedirect('/' + kwargs['post_slug'])


# def post_single(request, post_slug):
#
#     post = get_object_or_404(models.Post, slug=post_slug, status=models.Post.Status.PUBLISHED)
#
#     comments = post.comments.filter(status=True)
#
#     user_comment = None
#
#     if request.method == 'POST':
#         comment_form = forms.NewComment(request.POST)
#         if comment_form.is_valid():
#             user_comment = comment_form.save(commit=False)
#             user_comment.post = post
#             user_comment.save()
#             return HttpResponseRedirect('/' + post_slug)
#     else:
#         comment_form = forms.NewComment()
#
#     context = {
#         'post': post,
#         # 'comments': user_comment,
#         'comments': comments,
#         'category': post.category,
#         'comments_form': comment_form,
#     }
#     return render(request, 'blog/post_single.html', context)


class CategoryListView(ListView):

    template_name = 'blog/category.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {
            'current_category': self.kwargs['category_slug'],
            'posts': models.Post.objects.filter(category__slug=self.kwargs['category_slug']).filter(status=models.Post.Status.PUBLISHED),
            'categories': models.Category.objects.all(),
            'tags': models.Tag.objects.all(),
        }
        return content

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = models.Tag.objects.all()
        return context

class TagListView(ListView):

    template_name = 'blog/tag.html'
    context_object_name = 'taglist'

    def get_queryset(self):
        return models.Post.objects.filter(tags__slug=self.kwargs['tag_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['categories'] = models.Category.objects.all()
        context['posts'] = models.Post.objects.filter(tags__slug=self.kwargs['tag_slug'])
        context['tags'] = models.Tag.objects.all()
        return context
