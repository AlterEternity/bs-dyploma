import telebot

from bot import botconfig

# TODO: store state in DB
DEFAULT_STATE = botconfig.State.S_START
CURRENT_STATE = DEFAULT_STATE
LANGUAGE = 'eng'
CHAT_ID = None
EVENT_INFO = dict()

bot = telebot.TeleBot(botconfig.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def display_start(message):
    """
    Displays starting message for user. Getting event name in dictionary
    :param message:
    """
    global CURRENT_STATE, CHAT_ID
    inline = telebot.types.InlineKeyboardMarkup()
    rus = telebot.types.InlineKeyboardButton(text="Русский", callback_data='rus')
    eng = telebot.types.InlineKeyboardButton(text="English", callback_data='eng')
    ukr = telebot.types.InlineKeyboardButton(text="Українська", callback_data='ukr')
    inline.add(rus, eng, ukr)
    bot.send_message(message.chat.id, "Hello world!", reply_markup=inline)
    CURRENT_STATE = botconfig.State.S_ENTER_LANG
    CHAT_ID = message.chat.id


@bot.callback_query_handler(func=lambda call: True)
def set_language(call):
    global LANGUAGE
    if call.message:
        LANGUAGE = call.data


# For English language
def dialogue():
    global LANGUAGE, CURRENT_STATE, CHAT_ID
    if LANGUAGE == 'eng':
        print(LANGUAGE == 'eng')
        print(CURRENT_STATE == botconfig.State.S_ENTER_LANG)
        print("checking lang")
        print(CHAT_ID)

        @bot.message_handler(commands=['restart'])
        def display_restart(message):
            """
            Returning to start state
            :param message:
            """
            global EVENT_INFO, CURRENT_STATE
            bot.send_message(message.chat.id, "Okay...")
            EVENT_INFO = dict()
            CURRENT_STATE = DEFAULT_STATE

        @bot.message_handler(func=lambda CURRENT_STATE: True)
        def get_event_name(message):
            """
            Getting event name to add it to dictionary
            :param message:
            """
            print("I'm in")
            bot.send_message(CHAT_ID, "Please enter the name of event you want to go...")
            EVENT_INFO.update({'name': message.text})

        @bot.message_handler(func=lambda x:CURRENT_STATE == botconfig.State.S_ENTER_EVENT_NAME)
        def get_event_date(message):
            """
            Getting event date to add it to dictionary
            :param message:
            """
            pass


def check_value(a, b) -> bool:
    if a == b:
        return True
    else:
        return False

