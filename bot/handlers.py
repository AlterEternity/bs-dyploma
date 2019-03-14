import telebot

import botconfig

bot = telebot.TeleBot(botconfig.token)


@bot.message_handler(commands=['start', 'help'])
def display_start(message):
    bot.send_message(message.chat.id, "Hello World!")
