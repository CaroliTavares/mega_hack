# Instalar biblioteca abaixo:
# pip install pyTelegramBotAPI

import telebot
import datetime


# Função para definir resposta.
# Será usada para identificar o conteúdo da mensagem do usuário, e tomar a
# direção certa para gerar a resposta.
# Neste caso, verifica se a mensagem é uma pergunta.

def is_question(message):         # A entrada é um objeto message, retornado pela própria API do Telegram.
    return '?' in message.text    # Esse objeto message contém o atributo text, que é o texto da mensagem.

# Token do bot que vai manter a conversa.
# Este token leva ao bot Alice, em telegram.me/alice_zbot
# Para criar seu próprio bot, converse com @BotFather no telegram (fonte: https://core.telegram.org/bots)

tkn = '1252935213:AAG0QlCDGVaWxXWHe6TJxKqutqd5NhoXqg8'

# Criando o objeto bot com o token definido
bot = telebot.TeleBot(tkn, threaded=False)

# Criando caminhos de mensagems

# Aqui definimos a resposta para as mensagem que receberemos.
# A API vai nos mostrar a mensagem, e nós precisamos decidir, através dela, o que retornar ao usuário.
# Essa decisão pode acontecer através de uma função de reconhecimento (como  a is_question definida acima)
# ou através de um commando, em que o usuário envia /algum_comando, e a api identifica automaticamente.
# Primeiramente, definiremos o comando /start, dando uma mensagem inicial para o usuário.
# No decorator (@bot.message_handler) passamos a forma de reconhecimento que usaremos. Nesse caso, commands = ['start']
# Em seguida, criamos uma função para ser executada através desse comando, cuja entrada é um message, e
# o objetivo é enviar uma mensagem ao usuário.

@bot.message_handler(commands = ['start'])
def start_talking(message):
    msg = 'Olá'
    
    bot.send_message(message.chat.id, msg)    # send_message usa obrigatoriamente as entradas de ID do chat e mensagem a ser enviada.
  
# Definiremos então um caminho para caso a mensagem do usuário seja uma pergunta.
# Para isso, passamos a função is_question como parâmetro func no decorator.

@bot.message_handler(func = is_question)
def answer_questions(message):
    print(message.text)
    print(message.chat.id)
    print(message.chat.first_name)
    timestamp = datetime.datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S')
    date=str(timestamp)
    

    msg = 'Hm... não sei responder essa pergunta.'
    bot.send_message(message.chat.id, msg)
    
# Por fim, definiremos uma escapatória, que será realizada caso nenhum dos caminhos acima sejam tomados.
# Para isso, basta passarmos uma função sempre verdadeira.
# Para tomar o caminho de uma mensagem, a API acompanha a ordem de definição das funções. Nesse caso,
# será analisado start_talking -> answer_questions -> no_question. Caso uma seja verdadeira, as seguintes
# não são analisadas.

@bot.message_handler(func=lambda message: True)
def no_question(message):
    msg = 'Digite seu nome email e cidade na mesma linha'
    bot.send_message(message.chat.id, msg)
    
# Iniciando o bot.
# Ao executar esse script, sua máquina funcionará como servidor para o bot, e ele só estará
# habilitado a responder enquanto o código estiver sendo executado. 

bot.infinity_polling(True)