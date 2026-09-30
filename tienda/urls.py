# tienda/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Ruta de administración de Django
    path("admin/", admin.site.urls),
    
    # Incluyo el sistema de autenticación nativo de Django para gestionar login y logout
    path("accounts/", include("django.contrib.auth.urls")),
    
    # Redirijo la ruta raíz a las URLs de la aplicación 'productos'
    path("", include("productos.urls")),
]

# Durante la etapa de desarrollo (DEBUG = True), configuro Django para que sirva
# directamente los archivos multimedia subidos por los usuarios desde MEDIA_ROOT.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)