from typing import Optional

from geo.clients.shemas import CurrencyRatesDTO
from geo.clients.currency import CurrencyClient


class CurrencyService:
    """
    Сервис для работы с данными о погоде.
    """

    def get_rub_rates(self) -> Optional[CurrencyRatesDTO]:
        """
        Получение курсов валют относительно рубля

        :return:
        """

        if data := CurrencyClient().get_currency_rates():
            return data

        return None

    def convert_rates(
        self, rates_info: CurrencyRatesDTO, currency: str
    ) -> Optional[CurrencyRatesDTO]:
        """
        Вычислить курсы валют на основе курсов для другой валюты

        :param rates_info CurrencyRatesDTO: курсы валют
        :param str currency: ISO 4217 буквенный код валюты
        :return:
        """
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
