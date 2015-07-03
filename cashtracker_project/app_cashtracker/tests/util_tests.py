from django.test import TestCase
from app_cashtracker.helpers.util import hash_password
from app_cashtracker.helpers.util import currency_converter
from app_cashtracker.helpers.util import check_password
from app_cashtracker.helpers.util import take_date
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
import os


class UtilTests(TestCase):

    def test_currency_converter(self):
        converted = currency_converter('USD', 'USD', 1)
        self.assertEqual(converted, '1.00')

        converted = currency_converter('EUR', 'BGN', 1)
        self.assertEqual(converted, '1.96')

        converted = currency_converter('BGN', 'BGN', 1)
        self.assertEqual(converted, '1.00')

    def test_currency_converter_with_download_new_rates(self):
        basepath = os.path.dirname(__file__)
        now = timezone.now()  # + timedelta(hours=3)
        file_name = "{}.json".format(now.strftime('%Y_%m_%d'))
        rel_filepath = os.path.join(basepath, "..", "tmp", file_name)
        abs_filepath = os.path.abspath(rel_filepath)
        os.remove(abs_filepath)

        converted = currency_converter('USD', 'USD', 1)
        self.assertEqual(converted, '1.00')

        converted = currency_converter('EUR', 'BGN', 1)
        self.assertEqual(converted, '1.96')

        converted = currency_converter('BGN', 'BGN', 1)
        self.assertEqual(converted, '1.00')

    def test_hash_password(self):
        hashed_password = hash_password('42')
        self.assertEqual(len(hashed_password), 97)

    def test_hash_and_check_password(self):
        hashed_password = hash_password('42')
        self.assertEqual(check_password(hashed_password, '42'), True)

    def test_check_password(self):
        self.assertEqual(
            check_password(
                'b2e7bcc53f44ae4e5ca7c67108cd04bcfa2d8e40e2170ea22d18ecef'
                'd70e7a74:7d45a8ddea174d80b453f23824576cda',
                '42'
            ), True)

    def test_take_date(self):
        now = timezone.now()
        self.assertEqual(take_date('today', now), now - timedelta(hours=24))
        self.assertEqual(take_date('week', now), now - timedelta(days=7))
        self.assertEqual(take_date('month', now), now - timedelta(days=32))
        self.assertEqual(take_date('year', now), now - timedelta(days=365))
        self.assertEqual(
            take_date('beginning', now),
            now - timedelta(days=1000)
        )
