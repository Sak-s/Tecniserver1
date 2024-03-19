import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from core.models import SoilCompactionTest, Engineer

@pytest.fixture
def engineer():
    return Engineer.objects.create(
        engineer_na='Ingeniero Prueba',
        email='ingeniero_prueba@example.com',
        cell_number='1234567890',
        nit='1234567890',
        role=Engineer.ENGINEER_CAMPO
    )

@pytest.fixture
def sample_soil_compaction_test(engineer):
    # Crear una instancia válida de SoilCompactionTest
    return SoilCompactionTest.objects.create(
        engineer_name=engineer,
        test_number=1,
        location='Ubicación de prueba',
        test_date=timezone.now().date(),
        soil_type='Franco-arcilloso',
        natural_moisture_content=5.0,
        compaction_equipment_c='Rodillo vibratorio',
        number_of_passes=10,
        compaction_energy=50.0,
        adjustments_calibrations='No se realizaron ajustes durante el proceso',
        max_dry_density=1.8,
        optimal_moisture_content=10.0,
        field_dry_density=1.6,
        compaction_profile='Perfil de compactación',
        results_conclusions='Resultados y conclusiones de la prueba',
        approval_status='Aprobado'
    )

@pytest.mark.django_db
def test_create_soil_compaction_test(engineer):
    # Crear una instancia válida de SoilCompactionTest
    soil_compaction_test = SoilCompactionTest.objects.create(
        engineer_name=engineer,
        test_number=1,
        location='Ubicación de prueba',
        test_date=timezone.now().date(),
        soil_type='Franco-arcilloso',
        natural_moisture_content=5.0,
        compaction_equipment_c='Rodillo vibratorio',
        number_of_passes=10,
        compaction_energy=50.0,
        adjustments_calibrations='No se realizaron ajustes durante el proceso',
        max_dry_density=1.8,
        optimal_moisture_content=10.0,
        field_dry_density=1.6,
        compaction_profile='Perfil de compactación',
        results_conclusions='Resultados y conclusiones de la prueba',
        approval_status='Aprobado'
    )

    # Verificar que la instancia se haya creado correctamente
    assert soil_compaction_test.pk is not None

@pytest.mark.django_db
def test_edit_soil_compaction_test(sample_soil_compaction_test):
    # Obtener la instancia de SoilCompactionTest creada
    soil_compaction_test = sample_soil_compaction_test

    # Modificar algunos campos
    soil_compaction_test.location = 'Nueva Ubicación'
    soil_compaction_test.results_conclusions = 'Nuevos resultados y conclusiones'
    soil_compaction_test.save()

    # Recuperar la instancia de SoilCompactionTest de la base de datos para asegurar que los cambios se han guardado correctamente
    edited_soil_compaction_test = SoilCompactionTest.objects.get(pk=soil_compaction_test.pk)

    # Verificar que los cambios se hayan guardado correctamente
    assert edited_soil_compaction_test.location == 'Nueva Ubicación'
    assert edited_soil_compaction_test.results_conclusions == 'Nuevos resultados y conclusiones'

@pytest.mark.django_db
def test_delete_soil_compaction_test(sample_soil_compaction_test):
    # Obtener la instancia de SoilCompactionTest creada
    soil_compaction_test = sample_soil_compaction_test

    # Eliminar la instancia de SoilCompactionTest
    soil_compaction_test.delete()

    # Verificar que la instancia haya sido eliminada correctamente
    assert not SoilCompactionTest.objects.filter(pk=soil_compaction_test.pk).exists()
