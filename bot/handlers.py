import telebot

from bot import botconfig

# TODO: store state in DB
DEFAULT_STATE = botconfig.State.S_START
CURRENT_STATE = DEFAULT_STATE
LANGUAGE = 'eng'
EVENT_INFO = dict()

bot = telebot.TeleBot(botconfig.token)


# For English language
@bot.message_handler(commands=['start', 'help'])
def display_start(message):
    """
    Displays starting message for user. Getting event name in dictionary
    :param message:
    """
    bot.send_message(message.chat.id, "Hello world!")
    EVENT_INFO = {'name': message.text}
    CURRENT_STATE = botconfig.State.S_ENTER_EVENT_NAME


@bot.message_handler(commands=['restart'])
def display_start(message):
    """
    Returning to start state
    :param message:
    """
    bot.send_message(message.chat.id, "Okay...")
    EVENT_INFO = dict()
    CURRENT_STATE = DEFAULT_STATE


@bot.message_handler(func=lambda x: CURRENT_STATE == botconfig.State.S_ENTER_EVENT_NAME)
def get_event_date(message):
    """
    Getting event date to add it to dictionary
    :param message:
    """
    pass








