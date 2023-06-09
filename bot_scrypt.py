from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
#importing bot 
from create_bot import bot, dp
#importing all database functions 
from db import sql_start, add_value, add_user, add_order, print_products, get_info, checker, receive_method, add_suggestion, pay_method_db, add_check, get_check, delete_check, get_floor, add_campus, get_campus, add_choices, get_choices, add_order_new
#importing all keyboards
from markups import kb_client, order_markup, main_markup, basket_markup, pick_method_markup, buy_markup, pay_method, cash_markup, menu_markup, basket_main_markup, pay_menu
#importing all admon functions
# from admin import send_order, send_question
#importing qiwip2p for payment
# from pyqiwip2p import QiwiP2P
import random
import re

#some necessary variables
#choices = []
#rent_price = 0
#final_price = 0
offset = 0
limit = 5
showed = limit
message_def = ""
name = ""
remove_check = []
flag = True

# p2p = QiwiP2P(auth_key = "")

#adds some states for user
class Address(StatesGroup):
    address = State()
class Suggestion(StatesGroup):
    suggestion = State()
class Ask(StatesGroup):
    question = State()

#start function
@dp.message_handler(commands = ["start"])
async def begin(message: types.Message):
    #global name
    #defines user
    user_info = await bot.get_chat_member(message.chat.id, message.from_user.id)
    #gets username
    name = user_info["user"]["username"]
    #sets user username to database
    sql_start()
    add_user(name)
    #greeting photo
    await bot.send_photo(message.chat.id, photo=open("App/ui/img/greeting_photo.png", "rb"), reply_markup=kb_client)




#show basket info by command
@dp.message_handler(commands = ["basket"])
async def basket_show(message: types.Message):
    #global choices
    choices = await get_choices(message.from_user.username)
    if (choices[0][1] is not None and choices[0][0] is not None):
        if (choices[0][0] != '' and choices[0][1] != 0):
            choices = choices[0][0].split(',')
            basket_games = "\n\n🍫 ".join(choices)
            await bot.send_message(message.chat.id, "<b>Корзина: </b>\n\n🍫 {games}\n\n<b>Сумма аренды:</b> {rent}\n\n<b>Сумма залога:</b> {deposit_price}\n\n<b>Общая сумма:</b> {final_price} ".format(games=basket_games, rent=rent_price, final_price=final_price, deposit_price=deposit_price),
                            parse_mode="html", reply_markup = basket_markup)
        else:
            await bot.send_message(message.chat.id, "🕸 Корзина пуста")
    #if basket is empty
    else:
        await bot.send_message(message.chat.id, "🕸 Корзина пуста")

#home menu by command
@dp.message_handler(commands = ["home"])
async def basket_show(message: types.Message):
    sql_start()
    choices_temp = await get_choices(message.from_user.username)
    #if basket is not empty
    if choices_temp[0][0] == "":
        await bot.send_message(message.chat.id, "<b>Вы вышли в главное меню</b>", parse_mode="html", reply_markup = main_markup)
    #if basket is empty
    elif choices_temp[0][0] != "":
        await bot.send_message(message.chat.id, "<b>Вы вышли в главное меню</b>", parse_mode="html", reply_markup = basket_main_markup)

#choose game by command
@dp.message_handler(commands = ["choose"])
async def choose_game(message: types.Message):
    global offset, limit, showed, message_def
    offset = 0
    showed = limit
    #checks in db if any games are available and returns number
    sql_start()
    ff = await get_campus(name)
    check = checker(ff[0][0])
    message_def = message
    #checks if any games are available
    if check is not None:
        await bot.send_message(message.chat.id, "🍫 Продукты в наличии:", reply_markup = order_markup)
        #prints all games from db (connector.py function)
        await print_products(message, offset, limit, showed, ff[0][0])
        offset += limit
        showed += limit
    else:
        await bot.send_message(message.chat.id, "🍫 Продуктов в наличии нет")

#reply buttons funcrions
@dp.message_handler(content_types = ['text'])
async def text(message: types.Message):
    global offset, limit, showed, message_def, remove_check
    sql_start()

    #if message text = choose game    if (message.text in ['Корпус 1', 'Корпус 2', 'Корпус 3', 'Кошка']):
    if message.text in ['Корпус 1', 'Корпус 2', 'Корпус 3', 'Кошка']:
        # corpus = re.sub(r'\s+', '_', message.text.strip())
        # defines user
        user_info = await bot.get_chat_member(message.chat.id, message.from_user.id)
        # gets username
        sql_start()
        # defines user
        user_info = await bot.get_chat_member(message.chat.id, message.from_user.id)
        name = user_info["user"]["username"]
        corpus = message.text.replace(' ', '_')
        add_campus(name, corpus)
        await bot.send_message(message.chat.id, "Отлично, выбери пункт меню", reply_markup=main_markup)
    if message.text == "🍫 Продукты":
        offset = 0
        showed = limit
        #checks in db if any games are available and returns number
        user_info = await bot.get_chat_member(message.chat.id, message.from_user.id)
        name = user_info["user"]["username"]
        ff = await get_campus(name)
        camp = ff[0][0].replace(" ", "_")
        check = checker(ff[0][0])
        message_def = message
        #checks if any games are available
        if check is not None:
            await bot.send_message(message.chat.id, "🍫 Продукты:", reply_markup = order_markup)
            #prints all games from db (connector.py function)
            await print_products(message, offset, limit, showed, camp)
            offset += limit
            showed += limit
        else:
            await bot.send_message(message.chat.id, "🍫 Продуктов в наличии нет")

    #if message text = basket
    elif message.text == "🗑 Корзина":
        choices = await get_choices(message.from_user.username)
        print(choices)
        if (choices[0][1] is not None and choices[0][0] is not None):
            if (choices[0][0] != '' and choices[0][1] != 0):
                final_price = choices[0][1]
                choices = choices[0][0].split(",")
                basket_games = "\n\n🍫 ".join(choices)
                await bot.send_message(message.chat.id, "<b>Корзина: </b>\n\n🍫 {games}\n\n<b>Общая сумма:</b> {final_price} ".format(games=basket_games, final_price=final_price),
                                    parse_mode="html", reply_markup = basket_markup)
            else:
                await bot.send_message(message.chat.id, "🕸 Корзина пуста")
        else:
            await bot.send_message(message.chat.id, "🕸 Корзина пуста")


    #if message text = home
    elif message.text == "🏠 Главное меню":
        #if basket is not empty
        choices_temp = await get_choices(message.from_user.username)
        print(choices_temp)
        if choices_temp[0][0] == "":
            await bot.send_message(message.chat.id, "<b>Вы вышли в главное меню</b>", parse_mode="html", reply_markup = main_markup)
        #if basket is empty
        elif choices_temp != "":
            await bot.send_message(message.chat.id, "<b>Вы вышли в главное меню</b>", parse_mode="html", reply_markup = basket_main_markup)

    elif message.text == "🌀 О нас":
        await bot.send_message(message.chat.id, "FoodUpstairs - бот для покупки базовых бытовых вещей в пределах общежитий МИФИ\n\n💯 Мы прислушиваемся к вашим предложениям и идеям, администрация отвечает на вопросы с 10:00 до 22:00.\n\n🎯 Мы также готовы к сотрудничеству со студенческими объединениями (как официальными, так и неформальными). Если вы проводите какие-либо мероприятия - напишите нам по контактам ниже, у нас есть что вам предложить.\n\n🤗 Ждем каждого в нашем сервисе!\n\nКонтакты для связи:\n@alexmansura", parse_mode="html")

    elif message.text == "🆔️ ID":
        user_info = await bot.get_chat_member(message.chat.id, message.from_user.id)
        name = user_info["user"]["username"]
        #await bot.send_message(message.chat.id, "" , parse_mode="html")#🏮 Ответы на популярные вопросы\n\n🔷 <b>Как мне забрать мой заказ?</b>\n🔹 Вы можете заказать доставку вашего заказа (платно), либо забрать его по адресу(бесплатно).\n\n🔷 <b>Как проходит оплата заказа?</b>\n🔹 После того, как вы оформили заказ, вы можете выбрать способ оплаты: банковская карта, наличные. Оплата наличными принимается только при самовывозе. Вы сможете оплатить заказ банковской картой по ссылке, полученной от бота.\n\n🔷 <b>Как мне вернуть заказ?</b>\n🔹Возврат заказа происходит по адресу:\n\n🔷 <b>Продавец долго не отвечает, что делать?</b>\n🔹 Свяжитесь с ним напрямую, ссылка на чат в телеграмме\n\n
        ff = await get_campus(name)
        # check = checker(ff[0][0])
        camp = ff[0][0].replace("_", " ")
        await bot.send_message(message.chat.id, f'Ваш ID: {message.from_user.id}\nВаш корпус: {camp}\n')
    #if message text = remove from basket
    elif message.text == "✂️ Убрать из корзины":
        #creating variable for indexing choices values
        choices_temp = await get_choices(message.from_user.username)
        final_price = choices_temp[0][1]
        choices = choices_temp[0][0].split(",")
        choices_ind = 0
        #creating remove from basket markup
        remove_markup = InlineKeyboardMarkup(resize_keyboard = True)
        #for each item in basket

        for item in choices:
            #checks for how long user is going to rent a game
            rent_check = item[-6:]
            #gets game's name
            game_name = item.split("[")[0]
            #if the game is rented for one day
            # if rent_check == "1 день":
                #adds remove buttons to markup
            rem_day_button = InlineKeyboardButton(f"Убрать '{game_name}'", callback_data = f"rem_day_{game_name}i{choices_ind}")
            remove_markup.add(rem_day_button)
            remove_check.append(game_name)
            #if the game is rented for one week
            #elif rent_check == "7 дней":
                #adds remove buttons to markup
            #    rem_week_button = InlineKeyboardButton(f"Убрать '{game_name}'", callback_data = f"rem_week_{game_name}i{choices_ind}")
            #    remove_markup.add(rem_week_button)
            #    remove_check.append(game_name)
            #equals index of value in choices
            choices_ind += 1
        await bot.send_message(message.chat.id, "Что убрать?", reply_markup= remove_markup)
    
    #if message text = formalize
    elif message.text == "🟢 Оформить":
        name = message.from_user.username
        choices = await get_choices(name)
        camp = await get_campus(name)
        #asserts basket games to a string
        # order_games = ", ".join(choices)

        #adds order's info to db
        add_order_new(name, choices[0][0], choices[0][1], camp[0][0])
        await bot.send_message(message.chat.id, "❇️ Ваш заказ принят. Мы свяжемся с вами как только можно будет забирать.\n\nЕсли с вами не свяжутся в течение 10 минут, пожалуйста, сообщите об этом @alexmansura.",
                               reply_markup=menu_markup)
        # sends username to a function to order_functions.py which sends the order info to admin chat
        # await send_order(name)
        # removes all games from basket
        choices = ""
        rent_price = 0
        final_price = 0
        add_choices(name, choices, final_price)


        # await bot.send_message(message.chat.id, "🎯 Выберите метод получения заказа", reply_markup = pick_method_markup)
    
    #if message text = pickup
    elif message.text == "🚶🏻 Самовывоз":
        await receive_method("Самовывоз", 0, name)
        await bot.send_message(message.chat.id, "🗺 Самовывоз с адреса:\n<b></b>", parse_mode="html", reply_markup= buy_markup)
    
    #if message text = delivery
    elif message.text == "🚗 Доставка":
        await Address.address.set()
        await bot.send_message(message.chat.id, "🔥 Доставка от <b>200</b> рублей\n(оплачивается отдельно)\n\nВведите адрес доставки:", parse_mode="html", )      
    
    #if message text = pay
    elif message.text == "💰 Оплатить":
        await bot.send_message(message.chat.id, "Выберите способ оплаты:", reply_markup = pay_method)

    #if message text = credit card
    elif message.text == "💳 Банковская карта":
        #adds credit card payment method to db
        sql_start()
        await pay_method_db("Банковская карта", name)
        #comment for qiwi bill
        comment = name + "_" + str(random.randint(1000, 9999))
        #bill config
        bill = p2p.bill(amount = int(final_price), lifetime = 15, comment = comment)
        #adds bill to db
        add_check(name, bill.bill_id)
        await bot.send_message(message.chat.id, f"Ваш счет на оплату сформирован: {bill.pay_url}\n На сумму: {final_price} рублей", reply_markup = pay_menu(url=bill.pay_url, bill = bill.bill_id))

    #if message text = cash
    elif message.text == "💵 Наличными":
        await bot.send_message(message.chat.id, "❗️ Оплата наличными только при самовывозе", reply_markup = cash_markup)    
        sql_start()
        await pay_method_db("Наличными", name)

    #if message text = submit
    elif message.text == "✅ Подтвердить":
        await bot.send_message(message.chat.id, "❇️ Ваш заказ принят, скоро с вами свяжется продавец", reply_markup= menu_markup)
        #sends username to a function to order_functions.py which sends the order info to admin chat

        await send_order(name)
        #removes all games from basket
        choices = []

    #if message text = change payment method
    elif message.text == "🖌 Изменить метод оплаты": 
        await bot.send_message(message.chat.id, "Выберите способ оплаты:", reply_markup = pay_method)

    #if message text = suggest a new game
    elif message.text == "🔙 Вернуться":
        #activates state for saving suggestion from user
        # await Suggestion.suggestion.set()
        # await bot.send_message(message.chat.id, "⌨️ Введите названия игр, которые хотели бы увидеть у нас в сервисе")
        await bot.send_message(message.chat.id, "Выбери корпус", reply_markup=kb_client)
    
#saves address from message
@dp.message_handler(state = Address.address)
async def load_address(message: types.Message, state: Address.address):
    address = message.text
    await bot.send_message(message.chat.id, "✅ Адрес записан", reply_markup = buy_markup)
    #adds address to db
    await receive_method(address, 1, name)
    await state.finish()

#saves suggestion from user
@dp.message_handler(state = Suggestion.suggestion)
async def load_suggestion(message: types.Message, state: Suggestion.suggestion):
    suggestion = message.text
    await bot.send_message(message.chat.id, "📤 Спасибо, ваше предложение сохранено", reply_markup = main_markup)
    #adds suggestion to db
    sql_start()
    await add_suggestion(suggestion, name)
    await state.finish()

#saves question from user
@dp.message_handler(state = Ask.question)
async def load_suggestion(message: types.Message, state: Suggestion.suggestion):
    global name
    question = message.text
    await bot.send_message(message.chat.id, "✳️ Ваш вопрос сохранен и отправлен продавцу", reply_markup = main_markup)
    #adds question to db
    await send_question(name, question)
    await state.finish()

#payment check
@dp.callback_query_handler(lambda c: c.data.startswith("check_"))
async def check(callback: types.CallbackQuery):
    global choices, name
    #gets bill id from callback query
    bill = str(callback.data[6:])
    #checks if bill is in db
    all_info = get_check(bill)
    #if bill is in db
    if all_info != False:
        #if bill is paid
        if str(p2p.check(bill_id = bill).status) == "PAID":
            await bot.send_message(callback.from_user.id, "❇️ Ваш заказ принят, скоро с вами свяжется продавец", reply_markup= menu_markup)
            #sends username to a function to order_functions.py
            await send_order(name)
            #removes all games from basket
            choices = []
            #deletes check
            delete_check(name)
        else:
            await bot.send_message(callback.from_user.id, "🔒 Вы не оплатили заказ", reply_markup = pay_menu(False, bill= bill))
    else:
        await bot.send_message(callback.from_user.id, "❔ Счет не найден")

#add to basket functions
@dp.callback_query_handler(lambda c: c.data.startswith("add_"))
async def add_to_basket(callback: types.CallbackQuery):

    global  offset, limit, showed
    # gets game's info from db
    sql_start()
    # user_info = await bot.get_chat_member(message.chat.id, message.from_user.id)
    # name = user_info["user"]["username"]
    # camp = await get_campus(name)
    # print(camp)
    name = callback.from_user.username
    choices_temp = await get_choices(name)
    if (choices_temp[0][1] is not None and choices_temp[0][0] is not None):
        final_price = choices_temp[0][1]
        choices = choices_temp[0][0].split(",")
    else:
        choices = []
        final_price = 0
    ss = await get_campus(name)
    camp = ss[0][0]

    #adds game's price per day and info to basket  
    if callback.data.startswith("add_day_"):
        #if game is not in basket
        if callback.data.replace("add_day_", "") not in choices:
            print("FDAHFHUDSVFJVADFADF**************************************************************")
            product = await get_info(callback.data.replace("add_day_", ""), camp)
            #alerts that game is in basket 
            await callback.answer(text=f"Продукт '{product[0][0]}' добавлен в корзину")
            #appends game's name and rental period to basket list
            ff = await get_floor(product[0][0], camp)
            floor = ff[0][0]
            floor = floor.replace(',', '|')
            # choices[i] = choices[i] + " Этаж: " + str(ff[0][0])
            choices.append(product[0][0] + "[Этаж: " + str(floor) + "]")
            #summarise game's prices with basket variables
            final_price += int(product[0][1]) #int(product[0][1]) + int(product[0][3])
            #rent_price += int(product[0][1])
            floor = product[0][2]
            print(choices)
            mm = ",".join(choices)
            add_choices(name, mm, final_price)

            #sets that a game is unavailable
            add_value(product[0][0], product[0][3] - 1, camp)

#remove from basket functions
@dp.callback_query_handler(lambda c: c.data.startswith("rem_"))
async def remove_from_basket(callback: types.CallbackQuery):

    global rent_price, final_price, deposit_price, offset, limit, showed
    
    #removes one day game rental from basket
    if callback.data.startswith("rem_day_"):
        basket_name = callback.data.replace("rem_day_", "")
        #getting the name of a game and game's index in choices list
        game_name_ind = basket_name.split("[")[0]
        #getting game's index in choices list
        choices_index = game_name_ind.split("i")[1]
        #getting game's name
        game_name = game_name_ind.split("i")[0]
        #if game is in basket
        if game_name in remove_check:

            #gets game's info from db
            sql_start()
            name = callback.from_user.username
            ss = await get_campus(name)
            camp = ss[0][0]
            product = await get_info(game_name, camp)
            #alerts that game has been removed from basket
            await callback.answer(text=f"Продукт '{game_name}' убран из корзины")

            #removes game's name from remove basket(special variable, which contains only names of games)
            remove_check.remove(game_name)
            choices_temp = await get_choices(name)
            final_price = choices_temp[0][1]
            choices = choices_temp[0][0].split(",")
            #removes game from basket
            choices.pop(int(choices_index))
            #subtracts game's prices from basket variables
            final_price -= int(product[0][1]) # + int(product[0][3])
            rent_price -= int(product[0][1])
            mm = ','.join(choices)
            #  deposit_price -= int(product[0][3])
            add_choices(name, mm, final_price)

            #sets that game is available
            add_value(game_name, product[0][3] + 1, camp)


#load more function
@dp.callback_query_handler(lambda c: c.data)
async def load_more(callback: types.CallbackQuery):
    global message_def, offset, limit, showed
    #load_more function
    camp = await get_campus(name)
    if callback.data == "load_more":
        await print_products(message_def, offset, limit, showed, camp)
        #appending offset for db
        offset += limit
        #counting showed games
        showed += limit