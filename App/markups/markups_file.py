from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

btn1: KeyboardButton = KeyboardButton(text='Корпус 1')
btn2: KeyboardButton = KeyboardButton(text='Корпус 2')
btn3: KeyboardButton = KeyboardButton(text='Корпус 3')
btn4: KeyboardButton = KeyboardButton(text='Кошка')

kb_client = ReplyKeyboardMarkup(keyboard=[[btn1, btn2, btn3, btn4]], resize_keyboard=True, one_time_keyboard=True)

#creating keyboard buttons for start menu keyboard
choose_game = KeyboardButton("🍫 Продукты")
menu_btn = KeyboardButton("🏠 Главное меню")

#adding some keyboard buttons to start menu keyboard
menu_markup = ReplyKeyboardMarkup(resize_keyboard= True).add(menu_btn)

#creating keyboard buttons for main menu keyboard
about_btn = KeyboardButton("🌀 О нас")
faq_btn = KeyboardButton("🆔️ ID")
ask_btn = KeyboardButton("🖌 Спросить")
suggestion_btn = KeyboardButton("🔙 Вернуться")

#creating basket button
basket_btn = KeyboardButton("🗑 Корзина")

#adding all keyboard buttons to main menu keyboard
main_markup = ReplyKeyboardMarkup(resize_keyboard = True).add(about_btn, faq_btn, basket_btn, choose_game, suggestion_btn)

#creating remove from basket button
basket_remove_btn = KeyboardButton("✂️ Убрать из корзины")

#creating menu with basket button
order_markup = ReplyKeyboardMarkup(resize_keyboard = True,).add(basket_btn, menu_btn)

#adding main markup with basket
basket_main_markup = ReplyKeyboardMarkup(resize_keyboard = True).add(about_btn, faq_btn, basket_btn, choose_game, suggestion_btn)

#creating buy button
buy_btn = KeyboardButton("🟢 Оформить")

#creating order menu 
basket_markup = ReplyKeyboardMarkup(resize_keyboard = True, row_width=2).add(basket_remove_btn, basket_btn, menu_btn, choose_game, buy_btn)
#creating keyboard for choosing games with basket
choice_basket_markup = ReplyKeyboardMarkup(resize_keyboard= True, row_width=2).add(choose_game, menu_btn, basket_btn)

#creating load more button
load_more = InlineKeyboardButton("Показать ещё", callback_data="load_more")
#adding to inline keyboard 
load_markup = InlineKeyboardMarkup(resize_keyboard = True).add(load_more)

#creating different pick up games buttons
pickup = KeyboardButton("🚶🏻 Самовывоз")
delivery = KeyboardButton("🚗 Доставка")
#creating pick games method markup
pick_method_markup = ReplyKeyboardMarkup(resize_keyboard = True, row_width=2).add(pickup, delivery, menu_btn)

#creating buy function
buy_btn = KeyboardButton("💰 Оплатить")
#creating buy markup
buy_markup = ReplyKeyboardMarkup(resize_keyboard = True, row_width=2).add(buy_btn, basket_btn, menu_btn)

#creating remove markup
rmarkup = ReplyKeyboardMarkup(resize_keyboard = True)

#adding payment choice markup
card_btn = KeyboardButton("💳 Банковская карта")
cash_btn = KeyboardButton("💵 Наличными")
#adding payment choice markup
pay_method = ReplyKeyboardMarkup(resize_keyboard = True, row_width=2).add(card_btn, cash_btn, menu_btn)

#adding buttons before final order's submint with cash payment method
submit_btn = KeyboardButton("✅ Подтвердить")
change_btn = KeyboardButton("🖌 Изменить метод оплаты")
#adding markup before final order's submint with cash payment method
cash_markup = ReplyKeyboardMarkup(resize_keyboard = True, row_width=1).add(submit_btn, change_btn, menu_btn)

#adding return available button
available_btn = KeyboardButton("📪 Вернуть в наличие")
#adding add new game to db
add_new = KeyboardButton("🎲 Добавить новую игру")
#adding delete game from db button
del_game_btn = KeyboardButton("💥 Удалить игру")

#adding admin markup
admin_markup = ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2).add(available_btn, add_new, del_game_btn, menu_btn)

#adding submit adding new game to db
sub_add_btn = KeyboardButton("✅ Добавить")
reset_btn = KeyboardButton("🗯 Сбросить")

#adding submit or reset all info about new game
sub_res_markup = ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2).add(sub_add_btn, reset_btn, menu_btn)

#creating pay menu function
def pay_menu(isUrl = True, url="", bill=""):
    qiwi_menu = InlineKeyboardMarkup(row_width = 1)
    if isUrl:
        urlQiwi = InlineKeyboardButton("Ссылка на оплату", url=url)
        qiwi_menu.add(urlQiwi)
    checkQiwi = InlineKeyboardButton("Проверить оплату", callback_data = f"check_{bill}")
    qiwi_menu.add(checkQiwi)
    return qiwi_menu