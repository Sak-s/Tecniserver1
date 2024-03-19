# import datetime
# from django.forms import ValidationError
# import pytest
# from core.models import Escarificacion, FielTrial, Engineer
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
# from django.conf import settings

# @pytest.fixture
# @pytest.mark.django_db
# def create_engineer():
#     engineer = Engineer.objects.create(
#         engineer_na='John Doe',
#         email='john.doe@example.com',
#         cell_number='1234567890',
#         nit='123456789',
#         role=Engineer.ENGINEER_CAMPO
#     )
#     return engineer

# @pytest.fixture
# @pytest.mark.django_db
# def create_fiel_trial(create_engineer):
#     return FielTrial.objects.create(
#         engineer_name=create_engineer,
#         pdf_file=None,
#         pdf_file_1=None,
#         pdf_file_2=None,
#         date=datetime.datetime.now().date(),
#         city='Bogotá',
#         address='123 Main St'
#     )
