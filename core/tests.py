from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from reviews.models import Review
from .models import Profile

######### PASS ############
class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.profile, created = Profile.objects.get_or_create(user=self.user)

    def test_profile_creation(self):
        profile = Profile.objects.get(id=self.profile.id)
        self.assertEqual(profile.user.username, 'testuser')
        self.assertTrue(profile.is_subscribed)

    def test_profile_str(self):
        profile = Profile.objects.get(id=self.profile.id)
        self.assertEqual(str(profile), 'testuser Profile')

    def test_profile_default_values(self):
        profile = Profile.objects.get(id=self.profile.id)
        self.assertTrue(profile.is_subscribed)

    def test_profile_update(self):
        self.profile.is_subscribed = False
        self.profile.save()
        profile = Profile.objects.get(id=self.profile.id)
        self.assertFalse(profile.is_subscribed)

    def test_profile_delete(self):
        self.profile.delete()
        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(id=self.profile.id)



############## PASS ################
class HomeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create test reviews
        self.review1 = Review.objects.create(user=self.user, rating=5, comment="Great!", created_at="2023-01-01")
        self.review2 = Review.objects.create(user=self.user, rating=4, comment="Good", created_at="2023-01-02")
        self.review3 = Review.objects.create(user=self.user, rating=3, comment="Average", created_at="2023-01-03")

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
        self.assertContains(response, 'Great!')
        self.assertContains(response, 'Good')
        self.assertContains(response, 'Average')

    

########### PASS ##############
class ShowMoreReviewsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create test reviews
        self.review1 = Review.objects.create(user=self.user, rating=5, comment="Great!", created_at="2023-01-01")
        self.review2 = Review.objects.create(user=self.user, rating=4, comment="Good", created_at="2023-01-02")
        self.review3 = Review.objects.create(user=self.user, rating=3, comment="Average", created_at="2023-01-03")
        self.review4 = Review.objects.create(user=self.user, rating=2, comment="Below average", created_at="2023-01-04")

    def test_show_more_reviews_view(self):
        response = self.client.get(reverse('show_more_reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/show_more_reviews.html')
        self.assertContains(response, 'Great!')
        self.assertContains(response, 'Below average')
############ PASS ################
class ContactViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_view(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')

################ FAIL #############
class SubscribeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        self.client.login(username='testuser', password='testpassword')

    def test_subscribe_view(self):
        response = self.client.post(reverse('subscribe'))
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.is_subscribed)
        self.assertRedirects(response, reverse('home'))

    def test_unsubscribe_view(self):
        self.profile.is_subscribed = True
        self.profile.save()
        response = self.client.post(reverse('subscribe'))
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.is_subscribed)
        self.assertRedirects(response, reverse('home'))

############# PASS #################
class Handler404ViewTestCase(TestCase):
    def test_handler404_view(self):
        response = self.client.get('/nonexistentpage/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'errors/404.html')

