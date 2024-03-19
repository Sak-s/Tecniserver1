import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
from core.models import Client

@pytest.mark.django_db
def test_valid_client():
    client = Client(
        name_client='John',
        last_name_client='Doe',
        cell_number='1234567890',
        address='123 Main St',
        date=timezone.now().date() + timedelta(days=1),  # Tomorrow
        time=datetime.strptime('12:00:00', '%H:%M:%S').time(),  # 12:00 PM
        email='john@example.com'
    )
    client.full_clean()  # Should not raise ValidationError

@pytest.mark.django_db
def test_invalid_phone_number():
    with pytest.raises(ValidationError):
        client = Client(
            name_client='John',
            last_name_client='Doe',
            cell_number='123',  # Invalid phone number
            address='123 Main St',
            date=timezone.now().date() + timedelta(days=1),
            time=datetime.strptime('12:00:00', '%H:%M:%S').time(),
            email='john@example.com'
        )
        client.full_clean()

@pytest.mark.django_db
def test_invalid_past_date():
    with pytest.raises(ValidationError):
        client = Client(
            name_client='John',
            last_name_client='Doe',
            cell_number='1234567890',
            address='123 Main St',
            date=timezone.now().date() - timedelta(days=1),  # Past date
            time=datetime.strptime('12:00:00', '%H:%M:%S').time(),
            email='john@example.com'
        )
        client.full_clean()

@pytest.mark.django_db
def test_invalid_future_date():
    with pytest.raises(ValidationError):
        client = Client(
            name_client='John',
            last_name_client='Doe',
            cell_number='1234567890',
            address='123 Main St',
            date=timezone.now().date() + timedelta(days=365),  # 1 year from now
            time=datetime.strptime('12:00:00', '%H:%M:%S').time(),
            email='john@example.com'
        )
        client.full_clean()

@pytest.mark.django_db
def test_invalid_time():
    with pytest.raises(ValidationError):
        client = Client(
            name_client='John',
            last_name_client='Doe',
            cell_number='1234567890',
            address='123 Main St',
            date=timezone.now().date() + timedelta(days=1),
            time=datetime.strptime('06:00:00', '%H:%M:%S').time(),  # Before 7:00 AM
            email='john@example.com'
        )
        client.full_clean()