from django.conf import settings
from django.test.signals import setting_changed
from django.utils.translation import gettext_lazy as _

from rest_framework.settings import APISettings, api_settings

USER_SETTINGS = getattr(settings, 'HEALTH_CHECK', None)

DEFAULTS = {
    # View
    'PERMISSION_CLASSES': api_settings.DEFAULT_AUTHENTICATION_CLASSES,
    'AUTHENTICATION_CLASSES': api_settings.DEFAULT_PERMISSION_CLASSES,
    'SERIALIZER_CLASS': 'django_k8s_health_check.serializer.HealthSerializer',

    # SERVICE INFO
    'SERVICE_NAME': None,
    'SERVICE_VERSION': None,
    'CHECK_DATABASE': True,
    'CHECK_CACHE': True,

    # Middleware
    'HEADER_FIELD': 'X-Health',
    'HEADER_VALUE': 'health-check',
    'ALLOWED_PATHS': None,
    'ALLOWED_HOSTS': None,
}

IMPORT_STRINGS = ('PERMISSION_CLASSES', 'AUTHENTICATION_CLASSES', 'SERIALIZER_CLASS')

REMOVED_SETTINGS = ()


api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(*args, **kwargs):  # pragma: no cover
    global api_settings

    setting, value = kwargs['setting'], kwargs['value']

    if setting == 'HEALTH_CHECK':
        api_settings = APISettings(value, DEFAULTS, IMPORT_STRINGS)


setting_changed.connect(reload_api_settings)
