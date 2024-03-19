import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models import Escarificacion, Engineer

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
def sample_escarificacion(engineer):
    # Crear una instancia válida de Escarificacion
    return Escarificacion.objects.create(
        engineer_name=engineer,
        test_number=1,
        location='Ubicación de prueba',
        sampling_date=timezone.now().date(),
        depth_1='0-30',
        depth_sample_1='cm',
        color='marron_oscuro',
        texture_sample_1='limosa',
        sample_1_structure='agregados_granulares',
        sample_1_porosity=0.5,
        sample_1_apparent_density=1.2,
        ph_sample_1='acido',
        sample_1_organic_matter=3.5,
        compaction_equipment_1='Espectrofotometros',
        depth_2='30-60',
        depth_sample_2='m',
        texture_sample_2='arena',
        sample_2_structure='agregados_bien_definidos',
        sample_2_porosity=0.6,
        sample_2_apparent_density=1.3,
        ph_sample_2='lig_acido',
        sample_2_organic_matter=4.0,
        sample_nu='nitrogeno',
        compaction_equipment_2='Equipos de agitación o mezclado',
        conclusions_recommendations='Conclusiones y recomendaciones de prueba',
        approval_status='Aprobado'
    )

@pytest.mark.django_db
def test_edit_escarificacion(sample_escarificacion):
    # Obtener la instancia de Escarificacion creada
    escarificacion = sample_escarificacion

    # Modificar algunos campos
    escarificacion.location = 'Nueva Ubicación'
    escarificacion.conclusions_recommendations = 'Nuevas conclusiones y recomendaciones'
    escarificacion.save()

    # Recuperar la instancia de Escarificacion de la base de datos para asegurar que los cambios se han guardado correctamente
    edited_escarificacion = Escarificacion.objects.get(pk=escarificacion.pk)

    # Verificar que los cambios se hayan guardado correctamente
    assert edited_escarificacion.location == 'Nueva Ubicación'
    assert edited_escarificacion.conclusions_recommendations == 'Nuevas conclusiones y recomendaciones'

@pytest.mark.django_db
def test_delete_escarificacion(sample_escarificacion):
    # Obtener la instancia de Escarificacion creada
    escarificacion = sample_escarificacion

    # Eliminar la instancia de Escarificacion
    escarificacion.delete()

    # Verificar que la instancia haya sido eliminada correctamente
    assert not Escarificacion.objects.filter(pk=escarificacion.pk).exists()

@pytest.mark.django_db
def test_create_escarificacion(engineer):
    # Crear una instancia válida de Escarificacion
    escarificacion = Escarificacion.objects.create(
        engineer_name=engineer,
        test_number=1,
        location='Ubicación de prueba',
        sampling_date=timezone.now().date(),
        depth_1='0-30',
        depth_sample_1='cm',
        color='marron_oscuro',
        texture_sample_1='limosa',
        sample_1_structure='agregados_granulares',
        sample_1_porosity=0.5,
        sample_1_apparent_density=1.2,
        ph_sample_1='acido',
        sample_1_organic_matter=3.5,
        compaction_equipment_1='Espectrofotometros',
        depth_2='30-60',
        depth_sample_2='m',
        texture_sample_2='arena',
        sample_2_structure='agregados_bien_definidos',
        sample_2_porosity=0.6,
        sample_2_apparent_density=1.3,
        ph_sample_2='lig_acido',
        sample_2_organic_matter=4.0,
        sample_nu='nitrogeno',
        compaction_equipment_2='Equipos de agitación o mezclado',
        conclusions_recommendations='Conclusiones y recomendaciones de prueba',
        approval_status='Aprobado'
    )

    # Verificar que la instancia se haya creado correctamente
    assert escarificacion.pk is not None