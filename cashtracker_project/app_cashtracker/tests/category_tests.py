from django.test import TestCase

from django.shortcuts import get_object_or_404
from django.utils import timezone
from app_cashtracker.models.Category import Category
from app_cashtracker.models.User import User


class CategoryTests(TestCase):

    def test_create_new_category(self):
        user = User()
        user.created = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        user.save()
        category = Category()
        category.name = 'Test category'
        category.description = ''
        category.user = user
        category.save()

        category_from_DB = get_object_or_404(Category, id=category.id)

        self.assertEqual(category, category_from_DB)
        self.assertEqual(category.name, category_from_DB.name)
        self.assertEqual(category.description, category_from_DB.description)
        self.assertEqual(category.user, category_from_DB.user)

    def test_get_category_name_all(self):
        self.assertEqual(Category.get_category_name(0), 'All')

    def test_get_category_name_not_all(self):
        user = User()
        user.created = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        user.save()
        category = Category()
        category.name = 'Test category'
        category.description = ''
        category.user = user
        category.save()
        self.assertEqual(
            Category.get_category_name(category.id),
            'Test category'
        )