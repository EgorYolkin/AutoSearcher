import logging
import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.types.wb_parser import WBParseProductResult

# --- КОНФИГУРАЦИЯ И КОНСТАНТЫ ---

# URL для получения полного каталога категорий
MAIN_MENU_URL = "https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json"
# Шаблон URL для запроса товаров в категории
CATALOG_API_URL = "https://catalog.wb.ru/catalog/{shard}/v2/catalog"

# Стандартные заголовки для HTTP-запросов
DEFAULT_HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

# Максимальное количество страниц для парсинга одной категории
MAX_PAGES_TO_SCRAPE = 100

# Настройка логирования для вывода критических ошибок
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stderr)



@dataclass(frozen=True)
class _Category:
    """Внутренняя модель данных для категории товаров."""
    name: str
    url: str
    shard: Optional[str] = None
    query: Optional[str] = None


# --- ОСНОВНОЙ КЛАСС СКРАПЕРА ---

class WbScraper:
    """
    Класс для скрапинга данных о товарах с сайта Wildberries по заданной категории.
    Инициализирует сессию с автоматическими повторными попытками при сбоях сети.
    """

    def __init__(self):
        self._session = self._init_session()
        self._categories_cache: Optional[List[_Category]] = None

    @staticmethod
    def _init_session() -> requests.Session:
        """Создает и настраивает сессию requests с логикой повторных запросов."""
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("https://", adapter)
        session.headers.update(DEFAULT_HEADERS)
        return session

    def _get_full_catalog_data(self) -> List[Dict[str, Any]]:
        """Получает полный каталог категорий с серверов Wildberries."""
        try:
            response = self._session.get(MAIN_MENU_URL, timeout=15)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as e:
            logging.error(f"Не удалось загрузить каталог Wildberries: {e}")
            return []

    def _parse_categories(self, raw_catalog_data: List[Dict[str, Any]]) -> List[_Category]:
        """Рекурсивно обходит дерево каталога и извлекает все конечные категории."""
        categories = []

        def recurse(items):
            for item in items:
                if 'childs' in item and item['childs']:
                    recurse(item['childs'])
                elif 'url' in item:
                    categories.append(_Category(
                        name=item.get('name', 'Без имени'),
                        url=item.get('url', ''),
                        shard=item.get('shard'),
                        query=item.get('query')
                    ))

        recurse(raw_catalog_data)
        return categories

    def _load_and_cache_categories(self):
        """Загружает и кэширует категории, если это еще не сделано."""
        if self._categories_cache is None:
            raw_catalog = self._get_full_catalog_data()
            if raw_catalog:
                self._categories_cache = self._parse_categories(raw_catalog)
            else:
                self._categories_cache = []

    def _find_category_by_url(self, url: str) -> Optional[_Category]:
        """Находит объект категории по её URL."""
        self._load_and_cache_categories()
        clean_url_part = url.split("wildberries.ru")[-1]
        for category in self._categories_cache:
            if category.url == clean_url_part:
                return category
        return None

    def _get_products_page_json(self, category: _Category, page: int, price_range: tuple, discount: int) -> Optional[
        Dict[str, Any]]:
        """Загружает одну страницу с товарами и возвращает JSON."""
        params = {
            "appType": 1, "curr": "rub", "dest": -1257786, "locale": "ru",
            "page": page, "priceU": f"{price_range[0] * 100};{price_range[1] * 100}",
            "sort": "popular", "spp": 0, "discount": discount,
        }
        url = f"{CATALOG_API_URL.format(shard=category.shard)}?{category.query}"
        try:
            response = self._session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as e:
            logging.error(f"Ошибка при загрузке страницы {page} для категории '{category.name}': {e}")
            return None

    @staticmethod
    def _parse_products_from_json(json_data: Dict[str, Any]) -> List[WBParseProductResult]:
        """Извлекает данные о товарах из JSON и преобразует их в список датаклассов."""
        products = []
        raw_products = json_data.get('data', {}).get('products', [])

        for item in raw_products:
            try:
                # Безопасное извлечение цены, чтобы избежать ошибок на товарах без размеров
                sizes = item.get("sizes", [])
                if not sizes:
                    continue
                price_info = sizes[0].get('price', {})
                basic_price = price_info.get('basic', 0)
                sale_price = price_info.get('product', 0)

                product = WBParseProductResult(
                    id=item['id'],
                    name=item.get('name', 'N/A'),
                    price=int(basic_price / 100),
                    sale_price=int(sale_price / 100),
                    brand=item.get('brand', 'N/A'),
                    rating=float(item.get('rating', 0.0)),
                    feedbacks=int(item.get('feedbacks', 0)),
                    supplier=item.get('supplier'),
                    link=f'https://www.wildberries.ru/catalog/{item["id"]}/detail.aspx'
                )
                products.append(product)
            except (KeyError, IndexError, TypeError) as e:
                logging.warning(f"Не удалось обработать товар с ID {item.get('id')}: {e}")
                continue
        return products

    def scrape_category(self, target_url: str, low_price: int = 1, top_price: int = 1000000, discount: int = 0,
                        max_pages: int = MAX_PAGES_TO_SCRAPE) -> List[WBParseProductResult]:
        """
        Основной публичный метод. Выполняет скрапинг товаров из указанной категории.

        :param target_url: URL каталога Wildberries для скрапинга.
        :param low_price: Минимальная цена.
        :param top_price: Максимальная цена.
        :param discount: Минимальная скидка в процентах.
        :param max_pages: Максимальное количество страниц для обхода.
        :return: Список объектов WBParseProductResult.
        """
        category = self._find_category_by_url(target_url)
        if not category:
            logging.error(f"Категория для URL '{target_url}' не найдена.")
            return []

        all_products: List[WBParseProductResult] = []
        for page_num in range(1, max_pages + 1):
            json_data = self._get_products_page_json(category, page_num, (low_price, top_price), discount)
            if not json_data:
                break

            products_on_page = self._parse_products_from_json(json_data)
            if not products_on_page:
                break

            all_products.extend(products_on_page)

        return all_products


if __name__ == '__main__':
    #  example

    TEST_URL = "https://www.wildberries.ru/catalog/sport/vidy-sporta/velosport/velosipedy"

    scraper = WbScraper()

    print(f"Запускаю скрапинг для URL: {TEST_URL}")
    products_list = scraper.scrape_category(
        target_url=TEST_URL,
        low_price=20000,
        top_price=50000,
        discount=10,
        max_pages=2
    )

    if products_list:
        print(f"\nСкрапинг завершен. Собрано товаров: {len(products_list)}")
        print("--- Первые 3 товара ---")
        for product in products_list[:3]:
            print(asdict(product))
    else:
        print("\nСкрапинг завершен. Товары не найдены или произошла ошибка.")
