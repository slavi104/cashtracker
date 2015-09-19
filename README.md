<h1><a href="http://app.cashtracker.info"><strong>Cashtracker™</strong></a> - mobile site for money tracking</h1>

In the site all registered user will add each of his payments into pre-defined categories of them. The strength of this application will be, that upon request by the user will generate reports based on all payments. Of reports will be daily, weekly, monthly or yearly. It can also be for all categories of payments and just determined. So user can track what spends the most and where it can reduce its costs. Site will generate PDF documents containing certain reports. These documents will be downloaded directly to the user's device.

# Basic functionality:
    1. Login / Register
    2. Settings:
        a. type Content Management categories for payments
        b. edited profile
        c. PDF documents (if necessary)
    3. Add payment to the relevant category
    4. Check all added payments for last day/week/month/year
    5. Generate Report directly within the application to set parameters(period and category)
    6. Generate and download a report in PDF

# Advanced functionality:
    1. Multi currency maintenance
    2. Generating demo account with fake payments(only for administrators)
       - URL: http://localhost:8000/app_cashtracker/generate_fake_payments/[number_of_payments]

# Installation 
    1. Download and install python3.4.x
    2. Add python and pip to PATH variables
    3. Console(CMD or your favorite) commands:
        - pip install django
        - pip install django_nose
        - pip install requests
        - pip install reportlab
        - cd [path_to_app]/cashtracker_project
        - python manage.py makemigrations
        - python manage.py migrate
        - python manage.py runserver
    4. Open your favorite browser and go in localhost:8000
    5. Make new registration and you are ready! :)
