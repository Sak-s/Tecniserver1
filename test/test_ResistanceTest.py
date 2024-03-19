import pytest
from django.core.exceptions import ValidationError
from core.models import ResistanceTest, LaboratoryWorker

@pytest.fixture
def sample_laboratory_worker():
    # Crear una instancia válida de LaboratoryWorker para asociarla a ResistanceTest
    return LaboratoryWorker.objects.create(
        laboratory_name='Laboratorio de Prueba',
        email='laboratorista_prueba@example.com',
        cell_number='1234567890',
        nit='1234567890',
        rol=LaboratoryWorker.LABORATORISTA
    )

@pytest.mark.django_db
def test_create_resistance_test(sample_laboratory_worker):
    # Crear una instancia válida de ResistanceTest
    resistance_test = ResistanceTest.objects.create(
        NameLaboratory=sample_laboratory_worker,
        test_number=1,
        soil_type='arcilla',
        sample_depth=1.0,
        location_latitude=0,
        location_longitude=0,
        test_date='2024-03-16',
        test_method='ensayo_permeabilidad_constante',
        procedure='Este es un procedimiento de prueba.',
        permeability=0.001,
        compaction_equipment_r='Cilindros de carga',
        approval_status='Aprobado'
    )

    # Verificar que la instancia se haya creado correctamente
    assert resistance_test.pk is not None

@pytest.mark.django_db
def test_edit_resistance_test(sample_laboratory_worker):
    # Crear una instancia válida de ResistanceTest para editar
    resistance_test = ResistanceTest.objects.create(
        NameLaboratory=sample_laboratory_worker,
        test_number=1,
        soil_type='arcilla',
        sample_depth=1.0,
        location_latitude=0,
        location_longitude=0,
        test_date='2024-03-16',
        test_method='ensayo_permeabilidad_constante',
        procedure='Este es un procedimiento de prueba.',
        permeability=0.001,
        compaction_equipment_r='Cilindros de carga',
        approval_status='Aprobado'
    )

    # Modificar algunos campos
    resistance_test.soil_type = 'arena'
    resistance_test.save()

    # Recuperar la instancia de ResistanceTest de la base de datos para asegurar que los cambios se han guardado correctamente
    edited_resistance_test = ResistanceTest.objects.get(pk=resistance_test.pk)

    # Verificar que los cambios se hayan guardado correctamente
    assert edited_resistance_test.soil_type == 'arena'

@pytest.mark.django_db
def test_delete_resistance_test(sample_laboratory_worker):
    # Crear una instancia válida de ResistanceTest para eliminar
    resistance_test = ResistanceTest.objects.create(
        NameLaboratory=sample_laboratory_worker,
        test_number=1,
        soil_type='arcilla',
        sample_depth=1.0,
        location_latitude=0,
        location_longitude=0,
        test_date='2024-03-16',
        test_method='ensayo_permeabilidad_constante',
        procedure='Este es un procedimiento de prueba.',
        permeability=0.001,
        compaction_equipment_r='Cilindros de carga',
        approval_status='Aprobado'
    )

    # Eliminar la instancia de ResistanceTest
    resistance_test.delete()

    # Verificar que la instancia haya sido eliminada correctamente
    assert not ResistanceTest.objects.filter(pk=resistance_test.pk).exists()
