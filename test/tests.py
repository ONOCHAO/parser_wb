from main import white_list, bool_login, get_html, get_price  

def test_bool_login_existing():
    """Тест: ID уже в белом списке"""
    test_id = 1079713104
    result = bool_login(test_id)
    print(f"✅ ID {test_id} уже в списке? → {result}")

def test_bool_login_new():
    """Тест: ID отсутствует в белом списке"""
    new_id = 555555555
    result = bool_login(new_id)
    print(f"✅ ID {new_id} в списке? → {result}")

def test_add_to_white_list():
    """Тест: добавление нового ID (без дублирования)"""
    new_id = 555555555
    if new_id not in white_list:
        print(f"⚡ Добавляем ID {new_id}...")
        white_list.append(new_id)
    else:
        print(f"ℹ️ ID {new_id} уже в списке!")
    result = bool_login(new_id)
    print(f"✅ ID {new_id} теперь в списке? → {result}")

def test_get_html_valid():
    """Тест: корректное получение данных о товаре"""
    test_articul = "123456"
    result = get_html(test_articul)
    print(f"✅ Полученные данные:\n{result}")

def test_get_html_invalid():
    """Тест: запрос с неверным артикулом"""
    test_articul = "000000"  
    result = get_html(test_articul)
    print(f"✅ Ошибка при неверном артикуле:\n{result}")

def test_get_price_valid():
    """Тест: корректное получение цен"""
    test_articul = "123456"
    result = get_price(test_articul)
    
    if result:
        print(f"✅ Текущая цена: {result.get('current_price', 'Нет данных')} RUB")
        print(f"✅ Средняя цена: {result.get('average_price', 'Нет данных')} RUB")
    else:
        print("❌ Ошибка получения цены!")

def test_get_price_invalid():
    """Тест: запрос цены с неверным артикулом"""
    test_articul = "000000"
    result = get_price(test_articul)

    if result:
        print(f"✅ Ошибка при неверном артикуле: {result}")
    else:
        print("❌ Ошибка запроса! Нет данных.")

def run_tests():
    """Запускает все тесты"""
    test_bool_login_existing()
    test_bool_login_new()
    test_add_to_white_list()
    test_get_html_valid()
    test_get_html_invalid()
    test_get_price_valid()
    test_get_price_invalid()
    print(f"📌 Итоговый `white_list`: {white_list}")

if __name__ == "__main__":
    run_tests()
