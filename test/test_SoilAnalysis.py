import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from core.models import SoilAnalysis, Engineer

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
def sample_soil_analysis(engineer):
    # Crear una instancia válida de SoilAnalysis
    return SoilAnalysis.objects.create(
        engineer_name=engineer,
        test_number=1,
        location='Ubicación de prueba',
        sampling_date=timezone.now().date(),
        depth='0-30',
        texture='Arcilloso',
        ph='6.5',
        organic_matter=3.5,
        cation_exchange_capacity=5.0,
        total_nitrogen=10.0,
        available_phosphorus=20.0,
        available_potassium=30.0,
        iron=2.0,
        manganese=1.5,
        zinc=1.0,
        compaction_equipment='Barrena de suelo',
        conclusions_recommendations='Conclusiones y recomendaciones de prueba',
        approval_status='Aprobado'
    )

@pytest.mark.django_db
def test_create_soil_analysis(sample_soil_analysis):
    # Obtener la instancia de SoilAnalysis creada
    soil_analysis = sample_soil_analysis

    # Verificar que la instancia se haya creado correctamente
    assert soil_analysis.pk is not None

@pytest.mark.django_db
def test_edit_soil_analysis(sample_soil_analysis):
    # Obtener la instancia de SoilAnalysis creada
    soil_analysis = sample_soil_analysis

    # Modificar algunos campos
    soil_analysis.location = 'Nueva Ubicación'
    soil_analysis.conclusions_recommendations = 'Nuevas conclusiones y recomendaciones'
    soil_analysis.save()

    # Recuperar la instancia de SoilAnalysis de la base de datos para asegurar que los cambios se han guardado correctamente
    edited_soil_analysis = SoilAnalysis.objects.get(pk=soil_analysis.pk)

    # Verificar que los cambios se hayan guardado correctamente
    assert edited_soil_analysis.location == 'Nueva Ubicación'
    assert edited_soil_analysis.conclusions_recommendations == 'Nuevas conclusiones y recomendaciones'

@pytest.mark.django_db
def test_delete_soil_analysis(sample_soil_analysis):
    # Obtener la instancia de SoilAnalysis creada
    soil_analysis = sample_soil_analysis

    # Eliminar la instancia de SoilAnalysis
    soil_analysis.delete()

    # Verificar que la instancia haya sido eliminada correctamente
    assert not SoilAnalysis.objects.filter(pk=soil_analysis.pk).exists()
