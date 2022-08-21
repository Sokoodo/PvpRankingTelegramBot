import telebot
from openpyxl import load_workbook

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['top20_greatleague', 'top20_ultraleague', 'top20_masterleague'])
def send_top20(message):
    workbook = load_workbook(filename='pokemon_leagues.xlsx', read_only=True)
    if message.text == '/top20_greatleague':
        league_sheet = workbook['great_league']
    elif message.text == '/top20_ultraleague':
        league_sheet = workbook['ultra_league']
    else:
        league_sheet = workbook['master_league']
    top20_str = ''
    i = 0
    for row in league_sheet.rows:
        if i < 20:
            for cell in row:
                if cell.value is not None and cell.value != 'Pokemon':
                    if cell.column_letter == 'A':
                        i += 1
                        top20_str = top20_str + str(i) + ' ' + cell.value + '\n'
        else:
            bot.reply_to(message, top20_str)
            break


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am the PvpRanking Bot.
You can start with commands /top20_greatleague, /top20_ultraleague or /top20_masterleague\
""")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    message.text = message.text.lower()
    if message.text == 'hello':
        bot.reply_to(message, 'Hello, how are you?')
    else:
        bot.reply_to(message, 'I don\'t know what to do, try with /help or /add.')


bot.infinity_polling()
