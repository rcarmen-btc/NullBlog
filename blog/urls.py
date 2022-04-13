from django.urls import path, include

from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('<slug:post_slug>/', views.post_single, name='post_single')
]
