from main import get_rating, get_html, get_price, get_otnoch  

def test_get_rating_valid():
    """Тест: получение рейтинга и отзывов для валидного артикула"""
    articul = "160805675"
    rating, feedback = get_rating(articul)
    print(f"✅ Рейтинг для артикула {articul}: {rating}")
    print(f"✅ Количество отзывов: {feedback}")

def test_get_rating_invalid():
    """Тест: запрос рейтинга с несуществующим артикулом"""
    articul = "000000"
    rating, feedback = get_rating(articul)
    print(f"✅ Ошибка рейтинга (ожидаем 'Нет данных'): {rating}")
    print(f"✅ Ошибка отзывов (ожидаем 'Нет данных'): {feedback}")

def test_get_otnoch_valid():
    """Тест: анализ оценки товара"""
    print(f"✅ Оценка качества товара (10 отзывов, рейтинг 4.8): {get_otnoch(4.8, 10)}")
    print(f"✅ Оценка качества товара (500 отзывов, рейтинг 3.5): {get_otnoch(3.5, 500)}")
    print(f"✅ Оценка качества товара (5 отзывов, рейтинг 5.0): {get_otnoch(5.0, 5)}")

def test_get_html_valid():
    """Тест: получение информации о товаре"""
    articul = "123456"
    result = get_html(articul)
    print(f"✅ Данные о товаре:\n{result}")

def test_get_html_invalid():
    """Тест: запрос с несуществующим артикулом"""
    articul = "000000"
    result = get_html(articul)
    print(f"✅ Ошибка данных о товаре (ожидаем 'Ошибка запроса'): {result}")

def test_get_price_valid():
    """Тест: получение ценового анализа"""
    articul = "123456"
    result = get_price(articul)
    print(f"✅ Цена товара: {result}")

def test_get_price_invalid():
    """Тест: запрос цен с неверным артикулом"""
    articul = "000000"
    result = get_price(articul)
    print(f"✅ Ошибка ценового анализа: {result}")

def run_tests():
    """Запускает все тесты"""
    test_get_rating_valid()
    test_get_rating_invalid()
    test_get_otnoch_valid()
    test_get_html_valid()
    test_get_html_invalid()
    test_get_price_valid()
    test_get_price_invalid()

if __name__ == "__main__":
    run_tests()
