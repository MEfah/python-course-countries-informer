from http import HTTPStatus
from typing import Optional

import httpx
from rest_framework import serializers

from base.clients.base import BaseClient
from geo.clients.shemas import CurrencyRatesDTO


class CurrencyClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером данных о курсах валют
    """

    def get_base_url(self) -> str:
        return "https://www.cbr-xml-daily.ru/latest.js"

    def _request(self, endpoint: str) -> Optional[dict]:
        with httpx.Client(timeout=30) as client:
            # получение ответа
            response = client.get(endpoint)
            if response.status_code == HTTPStatus.OK:
                return response.json()

            return None

    def get_currency_rates(self) -> Optional[CurrencyRatesDTO]:
        """
        Получение данных о курсах валют.

        :param name: Название страны
        :return:
        """

        if response := self._request(self.get_base_url()):
            ratesDTO = CurrencyRatesDTO(
                base=response["base"], date=response["date"], rates=response["rates"]
            )

            return ratesDTO

        return None


class CurrencyService:
    """
    Сервис для работы с данными о погоде.
    """

    def get_rub_rates(self) -> Optional[CurrencyRatesDTO]:
        """
        Получение курсов валют относительно рубля

        :param alpha2code: ISO Alpha2 код страны
        :param city: Город
        :return:
        """

        if data := CurrencyClient().get_currency_rates():
            return data

        return None

    def convert_rates(
        self, rates_info: CurrencyRatesDTO, currency: str
    ) -> Optional[CurrencyRatesDTO]:
        if currency == rates_info.base:
            return rates_info

        rates = rates_info.rates

        if currency in rates_info.rates:
            rate = rates[currency]
            rates = {c: v / rate for c, v in rates.items()}
            rates["RUB"] = 1 / rate
            rates.pop(currency)

            return CurrencyRatesDTO(base=currency, date=rates_info.date, rates=rates)

        return None


class CurrencySerializer(serializers.ModelSerializer):
    """
    Сериализатор курсов валют
    """

    class Meta:
        model = CurrencyRatesDTO
        fields = [
            "base",
            "date",
            "rates",
        ]


a = "asdf"

print(a[1:3])
