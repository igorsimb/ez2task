from unittest import skip

import pytest
from django.test import TestCase, tag

from main_app.models import Item, Category, Comment
from django.contrib.auth import get_user_model as user_model
User = user_model()

@tag('unit')
class TestModels(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            username='Test User 1'
        )

        self.category1 = Category.objects.create(
            category_title='category1'
        )

        self.task1 = Item.objects.create(
            title='Task 1',
            category=self.category1,
            author=self.user1
        )

        self.comment1 = Comment.objects.create(
            user=self.user1,
            item=self.task1,
            content='Test Content'
        )

    def test_user_created(self):
        self.assertEquals(self.user1.id, 1)

    def test_user_is_assigned_slug_on_creation(self):
        self.assertEquals(self.user1.slug, 'test-user-1')

    def test_items_is_assigned_category_on_creation(self):
        self.assertEquals(self.task1.category.category_title, 'category1')

    def test_comment_is_assigned_to_task(self):
        self.assertEquals(self.comment1.item, self.task1)