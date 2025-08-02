from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Review
from django.contrib.messages import get_messages
from datetime import datetime
from .forms import ReviewForm
from django.utils import timezone

########## PASS ############
class ReviewModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.review = Review.objects.create(
            user=self.user,
            rating=5,
            comment="This is a test review.",
            created_at=timezone.now()
        )

    def test_review_creation(self):
        review = Review.objects.get(id=self.review.id)
        self.assertEqual(review.user.username, 'testuser')
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "This is a test review.")
        self.assertIsInstance(review.created_at, timezone.datetime)

    def test_review_str(self):
        review = Review.objects.get(id=self.review.id)
        self.assertEqual(str(review), 'Review by testuser - Rating: 5')

    def test_review_rating_choices(self):
        for i in range(1, 6):
            review = Review.objects.create(
                user=self.user,
                rating=i,
                comment=f"Rating {i} test review.",
                created_at=timezone.now()
            )
            self.assertIn(review.rating, [1, 2, 3, 4, 5])

    def test_review_update(self):
        self.review.rating = 3
        self.review.comment = "Updated review comment."
        self.review.save()
        review = Review.objects.get(id=self.review.id)
        self.assertEqual(review.rating, 3)
        self.assertEqual(review.comment, "Updated review comment.")

    def test_review_delete(self):
        self.review.delete()
        with self.assertRaises(Review.DoesNotExist):
            Review.objects.get(id=self.review.id)


########## PASS ############
class SubmitReviewViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_get_submit_review_view(self):
        response = self.client.get(reverse('submit_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/submit_review.html')
        self.assertContains(response, '<form')

    def test_post_submit_review_view(self):
        post_data = {
            'rating': 5,
            'comment': 'Great product!'
        }
        response = self.client.post(reverse('submit_review'), data=post_data, follow=True)
        
        # Debugging: Print form errors if the response code is 200
        if response.status_code == 200:
            form = ReviewForm(data=post_data)
            if not form.is_valid():
                print(form.errors)
        
        self.assertRedirects(response, reverse('home'))

        # Check if the review was created
        self.assertTrue(Review.objects.filter(comment='Great product!').exists())

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'Your review has been added successfully!' for message in messages))


############## PASS ##############
class ViewReviewsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.review1 = Review.objects.create(user=self.user, rating=5, comment='Excellent!', created_at=datetime.now())
        self.review2 = Review.objects.create(user=self.user, rating=4, comment='Good!', created_at=datetime.now())

    def test_view_reviews_view(self):
        response = self.client.get(reverse('view_reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/show_more_reviews.html')
        self.assertContains(response, 'Excellent!')
        self.assertContains(response, 'Good!')


############ PASS ###########
class ReviewFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {'rating': 5, 'comment': 'Great product!'}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_rating(self):
        form_data = {'comment': 'Great product!'}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_invalid_form_invalid_rating(self):
        form_data = {'rating': 6, 'comment': 'Great product!'}  # Invalid rating (should be 1-5)
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_invalid_form_missing_comment(self):
        form_data = {'rating': 5}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('comment', form.errors)

    def test_widgets(self):
        form = ReviewForm()
        self.assertEqual(form.fields['rating'].widget.__class__.__name__, 'RadioSelect')
        self.assertEqual(form.fields['comment'].widget.__class__.__name__, 'Textarea')
