from django.urls import path
from . import views
from .views import add_article, edit_article, delete_article

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('<int:pk>/', views.article_detail, name='article_detail'),
    #SUPERUSER
    path('add/', add_article, name='add_article'), 
    path('edit/<int:pk>/', edit_article, name='edit_article'), 
    path('delete/<int:pk>/', delete_article, name='delete_article'),
]
