import telebot

from config.settings import TELEGRAM_BOT_TOKEN
from reminderer.models import Habit

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


def send_reminder(habit: Habit):
    chat_id = habit.owner.tg_chat_id
    text = str(habit)
    bot.send_message(chat_id, text)
