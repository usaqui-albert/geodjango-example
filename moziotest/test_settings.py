from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': "db_test",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
