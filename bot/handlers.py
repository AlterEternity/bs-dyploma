import telebot

import botconfig

# TODO: store state in DB
default_state = botconfig.State.S_START
bot = telebot.TeleBot(botconfig.token)


@bot.message_handler(commands=['start', 'help'])
def display_start(message) -> int:
    bot.send_message(message.chat.id, "Hello World!")
    current_state = botconfig.State.S_ENTER_EVENT_NAME
    return current_state

