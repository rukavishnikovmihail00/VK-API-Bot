from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboardButton, VkKeyboardColor, VkKeyboard
import vk_api
import random
from bs4 import BeautifulSoup as BS
import requests
import time
#import bitly_api
token = 'TOKEN' 

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
        keyboard.add_line()
        keyboard.add_button('Новости', color = VkKeyboardColor.POSITIVE)
        
       

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


def get_news():
    #con = bitly_api.Connection(access_token='4d0f710792290bbaac321cc226cf1ca755eb7dfd')
    r = requests.get('https://yandex.ru/')
    main_text = r.text
    soup = BS(main_text)

    temp = soup.find('div', {'id':'news_panel_news'})
    count = 0
    news = []
    for el in temp.findAll('a', {'area-label':''}):
        news.append(el.text)
        news.append(el.get('href'))
        #resp = con.shorten(str(el.get('href')))
        #news.append(resp["url"])
        count += 1
        if (count == 5):
            break

    session.method('messages.send', {'user_id': event.user_id, 'message': str(1) +") " + news[0] + "\n" + news[1] + "\n"
    + str(2) +") " + news[2] + "\n" + news[3] + "\n"
    + str(3) +") " + news[4] + "\n" + news[5] + "\n"
    + str(4) +") " + news[6] + "\n" + news[7] + "\n"
    + str(5) +") " + news[8] + "\n" + news[9] + "\n"
    , 'random_id': random_id()})

def get_korona_report():
    r = requests.get('http://zdrav-nnov.ru/koronavirus/')
    mas = []
    soup = BS(r.text)

    date = soup.find('div', {'class':'statistic-date'})
    mas.append(date.text)

    html = soup.find('div', {'class':'statistic-blocks'})



    for el in html.findAll('div', {'class':'statistic-block border-radius'}):
        mas.append(el.text)
    

    session.method('messages.send', {'user_id': event.user_id, 'message': mas[0] + "\n\n" + mas[1] + "\n\n"
    + mas[2] + "\n\n" + mas[3] + "\n\n"
    + mas[4] + "\n\n" + mas[5] + "\n\n"
    + mas[6] + "\n" 
    , 'random_id': random_id()})

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
                elif response == 'новости':
                    get_news()
                elif response == 'коронавирус':
                    get_korona_report()    
                elif response == 'установить таймер':
                    session.method('messages.send', {'user_id': event.user_id, 'message': 'Введите время в секундах: ', 'random_id': random_id()})
                elif response.isdigit():
                    set_timer(response)

