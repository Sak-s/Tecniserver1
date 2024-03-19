import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
from core.models import LegalClient, validate_future_time, validate_future_date, validate_phone_number, validate_nit_length

@pytest.fixture
def legal_client_data():
    return {
        "registered_name": "Empresa XYZ",
        "nit": 1234567890123,  # Añade un NIT válido
        "cell_number": "1234567890",  # Añade un número de teléfono válido
        "address": "Calle Principal 123",
        "date": timezone.now().date(),  # Añade una fecha válida
        "time": datetime.strptime("12:00:00", "%H:%M:%S").time(),  # Añade una hora válida
        "email": "empresa@example.com"
    }

@pytest.mark.django_db
def test_legal_client_creation(legal_client_data):
    legal_client = LegalClient(**legal_client_data)
    legal_client.full_clean()  # Ejecuta las validaciones del modelo
    legal_client.save()  # Guarda el cliente jurídico en la base de datos

    assert LegalClient.objects.count() == 1

@pytest.mark.django_db
def test_future_time_validation():
    # Hora anterior a las 7:00 AM
    with pytest.raises(ValidationError):
        validate_future_time(datetime.strptime("06:00:00", "%H:%M:%S").time())

    # Hora posterior a las 7:00 PM
    with pytest.raises(ValidationError):
        validate_future_time(datetime.strptime("20:00:00", "%H:%M:%S").time())

    # Hora válida dentro del rango
    validate_future_time(datetime.strptime("12:00:00", "%H:%M:%S").time())

@pytest.mark.django_db
def test_future_date_validation():
    # Fecha en el pasado
    with pytest.raises(ValidationError):
        validate_future_date(timezone.now().date() - timedelta(days=1))

    # Fecha válida dentro del rango futuro
    validate_future_date(timezone.now().date() + timedelta(days=1))

    # Fecha más de 6 meses en el futuro
    with pytest.raises(ValidationError):
        validate_future_date(timezone.now().date() + timedelta(days=181))

@pytest.mark.django_db
def test_phone_number_validation():
    # Número con menos de 10 dígitos
    with pytest.raises(ValidationError):
        validate_phone_number("123456789")

    # Número con más de 10 dígitos
    with pytest.raises(ValidationError):
        validate_phone_number("12345678901")

    # Número con caracteres no numéricos
    with pytest.raises(ValidationError):
        validate_phone_number("123456789x")

    # Número negativo
    with pytest.raises(ValidationError):
        validate_phone_number("-1234567890")

    # Número válido
    validate_phone_number("1234567890")

@pytest.mark.django_db
def test_nit_length_validation():
    # NIT con menos de 10 dígitos
    with pytest.raises(ValidationError):
        validate_nit_length(123456789)

    # NIT con más de 15 dígitos
    with pytest.raises(ValidationError):
        validate_nit_length(1234567890123456)

    # NIT con 10 dígitos
    validate_nit_length(1234567890)

    # NIT con 15 dígitos
    validate_nit_length(123456789012345)