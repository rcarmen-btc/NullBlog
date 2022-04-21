from django.urls import path, include
from . import views

app_name = 'chunk'

urlpatterns = [
    path('', views.index, name='index'),
    path('form_get/', views.form_get, name='form_get'),
    path('form_post/', views.form_post, name='form_post'),
    path('form_class/', views.Guess.as_view(), name='form_class'),
    path('form_class_session/', views.GuessSession.as_view(), name='form_class_session'),
    path('cookies/', views.cookies, name='cookies'),
    path('sessions/', views.sessions, name='sessions'),
]
