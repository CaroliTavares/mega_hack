import telebot
import datetime
from telebot import types


tkn = '1252935213:AAG0QlCDGVaWxXWHe6TJxKqutqd5NhoXqg8'

# Criando o objeto bot com o token definido
bot = telebot.TeleBot(tkn, threaded=False)

user_dict = {}


class User:
    def __init__(self, name):
        self.funcao = funcao
        self.name = name
        self.age = None
        self.sex = None


# Handle '/start' and '/help'

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
    Hi there, I am Example bot.
    What's your name?
    """)
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'How old are you?')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(
                message, 'Age should be a number. How old are you?')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(types.KeyboardButton("1"))
        markup.add(types.KeyboardButton("2"))
        markup.add('Male', 'Female')
        msg = bot.reply_to(message, 'What is your gender', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


@bot.message_handler(commands=['inline'])
def teste_inline(message):
    chat_id = message.chat.id
    text = 'CI Test Message'
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        "Google", url="http://www.google.com"))
    markup.add(types.InlineKeyboardButton("Yahoo", url="http://www.yahoo.com"))
    ret_msg = bot.send_message(
        chat_id, text, disable_notification=True, reply_markup=markup)
    assert ret_msg.message_id


def process_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Male') or (sex == u'Female'):
            user.sex = sex
        else:
            raise Exception()
        bot.send_message(chat_id, 'Nice to meet you ' + user.name +
                         '\n Age:' + str(user.age) + '\n Sex:' + user.sex)
        print(user_dict)
    except Exception as e:
        bot.reply_to(message, 'oooops')


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.polling()
