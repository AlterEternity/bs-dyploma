import telebot
import mongoengine

from bot import botconfig
from bot import parsing
from .db_model.user import User

# TODO: Configure logger for info and critical events

# TODO: store state in DB
DEFAULT_STATE = botconfig.State.S_START
CURRENT_STATE = DEFAULT_STATE  # TODO: Delete when will be redesigned to use db
LANGUAGE = None  # TODO: Delete when will be redesigned to use db
CHAT_ID = None  # TODO: Delete when will be redesigned to use db
EVENT_INFO = dict()
EVENT_INFO_SITE = []

mongoengine.connect(botconfig.PROJECT_NAME)
bot = telebot.TeleBot(botconfig.TOKEN)


@bot.message_handler(commands=['start'])
def display_start(message):
    """
    Displays starting message for user. Getting event name in dictionary
    :param message:
    """
    global CURRENT_STATE, CHAT_ID, user  # TODO: Delete when will be redesigned to use db
    try:
        user = User.objects(user_id=message.chat.id).first()
        if user is None:
            user = User()
            user.user_id = message.chat.id
            user.username = str(message.from_user.username)
            user.state = botconfig.State.S_START
            user.first_name = message.from_user.first_name
            user.last_name = message.from_user.last_name
            user.save()

        inline = telebot.types.InlineKeyboardMarkup()
        rus = telebot.types.InlineKeyboardButton(text="Русский", callback_data='rus')
        eng = telebot.types.InlineKeyboardButton(text="English", callback_data='eng')
        ukr = telebot.types.InlineKeyboardButton(text="Українська", callback_data='ukr')
        inline.add(rus, eng, ukr)
        bot.send_message(message.chat.id, "Hello! \nI'm Ticket Bot. I was created to help you in ordering tickets!"
                                          "\nPlease choose your language by clicking the button below."
                                          "\nNOTE! I'm currently in development, so the only language supported is "
                                          "English", reply_markup=inline)
        CHAT_ID = message.chat.id  # TODO: Delete when will be redesigned to use db
    except Exception as e:
        None


@bot.message_handler(commands=['restart'])
def display_restart(message):
    """
    Returning to start state
    :param message:
    """
    global EVENT_INFO  # TODO: Delete when will be redesigned to use db
    try:
        user = User.objects(user_id=message.chat.id).first()
        bot.send_message(message.chat.id, "Okay...")
        user.state = botconfig.State.S_START
        EVENT_INFO = dict()
    except Exception as e:
        None


@bot.message_handler(func=lambda x: CURRENT_STATE == botconfig.State.S_ENTER_LANG)
def get_event_name(message):
    """
    Getting event name to add it to dictionary
    :param message:
    """
    global CURRENT_STATE, EVENT_INFO, FOR_PARSE  # TODO: Delete when will be redesigned to use db
    EVENT_INFO.update({'name': message.text})
    bot.send_message(CHAT_ID, "Okay, saving it")
    bot.send_message(CHAT_ID, "Which date you want to attend?")
    print(EVENT_INFO)  # TODO: Delete when will be working stable
    CURRENT_STATE = botconfig.State.S_ENTER_EVENT_NAME  # TODO: Delete when will be redesigned to use db
    # getting text of response
    FOR_PARSE = parsing.http_get(EVENT_INFO['name'])
    print(FOR_PARSE)  # TODO: Delete when will be working stable


@bot.message_handler(func=lambda x: CURRENT_STATE == botconfig.State.S_ENTER_EVENT_NAME)
def get_event_date(message):
    """
    Getting event date to add it to dictionary
    :param message:
    """
    global CURRENT_STATE, EVENT_INFO  # TODO: Delete when will be redesigned to use db
    EVENT_INFO.update({'date': message.text})
    inline = telebot.types.InlineKeyboardMarkup()
    yes = telebot.types.InlineKeyboardButton(text="Yes", callback_data='yes')
    no = telebot.types.InlineKeyboardButton(text="No", callback_data='no')
    inline.add(yes, no)
    bot.send_message(CHAT_ID, "Great, let's check what you've got:")
    bot.send_message(CHAT_ID, "Event name: " + EVENT_INFO.get('name') + "\n" + "Event date: " +
                     EVENT_INFO.get('date') + "\nIs that correct?", reply_markup=inline)
    CURRENT_STATE = botconfig.State.S_ENTER_DATE  # TODO: Delete when will be redesigned to use db


@bot.callback_query_handler(func=lambda x: CURRENT_STATE == botconfig.State.S_START)
def set_language(call):
    global LANGUAGE, CURRENT_STATE, CHAT_ID  # TODO: Delete when will be redesigned to use db
    if call.message:
        try:
            user.user_lang = call.data
            bot.send_message(CHAT_ID, "Please enter the name of event you want to go...")
            user.state = botconfig.State.S_ENTER_LANG
        except Exception as e:
            None


@bot.callback_query_handler(func=lambda x: CURRENT_STATE == botconfig.State.S_ENTER_DATE)
def show_event_list(call):
    global EVENT_INFO_SITE, CURRENT_STATE  # TODO: Delete when will be redesigned to use db
    if call.data == 'yes':
        EVENT_INFO_SITE = parsing.parse_html(text=FOR_PARSE)
        msg_text = "Look what I've found: \n"
        for row in EVENT_INFO_SITE:
            event = "EVENT: " + row['name'] + "\nWHEN:" + row['date'] + "\nWHERE: " + row['location'] + \
                    "\nPRICE: " + row['price'] + "\nBUY TICKETS: " + row['link'] + "\n----------------------\n"
            msg_text += event
    else:
        msg_text = 'Sorry, It can be unexpected error.\n\nPlease use /restart command to start again.'
    bot.send_message(CHAT_ID, msg_text)
    CURRENT_STATE = botconfig.State.S_CHOOSE_EVENT  # TODO: Delete when will be redesigned to use db










