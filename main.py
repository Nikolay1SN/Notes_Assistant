import random
from telebot import TeleBot
import telebot
import random
from telebot .handler_backends import BaseMiddleware
from telebot .handler_backends import CancelUpdate


bot = TeleBot('5300816780:AAGrv99lILw9Q_0hlj4erGzkvHB0OLYIcJk',
              use_class_middlewares=True)
tasks = {}
random_tasks = ['позвонить бабушке', 'позвонить маме', 'посмотреть фильм']


class SimpleMiddleware(BaseMiddleware):
    def __init__(self, limit) -> None:
        self.last_time = {}
        self.limit = limit
        self.update_types = ['message']

    def pre_process(self, message, data):
        if not message.from_user.id in self.last_time:

            self.last_time[message.from_user.id] = message.date
            return
        if message.date - self.last_time[message.from_user.id] < self.limit:
            # User is flooding
            bot.send_message(message.chat.id, 'You are making request too often')
            return CancelUpdate()
        self.last_time[message.from_user.id] = message.date

    def post_process(self, message, data, exception):
        pass


bot.setup_middleware(SimpleMiddleware(2))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет я придумаю что тебе делать сегодня или запишу твои планы!')


def add(date, task):
    if date in tasks:
        # Дата есть в словаре
        # Добавляем в список задачу
        tasks[date].append(task)
    else:
        # Даты нет в словаре
        # Создаем записить с ключом date
        tasks[date] = []
        tasks[date].append(task)


HELP = """
/help - вывести список доступных команд.
/add - добавить задачу в список.
/show - напечатать все добавления задачи.
/random - добавлять случайную задачу на дату Сегодня
"""


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['add'])
def add_todo(message):
    command = message.text.split(maxsplit=2)
    add(command[1].lower(), command[2])
    bot.send_message(message.chat.id, 'Задача: ' + command[2] + '\n' + 'Добавлена на дату: ' + command[1].lower())


@bot.message_handler(commands=['random'])
def random_add(message):
    date = 'сегодня'
    task = random.choice(random_tasks)
    add(date, task)
    text = 'Задача: ' + task + '\n' + 'Добавлена на дату: ' + date
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['show', 'print'])
def show(message):
    command = message.text.split(maxsplit=1)
    date = command[1].lower()
    text = ''
    if date in tasks:
        text = date.upper() + '\n'
        for task in tasks[date]:
            text = text + '[]' + task + '\n'
    else:
        text = 'Задач на эту дату нет'
    bot.send_message(message.chat.id, text)


bot.infinity_polling()

