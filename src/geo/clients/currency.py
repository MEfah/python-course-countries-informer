"""
Функции для взаимодействия с внешним сервисом-провайдером данных о курсах валют
https://www.cbr-xml-daily.ru/latest.js
"""
from http import HTTPStatus
from typing import Optional

import httpx

from src.base.clients.base import BaseClient
from src.geo.clients.shemas import CurrencyRatesDTO


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

    def get_currency_rates(self, currency: str) -> Optional[dict]:
        """
        Получение данных о курсах валют.

        :param name: Название страны
        :return:
        """
        
        if response := self._request(self.get_base_url()):
            item = response[0]
            rates = item["rates"]
            currency = currency.capitalize()

            if currency == "RUB":
                return CurrencyRatesDTO(
                    base=currency,
                    date=item["date"],
                    rates=rates
                )
            
            elif currency in rates:
                rate = rates[currency]
                rates = { c: v / rate for c, v in rates }
                rates["RUB"] = 1 / rate
                rates.pop(currency)
                
                ratesDTO = CurrencyRatesDTO(
                    base=currency,
                    date=item["date"],
                    rates=rates
                )
                
                return ratesDTO

        return None