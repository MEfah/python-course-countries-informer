import logging

from celery import shared_task

from geo.services.country import CountryService
from news.services.news import NewsService

logger = logging.getLogger()


@shared_task(name="import_news")
def import_news() -> None:
    """
    Импорт актуальной новостной ленты по странам, сохраненным в базе данных.

    :return:
    """

    logger.info("Running 'import_news'...")
    # получение кодов стран, сохраненных в базе данных
    codes = CountryService().get_countries_codes()
    if not codes:
        logger.info("Countries codes not found.")
        return None

    logger.info("Found countries codes: %s.", codes)

    news_service = NewsService()

    # пример для теста одной страны:
    # codes = {"us": 17}

    for country_code, country_pk in codes.items():
        # запрос новостной ленты для страны
        news = news_service.get_api_news(country_code)
        if not news:
            logger.info("No news found for '%s'.", country_code)
            continue

        logger.info("Received news for '%s': %s length.", country_code, len(news))
        # сохранение новостей в базе данных для страны
        news_service.save_news(country_pk, news)
        logger.info("News data for '%s' has been saved.", country_code)

    logger.info("Function 'import_news' finished.")

    return None
