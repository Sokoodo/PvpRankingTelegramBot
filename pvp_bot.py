import telebot

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am the PvpRanking Bot.
You can start with commands /pokemon or /top10greatleague\
""")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    message.text = message.text.lower()
    if message.text == 'hello':
        bot.reply_to(message, 'Hello, how are you?')
    else:
        bot.reply_to(message, 'I don\'t know what to do, try with /help or /add.')


bot.infinity_polling()
