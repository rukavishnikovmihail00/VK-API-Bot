from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboardButton, VkKeyboardColor, VkKeyboard
import vk_api
import random
from bs4 import BeautifulSoup as BS
import requests
import time
token = 'c3818740c6bf83c97ff76b2988aab95ed06be60326a8db18bc979b908b0c50db76a02283834dff0c4bfc8'

session = vk_api.VkApi(token = token)
vk = session.get_api()
longpoll = VkLongPoll(session)


global Random

def random_id():
    Random = 0
    Random += random.randint(0,10000000)
    return Random

def createKeyboard(response):
    keyboard = VkKeyboard(one_time=False)
    if response == 'начать' or response == 'меню':
        keyboard.add_button('Узнать погоду', color = VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Установить таймер', color = VkKeyboardColor.PRIMARY)

    keyboard = keyboard.get_keyboard()
    return keyboard


def get_weather():
    r = requests.get('https://sinoptik.ua/погода-нижний-новгород')
    html = BS(r.content, 'html.parser')

    for el in html.select('#content'):
        t_min = el.select('.temperature .min')[0].text
        t_max = el.select('.temperature .max')[0].text
        text = el.select('.wDescription .description')[0].text
    session.method('messages.send', {'user_id': event.user_id, 'message': text + '\n' + t_min + '\n' + t_max, 'random_id': random_id()})


def set_timer(response):
    time.sleep(int(response))
    session.method('messages.send',  {'user_id': event.user_id, 'message': 'Таймер закончился', 'random_id': random_id()})


while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.from_user:
            response = event.text.lower()
            if event.from_user:

                if response == 'начать' or response == 'меню':
                    keyboard = createKeyboard(response)
                    session.method('messages.send', {'user_id': event.user_id, 'message': 'Что ты хочешь сделать?', 'random_id': random_id(), 'keyboard': keyboard})
                elif response == 'узнать погоду':
                    get_weather()
                elif response == 'установить таймер':
                    session.method('messages.send', {'user_id': event.user_id, 'message': 'Введите время в секундах: ', 'random_id': random_id()})
                elif response.isdigit():
                    set_timer(response)


