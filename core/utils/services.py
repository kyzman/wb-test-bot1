import requests
from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from core.keyboards.inline import subscribe_kbd
from core.keyboards.stdkbd import main_kbd
from core.settings import BASE_HELP


async def cancel_command(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer(BASE_HELP, parse_mode='HTML', reply_markup=main_kbd)


async def get_wb_card_nested_info(article: int):
    # это конечно плохо, что функция возвращает разные типы данных, но в данном конкретном случае почему бы и нет?
    request = requests.get(f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}")
    if request.status_code == 200:
        products = request.json().get("data").get("products")
    else:
        return 'Ошибка запроса к сайту wildberries!'
    result = {"products": []}
    if products:
        qty = 0
        for product in products:
            if stores := product.get("sizes")[0].get("stocks"):
                for store in stores:
                    qty += store.get("qty")
            else:
                qty = 'Товар закончился!'

            result["products"].append({
                "brand": product.get("brand"),
                "name": product.get("name"),
                "article": product.get("id"),
                "orig_price": product.get("priceU")/100,
                "price": product.get("salePriceU")/100,
                "rating": product.get("reviewRating"),
                "stocks": qty,
                                       })
    else:
        result = 'Товары с таким артикулом не найдены!'
    return result


async def send_card_msg_info(bot: Bot, chat_id: int, article: int, add_subscribe_kbd: bool = False, header: str = ''):
    data = await get_wb_card_nested_info(article)
    kbd = None
    output = ""
    if type(data) is str:
        output = data
    else:
        products = data.get("products")
        if add_subscribe_kbd:
            kbd = subscribe_kbd(int(article))
        for product in products:
            output += (f'[{product.get("brand")}] {product.get("name")}\n'
                       f'Текущая цена: {product.get("price")}\n'
                       f'Рейтинг: {product.get("rating")}\n'
                       f'Количество на складах: {product.get("stocks")}\n')

    name = f'{header}\nИнформация по товару с артикулом {article}\n {output}'
    await bot.send_message(chat_id, name, reply_markup=kbd)
    return data
