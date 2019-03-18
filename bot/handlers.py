import telebot

import botconfig

# TODO: store state in DB
DEFAULT_STATE = botconfig.State.S_START
CURRENT_STATE = DEFAULT_STATE
EVENT_INFO = dict()

bot = telebot.TeleBot(botconfig.token)


@bot.message_handler(commands=['start', 'help'])
def display_start(message):
    """
    Displays starting message for user
    :param message:
    """
    bot.send_message(message.chat.id, "Hello World!")
    EVENT_INFO = {}
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




