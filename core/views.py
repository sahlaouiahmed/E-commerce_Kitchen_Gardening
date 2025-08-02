from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Profile
from reviews.models import Review

def home(request):
    # Retrieve the latest three reviews and render the home page with those reviews
    reviews = Review.objects.all().order_by('-created_at')[:3]  # Retrieve the latest three reviews
    return render(request, 'core/home.html', {'reviews': reviews})

def show_more_reviews(request):
    # Retrieve all reviews ordered by creation date and render the show more reviews page
    reviews = Review.objects.all().order_by('-created_at')  # Retrieve all reviews ordered by creation date
    return render(request, 'core/show_more_reviews.html', {'reviews': reviews})

def contact(request):
    # Render the contact page
    return render(request, 'core/contact.html')


@login_required
def subscribe(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile.is_subscribed = not profile.is_subscribed
    profile.save()
    action = "subscribed" if profile.is_subscribed else "unsubscribed"

    if profile.is_subscribed:
        messages.success(request, 'You have successfully subscribed to the newsletter. Welcome aboard!')
        email_subject = 'Subscription Confirmation'
        email_body = (
            f"Dear {request.user.username},\n\n"
            f"Thank you for subscribing to our newsletter! Stay tuned for the latest updates, tips, and special offers.\n\n"
            f"Best regards,\n"
            f"The Kitchen Garden Team"
        )
    else:
        messages.success(request, 'You have successfully unsubscribed from the newsletter. We hope to see you back soon!')
        email_subject = 'Unsubscription Confirmation'
        email_body = (
            f"Dear {request.user.username},\n\n"
            f"You have been unsubscribed from our newsletter. We're sorry to see you go, but you can always subscribe again for more updates.\n\n"
            f"Best regards,\n"
            f"The Kitchen Garden Team"
        )

    try:
        send_mail(
            email_subject,
            email_body,
            'kitchengardenci@gmail.com',
            [request.user.email],
            fail_silently=False,
        )
        messages.info(request, "A confirmation email has been sent to your email address.")
    except Exception as e:
        messages.error(request, f"There was an error sending the confirmation email: {e}")

    return redirect('home')




def handler404(request, exception):
    """ Error Handler 404 - Page Not Found """
    # Render the custom 404 error page
    return render(request, "errors/404.html", status=404)
