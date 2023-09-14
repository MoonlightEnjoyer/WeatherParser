from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import datetime
import queue
from common_types import Report

def parse_for_user(user_id):
    url = f'https://www.gismeteo.by/weather-minsk-4248/'
    ua = UserAgent()

    headers = {
        'accept': 'application/json, text/plain, */*',
        'user-Agent': ua.google,
    }

    res = requests.get(url, headers=headers)
    res.close()

    req = res.text

    soup = BeautifulSoup(req, 'lxml')

    raw_time = soup.find('div', class_='widget-row widget-row-time')

    time_list = raw_time.find_all('div', class_="row-item")

    raw_icon = soup.find('div', class_='widget-row widget-row-icon')

    icon_list = raw_icon.find_all('div', class_="weather-icon tooltip")

    raw_temperature = soup.find('div', class_='widget-row-chart widget-row-chart-temperature row-with-caption')

    raw_temperature = raw_temperature.find('div', class_='chart')

    temperature_list = raw_temperature.find_all('span', class_="unit unit_temperature_c")

    l = []

    for i in range(len(time_list)):
        print(f"{time_list[i].text[-4:-2]}:{time_list[i].text[-2:]} : {icon_list[i].get('data-text')}, {temperature_list[i].text}")
        l.append(Report(f"{time_list[i].text[-4:-2]}:{time_list[i].text[-2:]} : {icon_list[i].get('data-text')}, {temperature_list[i].text}", "Minsk", user_id))

    return l

def parse(reports_queue):
    url = f'https://www.gismeteo.by/weather-minsk-4248/'
    ua = UserAgent()

    headers = {
        'accept': 'application/json, text/plain, */*',
        'user-Agent': ua.google,
    }

    res = requests.get(url, headers=headers)
    res.close()

    req = res.text

    soup = BeautifulSoup(req, 'lxml')

    raw_time = soup.find('div', class_='widget-row widget-row-time')

    time_list = raw_time.find_all('div', class_="row-item")

    raw_icon = soup.find('div', class_='widget-row widget-row-icon')

    icon_list = raw_icon.find_all('div', class_="weather-icon tooltip")

    raw_temperature = soup.find('div', class_='widget-row-chart widget-row-chart-temperature row-with-caption')

    raw_temperature = raw_temperature.find('div', class_='chart')

    temperature_list = raw_temperature.find_all('span', class_="unit unit_temperature_c")

    for i in range(len(time_list)):
        print(f"{time_list[i].text[-4:-2]}:{time_list[i].text[-2:]} : {icon_list[i].get('data-text')}, {temperature_list[i].text}")
        reports_queue.put(Report(f"{time_list[i].text[-4:-2]}:{time_list[i].text[-2:]} : {icon_list[i].get('data-text')}, {temperature_list[i].text}", "Minsk", "broad"))

