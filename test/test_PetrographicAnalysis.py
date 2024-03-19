import pytest
from django.core.exceptions import ValidationError
from core.models import PetrographicAnalysis, LaboratoryWorker

@pytest.fixture
def sample_laboratory_worker():
    # Crear una instancia válida de LaboratoryWorker para asociarla a PetrographicAnalysis
    return LaboratoryWorker.objects.create(
        laboratory_name='Laboratorio de Prueba',
        email='laboratorista_prueba@example.com',
        cell_number='1234567890',
        nit='1234567890',
        rol=LaboratoryWorker.LABORATORISTA
    )

@pytest.mark.django_db
def test_create_petrographic_analysis(sample_laboratory_worker):
    # Crear una instancia válida de PetrographicAnalysis
    petrographic_analysis = PetrographicAnalysis.objects.create(
        name_laboratory=sample_laboratory_worker,
        test_number=1,
        test_date='2024-03-16',
        sample_description='Descripción de la muestra',
        mineral_composition='Cuarzo',
        grain_size_distribution='Fino',
        texture='Compacto',
        porosity='Baja',
        cementation='Arcilla',
        mineral_identification='Cuarzo',
        mineral_quantification='Medio',
        rock_type='Ígnea',
        color='Blanco',
        compaction_equipment_P='Microscopio Petrográfico',
        conclusions='Conclusiones de prueba',
        approval_status='Aprobado'
    )

    # Verificar que la instancia se haya creado correctamente
    assert petrographic_analysis.pk is not None

@pytest.mark.django_db
def test_edit_petrographic_analysis(sample_laboratory_worker):
    # Crear una instancia válida de PetrographicAnalysis para editar
    petrographic_analysis = PetrographicAnalysis.objects.create(
        name_laboratory=sample_laboratory_worker,
        test_number=1,
        test_date='2024-03-16',
        sample_description='Descripción de la muestra',
        mineral_composition='Cuarzo',
        grain_size_distribution='Fino',
        texture='Compacto',
        porosity='Baja',
        cementation='Arcilla',
        mineral_identification='Cuarzo',
        mineral_quantification='Medio',
        rock_type='Ígnea',
        color='Blanco',
        compaction_equipment_P='Microscopio Petrográfico',
        conclusions='Conclusiones de prueba',
        approval_status='Aprobado'
    )

    # Modificar algunos campos
    petrographic_analysis.mineral_composition = 'Feldespato'
    petrographic_analysis.save()

    # Recuperar la instancia de PetrographicAnalysis de la base de datos para asegurar que los cambios se han guardado correctamente
    edited_petrographic_analysis = PetrographicAnalysis.objects.get(pk=petrographic_analysis.pk)

    # Verificar que los cambios se hayan guardado correctamente
    assert edited_petrographic_analysis.mineral_composition == 'Feldespato'

@pytest.mark.django_db
def test_delete_petrographic_analysis(sample_laboratory_worker):
    # Crear una instancia válida de PetrographicAnalysis para eliminar
    petrographic_analysis = PetrographicAnalysis.objects.create(
        name_laboratory=sample_laboratory_worker,
        test_number=1,
        test_date='2024-03-16',
        sample_description='Descripción de la muestra',
        mineral_composition='Cuarzo',
        grain_size_distribution='Fino',
        texture='Compacto',
        porosity='Baja',
        cementation='Arcilla',
        mineral_identification='Cuarzo',
        mineral_quantification='Medio',
        rock_type='Ígnea',
        color='Blanco',
        compaction_equipment_P='Microscopio Petrográfico',
        conclusions='Conclusiones de prueba',
        approval_status='Aprobado'
    )

    # Eliminar la instancia de PetrographicAnalysis
    petrographic_analysis.delete()

    # Verificar que la instancia haya sido eliminada correctamente
    assert not PetrographicAnalysis.objects.filter(pk=petrographic_analysis.pk).exists()
