"""Представления Django"""
import re
from typing import Any

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request

from news.services.news import NewsService


@api_view(["GET"])
def get_city(request: Request, alpha2code: str) -> JsonResponse:
    """
    Получить новости

    :param Request request: Объект запроса
    :param str alpha2code: ISO Alpha2 код страны
    :return:
    """

    offset = request.query_params.get('offset')
    offset = int(offset) if offset is not None and offset.isdigit() else 0
    
    count = request.query_params.get('count')
    count = int(count) if count is not None and count.isdigit() else 10

    if cities := CityService().get_cities(name, offset, count):
        serializer = CitySerializer(cities, many=True)

        return JsonResponse(serializer.data, safe=False)

    raise NotFound
