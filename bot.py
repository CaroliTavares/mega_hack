import json
import requests
import telebot
import datetime
from telebot import types
import time
import requests
import json

tkn = '1204137702:AAGe3J321YzM21bKj5nLphLF8aDNYmSaOBY'
BASE_URL = 'https://megawomen.herokuapp.com/'

# Criando o objeto bot com o token definido
bot = telebot.TeleBot(tkn, threaded=False)


# A entrada é um objeto message, retornado pela própria API do Telegram.
def is_question(message):
    return '?' in message.text


def is_ajudar(message):
    return 'Web' or 'Data_Science' or 'Iot' or 'Outras' in message.text


def reset_a(lista):
    del lista[:]


pergunta = []

tech = []

user_dict = {}


class User:
    def __init__(self, name):
        self.func = None
        self.name = None
        self.email = None

    def __str__(self):
        return str({
            "func": self.func,
            "name": self.name,
            "email": self.email,
        })

    def json(self):
        return {
            "func": self.func,
            "name": self.name,
            "email": self.email,
        }


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    reset_a(pergunta)
    reset_a(tech)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add(types.KeyboardButton("Mulher com dúvidas na área tech"))
    markup.add(types.KeyboardButton("Mentor"))
    #markup.add('Mentor', 'Menina')
    msg = bot.reply_to(
        message, 'Olá, sou Dora e vou te auxiliar nessa jornada. Você é?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        func = message.text
        user = User(func)
        user_dict[str(chat_id)] = user
        user.func = func
        msg = bot.reply_to(message, 'Qual o seu nome?')
        bot.register_next_step_handler(msg, process_name)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_name(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = user_dict[str(chat_id)]
        user.name = name
        msg = bot.reply_to(message, 'Qual o seu email?')
        bot.register_next_step_handler(msg, process_email)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_email(message):
    try:
        chat_id = message.chat.id
        email = message.text
        user = user_dict[str(chat_id)]
        user.email = email
        if user.func == "Mulher com dúvidas na área tech":

            msg = bot.reply_to(message, 'Você se juntou à um grupo de mulheres empoderadas da área tech. Seja bem vinda ' + user.name + "!"
                               "\n Qual dúvida você tem sobre tecnologias?")
            bot.register_next_step_handler(msg, start_talking)

            response = requests.post(
                BASE_URL + '/pergunta',
                json={'name': user.name, 'email': user.email, 'id_tele': str(message.chat.id)})

            task = response.json()
            print(task)

        if user.func == "Mentor":
            msg = bot.reply_to(message, 'Muito prazer ' + user.name +
                               ". Poderia auxiliar no direcionamento de mulheres na área tech?")
            bot.register_next_step_handler(msg, start_talking)

    except:
        "OK"


def start_talking(message):
    chat_id = message.chat.id
    pergunta.append(message.text)
    user = user_dict[str(chat_id)]
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton(
            'Web', callback_data='Web'
        ),
        telebot.types.InlineKeyboardButton(
            'Data_Science', callback_data='Data_Science'
        ),

    )
    keyboard.row(
        telebot.types.InlineKeyboardButton(
            'Iot', callback_data='Iot'
        ),
        telebot.types.InlineKeyboardButton(
            'Outras', callback_data='Outras'
        ),
    )
    if user.func == "Mulher com dúvidas na área tech":
        msg = 'Ok. Encontrarei um mentor experiente pra te auxiliar com essa dúvida. ' + \
            "\nEscolha uma área de interesse."
        bot.send_message(message.chat.id, msg, reply_markup=keyboard)
    if user.func == "Mentor":
        msg = 'Qual área gostaria de auxiliar?'
        bot.send_message(message.chat.id, msg, reply_markup=keyboard)


def pesquisar(query):
    ops = ['Web', 'Data_Science', 'Iot', 'Outras']
    return any(x in ops for x in query.data.split())


@bot.callback_query_handler(func=pesquisar)
def search(query):

    chat_id = query.message.chat.id
    print(str(chat_id))
    user = user_dict[str(chat_id)]

    if user.func == "Mulher com dúvidas na área tech":
        print(query.data)
        response = requests.post(
            BASE_URL + '/pergunta',
            json={'pergunta': pergunta[-1], 'tech': query.data, 'id_girl': query.message.chat.id})

        msg = f'Busque sua resposta em: /consultar e para mais perguntas: /pergunta'
        bot.send_message(query.message.chat.id, msg)

    if user.func == "Mentor":
        print(query.data)
        response = requests.post(
            BASE_URL + '/mentor',
            json={'name': user.name, 'email': user.email, 'id_tele': query.message.chat.id, 'tech': query.data})

        msg = f'Muito obrigada pelo contato ' + user.name + "!"\
            '\n Com a sua ajuda iremos mudar o cenário atual do mercado tech. Em breve,  receberá perguntas sobre sua área de conhecimento.'
        bot.send_message(query.message.chat.id, msg)


@bot.message_handler(commands=['pergunta'])
def activate_pergunta_da_garota(message):
    chat_id = message.chat.id
    bot_reply = bot.reply_to(message, "Por gentiliza faça a sua pergunta")
    bot.register_next_step_handler(bot_reply, recebe_pergunta_da_garota)


def recebe_pergunta_da_garota(message):

    chat_id = message.chat.id
    tech = "Data_Science"
    question = message.text
    print(tech)

    # save question
    response = requests.post(BASE_URL + '/pergunta', json={
        'pergunta': question,
        'id_girl': chat_id,
        'tech': tech
    })

    # search mentors
    response = requests.post(BASE_URL + '/find_mentors', json={
        "tech": tech
    })
    mentors_id_list = response.json()['foundedMentorsIds']

    # send question to mentors
    for mentor_id in mentors_id_list:
        bot.send_message(mentor_id, question)

    # ask girl to wait
    bot.send_message(
        chat_id, "Aguarde a resposta e consulte a resposta em: /consultar")

    #bot.send_message(message.chat.id, "Vá para: /start")


@bot.message_handler(commands=['resposta'])
def teste(message):
    print(message.text)

    response = requests.post(BASE_URL + '/resposta', json={
        "texto": message.text,
        "id_mentor": message.chat.id
    })

    msg = "Obrigada por responder"
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['consultar'])
def consultar(message):
    bot.send_message(
        message.chat.id, "Olá o stackoverflow é um ótimo fórum de pra auxiliar com dúvidas de programação.")


@bot.message_handler(commands=['enviar'])
def activate_pergunta_da_garota(message):
    chat_id = message.chat.id
    msg = "Deseja enviar dados para recrutadores?"
    bot.send_message(chat_id, msg)


bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.polling()
