from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm

@login_required
def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been added successfully!')
            return redirect('home')
    else:
        form = ReviewForm()
    return render(request, 'reviews/submit_review.html', {'form': form})


def view_reviews(request):
    reviews = Review.objects.all()
    return render(request, 'core/show_more_reviews.html', {'reviews': reviews})

