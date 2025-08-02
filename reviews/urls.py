from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_review, name='submit_review'),
    path('view/', views.view_reviews, name='view_reviews'),
]
