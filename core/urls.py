from django.urls import path
from . import views
from reviews.views import submit_review, view_reviews

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('reviews/', views.show_more_reviews, name='show_more_reviews'),
    path('reviews/submit/', submit_review, name='submit_review'),
    path('reviews/view/', view_reviews, name='view_reviews'), 
    path('subscribe/', views.subscribe, name='subscribe'),
    
]