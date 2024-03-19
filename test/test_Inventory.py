import pytest
from django.core.exceptions import ValidationError
from core.models import Inventory, Category

@pytest.fixture
def sample_category():
    # Crear una instancia válida de Category para usar en las pruebas
    return Category.objects.create(category_name='Categoria de Prueba')

@pytest.mark.django_db
def test_create_inventory(sample_category):
    # Crear una instancia válida de Inventory
    inventory = Inventory.objects.create(
        product_name_invent='Producto de Prueba',
        amount_invent='10',
        category_name=sample_category,
        description_invent='Descripción del producto de prueba',
        image_invent=None  # Opcional: Si deseas agregar una imagen, proporciona la ruta correcta
    )

    # Verificar que la instancia se haya creado correctamente
    assert inventory.pk is not None

@pytest.mark.django_db
def test_edit_inventory(sample_category):
    # Crear una instancia de Inventory para editar
    inventory = Inventory.objects.create(
        product_name_invent='Producto de Prueba',
        amount_invent='10',
        category_name=sample_category,
        description_invent='Descripción del producto de prueba',
        image_invent=None
    )

    # Modificar algunos campos
    inventory.product_name_invent = 'Nuevo Producto'
    inventory.save()

    # Recuperar la instancia de Inventory de la base de datos para asegurar que los cambios se han guardado correctamente
    edited_inventory = Inventory.objects.get(pk=inventory.pk)

    # Verificar que los cambios se hayan guardado correctamente
    assert edited_inventory.product_name_invent == 'Nuevo Producto'

@pytest.mark.django_db
def test_delete_inventory(sample_category):
    # Crear una instancia de Inventory para eliminar
    inventory = Inventory.objects.create(
        product_name_invent='Producto de Prueba',
        amount_invent='10',
        category_name=sample_category,
        description_invent='Descripción del producto de prueba',
        image_invent=None
    )

    # Eliminar la instancia de Inventory
    inventory.delete()

    # Verificar que la instancia haya sido eliminada correctamente
    assert not Inventory.objects.filter(pk=inventory.pk).exists()
