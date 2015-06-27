import json
import requests
import os
from datetime import datetime
from datetime import timedelta
from decimal import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas 
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.platypus.flowables import PageBreak 
from django.utils import timezone


# for password hashing
import uuid
import hashlib

def currency_converter(curr_from, curr_to, value_input):
    basepath = os.path.dirname(__file__)
    file_name = "{}.json".format(timezone.now().strftime('%Y_%m_%d'))
    rel_filepath = os.path.join(basepath, "..", "tmp", file_name)
    abs_filepath = os.path.abspath(rel_filepath)

    # if file exist so we already have current currencies
    if os.path.isfile(abs_filepath):
        with open(abs_filepath, "r") as f:
            exchange = json.loads(f.read())
    else:
        response = requests.get('http://api.fixer.io/latest')
        exchange = json.loads(response.content.decode())
        with open(abs_filepath, "w") as f:
            f.write(response.content.decode())

    rates = exchange['rates']
    from_value = Decimal(rates.get(curr_from, '1'))
    to_value = Decimal(rates.get(curr_to, '1'))
    result = Decimal(value_input/from_value*to_value)
    return "{0:.2f}".format(result)



def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


def take_date(srting_repr):
    calc_functions = {
        'today': timezone.now() - timedelta(hours=24),
        'week': timezone.now() - timedelta(days=7),
        'month': timezone.now() - timedelta(days=32),
        'year': timezone.now() - timedelta(days=365),
        'beginning': timezone.now() - timedelta(days=3650)
    }
    return calc_functions.get(srting_repr, timezone.now())


if __name__ == "__main__":
    import sys
    fib(int(sys.argv[1]))