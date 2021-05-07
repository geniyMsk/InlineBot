from loader import bot, dp

from aiogram import types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

#ИНТЕГРАЦИЯ С ГУГЛ ТАБЛИЦАМИ
import httplib2
import apiclient
from apiclient import  discovery
from oauth2client.service_account import ServiceAccountCredentials
CREDENTIALS_FILE = 'XXX.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',                                                                               'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
spreadsheetId ='1ntd6s-GpuAE435w8BL8_orb4AYrdspD1wtULBYtmrAM'
range_name = 'Лист1!B1:C3115'
table = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=range_name).execute()

#МАССИВЫ С МАРКАМИ + МОДЕЛЯМИ АВТО
autos = table['values']

@dp.inline_handler()
async def inline(query: types.InlineQuery):
    #ТЕКСТ ЗАПРОСА
    text = query.query
    #ПОДСКАЗКА
    if text == '':
        result = InlineQueryResultArticle(
            id='1', title='Бот',
            description='Введите марку и модель автомобиля',
            input_message_content=InputTextMessageContent(
            message_text='Бот для определения марки и модели автомобиля')
            )
        await bot.answer_inline_query(query.id, [result])

#СЧЁТЧИК НАЙДЕННЫХ АВТОМОБИЛЕЙ
    id=0
#МАССИВ НАЙДЕННЫХ АВТО
    result = [] 

#ПОИСК ПО НАЧАЛУ(ТО ЕСТЬ НАДО НАЧАТЬ ПИСАТЬ СНАЧАЛА МАРКУ, ПОТОМ МОДЕЛЬ И ПОСЛЕ КАЖДОЙ БУКВЫЙ БУДЕТ ПОДСКАЗКА ВЫХОДИТЬ)
    for auto in autos:
        car = auto[0]+' '+auto[1]
        len = list(text).__len__()
        a = car[:len]
        if a.lower() == text.lower():
            result.append(InlineQueryResultArticle(
                id=f'{id}', title=f"{car}",
                description=f"{car}",
                input_message_content=InputTextMessageContent(
                    message_text=f"{car}")
            ))

            id += 1


# ПОИСК ПО СЛОВУ(В НЕ ЗАВИСИМОСТИ ГДЕ ОНО, МОЖНО ВБИТЬ МОДЕЛЬ, НАРИМЕР)
# НАЧИНАЕТСЯ ПОИСК ПО НЕМУ ЕСЛИ ПЕРВЫЙ ВЫДАЛ БОЛЬШЕ 50, ЛИБО НИЧЕГО НЕ ВЫДАЛ
    if id>50 or id==0:
        id=0
        result=[]
        for auto in autos:
            car = auto[0] + ' ' + auto[1]
            text_words = text.replace('(', ' ').replace(')', ' ').replace('/', ' ').split()
            car_words = car.replace('(', ' ').replace(')', ' ').replace('/', ' ').split()
            for text_word in text_words:
                for car_word in car_words:
                    if car_word.lower() == text_word.lower():
                        result.append(InlineQueryResultArticle(
                            id=f'{id}', title=f"{car}",
                            description=f"{car}",
                            input_message_content=InputTextMessageContent(
                                message_text=f"{car}")
                        ))
                        id += 1




    #СПИСОК АВТОМОБИЛЕЙ
    if id<=50 and id!=0:
        await bot.answer_inline_query(query.id, result)

    #МНОГО АВТОМОБИЛЕЙ(>50)
    elif id>50:
        r = InlineQueryResultArticle(
                id='1', title='Недостаточно данных',
                description='Слишком много результатов',
                input_message_content=InputTextMessageContent(
                    message_text='Бот для определения марки и модели автомобиля')
            )
        await bot.answer_inline_query(query.id, [r])

    #АВТОМОБИЛЬ НЕ НАЙДЕН
    else:
        x = InlineQueryResultArticle(
            id='1', title='Не найдено',
            description='Такого автомобиля нет',
            input_message_content=InputTextMessageContent(
                message_text='Бот для определения марки и модели автомобиля')
        )
        await bot.answer_inline_query(query.id, [x])
