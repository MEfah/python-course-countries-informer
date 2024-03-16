from rest_framework import serializers

from geo.models import Country, City
from geo.clients.shemas import CurrencyRatesDTO


class NewsSerializer(serializers.Serializer):
    """
    Сериализатор новостей
    """

    source = serializers.CharField()
    author = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    url = serializers.CharField()
    published_at = serializers.DateTimeField()
