# tienda/settings.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Configuro el directorio raíz 'templates' a nivel de proyecto para centralizar
        # la plantilla base (base.html) y tener una estructura más limpia y organizada.
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                # Incluyo el context processor de mensajes para poder mostrar
                # notificaciones emergentes (alertas Bootstrap) tras crear/editar/eliminar.
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuración de Archivos Estáticos y Archivos Media
STATIC_URL = 'static/'

# Defino MEDIA_URL y MEDIA_ROOT para gestionar las imágenes subidas por los usuarios.
# MEDIA_ROOT es la ruta absoluta en el disco duro donde se guardan las imágenes (Pillow).
# MEDIA_URL es la ruta pública con la que se accederá desde el navegador.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')