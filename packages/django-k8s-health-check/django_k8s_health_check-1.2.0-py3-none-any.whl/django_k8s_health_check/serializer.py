from rest_framework.fields import BooleanField, CharField
from rest_framework.serializers import Serializer


class GenericSerializer(Serializer):
    backend_name = BooleanField()


class HealthSerializer(Serializer):
    service = CharField()
    databases = GenericSerializer(many=True)
    caches = GenericSerializer(many=True)
