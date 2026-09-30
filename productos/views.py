from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Producto
from .forms import RegistroForm, CategoriaForm, ProductoForm


def home(request):
    return render(request, "home.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("home")
    else:
        form = RegistroForm()
    return render(request, "registration/register.html", {"form": form})


# --- CRUD CATEGORÍAS ---

@login_required
def categoria_lista(request):
    categorias = Categoria.objects.all()
    return render(request, "categorias/lista.html", {"categorias": categorias})


@login_required
def categoria_crear(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categoria_lista")
    else:
        form = CategoriaForm()
    return render(
        request,
        "categorias/formulario.html",
        {"form": form, "titulo": "Nueva categoría"}
    )


@login_required
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect("categoria_lista")
    else:
        form = CategoriaForm(instance=categoria)
    return render(
        request,
        "categorias/formulario.html",
        {"form": form, "titulo": "Editar categoría"}
    )


@login_required
def categoria_eliminar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        categoria.delete()
        return redirect("categoria_lista")
    return render(
        request,
        "categorias/eliminar.html",  # Corregido a plural
        {"categoria": categoria}
    )


# --- CRUD PRODUCTOS ---

def producto_lista(request):
    productos = Producto.objects.select_related("categoria")
    return render(
        request,
        "productos/lista.html",  # Corregido a plural
        {"productos": productos}
    )


def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(
        request,
        "productos/detalle.html",
        {"producto": producto}
    )


@login_required
def producto_crear(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("producto_lista")
    else:
        form = ProductoForm()
    return render(
        request,
        "productos/formulario.html",
        {"form": form, "titulo": "Nuevo producto"}
    )


@login_required
def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("producto_lista")
    else:
        form = ProductoForm(instance=producto)
    return render(
        request,
        "productos/formulario.html",
        {"form": form, "titulo": "Editar producto"}
    )


@login_required
def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        producto.delete()
        return redirect("producto_lista")
    return render(
        request,
        "productos/eliminar.html",
        {"producto": producto}
    )