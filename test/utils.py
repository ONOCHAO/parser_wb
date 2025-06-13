from main import *
import requests
import telebot

def bool_login(chat_id):
    """Проверяет, есть ли ID в белом списке"""
    return chat_id in white_list

def get_html(articul):
    """Отправляет GET-запрос и возвращает обработанные данные о товаре"""
    url = f"https://alm-basket-cdn-01.geobasket.ru/vol{articul[:4]}/part{articul[:6]}/{articul}/info/ru/card.json"

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()   
        data = response.json()  

        product_name = data.get("imt_name", "Нет информации")
        return f"🔹 **{product_name}**"

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None

def get_price(articul):
    """Отправляет GET-запрос и извлекает цены"""
    url = f"https://alm-basket-cdn-01.geobasket.ru/vol{articul[:4]}/part{articul[:6]}/{articul}/info/price-history.json"

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  
        data = response.json()  

        prices = [item["price"]["RUB"] for item in data]

        current_price = prices[-1] if prices else "Цена неизвестна"
        average_price = round(sum(prices) / len(prices), 2) if prices else "Нет данных"

        return {"current_price": current_price, "average_price": average_price}

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка запроса: {e}")
        return None
