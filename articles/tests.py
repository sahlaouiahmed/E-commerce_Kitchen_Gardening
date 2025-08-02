from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from articles.forms import ArticleForm
from .models import Article
import os
from django.utils import timezone

############## PASS ############
class ArticleModelTest(TestCase):

    def setUp(self):
        self.article = Article.objects.create(
            title="Test Article",
            content="This is a test article.",
            image="static/images/articles/test.jpg",
            published_date=timezone.now(),
            updated_date=timezone.now()
        )

    def test_article_creation(self):
        article = Article.objects.get(id=self.article.id)
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(article.content, "This is a test article.")
        self.assertEqual(article.image, "static/images/articles/test.jpg")
        self.assertEqual(str(article), "Test Article")

    def test_article_str(self):
        article = Article.objects.get(id=self.article.id)
        self.assertEqual(str(article), article.title)

    def test_article_default_values(self):
        article = Article.objects.get(id=self.article.id)
        self.assertIsInstance(article.published_date, timezone.datetime)
        self.assertIsInstance(article.updated_date, timezone.datetime)

    def test_article_update(self):
        self.article.title = "Updated Article"
        self.article.save()
        article = Article.objects.get(id=self.article.id)
        self.assertEqual(article.title, "Updated Article")
        self.assertNotEqual(article.updated_date, article.published_date)

    def test_article_delete(self):
        self.article.delete()
        with self.assertRaises(Article.DoesNotExist):
            Article.objects.get(id=self.article.id)


############## PASS ###############
class ArticleListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create a dummy image file
        dummy_image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        
        # Create test articles with the dummy image
        self.article1 = Article.objects.create(
            title='Test Article 1',
            content='This is the first test article.',
            image=dummy_image,
            published_date=datetime(2023, 1, 1),
        )
        self.article2 = Article.objects.create(
            title='Another Test Article',
            content='This is the second test article.',
            image=dummy_image,
            published_date=datetime(2023, 1, 2),
        )

    def test_article_list_view(self):
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article_list.html')
        self.assertContains(response, 'Test Article 1')
        self.assertContains(response, 'Another Test Article')

    def test_article_list_view_with_query(self):
        response = self.client.get(reverse('article_list'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article_list.html')
        self.assertContains(response, 'Test Article 1')
        self.assertContains(response, 'Another Test Article')

    def test_article_list_view_with_non_matching_query(self):
        response = self.client.get(reverse('article_list'), {'q': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article_list.html')
        self.assertNotContains(response, 'Test Article 1')
        self.assertNotContains(response, 'Another Test Article')

############## PASS ################
class ArticleDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create a dummy image file
        dummy_image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        
        # Create a test article with the dummy image
        self.article = Article.objects.create(
            title='Test Article',
            content='This is a test article.',
            image=dummy_image,
            published_date=datetime(2023, 1, 1),
        )

    def test_article_detail_view(self):
        response = self.client.get(reverse('article_detail', kwargs={'pk': self.article.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article_detail.html')
        self.assertContains(response, 'Test Article')
        self.assertContains(response, 'This is a test article.')

############## PASS #############
class AddArticleViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username='testsuperuser', password='testpassword')
        self.client.login(username='testsuperuser', password='testpassword')

    def test_get_add_article_view(self):
        response = self.client.get(reverse('add_article'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/add_article.html')
        self.assertContains(response, '<form')

    def test_post_add_article_view(self):
        # Correct path to the test image file
        image_path = os.path.join(os.path.dirname(__file__), '../static/images/articles/test_image.png')
        with open(image_path, 'rb') as img_file:
            dummy_image = SimpleUploadedFile(name='test_image.png', content=img_file.read(), content_type='image/png')
            post_data = {
                'title': 'Test Article',
                'content': 'This is a test article.',
                'published_date': datetime.now(),
                'image': dummy_image
            }
            response = self.client.post(reverse('add_article'), data=post_data, follow=True)
        
        # Debugging: Print form errors if the response code is 200
        if response.status_code == 200:
            form = ArticleForm(data=post_data, files={'image': dummy_image})
            if not form.is_valid():
                print(form.errors)
        
        self.assertRedirects(response, reverse('article_list'))
        
        # Check if the article was created
        self.assertTrue(Article.objects.filter(title='Test Article').exists())

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'Article added successfully!' for message in messages))

############# PASS #################
class EditArticleViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username='testsuperuser', password='testpassword')
        self.client.login(username='testsuperuser', password='testpassword')

        # Create a dummy image file
        image_path = os.path.join(os.path.dirname(__file__), '../static/images/articles/test_image.png')
        with open(image_path, 'rb') as img_file:
            dummy_image = SimpleUploadedFile(name='test_image.png', content=img_file.read(), content_type='image/png')
            self.article = Article.objects.create(
                title='Original Title',
                content='Original Content',
                image=dummy_image,
                published_date=datetime(2023, 1, 1),
            )

    def test_get_edit_article_view(self):
        response = self.client.get(reverse('edit_article', kwargs={'pk': self.article.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/edit_article.html')
        self.assertContains(response, '<form')

    def test_post_edit_article_view(self):
        image_path = os.path.join(os.path.dirname(__file__), '../static/images/articles/test_image.png')
        with open(image_path, 'rb') as img_file:
            dummy_image = SimpleUploadedFile(name='test_image.png', content=img_file.read(), content_type='image/png')
            post_data = {
                'title': 'Updated Title',
                'content': 'Updated Content',
                'published_date': datetime.now(),
                'image': dummy_image
            }
            response = self.client.post(reverse('edit_article', kwargs={'pk': self.article.pk}), data=post_data, follow=True)

        # Debugging: Print form errors if the response code is 200
        if response.status_code == 200:
            form = ArticleForm(data=post_data, files={'image': dummy_image}, instance=self.article)
            if not form.is_valid():
                print(form.errors)

        self.assertRedirects(response, reverse('article_list'))

        # Check if the article was updated
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated Title')
        self.assertEqual(self.article.content, 'Updated Content')

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'Article updated successfully!' for message in messages))

############### PASS ###############
class DeleteArticleViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username='testsuperuser', password='testpassword')
        self.client.login(username='testsuperuser', password='testpassword')

        # Create a dummy image file
        image_path = os.path.join(os.path.dirname(__file__), '../static/images/articles/test_image.png')
        with open(image_path, 'rb') as img_file:
            dummy_image = SimpleUploadedFile(name='test_image.png', content=img_file.read(), content_type='image/png')
            self.article = Article.objects.create(
                title='Test Article',
                content='This is a test article.',
                image=dummy_image,
                published_date=datetime(2023, 1, 1),
            )

    def test_get_delete_article_view(self):
        response = self.client.get(reverse('delete_article', kwargs={'pk': self.article.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/confirm_delete.html')
        self.assertContains(response, 'Are you sure you want to delete')

    def test_post_delete_article_view(self):
        response = self.client.post(reverse('delete_article', kwargs={'pk': self.article.pk}), follow=True)
        self.assertRedirects(response, reverse('article_list'))
        
        # Check if the article was deleted
        self.assertFalse(Article.objects.filter(pk=self.article.pk).exists())

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == 'Article deleted successfully!' for message in messages))
