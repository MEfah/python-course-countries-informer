"""Представления Django"""
import re
from typing import Any

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request

from news.services.news import NewsService
from news.serializers import NewsSerializer


@api_view(["GET"])
def get_news(request: Request, alpha2code: str) -> JsonResponse:
    """
    Получить новости

    :param Request request: Объект запроса
    :param str alpha2code: ISO Alpha2 код страны
    :return:
    """

    news_service = NewsService()

    if news := news_service.get_news(alpha2code):
        return JsonResponse(NewsSerializer(news, many=True).data, safe=False)

    raise NotFound
