from django.test import TestCase

from django.shortcuts import get_object_or_404
from django.utils import timezone
from app_cashtracker.models.Category import Category
from app_cashtracker.models.Subcategory import Subcategory
from app_cashtracker.models.User import User


class SubcategoryTests(TestCase):

    def test_create_new_subcategory(self):
        user = User()
        user.created = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        user.save()
        category = Category()
        category.name = 'Test category'
        category.description = ''
        category.user = user
        category.save()
        subcategory = Subcategory()
        subcategory.category = category
        subcategory.name = 'Test subcategory'
        subcategory.save()

        category_from_DB = get_object_or_404(Subcategory, id=subcategory.id)
        self.assertEqual(subcategory, category_from_DB)

    def test_save_subcategory_name(self):
        user = User()
        user.created = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        user.save()
        category = Category()
        category.name = 'Test category'
        category.description = ''
        category.user = user
        category.save()
        subcategory = Subcategory()
        subcategory.category = category
        subcategory.name = 'Test subcategory'
        subcategory.save()

        category_from_DB = get_object_or_404(Subcategory, id=subcategory.id)
        self.assertEqual(subcategory.name, 'Test subcategory')
