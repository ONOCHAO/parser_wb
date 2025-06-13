import telebot
import requests

token = ""

bot = telebot.TeleBot(token)
white_list = [1079713104]

def bool_login(chat_id):
    """Проверяет, есть ли ID в белом списке"""
    return chat_id in white_list  

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Обрабатывает команду /start"""
    if bool_login(message.chat.id):
        bot.reply_to(message, "Добро пожаловать. Напишите ваш артикул!")  
    else:
        bot.reply_to(message, "Нет доступа!")
        white_list.append(message.chat.id)  
        print(f"Добавлен новый ID: {message.chat.id}")  

@bot.message_handler(content_types=['text'])  
def handle_text(message):
    """Обрабатывает текстовые сообщения"""
    user_text = message.text.lower()
    
    if bool_login(message.chat.id):
        bot.reply_to(message, f"Вы написали: {user_text}")
        
        product_info = get_html(user_text)  
        price_info = get_price(user_text)

        if product_info and price_info:
            bot.reply_to(message, f"🔹 Информация о товаре:\n{product_info}")
            bot.reply_to(message, f"💰 Цена: {price_info['current_price']} ₸\n📊 Средняя цена: {price_info['average_price']} ₸")
            bot.reply_to(message, f"💡 Рекомендация: {price_info['recommendation']}")
        else:
            bot.reply_to(message, "❌ Ошибка! Данных нет или неверный артикул.")
    else:
        bot.reply_to(message, "Нет доступа!")

def get_rating(articul):
    """Получает рейтинг товара с API Wildberries"""
    url = f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=269&spp=30&hide_dtype=13&ab_testing=false&lang=ru&nm={articul}"

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()   
        data = response.json()

        if "data" in data and "products" in data["data"]:
            rating = data["data"]["products"][0].get("reviewRating", "Нет данных")
        else:
            rating = "Нет данных"

        return rating

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка запроса: {e}")
        return "❌ Ошибка получения данных!"

    
def get_html(articul):
    """Отправляет GET-запрос и возвращает расширенные данные о товаре"""
    url = f"https://alm-basket-cdn-01.geobasket.ru/vol{articul[:4]}/part{articul[:6]}/{articul}/info/ru/card.json"

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()   
        data = response.json()  

        product_name = data.get("imt_name", "Нет информации")    
        description = data.get("description", "Описание отсутствует")  
        image_url = data.get("photo_links", ["Нет изображения"])[0]  
        rating = get_rating(articul)  

        return f"""
🔹 **{product_name}**
⭐ Рейтинг: {rating}
📜 Описание: {description}
🖼 Фото: {image_url}
        """

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка запроса: {e}")
        return "❌ Ошибка получения данных!"

def process_number(num):
    """Конвертирует число в строку, удаляет две последние цифры и преобразует обратно"""
    string_price = str(num)  
    modified_string = string_price[:-3]  
    modified_num = int(modified_string)  
    result = modified_num * 6.42  
    return result

def get_price(articul):
    """Отправляет GET-запрос, извлекает цену и конвертирует в тенге"""
    url = f"https://alm-basket-cdn-01.geobasket.ru/vol{articul[:4]}/part{articul[:6]}/{articul}/info/price-history.json"

    exchange_rate = 6.42  

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  
        data = response.json()  

        prices_rub = [item["price"]["RUB"] for item in data]  

        if prices_rub:
            current_price_kzt = round(process_number(prices_rub[-1]) * exchange_rate, 2)
            average_price_kzt = round(sum(process_number(p) for p in prices_rub) * exchange_rate / len(prices_rub), 2)  

            if average_price_kzt > current_price_kzt:
                recommendation = "✅ Цена выгодна, можно приобретать!"
            elif average_price_kzt < current_price_kzt:
                recommendation = "⚠️ Цена выше среднего, покупка не рекомендуется!"
            else:
                recommendation = "ℹ️ Цены стабильны, решайте сами."

        else:
            current_price_kzt = None
            average_price_kzt = None
            recommendation = "❌ Нет информации о ценах."

        return {
            "current_price": current_price_kzt,
            "average_price": average_price_kzt,
            "recommendation": recommendation
        }

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка запроса: {e}")
        return None

bot.polling()
