import pytest
from django.core.exceptions import ValidationError
from core.models import TestPermeability, LaboratoryWorker

@pytest.fixture
def sample_laboratory_worker():
    # Crear una instancia válida de LaboratoryWorker para asociarla a TestPermeability
    return LaboratoryWorker.objects.create(
        laboratory_name='Laboratorio de Prueba',
        email='laboratorista_prueba@example.com',
        cell_number='1234567890',
        nit='1234567890',
        rol=LaboratoryWorker.LABORATORISTA
    )

@pytest.mark.django_db
def test_create_test_permeability(sample_laboratory_worker):
    # Crear una instancia válida de TestPermeability
    test_permeability = TestPermeability.objects.create(
        NameLaboratory=sample_laboratory_worker,
        test_number=1,
        test_date='2024-03-16',
        soil_type='arcilloso',
        grain_size='medio',
        soil_porosity='media',
        soil_compaction='alta',
        soil_temperature=25.6,
        soil_moisture_content=0.15,
        hydrostatic_pressure=100.0,
        loading_conditions='alta',
        drainage_conditions='buena',
        soil_chemistry='PH: 7.2, Nitrógeno: 0.08%',
        compaction_equipment_t='Equipos de medición de presión y flujo',
        permeability_velocity=0.25,
        intrinsic_permeability=0.003,
        permeability_coefficient=2.5,
        observations='Observaciones de prueba',
        conclusions='Conclusiones de prueba',
        approval_status='Aprobado'
    )

    # Verificar que la instancia se haya creado correctamente
    assert test_permeability.pk is not None

@pytest.mark.django_db
def test_edit_test_permeability(sample_laboratory_worker):
    # Crear una instancia válida de TestPermeability para editar
    test_permeability = TestPermeability.objects.create(
        NameLaboratory=sample_laboratory_worker,
        test_number=1,
        test_date='2024-03-16',
        soil_type='arcilloso',
        grain_size='medio',
        soil_porosity='media',
        soil_compaction='alta',
        soil_temperature=25.6,
        soil_moisture_content=0.15,
        hydrostatic_pressure=100.0,
        loading_conditions='alta',
        drainage_conditions='buena',
        soil_chemistry='PH: 7.2, Nitrógeno: 0.08%',
        compaction_equipment_t='Equipos de medición de presión y flujo',
        permeability_velocity=0.25,
        intrinsic_permeability=0.003,
        permeability_coefficient=2.5,
        observations='Observaciones de prueba',
        conclusions='Conclusiones de prueba',
        approval_status='Aprobado'
    )

    # Modificar algunos campos
    test_permeability.soil_type = 'arenoso'
    test_permeability.save()

    # Recuperar la instancia de TestPermeability de la base de datos para asegurar que los cambios se han guardado correctamente
    edited_test_permeability = TestPermeability.objects.get(pk=test_permeability.pk)

    # Verificar que los cambios se hayan guardado correctamente
    assert edited_test_permeability.soil_type == 'arenoso'

@pytest.mark.django_db
def test_delete_test_permeability(sample_laboratory_worker):
    # Crear una instancia válida de TestPermeability para eliminar
    test_permeability = TestPermeability.objects.create(
        NameLaboratory=sample_laboratory_worker,
        test_number=1,
        test_date='2024-03-16',
        soil_type='arcilloso',
        grain_size='medio',
        soil_porosity='media',
        soil_compaction='alta',
        soil_temperature=25.6,
        soil_moisture_content=0.15,
        hydrostatic_pressure=100.0,
        loading_conditions='alta',
        drainage_conditions='buena',
        soil_chemistry='PH: 7.2, Nitrógeno: 0.08%',
        compaction_equipment_t='Equipos de medición de presión y flujo',
        permeability_velocity=0.25,
        intrinsic_permeability=0.003,
        permeability_coefficient=2.5,
        observations='Observaciones de prueba',
        conclusions='Conclusiones de prueba',
        approval_status='Aprobado'
    )

    # Eliminar la instancia de TestPermeability
    test_permeability.delete()

    # Verificar que la instancia haya sido eliminada correctamente
    assert not TestPermeability.objects.filter(pk=test_permeability.pk).exists()
