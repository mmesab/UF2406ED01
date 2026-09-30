# productos/models.py

from django.db import models

class Categoria(models.Model):
    """
    Modelo para clasificar los productos. Decido separar las categorías en su propia
    tabla para mantener la base de datos normalizada y permitir añadir/editar categorías
    sin alterar la estructura de los productos.
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        # Devuelvo el nombre de la categoría para que en las relaciones y el panel de control
        # se muestre un texto descriptivo en lugar de la ID.
        return self.nombre


class Producto(models.Model):
    """
    Modelo principal para la gestión de productos del catálogo.
    """
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    
    # Utilizo DecimalField para el precio en lugar de FloatField para evitar errores
    # de redondeo de punto flotante en operaciones financieras.
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Relaciono con Categoria mediante clave foránea (1 N).
    # Aplico on_delete=models.CASCADE para mantener la integridad referencial.
    # Con related_name='productos' facilito las consultas inversas desde Categoria.
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="productos")
    
    # Añado ImageField para permitir imágenes en los productos.
    # Configuro blank=True y null=True para que no sea obligatorio subir una foto al crear el producto.
    imagen = models.ImageField(upload_to="productos/", blank=True, null=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre