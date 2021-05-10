from loader import bot, dp
from .inline_handlers import SEARCH, autos
from aiogram import types


from DBCommands import DBCommands

db = DBCommands()

all_marka=[]
markas=[]



for auto in autos:
    all_marka.append(auto[0])
for mark in all_marka:
    if mark not in markas:
        markas.append(mark)


@dp.message_handler(commands=['start'], state='*')
async def start(message:types.Message):
    await db.create()
    marka_in=message.text
    chatid = message.from_user.id

    user = (await db.select_user(chatid=(chatid,))).fetchall()[0][0]
    if user==0:
        par = (chatid, marka_in)
        await db.add_user(par=par)
    await message.answer(text=f"Выберите марку автомобиля", parse_mode=types.ParseMode.MARKDOWN_V2)
    await SEARCH.marka_in.set()

#HANDLER ДЛЯ МАРКИ АВТО
@dp.message_handler(state=SEARCH.marka_in)
async def marka_in_message(message:types.Message):
    marka = message.text
    chatid = message.from_user.id

    if marka not in markas:
        await message.answer("Марка указана неверно. Чтобы выбрать марку выберите её и предложенного списка")
        return
    par = (marka, chatid)
    try:
        await db.update_marka(par=par)
    except:
        await message.answer("Произошла ошибка, пожалуйста, выберите марку еще раз.")
        return
    await message.answer("Укажите модель(выберите из списка)")

    await SEARCH.model_in.set()

#HANDLER ДЛЯ МОДЕЛИ АВТО
@dp.message_handler(state=SEARCH.model_in)
async def model_in_message(message: types.Message):
    model_in = message.text
    chatid = message.from_user.id
    marka = (await db.select_marka(chatid=(chatid,))).fetchall()[0][0]
    models = []
    i=0
    for auto in autos:
        if auto[0] == marka:
            models.append(auto[1])

    for model in models:
        car = marka + ' ' + model
        if car ==model_in:
            i+=1
    if i!=0:
        try:
            par =(model_in, chatid)
            await db.update_model(par=par)
        except:
            message.answer("Произошла ошибка, пожалуйста укажите модель заново")
    else:
        await message.answer("Вы неправильно указали модель автомобиля")

