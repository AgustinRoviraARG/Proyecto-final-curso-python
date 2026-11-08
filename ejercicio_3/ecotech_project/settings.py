"""
Configuración del proyecto EcoTech (ejercicio 3).

Es una configuración mínima de desarrollo: no usa base de datos ni
migraciones, por lo que el servidor arranca sin pasos previos.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Solo para desarrollo. En producción debe venir de una variable de entorno.
SECRET_KEY = "django-insecure-ecotech-solo-para-desarrollo"
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "sustentabilidad",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "ecotech_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,  # busca sustentabilidad/templates/sustentabilidad/panel.html
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "ecotech_project.wsgi.application"

LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True
