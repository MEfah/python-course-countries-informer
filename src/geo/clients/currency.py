"""
Функции для взаимодействия с внешним сервисом-провайдером данных о курсах валют
https://www.cbr-xml-daily.ru/latest.js
"""
from http import HTTPStatus
from typing import Optional

import httpx

from app.settings import REQUESTS_TIMEOUT
from base.clients.base import BaseClient
from geo.clients.shemas import CurrencyRatesDTO


class CurrencyClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером данных о курсах валют
    """

    def get_base_url(self) -> str:
        return "https://www.cbr-xml-daily.ru/latest.js"

    def _request(self, endpoint: str) -> Optional[dict]:
        with httpx.Client(timeout=REQUESTS_TIMEOUT) as client:
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
                base=response["base"],
                date=response["date"],
                rates=response["rates"]
            )
            
            return ratesDTO

        return None