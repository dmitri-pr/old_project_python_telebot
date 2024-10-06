import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from geopy.geocoders import Nominatim
from geopy import distance
import json
import random
import sqlite3
from DB_manager import DB

bot = telebot.TeleBot("TOKEN", parse_mode=None)

# conn = sqlite3.connect('TB_.sqlite')
# cur = conn.cursor()
#
# cur.execute('''CREATE TABLE IF NOT EXISTS Users
#     (id INTEGER NOT NULL PRIMARY KEY, user_bot_id INTEGER UNIQUE, sex TEXT,
#      age TEXT, town TEXT)''')
#
# cur.execute('''CREATE TABLE IF NOT EXISTS Users_gelo
#     (id INTEGER NOT NULL PRIMARY KEY, user_bot_id INTEGER UNIQUE, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION )''')
#
# cur.execute('''CREATE TABLE IF NOT EXISTS Users_likes
#     (id INTEGER NOT NULL PRIMARY KEY, user_bot_id INTEGER UNIQUE, likes INTEGER, dislikes INTEGER )''')

HELP = """
/help - помощь;
/start - регистрация в боте;
/stop - прекращение диалога."""

users_reg = dict()
users_gelo = dict()
users_likes = dict()
user_step = dict()
user_letters = dict()
user_filter = dict()
user_pairs = dict()
# mid = dict()

letters = ['А', 'Б', 'В', 'Г', 'Д', ' Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н',
           'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я']

towns = ['Абакан', 'Азов', 'Александров', 'Алексин', 'Альметьевск', 'Анапа', 'Ангарск',
         'Анжеро-Судженск', 'Апатиты', 'Арзамас', 'Армавир', 'Арсеньев', 'Артем', 'Архангельск', 'Асбест', 'Астрахань',
         'Ачинск', 'Балаково', 'Балахна', 'Балашиха', 'Балашов', 'Барнаул', 'Батайск', 'Белгород', 'Белебей', 'Белово',
         'Белогорск (Амурская область)', 'Белорецк', 'Белореченск', 'Бердск', 'Березники',
         'Березовский (Свердловская область)',
         'Бийск', 'Биробиджан', 'Благовещенск (Амурская область)', 'Бор', 'Борисоглебск', 'Боровичи', 'Братск',
         'Брянск',
         'Бугульма', 'Буденновск', 'Бузулук', 'Буйнакск', 'Великие Луки', 'Великий Новгород', 'Верхняя Пышма', 'Видное',
         'Владивосток', 'Владикавказ', 'Владимир', 'Волгоград', 'Волгодонск', 'Волжск', 'Волжский', 'Вологда', 'Вольск',
         'Воркута', 'Воронеж', 'Воскресенск', 'Воткинск', 'Всеволожск', 'Выборг', 'Выкса', 'Вязьма', 'Гатчина',
         'Геленджик',
         'Георгиевск', 'Глазов', 'Горно-Алтайск', 'Грозный', 'Губкин', 'Гудермес', 'Гуково', 'Гусь-Хрустальный',
         'Дербент',
         'Дзержинск', 'Димитровград', 'Дмитров', 'Долгопрудный', 'Домодедово', 'Донской', 'Дубна', 'Евпатория',
         'Егорьевск',
         'Ейск', 'Екатеринбург', 'Елабуга', 'Елец', 'Ессентуки', 'Железногорск (Красноярский край)',
         'Железногорск (Курская область)',
         'Жигулевск', 'Жуковский', 'Заречный', 'Зеленогорск', 'Зеленодольск', 'Златоуст', 'Иваново', 'Ивантеевка',
         'Ижевск',
         'Избербаш', 'Иркутск', 'Искитим', 'Ишим', 'Ишимбай', 'Йошкар-Ола', 'Казань', 'Калининград', 'Калуга',
         'Каменск-Уральский',
         'Каменск-Шахтинский', 'Камышин', 'Канск', 'Каспийск', 'Кемерово', 'Керчь', 'Кинешма', 'Кириши',
         'Киров (Кировская область)',
         'Кирово-Чепецк', 'Киселевск', 'Кисловодск', 'Клин', 'Клинцы', 'Ковров', 'Когалым', 'Коломна',
         'Комсомольск-на-Амуре',
         'Копейск', 'Королев', 'Кострома', 'Котлас', 'Красногорск', 'Краснодар', 'Краснокаменск', 'Краснокамск',
         'Краснотурьинск',
         'Красноярск', 'Кропоткин', 'Крымск', 'Кстово', 'Кузнецк', 'Кумертау', 'Кунгур', 'Курган', 'Курск', 'Кызыл',
         'Лабинск',
         'Лениногорск', 'Ленинск-Кузнецкий', 'Лесосибирск', 'Липецк', 'Лиски', 'Лобня', 'Лысьва', 'Лыткарино',
         'Люберцы',
         'Магадан', 'Магнитогорск', 'Майкоп', 'Махачкала', 'Междуреченск', 'Мелеуз', 'Миасс', 'Минеральные Воды',
         'Минусинск',
         'Михайловка', 'Михайловск (Ставропольский край)', 'Мичуринск', 'Москва', 'Мурманск', 'Муром', 'Мытищи',
         'Набережные Челны',
         'Назарово', 'Назрань', 'Нальчик', 'Наро-Фоминск', 'Находка', 'Невинномысск', 'Нерюнгри', 'Нефтекамск',
         'Нефтеюганск',
         'Нижневартовск', 'Нижнекамск', 'Нижний Новгород', 'Нижний Тагил', 'Новоалтайск', 'Новокузнецк',
         'Новокуйбышевск',
         'Новомосковск', 'Новороссийск', 'Новосибирск', 'Новотроицк', 'Новоуральск', 'Новочебоксарск', 'Новочеркасск',
         'Новошахтинск', 'Новый Уренгой', 'Ногинск', 'Норильск', 'Ноябрьск', 'Нягань', 'Обнинск', 'Одинцово',
         'Озерск (Челябинская область)', 'Октябрьский', 'Омск', 'Орел', 'Оренбург', 'Орехово-Зуево', 'Орск', 'Павлово',
         'Павловский Посад', 'Пенза', 'Первоуральск', 'Пермь', 'Петрозаводск', 'Петропавловск-Камчатский', 'Подольск',
         'Полевской', 'Прокопьевск', 'Прохладный', 'Псков', 'Пушкино', 'Пятигорск', 'Раменское', 'Ревда', 'Реутов',
         'Ржев',
         'Рославль', 'Россошь', 'Ростов-на-Дону', 'Рубцовск', 'Рыбинск', 'Рязань', 'Салават', 'Сальск', 'Самара',
         'Санкт-Петербург', 'Саранск', 'Сарапул', 'Саратов', 'Саров', 'Свободный', 'Севастополь', 'Северодвинск',
         'Северск',
         'Сергиев Посад', 'Серов', 'Серпухов', 'Сертолово', 'Сибай', 'Симферополь', 'Славянск-на-Кубани', 'Смоленск',
         'Соликамск', 'Солнечногорск', 'Сосновый Бор', 'Сочи', 'Ставрополь', 'Старый Оскол', 'Стерлитамак', 'Ступино',
         'Сургут', 'Сызрань', 'Сыктывкар', 'Таганрог', 'Тамбов', 'Тверь', 'Тимашевск', 'Тихвин', 'Тихорецк', 'Тобольск',
         'Тольятти', 'Томск', 'Троицк', 'Туапсе', 'Туймазы', 'Тула', 'Тюмень', 'Узловая', 'Улан-Удэ', 'Ульяновск',
         'Урус-Мартан',
         'Усолье-Сибирское', 'Уссурийск', 'Усть-Илимск', 'Уфа', 'Ухта', 'Феодосия', 'Фрязино', 'Хабаровск',
         'Ханты-Мансийск',
         'Хасавюрт', 'Химки', 'Чайковский', 'Чапаевск', 'Чебоксары', 'Челябинск', 'Черемхово', 'Череповец', 'Черкесск',
         'Черногорск', 'Чехов', 'Чистополь', 'Чита', 'Шадринск', 'Шали', 'Шахты', 'Шуя', 'Щекино', 'Щелково',
         'Электросталь',
         'Элиста', 'Энгельс', 'Южно-Сахалинск', 'Юрга', 'Якутск', 'Ялта', 'Ярославль']


# hideBoard = ReplyKeyboardRemove()

def user_step_(cid):
    return user_step[cid]


def markup_gender():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="Мужской \u2642\uFE0F", callback_data="man"),
               InlineKeyboardButton(text="Женский \u2640\uFE0F", callback_data="woman"))
    return markup


def markup_age():
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(InlineKeyboardButton(text="до 14 лет", callback_data="14"),
               InlineKeyboardButton(text="15-17 лет", callback_data="17"),
               InlineKeyboardButton(text="18-21 год", callback_data="21"),
               InlineKeyboardButton(text="22-25 лет", callback_data="25"),
               InlineKeyboardButton(text="26-35 лет", callback_data="35"),
               InlineKeyboardButton(text="35+ лет", callback_data="35+"))
    return markup


def markup_town():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="Список городов 🌎", callback_data="list"),
               InlineKeyboardButton(text="Определить автоматически ⏭", callback_data="auto"))
    return markup


def markup_location():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    markup.add(KeyboardButton('Отправить геопозицию 📍', request_location=True), KeyboardButton('Назад \u21A9\uFE0F'))
    return markup


def markup_alphabet():
    buttons = [InlineKeyboardButton(text=letter, callback_data=letter)
               for letter in letters]
    markup = InlineKeyboardMarkup(row_width=5)
    markup.add(*buttons).row(InlineKeyboardButton(text="Назад \u21A9\uFE0F", callback_data="Назад \u21A9\uFE0F"))
    return markup


def markup_towns_list(letter):
    buttons = [InlineKeyboardButton(text=town, callback_data=town)
               for town in towns if town.startswith(letter)]
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(*buttons).row(InlineKeyboardButton(text="Назад \u21A9\uFE0F", callback_data="Назад \u21A9\uFE0F"))
    return markup


def part_towns_list(letter):
    return [town for town in towns if town.startswith(letter)]


def const_kearboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    markup.add(KeyboardButton('Поиск собеседника 💆'), KeyboardButton('Мой профиль 👤'))
    return markup


def change_profile():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text='Изменить профиль ⚙️', callback_data='Изменить профиль \u2699\uFE0F'))
    return markup


def markup_search():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton(text="Настроить поиск ⚙️", callback_data="Настроить поиск ⚙️"),
               InlineKeyboardButton(text="Очистить фильтр 🗑️", callback_data="Очистить фильтр 🗑️")
               ).row(InlineKeyboardButton(text="Начать поиск 🔎", callback_data="Начать поиск 🔎"))
    return markup


def markup_set_search():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="Пол 👫", callback_data="Пол 👫"),
               InlineKeyboardButton(text="Возраст 🗓️", callback_data="Возраст 🗓️"),
               InlineKeyboardButton(text="Город 🏙️", callback_data="Город 🏙️"),
               InlineKeyboardButton(text="Назад \u21A9\uFE0F", callback_data="back_from_set_to_search"))
    return markup


def markup_set_sex_search():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="Мужской \u2642\uFE0F", callback_data="Мужской \u2642\uFE0F"),
               InlineKeyboardButton(text="Женский \u2640\uFE0F", callback_data="Женский \u2640\uFE0F"),
               InlineKeyboardButton(text="Неважно", callback_data="None_sex"),
               InlineKeyboardButton(text="Назад \u21A9\uFE0F", callback_data=
               "back_from_set_sex_to_set_search"))
    return markup


def markup_set_age_search():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton(text="до 14 лет", callback_data="14"),
               InlineKeyboardButton(text="15-17 лет", callback_data="17"),
               InlineKeyboardButton(text="18-21 год", callback_data="21"),
               InlineKeyboardButton(text="22-25 лет", callback_data="25"),
               InlineKeyboardButton(text="26-35 лет", callback_data="35"),
               InlineKeyboardButton(text="35+ лет", callback_data="35+")
               ).row(InlineKeyboardButton(text="Неважно", callback_data="None_age")
                     ).row(InlineKeyboardButton(text="Назад \u21A9\uFE0F", callback_data=
    "back_from_set_age_to_set_search"))
    return markup


def markup_set_town_search():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="Мой город 🏙️", callback_data="Мой город 🏙️"),
               InlineKeyboardButton(text="Список городов 🌎", callback_data='5'),
               InlineKeyboardButton(text="Неважно", callback_data="None_town"),
               InlineKeyboardButton(text="Назад \u21A9\uFE0F", callback_data=
               "back_from_set_town_to_set_search"))
    return markup


def markup_like_dislike():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton(text="👍️", callback_data="cb_like"),
               InlineKeyboardButton(text="👎️", callback_data="cb_dislike"))
    return markup


def users_base_search(cid, *args):
    # conn = sqlite3.connect('TB_.sqlite')
    # cur = conn.cursor()
    # cur.execute('SELECT * FROM Users WHERE user_bot_id!=?', ( cid, ))
    # rows = cur.fetchall()
    rows = DB.check_all_users_ids()
    l = [arg for arg in args if arg != 'Неважно']
    if l == []:
        if [row[0] for row in rows if user_step.get(row[0], 0) != 10
                                      and user_step.get(row[0], None) != None and row[0] not in user_pairs.keys() and
                                      row[0] not in
                                      user_pairs.values()] == []:
            result = None
        else:
            result = random.choice([row[0] for row in rows if user_step.get(row[0], 0) != 10
                                    and user_step.get(row[0], None) != None and row[0] not in user_pairs.keys() and row[
                                        0] not in
                                    user_pairs.values()])
    else:
        if [row[1] for row in rows if all(arg in row for arg in l
                                          ) and user_step.get(row[1], None) != 10 and user_step.get(row[0],
                                                                                                    None) != None
                                      and row[0] not in user_pairs.keys() and row[0] not in user_pairs.values()] == []:
            result = None
        else:
            result = random.choice([row[0] for row in rows if all(arg in row for arg in l
                                                                  ) and user_step.get(row[0],
                                                                                      0) != 10 and user_step.get(row[0],
                                                                                                                 None) != None
                                    and row[0] not in user_pairs.keys() and row[0] not in user_pairs.values()])
    return result


def flag_in_not_in(rows, cid):
    flag = 0
    for row in rows:
        if row[0] == cid:
            flag = 1
            break
    return flag


def change_sex(text, text_, markup_set_field_search):
    @bot.callback_query_handler(func=lambda call: call.data == text)
    def callback_query(call):
        user_filter[call.message.chat.id][0] = text_
        text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
        {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text, reply_markup=markup_set_field_search())
        user_step[call.message.chat.id] = 0


def rating_with_like_dislike(callid, like, cid, place, mid):
    bot.answer_callback_query(callid, like)
    for k, v in user_pairs.items():
        if cid == k:
            users_likes[v][place] += 1
            bot.edit_message_reply_markup(chat_id=cid,
                                          message_id=mid, reply_markup=None)
            k_ = k
            v_ = v
            break
        elif cid == v:
            users_likes[k][place] += 1
            bot.edit_message_reply_markup(chat_id=cid,
                                          message_id=mid, reply_markup=None)
            k_ = k
            v_ = v
            break
    return [k_, v_]


@bot.message_handler(commands=['help'])
def help(message):
    # conn = sqlite3.connect('TB_.sqlite')
    # cur = conn.cursor()
    # cur.execute('SELECT user_bot_id FROM Users')
    # rows = cur.fetchall()
    rows = DB.check_all_users_ids()
    cid = message.chat.id
    bot.send_message(cid, HELP)
    # flag = 0
    # for row in rows:
    #     if row[0] == message.chat.id:
    #         flag = 1
    #         break
    if flag_in_not_in(rows, cid) == 0:
        text = 'Здравствуйте! Для начала Вам нужно пройти быструю регистрацию, введя\
        команду /start или просто набрав какой-либо текст.'
        bot.send_message(cid, text)
        text = 'После этого Вы сможете менять информацию в своем профиле и настраивать\
         и осуществлять поиск собеседников посредством кнопок специальной клавиатуры'
        bot.send_message(cid, text)
        text = 'Вы можете оценивать своих собеседников (до завершения диалога) посредством\
         нажатия кнопок 👍️ или 👎️'
        bot.send_message(cid, text)
        text = 'Чтобы прекратить общение с собеседником, введите /stop'
        bot.send_message(cid, text)
        user_step[cid] = 0
    else:
        text = 'Здравствуйте, я Вас знаю, Вы уже регистрировались!\nВы можете отредактировать свой профиль\
        в любой момент (кнопка "Мой профиль 👤" на клавиатуре)\nЧтобы начать общение,\
        используйте меню ниже\nВы также можете получить дополнительную информацию, введя команду /help\nУдачи!'
        bot.send_message(message.chat.id, text, reply_markup=const_kearboard())
        user_step[cid] = 0


@bot.message_handler(commands=['start'])
def command_reg(message):
    # conn = sqlite3.connect('TB_.sqlite')
    # cur = conn.cursor()
    # cur.execute('SELECT user_bot_id FROM Users')
    # rows = cur.fetchall()
    rows = DB.check_all_users_ids()
    cid = message.chat.id
    # flag = 0
    # for row in rows:
    #     if row[0] == message.chat.id:
    #         flag = 1
    #         break
    if flag_in_not_in(rows, cid) == 0:
        text = 'Добро пожаловать в наш телеграм бот! Тут Вы сможете найти себе новые знакомства и общение'
        bot.send_message(cid, text)
        text = 'Но сначала пройдите быструю регистрацию'
        bot.send_message(cid, text)
        text = '1. Выберите свой пол:'
        bot.send_message(cid, text, reply_markup=markup_gender())
        user_step[cid] = 1
    else:
        text = 'Здравствуйте, я Вас знаю, Вы уже регистрировались!\nВы можете отредактировать свой профиль\
        в любой момент (кнопка "Мой профиль 👤" на клавиатуре)\nЧтобы начать общение,\
        используйте меню ниже\nВы также можете получить дополнительную информацию, введя команду /help\nУдачи!'
        bot.send_message(message.chat.id, text, reply_markup=const_kearboard())
        user_step[cid] = 0


@bot.message_handler(commands=['stop'])
def stop_communication(message):
    cid = message.chat.id
    try:
        if user_step[message.chat.id] == 10:
            for k, v in user_pairs.items():
                if message.chat.id == k:
                    user_step[message.chat.id] = 0
                    user_step[v] = 0
                    bot.send_message(k, 'Вы прекратили диалог...😥')
                    bot.send_message(v, 'Ваш собеседник прекратил диалог...😥')
                    break
                elif message.chat.id == v:
                    user_step[message.chat.id] = 0
                    user_step[k] = 0
                    bot.send_message(v, 'Вы прекратили диалог...😥')
                    bot.send_message(k, 'Ваш собеседник прекратил диалог...😥')
                    break
            del user_pairs[k]
    except KeyError:
        pass


@bot.message_handler(func=lambda message: message.text != 'Назад \u21A9\uFE0F' and
                                          message.text != 'Мой профиль 👤' and message.text != 'Изменить профиль \u2699\uFE0F' and
                                          message.text != 'Поиск собеседника 💆')
def command_reg(message):
    # conn = sqlite3.connect('TB_.sqlite')
    # cur = conn.cursor()
    # cur.execute('SELECT user_bot_id FROM Users')
    # rows = cur.fetchall()
    rows = DB.check_all_users_ids()
    cid = message.chat.id
    try:
        if user_step[message.chat.id] == 10:
            for k, v in user_pairs.items():
                if message.chat.id == k:
                    bot.send_message(v, message.text, reply_markup=markup_like_dislike())
                elif message.chat.id == v:
                    bot.send_message(k, message.text, reply_markup=markup_like_dislike())
    except KeyError:
        # flag = 0
        # for row in rows:
        #     if row[0] == message.chat.id:
        #         flag = 1
        #         break
        if flag_in_not_in(rows, cid) == 0:
            text = 'Добро пожаловать в наш телеграм бот! Тут Вы сможете найти себе новые знакомства и общение'
            bot.send_message(cid, text)
            text = 'Но сначала пройдите быструю регистрацию'
            bot.send_message(cid, text)
            text = '1. Выберите свой пол:'
            bot.send_message(cid, text, reply_markup=markup_gender())
            user_step[cid] = 1
        else:
            text = 'Здравствуйте, я Вас знаю, Вы уже регистрировались!\nВы можете отредактировать свой профиль\
            в любой момент (кнопка "Мой профиль 👤" на клавиатуре)\nЧтобы начать общение,\
            используйте меню ниже\nВы также можете получить дополнительную информацию, введя команду /help\nУдачи!'
            bot.send_message(message.chat.id, text, reply_markup=const_kearboard())
            user_step[cid] = 0
    else:
        # flag = 0
        # for row in rows:
        #     if row[0] == message.chat.id:
        #         flag = 1
        #         break
        if user_step[message.chat.id] != 10 and flag_in_not_in(rows, message.chat.id) == 1:
            text = 'Увы, но я плохой собеседник...'
            bot.send_message(message.chat.id, text, reply_markup=const_kearboard())
            text = 'Попробуй найти себе собеседника получше, нажав кнопку "Поиск собеседника 💆" на клавиатуре'
            bot.send_message(message.chat.id, text, reply_markup=const_kearboard())
            user_step[cid] = 0
        elif user_step[message.chat.id] != 10 and message.chat.id == 0:
            text = 'Добро пожаловать в наш телеграм бот! Тут Вы сможете найти себе новые знакомства и общение'
            bot.send_message(cid, text)
            text = 'Но сначала пройдите быструю регистрацию'
            bot.send_message(cid, text)
            text = '1. Выберите свой пол:'
            bot.send_message(cid, text, reply_markup=markup_gender())
            user_step[cid] = 1


@bot.callback_query_handler(func=lambda call: user_step_(call.message.chat.id) == 1)
def callback_query(call):
    if call.data == "man":
        users_reg[call.message.chat.id] = ["Мужской \u2642\uFE0F"]
        bot.answer_callback_query(call.id, "Мужской \u2642\uFE0F")
    elif call.data == "woman":
        users_reg[call.message.chat.id] = ["Женский \u2640\uFE0F"]
        bot.answer_callback_query(call.id, "Женский \u2640\uFE0F")
    text = '2. Выберите свой возраст:'
    bot.send_message(call.message.chat.id, text, reply_markup=markup_age())
    user_step[call.message.chat.id] = 2


@bot.callback_query_handler(func=lambda call: user_step_(call.message.chat.id) == 2)
def callback_query(call):
    if call.data == "14":
        users_reg[call.message.chat.id].append("до 14 лет")
        bot.answer_callback_query(call.id, "до 14 лет")
    elif call.data == "17":
        users_reg[call.message.chat.id].append("15-17 лет")
        bot.answer_callback_query(call.id, "15-17 лет")
    elif call.data == "21":
        users_reg[call.message.chat.id].append("18-21 год")
        bot.answer_callback_query(call.id, "18-21 год")
    elif call.data == "25":
        users_reg[call.message.chat.id].append("22-25 лет")
        bot.answer_callback_query(call.id, "22-25 лет")
    elif call.data == "35":
        users_reg[call.message.chat.id].append("26-35 лет")
        bot.answer_callback_query(call.id, "26-35 лет")
    elif call.data == "35+":
        users_reg[call.message.chat.id].append("35+ лет")
        bot.answer_callback_query(call.id, "35+ лет")
    text = '3. Выберите свой город:'
    bot.send_message(call.message.chat.id, text, reply_markup=markup_town())
    user_step[call.message.chat.id] = 3


@bot.callback_query_handler(func=lambda call: user_step_(call.message.chat.id) == 3)
def callback_query(call):
    if call.data == "list":
        bot.answer_callback_query(call.id, "Список городов 🌎")
        text = '3. Выберите первую букву города:'
        bot.send_message(call.message.chat.id, text, reply_markup=markup_alphabet())
        user_step[call.message.chat.id] = 3.1
    elif call.data == "auto":
        bot.answer_callback_query(call.id, "Определить автоматически ⏭")
        text = "3. Нажмите кнопку 'Отправить геопозицию 📍' на клавиатуре ниже"
        bot.send_message(call.message.chat.id, text, reply_markup=markup_location())
        user_step[call.message.chat.id] = 3.2


@bot.callback_query_handler(func=lambda call: user_step_(call.message.chat.id) == 3.1)
def callback_query(call):
    for letter in letters:
        if call.data == letter:
            bot.answer_callback_query(call.id, letter)
            text = '3. Выберите свой город:'
            bot.send_message(call.message.chat.id, text, reply_markup=markup_towns_list(letter))
            user_letters[call.message.chat.id] = letter
            user_step[call.message.chat.id] = 3.11
            break
    if call.data == "Назад \u21A9\uFE0F":
        if user_step[call.message.chat.id] == 3.1 or user_step[call.message.chat.id] == 3.2:
            text = '3. Выберите свой город:'
            bot.send_message(call.message.chat.id, text, reply_markup=markup_town())
            user_step[call.message.chat.id] = 3
        elif user_step[call.message.chat.id] == 3.11:
            text = '3. Выберите свой город:'
            bot.send_message(call.message.chat.id, text, reply_markup=markup_alphabet())
            user_step[call.message.chat.id] = 3.1


@bot.callback_query_handler(func=lambda call: user_step_(call.message.chat.id) == 3.11)
def callback_query(call):
    for town in part_towns_list(user_letters[call.message.chat.id]):
        if call.data == town:
            users_reg[call.message.chat.id].append(town)
            bot.answer_callback_query(call.id, town)
            user_step[call.message.chat.id] = 4
            # conn = sqlite3.connect('TB_.sqlite')
            # cur = conn.cursor()
            # cur.execute('SELECT user_bot_id FROM Users')
            # rows = cur.fetchall()
            rows = DB.check_all_users_ids()
            # flag = 0
            # for row in rows:
            #     if row[0] == call.message.chat.id:
            #         flag = 1
            #         break
            if flag_in_not_in(rows, call.message.chat.id) == 0:
                # cur.execute('''INSERT OR IGNORE INTO Users (user_bot_id, sex, age, town)
                #  VALUES (?, ?, ?, ?)''', (call.message.chat.id, users_reg[call.message.chat.id][0],
                #   users_reg[call.message.chat.id][1], users_reg[call.message.chat.id][2]) )
                DB.user_info_insert(call.message.chat.id, users_reg[call.message.chat.id][0],
                                    users_reg[call.message.chat.id][1], users_reg[call.message.chat.id][2])
            else:
                # cur.execute('''UPDATE Users SET sex=?, age=?, town=? WHERE user_bot_id=?''', (users_reg[call.message.chat.id][0],
                #   users_reg[call.message.chat.id][1], users_reg[call.message.chat.id][2],
                #   call.message.chat.id) )
                DB.user_info_update(users_reg[call.message.chat.id][0],
                                    users_reg[call.message.chat.id][1], users_reg[call.message.chat.id][2],
                                    call.message.chat.id)
            # conn.commit()
            text = 'Поздравляем с успешной регистрацией!\nВы можете отредактировать свой профиль\
            в любой момент (кнопка "Мой профиль 👤" на клавиатуре)\nЧтобы начать общение,\
            используйте меню ниже\nВы также можете получить дополнительную информацию, введя\
            команду /help\nУдачи!'
            bot.send_message(call.message.chat.id, text, reply_markup=const_kearboard())
            break
    if call.data == "Назад \u21A9\uFE0F":
        if user_step[call.message.chat.id] == 3.11:
            text = '3. Выберите свой город:'
            bot.send_message(call.message.chat.id, text, reply_markup=markup_alphabet())
            user_step[call.message.chat.id] = 3.1


@bot.message_handler(content_types=['location'])
def location(message):
    geolocator = Nominatim(user_agent="sbmt@rambler.ru")
    users_gelo[message.chat.id] = (message.location.latitude, message.location.longitude)
    # conn = sqlite3.connect('TB_.sqlite')
    # cur = conn.cursor()
    # cur.execute('SELECT user_bot_id FROM Users_gelo')
    # rows = cur.fetchall()
    rows = DB.check_all_gelo_users_ids()
    # flag = 0
    # for row in rows:
    #     if row[0] == message.chat.id:
    #         flag = 1
    #         break
    if flag_in_not_in(rows, message.chat.id) == 0:
        DB.user_gelo_insert(message.chat.id, users_gelo[message.chat.id][0],
                            users_gelo[message.chat.id][1])
    else:
        DB.user_gelo_update(users_gelo[message.chat.id][0],
                            users_gelo[message.chat.id][1], message.chat.id)
    location = geolocator.reverse('{} {}'.format(message.location.latitude, message.location.longitude))
    try:
        users_reg[message.chat.id].append(location.raw['address']['town'])
        bot.send_message(message.chat.id, f"Твой населенный пункт: {location.raw['address']['town']}")
    except KeyError:
        users_reg[message.chat.id].append(location.raw['address']['city'])
        bot.send_message(message.chat.id, f"Твой населенный пункт: {location.raw['address']['city']}")
    bot.send_message(message.chat.id, f"Твой подробный адрес: {location.address}")
    user_step[message.chat.id] = 4
    # cur.execute('SELECT user_bot_id FROM Users')
    # rows = cur.fetchall()
    rows = DB.check_all_users_ids()
    for row in rows:
        if row[0] == message.chat.id:
            flag = 1
            break
    if flag == 0:
        # cur.execute('''INSERT OR IGNORE INTO Users (user_bot_id, sex, age, town)
        #  VALUES (?, ?, ?, ?)''', (message.chat.id, users_reg[message.chat.id][0],
        #   users_reg[message.chat.id][1], users_reg[message.chat.id][2]) )
        DB.user_info_insert(message.chat.id, users_reg[message.chat.id][0],
                            users_reg[message.chat.id][1], users_reg[message.chat.id][2])
    else:
        #     cur.execute('''UPDATE Users SET sex=?, age=?, town=? WHERE user_bot_id=?''',
        #      (users_reg[message.chat.id][0], users_reg[message.chat.id][1],
        #       users_reg[message.chat.id][2], message.chat.id) )
        # conn.commit()
        DB.user_info_update(users_reg[message.chat.id][0],
                            users_reg[message.chat.id][1], users_reg[message.chat.id][2],
                            message.chat.id)
    text = 'Поздравляем с успешной регистрацией!\nВы можете отредактировать свой профиль\
    в любой момент (кнопка "Мой профиль 👤" на клавиатуре)\nЧтобы начать общение,\
    используйте меню ниже\nВы также можете получить дополнительную информацию, введя\
     команду /help\nУдачи!'
    bot.send_message(message.chat.id, text, reply_markup=const_kearboard())


@bot.message_handler(func=lambda message: message.text == 'Назад \u21A9\uFE0F')
def message_handler(message):
    if user_step[message.chat.id] == 3.1 or user_step[message.chat.id] == 3.2:
        text = '3. Выберите свой город:'
        bot.send_message(message.chat.id, text, reply_markup=markup_town())
        user_step[message.chat.id] = 3


@bot.message_handler(func=lambda message: message.text == 'Мой профиль 👤')
def command_reg(message):
    # conn = sqlite3.connect('TB_.sqlite')
    # cur = conn.cursor()
    # cur.execute('SELECT sex, age, town FROM Users WHERE user_bot_id=?', (message.chat.id,))
    # row = cur.fetchone()
    row = DB.lookup_person_info(message.chat.id)
    sex_ = row[0]
    age_ = row[1]
    town_ = row[2]
    text = f'👫Пол: {sex_}\n🗓️Возраст: {age_}\
    \n🏙️Город: {town_}'
    bot.send_message(message.chat.id, text, reply_markup=change_profile())
    user_step[message.chat.id] = 0


@bot.callback_query_handler(func=lambda call: call.data == 'Изменить профиль \u2699\uFE0F')
def callback_query(call):
    user_step[call.message.chat.id] = 0
    text = '1. Выберите свой пол:'
    bot.send_message(call.message.chat.id, text, reply_markup=markup_gender())
    user_step[call.message.chat.id] = 1


@bot.message_handler(func=lambda message: message.text == 'Поиск собеседника 💆')
def command_reg(message):
    user_filter[message.chat.id] = ['Неважно', 'Неважно', 'Неважно']
    text = f'Ваш фильтр:\n👫Пол: {user_filter[message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[message.chat.id][1]}\n🏙️Город: {user_filter[message.chat.id][2]}'
    # mid[message.chat.id] = bot.send_message(message.chat.id, text, reply_markup=markup_search()).message_id
    bot.send_message(message.chat.id, text, reply_markup=markup_search())
    user_step[message.chat.id] = 0
    # bot.edit_message_reply_markup(message.chat.id, )


@bot.callback_query_handler(func=lambda call: call.data == 'Настроить поиск ⚙️')
def callback_query(call):
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_set_search())
    user_step[call.message.chat.id] = 0


@bot.callback_query_handler(func=lambda call: call.data == 'Пол 👫')
def callback_query(call):
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_set_sex_search())
    user_step[call.message.chat.id] = 0


# @bot.callback_query_handler(func = lambda call: call.data == 'Мужской \u2642\uFE0F')
# def callback_query(call):
#     user_filter[call.message.chat.id][0] = 'Мужской \u2642\uFE0F'
#     text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
#     {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                    text=text, reply_markup=markup_set_sex_search())
#     user_step[call.message.chat.id] = 0
change_sex('Мужской \u2642\uFE0F', 'Мужской \u2642\uFE0F', markup_set_sex_search)

# @bot.callback_query_handler(func = lambda call: call.data == 'Женский \u2640\uFE0F')
# def callback_query(call):
#     user_filter[call.message.chat.id][0] = 'Женский \u2640\uFE0F'
#     text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
#     {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                    text=text, reply_markup=markup_set_sex_search())
#     user_step[call.message.chat.id] = 0
change_sex('Женский \u2640\uFE0F', 'Женский \u2640\uFE0F', markup_set_sex_search)

# @bot.callback_query_handler(func = lambda call: call.data == 'None_sex')
# def callback_query(call):
#     user_filter[call.message.chat.id][0] = 'Неважно'
#     text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
#     {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                    text=text, reply_markup=markup_set_sex_search())
#     user_step[call.message.chat.id] = 0
change_sex('None_sex', 'Неважно', markup_set_sex_search)


@bot.callback_query_handler(func=lambda call: call.data == 'back_from_set_sex_to_set_search')
def callback_query(call):
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_set_search())
    user_step[call.message.chat.id] = 0


@bot.callback_query_handler(func=lambda call: call.data == 'Возраст 🗓️')
def callback_query(call):
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_set_age_search())
    user_step[call.message.chat.id] = 0


@bot.callback_query_handler(func=lambda call: call.data == '14')
def callback_query(call):
    user_filter[call.message.chat.id][1] = 'до 14 лет'
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_set_age_search())
    user_step[call.message.chat.id] = 0


@bot.callback_query_handler(func=lambda call: call.data == '17')
def callback_query(call):
    user_filter[call.message.chat.id][1] = '15-17 лет'
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_set_age_search())
    user_step[call.message.chat.id] = 0


@bot.callback_query_handler(func=lambda call: call.data == '21')
def callback_query(call):
    user_filter[call.message.chat.id][1] = '18-21 год'
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_set_age_search())
    user_step[call.message.chat.id] = 0


@bot.callback_query_handler(func=lambda call: call.data == '25')
def callback_query(call):
    user_filter[call.message.chat.id][1] = '22-25 лет'
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_set_age_search())
    user_step[call.message.chat.id] = 0


@bot.callback_query_handler(func=lambda call: call.data == '35')
def callback_query(call):
    user_filter[call.message.chat.id][1] = '26-35 лет'
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_set_age_search())
    user_step[call.message.chat.id] = 0


@bot.callback_query_handler(func=lambda call: call.data == '35+')
def callback_query(call):
    user_filter[call.message.chat.id][1] = '35+ лет'
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_set_age_search())
    user_step[call.message.chat.id] = 0


@bot.callback_query_handler(func=lambda call: call.data == 'None_age')
def callback_query(call):
    user_filter[call.message.chat.id][1] = 'Неважно'
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_set_age_search())
    user_step[call.message.chat.id] = 0


@bot.callback_query_handler(func=lambda call: call.data == 'back_from_set_age_to_set_search')
def callback_query(call):
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_set_search())
    user_step[call.message.chat.id] = 0


@bot.callback_query_handler(func=lambda call: call.data == 'Город 🏙️')
def callback_query(call):
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_set_town_search())
    user_step[call.message.chat.id] = 0


@bot.callback_query_handler(func=lambda call: call.data == 'Мой город 🏙️')
def callback_query(call):
    # conn = sqlite3.connect('TB_.sqlite')
    # cur = conn.cursor()
    # cur.execute('SELECT town FROM Users WHERE user_bot_id=?',
    #      (call.message.chat.id,))
    # row = cur.fetchone()
    row = DB.choose_self_town_for_filter(call.message.chat.id)
    town_ = row[0]
    user_filter[call.message.chat.id][2] = town_
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_set_town_search())
    user_step[call.message.chat.id] = 0


@bot.callback_query_handler(func=lambda call: call.data == '5')  # Кнопка 'Список городов'
def callback_query(call):
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_alphabet())
    user_step[call.message.chat.id] = 5.1


@bot.callback_query_handler(func=lambda call: user_step_(call.message.chat.id) == 5.1)
def callback_query(call):
    for letter in letters:
        if call.data == letter:
            bot.answer_callback_query(call.id, letter)
            text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
            {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=text, reply_markup=markup_towns_list(letter))
            user_letters[call.message.chat.id] = letter
            user_step[call.message.chat.id] = 5.11
            break
    if call.data == "Назад \u21A9\uFE0F":
        if user_step[call.message.chat.id] == 5.1:
            text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
            {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=text, reply_markup=markup_set_town_search())
            user_step[call.message.chat.id] = 0
        elif user_step[call.message.chat.id] == 5.11:
            text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
            {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=text, reply_markup=markup_alphabet())
            user_step[call.message.chat.id] = 5.1


@bot.callback_query_handler(func=lambda call: user_step_(call.message.chat.id) == 5.11)
def callback_query(call):
    for town in part_towns_list(user_letters[call.message.chat.id]):
        if call.data == town:
            user_filter[call.message.chat.id][2] = town
            text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
            {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
            user_step[call.message.chat.id] = 6
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=text, reply_markup=markup_set_town_search())
            break
    if call.data == "Назад \u21A9\uFE0F":
        if user_step[call.message.chat.id] == 5.11:
            text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
            {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=text, reply_markup=markup_alphabet())
            user_step[call.message.chat.id] = 5.1


@bot.callback_query_handler(func=lambda call: call.data == 'None_town')
def callback_query(call):
    user_filter[call.message.chat.id][2] = 'Неважно'
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_set_town_search())
    user_step[call.message.chat.id] = 0


@bot.callback_query_handler(func=lambda call: call.data == 'back_from_set_town_to_set_search')
def callback_query(call):
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_set_search())
    user_step[call.message.chat.id] = 0


@bot.callback_query_handler(func=lambda call: call.data == 'back_from_set_to_search')
def callback_query(call):
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_search())
    user_step[call.message.chat.id] = 0


@bot.callback_query_handler(func=lambda call: call.data == 'Очистить фильтр 🗑️')
def callback_query(call):
    user_filter[call.message.chat.id] = ['Неважно', 'Неважно', 'Неважно']
    text = f'Ваш фильтр:\n👫Пол: {user_filter[call.message.chat.id][0]}\n🗓️Возраст: \
    {user_filter[call.message.chat.id][1]}\n🏙️Город: {user_filter[call.message.chat.id][2]}'
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=markup_search())
    user_step[call.message.chat.id] = 0


@bot.callback_query_handler(func=lambda call: call.data == 'Начать поиск 🔎')
def callback_query(call):
    bot.send_message(call.message.chat.id, 'Ищу собеседника...🔎')
    user_step[call.message.chat.id] = 0
    cid = call.message.chat.id
    u = users_base_search(cid, *user_filter[call.message.chat.id])
    if u == None:
        bot.send_message(call.message.chat.id, 'К сожалению, никого не нашлось...😞')
    else:
        # conn = sqlite3.connect('TB_.sqlite')
        # cur = conn.cursor()
        # cur.execute('SELECT sex, age, town FROM Users WHERE user_bot_id=?', (u,))
        # row = cur.fetchone()
        row = DB.lookup_person_info(u)
        sex_u = row[0]
        age_u = row[1]
        town_u = row[2]
        # cur.execute('SELECT likes, dislikes FROM Users_likes WHERE user_bot_id=?',
        #  (u,))
        # row = cur.fetchone()
        row = DB.lookup_person_likes_info(u)
        try:
            likes_u = row[0]
            dislikes_u = row[1]
        except TypeError:
            likes_u = 0
            dislikes_u = 0
        # cur.execute('SELECT likes, dislikes FROM Users_likes WHERE user_bot_id=?',
        #  (call.message.chat.id,))
        # row = cur.fetchone()
        row = DB.lookup_person_likes_info(call.message.chat.id)
        try:
            likes_ = row[0]
            dislikes_ = row[1]
        except TypeError:
            likes_ = 0
            dislikes_ = 0
        # cur.execute('SELECT latitude, longitude FROM Users_gelo WHERE user_bot_id=?',
        #  (u,))
        # row = cur.fetchone()
        row = DB.lookup_person_gelo_info(u)
        try:
            latitude_u = row[0]
            longitude_u = row[1]
        except TypeError:
            latitude_u = None
            longitude_u = None
        # cur.execute('SELECT latitude, longitude FROM Users_gelo WHERE user_bot_id=?',
        #  (call.message.chat.id,))
        # row = cur.fetchone()
        row = DB.lookup_person_gelo_info(u)
        try:
            latitude_ = row[0]
            longitude_ = row[1]
        except TypeError:
            latitude_ = None
            longitude_ = None
        user_step[call.message.chat.id] = 10
        user_step[u] = 10
        user_pairs[call.message.chat.id] = u
        users_likes[call.message.chat.id] = [0, 0]
        users_likes[u] = [0, 0]
        if latitude_ and longitude_ is not None and \
                latitude_u and longitude_u is not None:
            dstnce = round(distance.distance((latitude_, longitude_),
                                             (latitude_u, longitude_u)).meters)
        else:
            dstnce = '----'
        text = f'Нашел кое-кого для тебя!🔥\n\nИнформация о собеседнике:\n\n' + \
               f'👫Пол: {sex_u}\n🗓️Возраст: {age_u}\n' + \
               f'🏙️Город: {town_u}\n\n⛳️Расстояние: {dstnce} метров\n\n' + \
               f'☝️Оценка: {likes_u}👍️{dislikes_u}👎️' + \
               f'\n\n\n/stop - остановить диалог.\nКнопка "Начать поиск 🔎" - ' + \
               f'найти другого собеседника.'
        bot.send_message(call.message.chat.id, text)


@bot.callback_query_handler(func=lambda call: user_step_(call.message.chat.id) == 10)
def callback_query(call):
    k_ = 0
    v_ = 0
    # conn = sqlite3.connect('TB_.sqlite')
    # cur = conn.cursor()
    if call.data == 'cb_like':
        # bot.answer_callback_query(call.id, "👍️")
        # for k,v in user_pairs.items():
        #     if call.message.chat.id == k:
        #         users_likes[v][0] += 1
        #         bot.edit_message_reply_markup(chat_id=call.message.chat.id,
        #                          message_id=call.message.message_id, reply_markup=None)
        #         k_ = k
        #         v_ = v
        #         break
        #     elif call.message.chat.id == v:
        #         users_likes[k][0] += 1
        #         bot.edit_message_reply_markup(chat_id=call.message.chat.id,
        #                          message_id=call.message.message_id, reply_markup=None)
        #         k_ = k
        #         v_ = v
        #         break
        k_, v_ = rating_with_like_dislike(call.id, "👍️", call.message.chat.id, 0,
                                          call.message.message_id)
    if call.data == 'cb_dislike':
        # bot.answer_callback_query(call.id, "👎️")
        # for k,v in user_pairs.items():
        #     if call.message.chat.id == k:
        #         users_likes[v][1] += 1
        #         bot.edit_message_reply_markup(chat_id=call.message.chat.id,
        #                          message_id=call.message.message_id, reply_markup=None)
        #         k_ = k
        #         v_ = v
        #         break
        #     elif call.message.chat.id == v:
        #         users_likes[k][1] += 1
        #         bot.edit_message_reply_markup(chat_id=call.message.chat.id,
        #                          message_id=call.message.message_id, reply_markup=None)
        #         k_ = k
        #         v_ = v
        #         break
        k_, v_ = rating_with_like_dislike(call.id, "👎️", call.message.chat.id, 1,
                                          call.message.message_id)
    # cur.execute('SELECT user_bot_id FROM Users_likes')
    # rows = cur.fetchall()
    rows = DB.check_all_likes_users_ids()
    # flag = 0
    # for row in rows:
    #     if row[0] == k_:
    #         flag = 1
    #         break
    if flag_in_not_in(rows, k_) == 0 and k_ != 0:
        # cur.execute('INSERT OR IGNORE INTO Users_likes (user_bot_id, likes, dislikes)  VALUES (?, ?, ?)',
        #                                            (k_, users_likes[k_][0], users_likes[k_][1]) )
        DB.user_likes_insert(k_, users_likes[k_][0], users_likes[k_][1])
    elif flag_in_not_in(rows, k_) == 1 and k_ != 0:
        # cur.execute('SELECT likes, dislikes FROM Users_likes WHERE user_bot_id=?', (k_,))
        # row = cur.fetchone()
        row = DB.lookup_person_likes_info(k_)
        likes_cur = row[0] + users_likes[k_][0]
        dislikes_cur = row[1] + users_likes[k_][1]
        # cur.execute('UPDATE Users_likes SET likes=?, dislikes=? WHERE user_bot_id=?',
        #                                                     (likes_cur, dislikes_cur, k_) )
        DB.user_likes_update(likes_cur, dislikes_cur, k_)
    # cur.execute('SELECT user_bot_id FROM Users_likes')
    # rows = cur.fetchall()
    rows = DB.check_all_likes_users_ids()
    # flag = 0
    # for row in rows:
    #     if row[0] == v_:
    #         flag = 1
    #         break
    if flag_in_not_in(rows, v_) == 0 and v_ != 0:
        # cur.execute('INSERT OR IGNORE INTO Users_likes (user_bot_id, likes, dislikes)  VALUES (?, ?, ?)',
        #                                                (v_, users_likes[v_][0], users_likes[v_][1]) )
        DB.user_likes_insert(v_, users_likes[v_][0], users_likes[v_][1])
    elif flag_in_not_in(rows, v_) == 1 and v_ != 0:
        # cur.execute('SELECT likes, dislikes FROM Users_likes WHERE user_bot_id=?', (v_,))
        # row = cur.fetchone()
        row = DB.lookup_person_likes_info(v_)
        likes_cur = row[0] + users_likes[v_][0]
        dislikes_cur = row[1] + users_likes[v_][1]
        #     cur.execute('UPDATE Users_likes SET likes=?, dislikes=? WHERE user_bot_id=?',
        #                                                     (likes_cur, dislikes_cur, v_) )
        # conn.commit()
        DB.user_likes_update(likes_cur, dislikes_cur, v_)
    users_likes[k_] = [0, 0]
    users_likes[v_] = [0, 0]


bot.infinity_polling()
