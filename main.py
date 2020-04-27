from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboardButton, VkKeyboardColor, VkKeyboard
import vk_api
import random

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
    keyboard = VkKeyboard(one_time=True)
    if response == 'начать':
        keyboard.add_button('Найти лица на фотографии', color = VkKeyboardColor.POSITIVE)

    keyboard = keyboard.get_keyboard()
    return keyboard

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            response = event.text.lower()
            if event.from_user:
                if response == 'начать':
                    keyboard = createKeyboard(response)
                    session.method('messages.send', {'user_id': event.user_id, 'message': 'Что ты хочешь сделать?', 'random_id': random_id(), 'keyboard': keyboard})
            elif event.from_chat:
                if response == 'Найти лица на фотографии':
                    session.method('messages.send', {'user_id': event.user_id, 'message': 'Сработало', 'random_id': random_id()})