from aiogram import types, Router

from src.service.wb_parse_service import WbScraper

handle_parse_router = Router()

scraper = WbScraper()


@handle_parse_router.message(lambda message: message.text and "wildberries.ru" in message.text)
async def handle_parse_lambda(message: types.Message):
    """
        Обработчик, который запускает парсинг и отправляет результаты
        порциями, чтобы избежать ошибки о превышении длины сообщения.
        """
    # Здесь вы получаете данные от пользователя (ссылку, цены и т.д.)
    # Для примера используем тестовые данные:
    target_url = message.text
    low_price = 10000
    top_price = 150000
    discount = 10

    await message.answer("Начинаю сбор товаров. Это может занять некоторое время...")

    # Получаем полный список товаров с помощью скрапера
    products = scraper.scrape_category(
        target_url=target_url,
        low_price=low_price,
        top_price=top_price,
        discount=discount,
        max_pages=5  # Рекомендуется ограничивать кол-во страниц для бота
    )

    if not products:
        await message.answer("Товары по вашему запросу не найдены.")
        return

    # --- КЛЮЧЕВОЕ ИЗМЕНЕНИЕ ---
    # Разбиваем результаты на несколько сообщений

    response_chunk = ""

    for product in products[:10]:
        product_info = (
            f"Название: {product.name}\n"
            f"Цена: {product.sale_price} руб. (старая цена: {product.price} руб.)\n"
            f"Рейтинг: {product.rating} ({product.feedbacks} отзывов)\n"
            f"Ссылка: {product.link}\n\n"
        )

        response_chunk += product_info

    if response_chunk:
        await message.answer(response_chunk)

    await message.answer(f"✅ Сбор завершен. Всего найдено: {len(products)} товаров.")
