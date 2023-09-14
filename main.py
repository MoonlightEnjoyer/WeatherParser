import weather_bot
import weather_parser
import threading
import time
import queue
from common_types import Config
import telebot

def get_new_weather_data(config, reports_queue):
    while(True):
        weather_parser.parse(reports_queue)
        time.sleep(60 * 60)

reports_queue = queue.Queue()

users = {}

config = Config()

bot = telebot.TeleBot(config.token)

bot_thread = threading.Thread(target=weather_bot.bot_thread, args=(bot, config, users, ))
notifyer_thread = threading.Thread(target=weather_bot.notifier_thread, args=(bot, users, reports_queue))
parser_thread = threading.Thread(target=get_new_weather_data, args=(config, reports_queue,))

bot_thread.start()
notifyer_thread.start()
parser_thread.start()