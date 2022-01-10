from unittest import skip

from django.test import TestCase, Client, tag
from django.urls import reverse
from main_app.models import Item, Category, Comment
import json
from django.contrib.auth import get_user_model as user_model
from django.contrib import auth
User = user_model()

@tag('unit')
class TestViews(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            username='Test User 1',
            email='test@email.com',
            password='password',
        )

        self.category1 = Category.objects.create(
            category_title='category1'
        )

        self.client = Client()
        self.index_url = reverse('main')
        self.login_url = reverse('login')
        self.detail_url = reverse('detail', args=[1])
        self.task1 = Item.objects.create(
            title='task1',
            author=self.user1,
            category=self.category1
        )

    def test_index_redirects_unauthenticated_user_to_login(self):
        redirect_response = self.client.get(self.login_url)
        main_page_response = self.client.get(self.login_url)
        print(f'{redirect_response = }')
        print(f'{User = }')

        self.assertEquals(redirect_response.status_code, 200)



