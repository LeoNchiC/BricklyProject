#Brickly - интуитивно понятный редактор сайтов, позволяющий создавать и редактировать
#различные виды сайтов без знания программирования. Идеально подходит для учреждений
#образования и начинающих предпринимателей!

#Это код бота нашего проекта, разршено полное пользование кодом - бесплатно

#FLIPUK DEVELOPER

import telebot
import os

API_TOKEN = ''

bot = telebot.TeleBot(API_TOKEN)

# Айди админов для отправки рассылок
ADMIN_ID = 
ADMIN_ID2 = 

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
@bot.message_handler(commands=['start']) # Задаем команду /start
def welcome(message):
    user_name = message.from_user.first_name 
    greeting = f"{user_name}"  

    bot.send_message(message.chat.id, f"Добро Пожаловать в Brickly Project, {greeting}! \nЗдесь вы можете получить информацию о Brickly Project и его услугах.")

    menu(message)

#--------------------------------------------------------------
@bot.message_handler(commands=['menu'])  # Задаем команду /menu
def menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    about = telebot.types.KeyboardButton('📖О нас📖')
    structure = telebot.types.KeyboardButton('🛠Структура Проекта🛠')
    autors = telebot.types.KeyboardButton('🧑‍💻Авторы Проекта🧑‍💻')
    social = telebot.types.KeyboardButton('📱Соцсети📱')
    news = telebot.types.KeyboardButton('🗞Новостные рассылки🗞')
    presentation = telebot.types.KeyboardButton('📊Презентация📊')
    # donate = telebot.types.KeyboardButton('Донат')
    markup.add(about, structure, autors, social, news, presentation)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)

#--------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == '📖О нас📖') # Задаем ответ на "О нас"
def about(message):
    answer = get_answer_for_key('О нас')
    if answer is not None: 
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, 'Информация по запросу "О нас" не найдена или произошла ошибка при чтении файла.')

#--------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == '🛠Структура Проекта🛠') # Задаем ответ на "Cтруктуру Проекта"
def handle_structure_project_text(message):
    try:
        with open("IMAGES/structure.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo)
    except FileNotFoundError:
        print("Structure file not found.")
        bot.send_message(message.chat.id, "Изображение структуры не найдено.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при отправке изображения: {e}")

    answer = get_answer_for_key('Структура Brickly Project')
    if answer is not None:
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, 'Информация по запросу "Структура Brickly Project" не найдена в файле или произошла ошибка при чтении.')

#--------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == '🧑‍💻Авторы Проекта🧑‍💻')# Задаем ответ на "Авторы Проекта" 
def handle_authors_text(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    flipuk = telebot.types.InlineKeyboardButton('CTO')
    chfr = telebot.types.InlineKeyboardButton('CEO')
    bulka = telebot.types.InlineKeyboardButton('DEV')
    back = telebot.types.InlineKeyboardButton('⬅️Назад⬅️')
    markup.add(flipuk, chfr, bulka, back)
    bot.send_message(message.chat.id, 'Авторы проекта:', reply_markup=markup)

#--------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == 'CTO') # Задаем ответ на "Разработчик"
def handle_flipuk_text(message):

    answer = get_answer_for_key('CTO') 

    flipuk4_image_path = os.path.join(BASE_DIR, "IMAGES", "Flipuk4.png") # Путь к фото
    try:

        with open(flipuk4_image_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption=answer if answer else None)

    except FileNotFoundError:
        print(f"Photo not found on route: {flipuk4_image_path}")
        bot.send_message(message.chat.id, "Фото не найдено.")

        if answer:
             bot.send_message(message.chat.id, answer)

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при отправке фото: {e}")
        if answer:
             bot.send_message(message.chat.id, answer)

    if answer is None and not os.path.exists(flipuk4_image_path):
         bot.send_message(message.chat.id, 'Информация по запросу "CTO" не найдена (фото или текст).')

#--------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == 'CEO') # Задаем ответ на "Дизайнер"
def handle_chfr_text(message):

    answer = get_answer_for_key('CEO')

    CHFR2_image_path = os.path.join(BASE_DIR, "IMAGES", "CHFR2.png") # Путь к фото
    try:

        with open(CHFR2_image_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption=answer if answer else None)

    except FileNotFoundError:
        print(f"Photo not found on route: {CHFR2_image_path}")
        bot.send_message(message.chat.id, "Фото не найдено.")

        if answer:
             bot.send_message(message.chat.id, answer)

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при отправке фото: {e}")
        if answer:
             bot.send_message(message.chat.id, answer)

    if answer is None and not os.path.exists(CHFR2_image_path):
         bot.send_message(message.chat.id, 'Информация по запросу "CEO" не найдена (фото или текст).')

#--------------------------------------------------------------

#--------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == 'DEV') # Задаем ответ на "Дизайнер"
def handle_chfr_text(message):

    answer = get_answer_for_key('FULLSTACK')

    BULKA_image_path = os.path.join(BASE_DIR, "IMAGES", "BULKA.png") # Путь к фото
    try:

        with open(BULKA_image_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption=answer if answer else None)

    except FileNotFoundError:
        print(f"Photo not found on route: {BULKA_image_path}")
        bot.send_message(message.chat.id, "Фото не найдено.")

        if answer:
             bot.send_message(message.chat.id, answer)

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при отправке фото: {e}")
        if answer:
             bot.send_message(message.chat.id, answer)

    if answer is None and not os.path.exists(BULKA_image_path):
         bot.send_message(message.chat.id, 'Информация по запросу "DEV" не найдена (фото или текст).')

#--------------------------------------------------------------

@bot.message_handler(func=lambda message: message.text == '📱Соцсети📱') # Задаем ответ на "Соцсети"
def handle_chfr_text(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    tg = telebot.types.KeyboardButton('✈️Telegram✈️')
    ig = telebot.types.KeyboardButton('📸Instagram📸')
    gt = telebot.types.KeyboardButton('😺Github😺')
    mail = telebot.types.KeyboardButton('📪Mail📪')
    site = telebot.types.KeyboardButton('🖥️Наш Сайт🖥️')
    back = telebot.types.KeyboardButton('⬅️Назад⬅️')
    markup.add(tg, ig, gt, mail, site, back)
    bot.send_message(message.chat.id, 'Выберите соцсети:', reply_markup=markup)
#--------------------------------------------------------------

#--------------------------------------------------------------

@bot.message_handler(func=lambda message: message.text == '✈️Telegram✈️') # Задаем ответ на "Telegram"
def handle_flipuk_text(message): 

    telegram_image_path = os.path.join(BASE_DIR, "IMAGES", "telegram.jpg") # Путь к фото
    
    try:
        # Создаем клавиатуру с кнопкой
        markup = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton("Перейти", url="https://t.me/bricklyproject")  
        markup.add(button)

        with open(telegram_image_path, "rb") as photo:
            bot.send_photo(
                message.chat.id, 
                photo,
                reply_markup=markup
            )

    except FileNotFoundError:
        print(f"Photo not found on route: {telegram_image_path}")
        # Отправляем кнопку даже если фото не найдено
        markup = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton("Перейти", url="https://t.me/bricklyproject")
        markup.add(button)
        
        bot.send_message(message.chat.id, "Фото не найдено.", reply_markup=markup)
       
@bot.message_handler(func=lambda message: message.text == '📸Instagram📸') # Задаем ответ на "Instagram"
def handle_flipuk_text(message): 

    instagram_image_path = os.path.join(BASE_DIR, "IMAGES", "instagram.jpg") # Путь к фото
    
    try:
        # Создаем клавиатуру с кнопкой
        markup = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton("Перейти", url="https://www.instagram.com/brickly.project?igsh=ajk1Z3Ixemp2dzg1")  
        markup.add(button)

        with open(instagram_image_path, "rb") as photo:
            bot.send_photo(
                message.chat.id, 
                photo,
                reply_markup=markup
            )

    except FileNotFoundError:
        print(f"Photo not found on route: {instagram_image_path}")
        # Отправляем кнопку даже если фото не найдено
        markup = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton("Перейти", url="https://www.instagram.com/brickly.project?igsh=ajk1Z3Ixemp2dzg1")
        markup.add(button)
        
        bot.send_message(message.chat.id, "Фото не найдено.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '😺Github😺') # Задаем ответ на "GitHub"
def handle_flipuk_text(message): 

    github_image_path = os.path.join(BASE_DIR, "IMAGES", "github.jpg") # Путь к фото
    
    try:
        # Создаем клавиатуру с кнопкой
        markup = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton("Перейти", url="https://github.com/LeoNchiC/BricklyProject/tree/main")  
        markup.add(button)

        with open(github_image_path, "rb") as photo:
            bot.send_photo(
                message.chat.id, 
                photo,
                reply_markup=markup
            )

    except FileNotFoundError:
        print(f"Photo not found on route: {github_image_path}")
        # Отправляем кнопку даже если фото не найдено
        markup = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton("Перейти", url="https://github.com/LeoNchiC/BricklyProject/tree/main")
        markup.add(button)
        
        bot.send_message(message.chat.id, "Фото не найдено.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '📪Mail📪') # Задаем ответ на "Mail"
def handle_flipuk_text(message):

    answer = get_answer_for_key('Мыло') 

    mail_image_path = os.path.join(BASE_DIR, "IMAGES", "mail.jpg") # Путь к фото
    try:

        with open(mail_image_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption=answer if answer else None)

    except FileNotFoundError:
        print(f"Photo not found on route: {mail_image_path}")
        bot.send_message(message.chat.id, "Фото не найдено.")

        if answer:
             bot.send_message(message.chat.id, answer)

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при отправке фото: {e}")
        if answer:
             bot.send_message(message.chat.id, answer)

    if answer is None and not os.path.exists(mail_image_path):
         bot.send_message(message.chat.id, 'Информация по запросу "📪Mail📪" не найдена или произошла ошибка при чтении файла.(фото или текст).')


@bot.message_handler(func=lambda message: message.text == '🖥️Наш Сайт🖥️') # Задаем ответ на "Наш сайт"
def handle_flipuk_text(message): 

    site_image_path = os.path.join(BASE_DIR, "IMAGES", "site.jpg") # Путь к фото
    
    try:
        # Создаем клавиатуру с кнопкой
        markup = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton("Перейти", url="https://brickly.by/")  
        markup.add(button)

        with open(site_image_path, "rb") as photo:
            bot.send_photo(
                message.chat.id, 
                photo,
                reply_markup=markup
            )

    except FileNotFoundError:
        print(f"Photo not found on route: {site_image_path}")
        # Отправляем кнопку даже если фото не найдено
        markup = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton("Перейти", url="https://brickly.by/")
        markup.add(button)
        
        bot.send_message(message.chat.id, "Фото не найдено.", reply_markup=markup)


        
#--------------------------------------------------------------

#--------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == '🗞Новостные рассылки🗞') # Задаем ответ на "Рассылки"
def news(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    sb = telebot.types.KeyboardButton('✅Подписаться на рассылку✅')
    unsb = telebot.types.KeyboardButton('❌Отписаться с рассылки❌')
    back = telebot.types.KeyboardButton('⬅️Назад⬅️')
    markup.add(sb, unsb, back)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
#--------------------------------------------------------------

#--------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == '✅Подписаться на рассылку✅') # Функция подписки на рассылку
def subscribe(message):
    add_subscriber(message.chat.id)
    bot.send_message(message.chat.id, '✅Вы успешно подписались на рассылку!')

@bot.message_handler(func=lambda message: message.text == '❌Отписаться с рассылки❌') # Функция отписки от рассылки
def unsubscribe(message):
    remove_subscriber(message.chat.id)
    bot.send_message(message.chat.id, '❌Вы успешно отписались с рассылки!')

@bot.message_handler(commands=['send']) # Функция отправки сообщения(для Админов)
def send_news(message):
    if message.from_user.id != ADMIN_ID and message.from_user.id != ADMIN_ID2:
        bot.send_message(message.chat.id, "⛔ У вас нет прав на выполнение этой команды.")
        return
    
    text = message.text.partition(' ')[2].strip()
    if not text:
        bot.send_message(message.chat.id, "⚠️ Пожалуйста, укажите сообщение после команды /send.")
        return
#--------------------------------------------------------------
    
    subscribers = load_subscribers()
    success = 0 
    fail = 0

    for user_id in subscribers:
        try:
            bot.send_message(user_id, f"📰 {text}")
            success += 1
        except:
            fail += 1

    bot.send_message(message.chat.id, f"📤 Рассылка завершена. Успешно: {success}, ошибок: {fail}")
    
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


@bot.message_handler(func=lambda message: True)
def fallback_handler(message):
    bot.send_message(message.chat.id, "о как")


bot.polling()


