from django.test import TestCase

from django.shortcuts import get_object_or_404
from django.utils import timezone
from app_cashtracker.models.Category import Category
from app_cashtracker.models.Subcategory import Subcategory
from app_cashtracker.models.Payment import Payment
from app_cashtracker.models.User import User


class PaymentTests(TestCase):
    USER = None
    CATEGORY = None
    SUBCATEGORY = None
    PAYMENT = None
    NOW = timezone.now()

    def test__create_new_payment(self):
        user = User()
        user.created = PaymentTests.NOW
        user.save()
        PaymentTests.USER = user

        category = Category()
        category.name = 'Test category'
        category.description = ''
        category.user = user
        category.save()
        PaymentTests.CATEGORY = category

        subcategory = Subcategory()
        subcategory.name = ''
        subcategory.category = category
        subcategory.save()
        PaymentTests.SUBCATEGORY = subcategory

        payment = Payment()
        payment.value = 10
        payment.currency = 'EUR'
        payment.category = category
        payment.subcategory = subcategory
        payment.comment = ''
        payment.date_time = PaymentTests.NOW
        payment.user = user
        payment.save()

        payment_from_DB = get_object_or_404(Payment, id=payment.id)
        PaymentTests.PAYMENT = payment_from_DB

        self.assertEqual(payment, payment_from_DB)
        self.assertEqual(payment_from_DB.value, 10)
        self.assertEqual(payment_from_DB.currency, 'EUR')
        self.assertEqual(payment_from_DB.category, category)
        self.assertEqual(payment_from_DB.subcategory, subcategory)
        self.assertEqual(payment_from_DB.comment, '')
        self.assertEqual(payment_from_DB.user, user)

    def test_parse_date(self):
        # test parse date
        PaymentTests.PAYMENT.parse_date('today')
        self.assertEqual(
            PaymentTests.PAYMENT.date_time,
            PaymentTests.NOW.strftime('%H:%M:%S')
        )

    def test_convert_currency(self):
        # test currency convertion
        PaymentTests.PAYMENT.convert_currency('BGN')
        self.assertEqual(PaymentTests.PAYMENT.currency, 'BGN')
        self.assertEqual(PaymentTests.PAYMENT.value, '19.56')

    def test_generate_and_fetch_payments(self):
        category = Category()
        category.name = 'Test category'
        category.description = ''
        category.user = PaymentTests.USER
        category.save()

        subcategory = Subcategory()
        subcategory.name = ''
        subcategory.category = category
        subcategory.save()

        Payment.generate_fake_payments(PaymentTests.USER, 10)
        payments = Payment.fetch_payments(
            'beginning',
            '0',
            'EUR',
            PaymentTests.USER
        )
        self.assertEqual(len(payments), 10)
