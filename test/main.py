import telebot
import requests

token = "7707639351:AAG_6PbazzZu78knFXA52-87ZNqWbTg4-rk"  

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
            bot.reply_to(message, f"💰 Цена: {price_info['current_price']} RUB\n📊 Средняя цена: {price_info['average_price']} RUB")
        else:
            bot.reply_to(message, "❌ Ошибка! Данных нет или неверный артикул.")
    else:
        bot.reply_to(message, "Нет доступа!")

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

bot.polling()
