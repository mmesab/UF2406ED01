from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
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
            messages.success(request, f"¡Bienvenido {usuario.username}! Tu cuenta ha sido creada exitosamente.")
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
            messages.success(request, "Categoría creada con éxito.")
            return redirect("categoria_lista")
    else:
        form = CategoriaForm()
    return render(request, "categorias/formulario.html", {"form": form, "titulo": "Nueva categoría"})


@login_required
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.info(request, "Categoría actualizada correctamente.")
            return redirect("categoria_lista")
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, "categorias/formulario.html", {"form": form, "titulo": "Editar categoría"})


@login_required
def categoria_eliminar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        nombre = categoria.nombre
        categoria.delete()
        messages.warning(request, f"La categoría '{nombre}' ha sido eliminada.")
        return redirect("categoria_lista")
    return render(request, "categorias/eliminar.html", {"categoria": categoria})


# --- CRUD PRODUCTOS CON BÚSQUEDA Y PAGINACIÓN ---

def producto_lista(request):
    query = request.GET.get("q", "")
    categoria_id = request.GET.get("categoria", "")

    productos = Producto.objects.select_related("categoria").order_by("-id")

    # Filtro por término de búsqueda
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )

    # Filtro por categoría
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    # Paginación (6 productos por página)
    paginator = Paginator(productos, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categorias = Categoria.objects.all()

    return render(
        request,
        "productos/lista.html",
        {
            "page_obj": page_obj,
            "categorias": categorias,
            "query": query,
            "categoria_id": categoria_id,
        },
    )


def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, "productos/detalle.html", {"producto": producto})


@login_required
def producto_crear(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)  # <-- Soporte para imágenes
        if form.is_valid():
            form.save()
            messages.success(request, "Producto registrado correctamente.")
            return redirect("producto_lista")
    else:
        form = ProductoForm()
    return render(request, "productos/formulario.html", {"form": form, "titulo": "Nuevo producto"})


@login_required
def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)  # <-- Soporte para imágenes
        if form.is_valid():
            form.save()
            messages.info(request, "Producto actualizado correctamente.")
            return redirect("producto_lista")
    else:
        form = ProductoForm(instance=producto)
    return render(request, "productos/formulario.html", {"form": form, "titulo": "Editar producto"})


@login_required
def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        nombre = producto.nombre
        producto.delete()
        messages.warning(request, f"El producto '{nombre}' ha sido eliminado.")
        return redirect("producto_lista")
    return render(request, "productos/eliminar.html", {"producto": producto})