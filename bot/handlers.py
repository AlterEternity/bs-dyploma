import telebot


from bot import botconfig
from bot import parsing


# TODO: store state in DB
DEFAULT_STATE = botconfig.State.S_START
CURRENT_STATE = DEFAULT_STATE
LANGUAGE = None
CHAT_ID = None
EVENT_INFO = dict()
TO_PARSE = None
EVENT_INFO_SITE = []
FOR_PARSE = None


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
    bot.send_message(message.chat.id, "Hello! \nI'm Ticket Bot. I was created to help you in ordering tickets!"
                                      "\nPlease choose your language by clicking the button below."
                                      "\nNOTE! I'm currently in development, so the only language supported is English"
                                      , reply_markup=inline)
    CHAT_ID = message.chat.id


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


@bot.message_handler(func=lambda x: CURRENT_STATE == botconfig.State.S_ENTER_LANG)
def get_event_name(message):
    """
    Getting event name to add it to dictionary
    :param message:
    """
    global CURRENT_STATE, EVENT_INFO, FOR_PARSE
    EVENT_INFO.update({'name': message.text})
    bot.send_message(CHAT_ID, "Okay, saving it")
    bot.send_message(CHAT_ID, "Which date you want to attend?")
    print(EVENT_INFO)
    CURRENT_STATE = botconfig.State.S_ENTER_EVENT_NAME
    # getting text of response
    FOR_PARSE = parsing.http_get(EVENT_INFO['name'])
    print(FOR_PARSE)


@bot.message_handler(func=lambda x: CURRENT_STATE == botconfig.State.S_ENTER_EVENT_NAME)
def get_event_date(message):
    """
    Getting event date to add it to dictionary
    :param message:
    """
    global CURRENT_STATE, EVENT_INFO
    EVENT_INFO.update({'date': message.text})
    inline = telebot.types.InlineKeyboardMarkup()
    yes = telebot.types.InlineKeyboardButton(text="Yes", callback_data='yes')
    no = telebot.types.InlineKeyboardButton(text="No", callback_data='no')
    inline.add(yes, no)
    bot.send_message(CHAT_ID, "Great, let's check what you've got:")
    bot.send_message(CHAT_ID, "Event name: " + EVENT_INFO.get('name') + "\n" + "Event date: " +
                     EVENT_INFO.get('date') + "\nIs that correct?", reply_markup=inline)
    CURRENT_STATE = botconfig.State.S_ENTER_DATE


@bot.callback_query_handler(func=lambda x: CURRENT_STATE == botconfig.State.S_START)
def set_language(call):
    global LANGUAGE, CURRENT_STATE, CHAT_ID
    if call.message:
        LANGUAGE = call.data
        bot.send_message(CHAT_ID, "Please enter the name of event you want to go...")
        CURRENT_STATE = botconfig.State.S_ENTER_LANG


@bot.callback_query_handler(func=lambda x: CURRENT_STATE == botconfig.State.S_ENTER_DATE)
def show_event_list(call):
    global EVENT_INFO_SITE, CURRENT_STATE
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
    CURRENT_STATE = botconfig.State.S_CHOOSE_EVENT










