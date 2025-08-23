#Brickly - интуитивно понятный редактор сайтов, позволяющий создавать и редактировать
#различные виды сайтов без знания программирования. Идеально подходит для учреждений
#образования и начинающих предпринимателей!

#Это код бота нашего проекта, разршено полное пользование кодом - бесплатно

#FLIPUK DEVELOPER

import telebot
import os

API_TOKEN = '8098581524:AAEQaZh_jZRdd-WDvzWs3ZDZY-idkE9uhkg'

bot = telebot.TeleBot(API_TOKEN)

last_messages = {}

# Айди админов для отправки рассылок
ADMIN_ID = 872274179
ADMIN_ID2 = 1639361324

SUBSCRIBERS_FILE = "subs.txt" #Подгружаем файл с подписками для рассылок
MESSAGE_FILE = 'answers.txt' #Подгружаем файл с главными ответами

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_subscribers(): #Загружаем список подписчиков
    if not os.path.exists(SUBSCRIBERS_FILE):
        return set()
    with open(SUBSCRIBERS_FILE, 'r') as f:
        return set(map(int, f.read().splitlines()))
    
def save_subscribers(subscribers): #Сохраняем список подписчиков
    with open(SUBSCRIBERS_FILE, 'w') as f:
        for user_id in subscribers:
            f.write(f"{user_id}\n")

def add_subscriber(user_id): #Добавляем нового подписчика
    subscribers = load_subscribers()
    if user_id not in subscribers:
        subscribers.add(user_id)
        save_subscribers(subscribers)

def remove_subscriber(user_id): #Удаляем подписчика
    subscribers = load_subscribers()
    if user_id in subscribers:
        subscribers.remove(user_id)
        save_subscribers(subscribers)

def get_answer_for_key(key): #Получаем ключ для ответа
    if not os.path.exists(MESSAGE_FILE):
        print(f"File is not found: {MESSAGE_FILE}")
        return None

    try:
        with open(MESSAGE_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        sections = content.split("##") # в answers.txt каждый раздел начинается с ## и заканчивается ##

        for section in sections:
            stripped_section = section.strip()
            if not stripped_section:
                continue

            lines = stripped_section.split('\n', 1)
            section_key = lines[0].strip()

            if section_key == key:
                if len(lines) > 1:
                    return lines[1].strip()
                else:
                    return "Информация по этому разделу пока отсутствует."

        print(f"Key '{key}' is not found in the file.{MESSAGE_FILE}")
        return None

    except Exception as e:
        print(f"Error reading file or parsing contents: {e}")
        return None

#--------------------------------------------------------------

def delete_previous_message(chat_id):
    if chat_id in last_messages:
        try:
            bot.delete_message(chat_id, last_messages[chat_id])
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Ошибка при удалении сообщения: {e}")
        del last_messages[chat_id] # Удаляем ID удаленного сообщения из словаря


#--------------------------------------------------------------

@bot.message_handler(commands=['start'])
def welcome(message):
    user_name = message.from_user.first_name
    greeting = f"{user_name}"

    markup = telebot.types.InlineKeyboardMarkup()
    menu_button = telebot.types.InlineKeyboardButton("Открыть меню", callback_data='menu')
    markup.add(menu_button)

    sent_msg = bot.send_message(message.chat.id,
                             f"Добро Пожаловать в Brickly Project, {greeting}! \nЗдесь вы можете получить информацию о Brickly Project и его услугах.",
                             reply_markup=markup)
    last_messages[message.chat.id] = sent_msg.message_id  # Сохраняем ID сообщения


#--------------------------------------------------------------

@bot.callback_query_handler(func=lambda call: call.data == "menu")
def callback_inline(call):
    chat_id = call.message.chat.id
    delete_previous_message(chat_id)  # Удаляем предыдущее сообщение
    send_menu(chat_id, 'Выберите действие:')


def send_menu(chat_id, text):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    about = telebot.types.KeyboardButton('📖О нас📖')
    structure = telebot.types.KeyboardButton('🛠Структура Проекта🛠')
    autors = telebot.types.KeyboardButton('🧑‍💻Авторы Проекта🧑‍💻')
    social = telebot.types.KeyboardButton('📱Соцсети📱')
    news = telebot.types.KeyboardButton('🗞Новостные рассылки🗞')
    presentation = telebot.types.KeyboardButton('📊Презентация📊')
    markup.add(about, structure, autors, social, news, presentation)
    sent_msg = bot.send_message(chat_id, text, reply_markup=markup)
    last_messages[chat_id] = sent_msg.message_id  # Сохраняем ID сообщения


#--------------------------------------------------------------

@bot.message_handler(func=lambda message: message.text == '📖О нас📖')
def about(message):
    chat_id = message.chat.id
    delete_previous_message(chat_id)
    answer = get_answer_for_key('О нас')
    sent_msg = bot.send_message(chat_id,
                             answer if answer else 'Информация по запросу "О нас" не найдена.')
    last_messages[chat_id] = sent_msg.message_id


#--------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == '🛠Структура Проекта🛠')
def handle_structure_project_text(message):
    chat_id = message.chat.id
    delete_previous_message(chat_id)
    try:
        with open("IMAGES/structure.jpg", "rb") as photo:
            sent_msg = bot.send_photo(chat_id, photo)
    except FileNotFoundError:
        sent_msg = bot.send_message(chat_id, "Изображение структуры не найдено.")
    except Exception as e:
        sent_msg = bot.send_message(chat_id, f"Произошла ошибка при отправке изображения: {e}")

    answer = get_answer_for_key('Структура Brickly Project')
    sent_msg = bot.send_message(chat_id,
                             answer if answer else 'Информация по запросу "Структура Brickly Project" не найдена.')
    last_messages[chat_id] = sent_msg.message_id


#--------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == '🧑‍💻Авторы Проекта🧑‍💻')
def handle_authors_text(message):
    chat_id = message.chat.id
    delete_previous_message(chat_id)
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    flipuk = telebot.types.InlineKeyboardButton('Разработчик')
    chfr = telebot.types.InlineKeyboardButton('Дизайнер')
    back = telebot.types.InlineKeyboardButton('⬅️Назад⬅️')
    markup.add(flipuk, chfr, back)
    sent_msg = bot.send_message(chat_id, 'Авторы проекта:', reply_markup=markup)
    last_messages[chat_id] = sent_msg.message_id


#--------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == 'Разработчик')
def handle_flipuk_text(message):
    chat_id = message.chat.id
    delete_previous_message(chat_id)
    answer = get_answer_for_key('Разработчик')
    image_path = os.path.join(BASE_DIR, "IMAGES", "Flipuk4.png")

    try:
        with open(image_path, "rb") as photo:
            sent_msg = bot.send_photo(chat_id, photo, caption=answer)
    except FileNotFoundError:
        sent_msg = bot.send_message(chat_id, "Фото не найдено.")
        if answer:
            bot.send_message(chat_id, answer)
    except Exception as e:
        sent_msg = bot.send_message(chat_id, f"Произошла ошибка при отправке фото: {e}")
        if answer:
            bot.send_message(chat_id, answer)

    if answer is None and not os.path.exists(image_path):
        sent_msg = bot.send_message(chat_id, 'Информация по запросу "Разработчик" не найдена.')
    last_messages[chat_id] = sent_msg.message_id


#--------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == 'Дизайнер')
def handle_chfr_text(message):
    chat_id = message.chat.id
    delete_previous_message(chat_id)
    answer = get_answer_for_key('Дизайнер')
    image_path = os.path.join(BASE_DIR, "IMAGES", "CHFR2.png")

    try:
        with open(image_path, "rb") as photo:
            sent_msg = bot.send_photo(chat_id, photo, caption=answer)
    except FileNotFoundError:
        sent_msg = bot.send_message(chat_id, "Фото не найдено.")
        if answer:
            bot.send_message(chat_id, answer)
    except Exception as e:
        sent_msg = bot.send_message(chat_id, f"Произошла ошибка при отправке фото: {e}")
        if answer:
            bot.send_message(chat_id, answer)

    if answer is None and not os.path.exists(image_path):
        sent_msg = bot.send_message(chat_id, 'Информация по запросу "Дизайнер" не найдена.')
    last_messages[chat_id] = sent_msg.message_id


#--------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == '📱Соцсети📱')
def handle_social_media(message):
    chat_id = message.chat.id
    delete_previous_message(chat_id)
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    tg = telebot.types.KeyboardButton('✈️Telegram✈️')
    ig = telebot.types.KeyboardButton('📸Instagram📸')
    gt = telebot.types.KeyboardButton('😺Github😺')
    mail = telebot.types.KeyboardButton('📪Mail📪')
    back = telebot.types.KeyboardButton('⬅️Назад⬅️')
    markup.add(tg, ig, gt, mail, back)
    sent_msg = bot.send_message(chat_id, 'Выберите соцсети:', reply_markup=markup)
    last_messages[chat_id] = sent_msg.message_id


#--------------------------------------------------------------

@bot.message_handler(func=lambda message: message.text == '✈️Telegram✈️')
def handle_telegram(message):
    chat_id = message.chat.id
    delete_previous_message(chat_id)
    answer = get_answer_for_key('ТГ')
    sent_msg = bot.send_message(chat_id,
                             answer if answer else 'Информация по запросу "Telegram" не найдена.')
    last_messages[chat_id] = sent_msg.message_id


@bot.message_handler(func=lambda message: message.text == '📸Instagram📸')
def handle_instagram(message):
    chat_id = message.chat.id
    delete_previous_message(chat_id)
    answer = get_answer_for_key('ИНСТ')
    sent_msg = bot.send_message(chat_id,
                             answer if answer else 'Информация по запросу "Instagram" не найдена.')
    last_messages[chat_id] = sent_msg.message_id


@bot.message_handler(func=lambda message: message.text == '😺Github😺')
def handle_github(message):
    chat_id = message.chat.id
    delete_previous_message(chat_id)
    answer = get_answer_for_key('ГТ')
    sent_msg = bot.send_message(chat_id,
                             answer if answer else 'Информация по запросу "Github" не найдена.')
    last_messages[chat_id] = sent_msg.message_id


@bot.message_handler(func=lambda message: message.text == '📪Mail📪')
def handle_mail(message):
    chat_id = message.chat.id
    delete_previous_message(chat_id)
    answer = get_answer_for_key('Мыло')
    sent_msg = bot.send_message(chat_id,
                             answer if answer else 'Информация по запросу "Mail" не найдена.')
    last_messages[chat_id] = sent_msg.message_id


#--------------------------------------------------------------

@bot.message_handler(func=lambda message: message.text == '🗞Новостные рассылки🗞')
def handle_newsletters(message):
    chat_id = message.chat.id
    delete_previous_message(chat_id)
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    sb = telebot.types.KeyboardButton('✅Подписаться на рассылку✅')
    unsb = telebot.types.KeyboardButton('❌Отписаться с рассылки❌')
    back = telebot.types.KeyboardButton('⬅️Назад⬅️')
    markup.add(sb, unsb, back)
    sent_msg = bot.send_message(chat_id, 'Выберите действие:', reply_markup=markup)
    last_messages[chat_id] = sent_msg.message_id


#--------------------------------------------------------------

@bot.message_handler(func=lambda message: message.text == '✅Подписаться на рассылку✅')
def subscribe(message):
    chat_id = message.chat.id
    delete_previous_message(chat_id)
    add_subscriber(chat_id)
    sent_msg = bot.send_message(chat_id, '✅Вы успешно подписались на рассылку!')
    last_messages[chat_id] = sent_msg.message_id


@bot.message_handler(func=lambda message: message.text == '❌Отписаться с рассылки❌')
def unsubscribe(message):
    chat_id = message.chat.id
    delete_previous_message(chat_id)
    remove_subscriber(chat_id)
    sent_msg = bot.send_message(chat_id, '❌Вы успешно отписались с рассылки!')
    last_messages[chat_id] = sent_msg.message_id


@bot.message_handler(commands=['send'])
def send_news(message):
    chat_id = message.chat.id
    delete_previous_message(chat_id)
    if message.from_user.id != ADMIN_ID and message.from_user.id != ADMIN_ID2:
        sent_msg = bot.send_message(chat_id, "⛔ У вас нет прав на выполнение этой команды.")
        last_messages[chat_id] = sent_msg.message_id
        return

    text = message.text.partition(' ')[2].strip()
    if not text:
        sent_msg = bot.send_message(chat_id, "⚠️ Пожалуйста, укажите сообщение после команды /send.")
        last_messages[chat_id] = sent_msg.message_id
        return

    subscribers = load_subscribers()
    success = 0
    fail = 0

    for user_id in subscribers:
        try:
            bot.send_message(user_id, f"📰 {text}")
            success += 1
        except:
            fail += 1

    sent_msg = bot.send_message(chat_id, f"📤 Рассылка завершена. Успешно: {success}, ошибок: {fail}")
    last_messages[chat_id] = sent_msg.message_id
    
#--------------------------------------------------------------
user_image_index = {} 


image_paths = [ # Путь к изображениям вашей презентации
    'slides/1.png',
    'slides/2.png',
    'slides/3.png',
    'slides/4.png',
    'slides/5.png',
    'slides/6.png',
    'slides/7.png',
    'slides/8.png',
    'slides/9.png',
    'slides/10.png'
]

user_image_index = {}
#--------------------------------------------------------------

#--------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == "📊Презентация📊")# Задаём ответ на "Презентация"
def press(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    look = telebot.types.KeyboardButton("👀Просмотреть Презентацию👀")
    download = telebot.types.KeyboardButton("📲Скачать Презентацию📲")
    back = telebot.types.KeyboardButton("⬅️Назад⬅️")
    markup.add(look, download, back)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
#--------------------------------------------------------------

#--------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == "👀Просмотреть Презентацию👀")# Функция для просмотра презентации
def send_first_image(message):
    chat_id = message.chat.id
    user_image_index[chat_id] = 0
    with open(image_paths[0], 'rb') as photo:
        markup = telebot.types.InlineKeyboardMarkup()
        next_button = telebot.types.InlineKeyboardButton("➡️", callback_data='next')
        markup.add(next_button)
        bot.send_photo(chat_id, photo, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'next' or call.data == 'prev')
def navigate_images(call):
    chat_id = call.message.chat.id
    current_index = user_image_index.get(chat_id, 0)

    if call.data == 'next':
        new_index = current_index + 1
    else:
        new_index = current_index - 1

    if 0 <= new_index < len(image_paths):
        user_image_index[chat_id] = new_index
        with open(image_paths[new_index], 'rb') as photo:
            markup = telebot.types.InlineKeyboardMarkup()
            buttons = []
            if new_index > 0:
                buttons.append(telebot.types.InlineKeyboardButton("⬅️", callback_data='prev')) #Создаём кнопку "назад"
            if new_index < len(image_paths) - 1:
                buttons.append(telebot.types.InlineKeyboardButton("➡️", callback_data='next')) #Создаём кнопку "вперёд"
            markup.add(*buttons)
            bot.edit_message_media(telebot.types.InputMediaPhoto(photo), chat_id=chat_id, message_id=call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id)
    else:
        bot.answer_callback_query(call.id, "Это последняя/первая картинка!")

@bot.message_handler(func=lambda message: message.text == "📲Скачать Презентацию📲") # Функция для скачивания презентации
def send_first_image(message):
    chat_id = message.chat.id

    try:
        with open('slides/BricklyPresentation.pdf', 'rb') as document:
            bot.send_document(chat_id, document)
        print("The document has been sent successfully.")
    except FileNotFoundError:
        bot.send_message(chat_id, "Файл не найден.")
    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка при отправке документа: {e}")

#--------------------------------------------------------------

#--------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == '⬅️Назад⬅️') # Функция для навигации назад
def handle_back_button(message):
    menu(message)
#--------------------------------------------------------------



bot.polling()

# import telebot

# # Замени 'YOUR_BOT_TOKEN' на токен своего бота
# bot = telebot.TeleBot('8098581524:AAEQaZh_jZRdd-WDvzWs3ZDZY-idkE9uhkg')

# # Словарь для хранения ID последних сообщений в каждом чате
# last_messages = {}

# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     sent_msg = bot.send_message(message.chat.id, "Привет! Я бот, который удаляет предыдущие сообщения.")
#     last_messages[message.chat.id] = sent_msg.message_id

# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     chat_id = message.chat.id
#     if chat_id in last_messages:
#         try:
#             bot.delete_message(chat_id, last_messages[chat_id])
#         except telebot.apihelper.ApiTelegramException as e:
#             # Обработка ошибки, если сообщение уже удалено или недоступно
#             print(f"Ошибка при удалении сообщения: {e}")
#     sent_msg = bot.send_message(chat_id, message.text)
#     last_messages[chat_id] = sent_msg.message_id

# if __name__ == '__main__':
#     print("Бот запущен...")
#     bot.polling(none_stop=True)