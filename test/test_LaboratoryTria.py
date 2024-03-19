# import pytest
# from django.core.exceptions import ValidationError
# from django.utils import timezone
# from core.models import LaboratoryTrial, Client, LaboratoryWorker

# @pytest.fixture
# def sample_client():
#     # Crear una instancia válida de Client
#     return Client.objects.create(
#         name_client='Cliente de Prueba',
#         last_name_client='Apellido de Prueba',
#         cell_number='1234567890',
#         address='Dirección de Prueba',
#         email='cliente_prueba@example.com'
#     )

# @pytest.fixture
# def sample_laboratory_worker():
#     # Crear una instancia válida de LaboratoryWorker
#     return LaboratoryWorker.objects.create(
#         laboratory_name='Laboratorio de Prueba',
#         email='laboratorista_prueba@example.com',
#         cell_number='1234567890',
#         nit='1234567890'
#     )

# @pytest.mark.django_db
# def test_create_laboratory_trial(sample_laboratory_worker, sample_client):
#     # Crear una instancia válida de LaboratoryTrial
#     laboratory_trial = LaboratoryTrial.objects.create(
#         laboratory_name=sample_laboratory_worker,
#         natural_client=sample_client,
#         test_date=timezone.now().date(),# Proporcionar un valor para el campo 'time'
#         address='Dirección de prueba'
#     )

#     # Verificar que la instancia se haya creado correctamente
#     assert laboratory_trial.pk is not None

# @pytest.mark.django_db
# def test_edit_laboratory_trial(sample_laboratory_worker, sample_client):
#     # Crear una instancia de LaboratoryTrial para editar
#     laboratory_trial = LaboratoryTrial.objects.create(
#         laboratory_name=sample_laboratory_worker,
#         natural_client=sample_client,
#         test_date=timezone.now().date(),# Proporcionar un valor para el campo 'time'
#         address='Dirección de prueba'
#     )

#     # Modificar algunos campos
#     laboratory_trial.address = 'Nueva Dirección de Prueba'
#     laboratory_trial.save()

#     # Recuperar la instancia de LaboratoryTrial de la base de datos para asegurar que los cambios se han guardado correctamente
#     edited_laboratory_trial = LaboratoryTrial.objects.get(pk=laboratory_trial.pk)

#     # Verificar que los cambios se hayan guardado correctamente
#     assert edited_laboratory_trial.address == 'Nueva Dirección de Prueba'

# @pytest.mark.django_db
# def test_delete_laboratory_trial(sample_laboratory_worker, sample_client):
#     # Crear una instancia de LaboratoryTrial para eliminar
#     laboratory_trial = LaboratoryTrial.objects.create(
#         laboratory_name=sample_laboratory_worker,
#         natural_client=sample_client,
#         test_date=timezone.now().date(),  # Proporcionar un valor para el campo 'time'
#         address='Dirección de prueba'
#     )

#     # Eliminar la instancia de LaboratoryTrial
#     laboratory_trial.delete()

#     # Verificar que la instancia haya sido eliminada correctamente
#     assert not LaboratoryTrial.objects.filter(pk=laboratory_trial.pk).exists()
