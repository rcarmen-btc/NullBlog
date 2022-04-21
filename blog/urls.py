from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.home, name='homepage'),
    # path('<slug:post_slug>/', views.post_single, name='post_single'),
    path('<slug:post_slug>/', views.PostDetailView.as_view(), name='post_single'),
    path('category/<slug:category_slug>/', views.CategoryListView.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagListView.as_view(), name='tag'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
