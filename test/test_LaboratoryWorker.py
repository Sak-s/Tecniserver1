import pytest
from django.core.exceptions import ValidationError
from core.models import LaboratoryWorker

@pytest.fixture
def sample_laboratory_worker():
    # Crear una instancia válida de LaboratoryWorker
    return LaboratoryWorker.objects.create(
        laboratory_name='Laboratorio de Prueba',
        email='laboratorista_prueba@example.com',
        cell_number='1234567890',
        nit='1234567890',
        rol=LaboratoryWorker.LABORATORISTA
    )

@pytest.mark.django_db
def test_create_laboratory_worker():
    # Crear una instancia válida de LaboratoryWorker
    laboratory_worker = LaboratoryWorker.objects.create(
        laboratory_name='Laboratorio de Prueba',
        email='laboratorista_prueba@example.com',
        cell_number='1234567890',
        nit='1234567890',
        rol=LaboratoryWorker.LABORATORISTA
    )

    # Verificar que la instancia se haya creado correctamente
    assert laboratory_worker.pk is not None

@pytest.mark.django_db
def test_edit_laboratory_worker(sample_laboratory_worker):
    # Obtener la instancia de LaboratoryWorker creada
    laboratory_worker = sample_laboratory_worker

    # Modificar algunos campos
    laboratory_worker.laboratory_name = 'Nuevo Nombre de Laboratorio'
    laboratory_worker.save()

    # Recuperar la instancia de LaboratoryWorker de la base de datos para asegurar que los cambios se han guardado correctamente
    edited_laboratory_worker = LaboratoryWorker.objects.get(pk=laboratory_worker.pk)

    # Verificar que los cambios se hayan guardado correctamente
    assert edited_laboratory_worker.laboratory_name == 'Nuevo Nombre de Laboratorio'

@pytest.mark.django_db
def test_delete_laboratory_worker(sample_laboratory_worker):
    # Obtener la instancia de LaboratoryWorker creada
    laboratory_worker = sample_laboratory_worker

    # Eliminar la instancia de LaboratoryWorker
    laboratory_worker.delete()

    # Verificar que la instancia haya sido eliminada correctamente
    assert not LaboratoryWorker.objects.filter(pk=laboratory_worker.pk).exists()

@pytest.mark.django_db
def test_create_laboratory_worker():
    # Crear una instancia válida de LaboratoryWorker
    laboratory_worker = LaboratoryWorker.objects.create(
        laboratory_name='Laboratorio de Prueba',
        email='laboratorista_prueba@example.com',
        cell_number='1234567890',
        nit='1234567890',
        rol=LaboratoryWorker.LABORATORISTA
    )

    # Verificar que la instancia se haya creado correctamente
    assert laboratory_worker.pk is not None