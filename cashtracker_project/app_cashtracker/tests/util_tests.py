from django.test import TestCase
from app_cashtracker.helpers.util import *


class UtilTests(TestCase):

    def test_currency_converter(self):
        converted = currency_converter('USD', 'USD', 1)
        self.assertEqual(converted, '1.00')

        converted = currency_converter('EUR', 'BGN', 1)
        self.assertEqual(converted, '1.96')

        converted = currency_converter('BGN', 'BGN', 1)
        self.assertEqual(converted, '1.00')

    def test_hash_and_check_password(self):
        hashed_password = hash_password('42')
        self.assertEqual(check_password(hashed_password, '42'), True)

    def test_take_date(self):
        now = timezone.now()
        self.assertEqual(take_date('today'), now - timedelta(hours=24))
        self.assertEqual(take_date('week'), now - timedelta(days=7))
        self.assertEqual(take_date('month'), now - timedelta(days=32))
        self.assertEqual(take_date('year'), now - timedelta(days=365))
        self.assertEqual(take_date('beginning'), now - timedelta(days=3650))
        