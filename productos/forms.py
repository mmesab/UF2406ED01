# productos/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Categoria, Producto


class RegistroForm(UserCreationForm):
    """
    Formulario de registro personalizado. Heredo de UserCreationForm pero le añado
    el campo email de forma explícita y le aplico una validación para evitar registros duplicados.
    """
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_email(self):
        # Implemento este método de limpieza para verificar si el correo ya está registrado.
        # Utilizo __iexact para asegurar que no influyan mayúsculas/minúsculas.
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Ya existe un usuario con este correo electrónico."
            )
        return email


class CategoriaForm(forms.ModelForm):
    """
    Formulario basado en modelo para la gestión de categorías.
    Aprovecho ModelForm para generar los campos automáticamente a partir del modelo Categoria.
    """
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion"]


class ProductoForm(forms.ModelForm):
    """
    Formulario basado en modelo para la gestión de productos (incluye el campo de imagen).
    """
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "precio", "categoria", "imagen"]