import telebot
from openpyxl import load_workbook
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)
leagues = ['GreatLeague', 'UltraLeague', 'MasterLeague']


def fill_names_list():
    workbook = load_workbook(filename='pokemon_leagues.xlsx', read_only=True)
    names_sheet = workbook['pokemon_names']
    pokemon_names = []
    for row in names_sheet.rows:
        for cell in row:
            if cell.value is not None:
                cell_val = '' + cell.value
                pokemon_names.append(cell_val.lower())
    return pokemon_names


@bot.message_handler(commands=['top20'])
def send_top20(message):
    bot.send_message(message.chat.id, "Select the league", reply_markup=gen_leagues())


def gen_leagues():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for i in range(0, 3):
        markup.add(InlineKeyboardButton(leagues[i], callback_data=leagues[i]))
    return markup


@bot.callback_query_handler(func=lambda query: query.data in leagues)
def callback_query(call):
    workbook = load_workbook(filename='pokemon_leagues.xlsx', read_only=True)
    if call.data == 'GreatLeague':
        league_sheet = workbook['great_league']
        top20_str = 'TOP 20 GreatLeague:\n'
    elif call.data == 'UltraLeague':
        league_sheet = workbook['ultra_league']
        top20_str = 'TOP 20 UltraLeague:\n'
    else:
        league_sheet = workbook['master_league']
        top20_str = 'TOP 20 MasterLeague:\n'
    i = 0
    for row in league_sheet.rows:
        if i < 20:
            for cell in row:
                if cell.value is not None and cell.value != 'Pokemon' and cell.value != 'Score':
                    if cell.column_letter == 'A':
                        i += 1
                        top20_str = top20_str + str(i) + '- ' + cell.value
                    if cell.column_letter == 'B':
                        top20_str = top20_str + ' ' + str(cell.value) + '\n'
        else:
            bot.send_message(call.from_user.id, top20_str)
            break


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am the PvpRanking Bot.
You can start with commands /top20\
""")


@bot.message_handler(func=lambda message: message.text in fill_names_list())
def pokemon_info(message):
    pokemon_names = fill_names_list()
    message.text = message.text.lower()
    for name in pokemon_names:
        if message.text == name.lower():
            get_pokemon_info()
            print(name.lower())


def get_pokemon_info():
    print('ciao')


@bot.message_handler(func=lambda message: message.text not in fill_names_list())
def echo_message(message):
    print(fill_names_list())
    bot.reply_to(message, 'I don\'t know what to do, try with /help or /top20.')


bot.infinity_polling()
