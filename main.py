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

    #КОЛИЧЕСТВО ВВЕДЕННЫХ СИМВОЛОВ В ЗАПРОС
    len =list(text).__len__()

    i=0
    result = []

    #ПЕРЕБИРАЕМ МАССИВ С АВТО
    for auto in autos:
        #МАССИВ -> СТРОКА
        car = auto[0]+' '+auto[1]

        a=car[:len]

        if a.lower()==text.lower():
            result.append(InlineQueryResultArticle(
            id=f'{i}', title=f"{car}",
            description=f"{car}",
            input_message_content=InputTextMessageContent(
            message_text=f"{car}")
            ))

            i+=1
            if i>50:
                return
    await bot.answer_inline_query(query.id, result)




