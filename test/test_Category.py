import pytest
from core.models import Category

@pytest.mark.django_db
def test_create_category():
    # Crear una instancia válida de Category
    category = Category.objects.create(
        category_name='Nombre de Categoría de Prueba',
        category_description='Descripción de la Categoría de Prueba'
    )

    # Verificar que la instancia se haya creado correctamente
    assert category.pk is not None

@pytest.fixture
def sample_category():
    # Crear una instancia válida de Category para utilizar en otras pruebas
    return Category.objects.create(
        category_name='Nombre de Categoría de Prueba',
        category_description='Descripción de la Categoría de Prueba'
    )

@pytest.mark.django_db
def test_edit_category(sample_category):
    # Obtener la instancia de Category creada
    category = sample_category

    # Modificar algunos campos
    category.category_name = 'Nuevo Nombre de Categoría'
    category.save()

    # Recuperar la instancia de Category de la base de datos para asegurar que los cambios se han guardado correctamente
    edited_category = Category.objects.get(pk=category.pk)

    # Verificar que los cambios se hayan guardado correctamente
    assert edited_category.category_name == 'Nuevo Nombre de Categoría'

@pytest.mark.django_db
def test_delete_category(sample_category):
    # Obtener la instancia de Category creada
    category = sample_category

    # Eliminar la instancia de Category
    category.delete()

    # Verificar que la instancia haya sido eliminada correctamente
    assert not Category.objects.filter(pk=category.pk).exists()
