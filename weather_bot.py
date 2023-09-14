import telebot
from telebot import types
from datetime import datetime
import queue
import weather_parser
from common_types import Config, User

def bot_thread(bot, config : Config, users : dict):
    @bot.message_handler(commands=['sub'])
    def sub_handler(message):
        if (message.from_user.id not in users):
            city = message.text.replace('/sub ', '')
            users[message.from_user.id] = User(message.from_user.id, city)
            
        l = weather_parser.parse_for_user(message.from_user.id)

        characters_to_replace = [".", "-", "!", "*", "'", "(", ")", ";", ":", "@", "&", "=", "+", "$", ",", "/", "?", "%", "#", "[", "]", '|']

        for ll in l:
            m = ll.message
            for c in characters_to_replace:
                m = m.replace(c, f'\{c}')
            bot.send_message(message.from_user.id, m, parse_mode='MarkdownV2', disable_web_page_preview=True)
            
    @bot.message_handler(commands=['unsub'])
    def unsub_handler(message):
        if (message.from_user.id in users):
            users.pop(message.from_user.id)
    while True:
        try:
            bot.polling(none_stop = True, interval = 0)
        except Exception:
            pass

def notifier_thread(bot, users : dict, reports_queue : queue.Queue):
    while(True):
        new_reports = []

        while not reports_queue.empty():
            new_reports.append(reports_queue.get())

        if len(new_reports) == 0:
            continue

        if len(users) == 0:
            continue

        characters_to_replace = [".", "-", "!", "*", "'", "(", ")", ";", ":", "@", "&", "=", "+", "$", ",", "/", "?", "%", "#", "[", "]", '|']

        for temp_report in new_reports:
            for user in users.values():
                if temp_report.city == user.city:
                    m = temp_report.message
                    for c in characters_to_replace:
                        m = m.replace(c, f'\{c}')
                    bot.send_message(user.id, m, parse_mode='MarkdownV2', disable_web_page_preview=True)