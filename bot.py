import telebot
import parser
import json

with open('token.json') as token_file:
    config = json.load(token_file)

TOKEN = config['token']
bot = telebot.TeleBot(TOKEN)

url = "https://www.slamdunk.ru/news/nba"

markup = telebot.types.ReplyKeyboardMarkup(True, False)
markup.row('/start', '/news')

@bot.message_handler(commands=['start'])
def info(message):
    bot.send_message(message.chat.id,
                     'Здравствуйте! Данный бот будет отправлять вам новости c сайта ' + url + '! Используйте команду /news для получения новостей!',
                     reply_markup=markup)

@bot.message_handler(commands=['news'])
def getNews(message):
    bot.send_message(message.chat.id, 'Пожалуйста, подождите... Операция выполняется... ⏳')
    waitMessage = True

    news = parser.parsing(url)

    for new in news:
        string = ''
        for i, subnew in enumerate(new):
            string += subnew
            if i == 0:
                string = '*' + string
                string = string + '*'
        if waitMessage:
            bot.delete_message(message.chat.id, message.message_id + 1)
            waitMessage = False

        if len(string) <= 4096:
            bot.send_message(message.chat.id, string, parse_mode='Markdown')
        else:
            while len(string)>0:
                substr = string[:4096]
                bot.send_message(message.chat.id, substr, parse_mode='Markdown')
                string = string[len(substr):]

@bot.message_handler(content_types=['text', 'photo', 'document'])
def errorMessage(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, 'Неверные входные данные! Используйте команду /news для того, чтобы получить последние новости!')

bot.polling()