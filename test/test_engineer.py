import pytest
from django.core.exceptions import ValidationError
from core.models import Engineer

@pytest.fixture
def sample_engineer():
    # Crear un ingeniero de muestra
    return Engineer.objects.create(
        engineer_na='Ingeniero de Prueba',
        email='ingeniero_prueba@example.com',
        cell_number='1234567890',
        nit='1234567890',
        role=Engineer.ENGINEER_CAMPO
    )

@pytest.mark.django_db
def test_create_edit_delete_engineer(sample_engineer):
    # Obtener el ingeniero de muestra
    engineer = sample_engineer

    # Verificar que el ingeniero se haya creado correctamente
    assert engineer.pk is not None

    # Modificar algunos campos del ingeniero
    engineer.engineer_na = 'Nuevo Nombre de Ingeniero'
    engineer.save()

    # Recuperar el ingeniero de la base de datos para asegurar que los cambios se han guardado correctamente
    edited_engineer = Engineer.objects.get(pk=engineer.pk)

    # Verificar que los cambios se hayan guardado correctamente
    assert edited_engineer.engineer_na == 'Nuevo Nombre de Ingeniero'

    # Eliminar el ingeniero
    engineer.delete()

    # Verificar que el ingeniero haya sido eliminado correctamente
    assert not Engineer.objects.filter(pk=engineer.pk).exists()
