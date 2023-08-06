Django Health Check
=

If you use or like the project, click `Star` and `Watch` to generate metrics and i evaluate project continuity.

# Install:
    pip install django-k8s-health-check

# Usage Health only:
1. In your urls:
    ```
    from django_k8s_health_check.views import HealthView
    ...

    urlpatterns = [
        path('', views.HealthView.as_view()),
    ]
    ```

# Usage in kubernetes:

If use health check in kubernetes, you need to add kubernetes ip/host to django allowed_hosts,
but is a bad practice, especially if there are multiple ip/hosts...
For this, i created a middleware to pass dynamic ip/hosts, using multiples validators

1. Request Way

    1. Add the middleware to django middleware`s:
        ```
        MIDDLEWARE = [
            'django_k8s_health_check.middleware.HealthCheckMiddleware',
            ...
        ]
        ```

    1. Try this request:
        ```
        import requests
        requests.get('your-url', headers={'X-Health': 'health-check'})
        ```

    1. Put this in your yml
        ```
        livenessProbe:
            httpGet:
            path: /your-path
            httpHeaders:
            - name: X-Health
                value: health-check
            timeoutSeconds: 5
        ```
    1. Check de configuration section, and change for security reasons...

1. Command Way (test database and cache only, this not guarantee application is running):

    1. Add this app to your installed apps:
        ```
        INSTALLED_APPS = [
            'django_k8s_health_check',
        ]
        ```
    
    1. Try to run this command:
        ```
        python manage.py health_check
        ```
    
    1. Put this in your yml
        ```
        livenessProbe:
            exec:
                command: ["python", "manage.py", "health_check"]
            timeoutSeconds: 5
        ```

# Configuration:

```
HEALTH_CHECK = {
    # View
    'SERVICE_NAME': None,  # Used only in API
    'CHECK_DATABASE': True,
    'CHECK_CACHE': True,

    # Middleware (All bellow is used only in API)
    'HEADER_FIELD': 'X-Health',
    'HEADER_VALUE': 'health-check',
    'ALLOWED_PATHS': None,  # all others urls, use original ALLOWED_HOSTS. Ex: ['api/v1/health', '/health'], None allow all
    'ALLOWED_HOSTS': None,  # check request host is in a list, Ex: ['127.0.0.1', 'www.domain.com'], None allow all
}
```