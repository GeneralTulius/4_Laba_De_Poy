# Подключение библиотек
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.types import BotCommand


# Уникальный токен бота
TOKEN = '8358160111:AAHpQ5ifFuiG20KT5esETovtZOv7_nDLsZE'


# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Словарь для хранения настройки языка пользователей
user_settings = {}

# Функции для работы с настройками
def set_user_setting(user_id: int, key: str, value):
    if user_id not in user_settings:
        user_settings[user_id] = {}
    user_settings[user_id][key] = value

def get_user_setting(user_id: int, key: str, default=None):
    return user_settings.get(user_id, {}).get(key, default)


# Команды в Telegram
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start",
                   description="Запустить бота"
        ),
        BotCommand(command="help",
                   description="Показать все команды"
        ),
        BotCommand(command="earth_photo",
                   description="🌍 Фото Земли со спутника"
        ),
        BotCommand(command="apod",
                   description="🛰 Фото дня от NASA (APOD)"
        ),
        BotCommand(command="planets",
                   description="🪐 Справка о планетах"
        ),
        BotCommand(command="news",
                   description="📰 Новости космоса"
        ),
        BotCommand(command="set_lang",
                   description="Выбрать язык: ru или en"
        )
    ]
    await bot.set_my_commands(commands)


# Функция меню
def get_menu(lang="ru"):
    if lang == "ru":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text='1 или /earth_photo - 🌍 Фото Земли со спутника',
                callback_data='photo of the earth')
            ],
            [InlineKeyboardButton(
                text='2 или /apod - 🛰 Фото дня от NASA (APOD)',
                callback_data='photo of the day')
            ],
            [InlineKeyboardButton(
                text='3 или /planets - 🪐 Справка о планетах',
                callback_data='planetary reference')
            ],
            [InlineKeyboardButton(
                text='4 или /news - 📰 Новости космоса',
                callback_data='news')
            ],
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text='1 or /earth_photo - 🌍 Earth from Space',
                callback_data='photo of the earth')
            ],
            [InlineKeyboardButton(
                text='2 or /apod - 🛰 NASA Picture of the Day',
                callback_data='photo of the day')
            ],
            [InlineKeyboardButton(
                text='3 or /planets - 🪐 Info about planets',
                callback_data='planetary reference')
            ],
            [InlineKeyboardButton(
                text='4 or /news - 📰 Space news',
                callback_data='news')
            ],
        ])

# Меню для выбора языка
def get_language_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Русский",
                callback_data="lang_ru"
            ),
            InlineKeyboardButton(
                text="English",
                callback_data="lang_en"
            )
        ]
    ])

# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_setting(
        user_id, "language", "ru")

    if lang == "ru":
        text = (f"Здравствуйте, "
                f"{message.from_user.first_name}. "
                f"🚀 Я — бот о космосе! "
                f"Что вы хотите узнать?"
        )
    else:
        text = (f"Hello, "
                f"{message.from_user.first_name}. "
                f"🚀 I am a space bot! "
                f"What would you like to know?"
        )
    await message.answer(
        text, reply_markup=get_menu(lang))

# Команда /help
@dp.message(Command("help"))
async def help(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_setting(user_id, "language", "ru")

    if lang == "ru":
        text = "Команды:"
    else:
        text = "Commands:"

    await message.answer(text, reply_markup=get_menu(lang))

# Команда /set_lang для выбора языка
@dp.message(Command("set_lang"))
async def set_language(message: types.Message):
    await message.answer(
        "Выберите язык / Choose language:",
        reply_markup=get_language_menu()
    )

# Команда /earth_photo
@dp.message(Command("earth_photo"))
async def earth_photo_cmd(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_setting(user_id, "language", "ru")

    if lang == "ru":
        caption="🌍 Это Земля из Космоса"
    else:
        caption="🌍 This is Earth from Space"

    await message.answer_photo(
        photo="https://resizer.mail.ru/p/"
              "a5db777f-57b6-56e2-a846-d28cb6add0f6/"
              "AQAKteqhd-KlJvH2QU-3mpvdd3E7LxmwXM0D8EpkGCZneW5xzAc7o3VbjvJgZQ_EcTfXrE0-3nFfEEon70v5Bwaf5DM.jpg",
        caption=caption,
        reply_markup=get_menu(lang)
    )

# Команда /apod
@dp.message(Command("apod"))
async def apod_cmd(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_setting(user_id, "language", "ru")

    if lang == "ru":
        caption = "🛰 Это фото дня от NASA"
    else:
        caption = "🛰 This is NASA's Picture of the Day"
    await message.answer_photo(
        photo="https://apod.nasa.gov/apod/image/"
              "2508/Crab_HubbleChandraSpitzer_3600.jpg",
        caption=caption,
        reply_markup = get_menu(lang)
    )

# Команда /planets
@dp.message(Command("planets"))
async def planets_cmd(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_setting(user_id, "language", "ru")
    if lang == "ru":
        text = ("🪐 Это справка о планетах\n"
            "https://astrovert.ru/journal/solar_system/"
            "planety-solnechnoy-sistemy-opisanie-klassifikatsiya-i-pravila-nablyudeniya/")
    else:
        text = ("🪐 This is info about planets\n"
         "https://astrovert.ru/journal/solar_system/"
         "planety-solnechnoy-sistemy-opisanie-klassifikatsiya-i-pravila-nablyudeniya/")

    await message.answer(text, reply_markup=get_menu(lang))

# Команда /news
@dp.message(Command("news"))
async def news_cmd(message: types.Message):
    user_id = message.from_user.id
    lang = get_user_setting(user_id, "language", "ru")
    if lang == "ru":
        text = ("📰 Это новости космоса\n"
                "https://lenta.ru/rubrics/"
                "science/cosmos/"
        )
    else:
        text = ("📰 This is space news\n"
                "https://lenta.ru/rubrics/"
                "science/cosmos/"
        )

    await message.answer(text, reply_markup=get_menu(lang))

# Обработка inline-кнопок
@dp.callback_query()
async def callback_message(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    lang = get_user_setting(user_id, "language", "ru")

    if callback.data == "lang_ru":
        set_user_setting(user_id,
                         "language", "ru"
        )
        lang = "ru"
        await callback.message.answer(
            "Язык установлен: Русский",
            reply_markup=get_menu(lang)
        )
    elif callback.data == "lang_en":
        set_user_setting(user_id,
                         "language", "en"
        )
        lang = "en"
        await callback.message.answer(
            "Language set: English",
            reply_markup=get_menu(lang)
        )

    if callback.data == 'photo of the earth':

        if lang == "ru":
            caption = "🌍 Это Земля из Космоса"
        else:
            caption = "🌍 This is Earth from Space"
        await callback.message.answer_photo(
            photo="https://resizer.mail.ru/p/"
                  "a5db777f-57b6-56e2-a846-d28cb6add0f6/"
                  "AQAKteqhd-KlJvH2QU-3mpvdd3E7LxmwXM0D8EpkGCZneW5xzAc7o3VbjvJgZQ_EcTfXrE0-3nFfEEon70v5Bwaf5DM.jpg",
            caption=caption,
            reply_markup = get_menu(lang)
        )

    elif callback.data == 'photo of the day':

        if lang == "ru":
            caption = "🛰 Это фото дня от NASA"
        else:
            caption = "🛰 This is NASA's Picture of the Day"
        await callback.message.answer_photo(
            photo="https://apod.nasa.gov/"
                  "apod/image/2508/"
                  "Crab_HubbleChandraSpitzer_3600.jpg",
             caption=caption,
            reply_markup=get_menu(lang)
        )

    elif callback.data == 'planetary reference':

        if lang == "ru":
            text = ("🪐 Это справка о планетах\n"
                    "https://astrovert.ru/journal/solar_system/"
                    "planety-solnechnoy-sistemy-opisanie-klassifikatsiya-i-pravila-nablyudeniya/"
            )
        else:
            text = ("🪐 This is info about planets\n"
                    "https://astrovert.ru/journal/solar_system/"
                    "planety-solnechnoy-sistemy-opisanie-klassifikatsiya-i-pravila-nablyudeniya/"
            )

        await callback.message.answer(text, reply_markup=get_menu(lang))

    elif callback.data == 'news':
        if lang == "ru":
            text = ("📰 Это новости космоса\n"
                    "https://lenta.ru/rubrics/"
                    "science/cosmos/"
            )
        else:
            text = ("📰 This is space news\n"
                    "https://lenta.ru/rubrics/"
                    "science/cosmos/"
            )

        await callback.message.answer(text, reply_markup=get_menu(lang))

    await callback.answer()


# Пользовательский ввод и обработка исключений
@dp.message()
async def text_commands(message: types.Message):
    text = message.text.strip()
    user_id = message.from_user.id
    lang = get_user_setting(user_id, "language", "ru")

    if text == "1":

        if lang == "ru":
            caption = "🌍 Это Земля из Космоса"
        else:
            caption = "🌍 This is Earth from Space"

        await message.answer_photo(
            photo="https://resizer.mail.ru/p/"
                  "a5db777f-57b6-56e2-a846-d28cb6add0f6/"
                  "AQAKteqhd-KlJvH2QU-3mpvdd3E7LxmwXM0D8EpkGCZneW5xzAc7o3VbjvJgZQ_EcTfXrE0-3nFfEEon70v5Bwaf5DM.jpg",
            caption=caption,
            reply_markup=get_menu(lang)
        )

    elif text == "2":

        if lang == "ru":
            caption = "🛰 Это фото дня от NASA"
        else:
            caption = "🛰 This is NASA's Picture of the Day"

        await message.answer_photo(
            photo="https://apod.nasa.gov/"
                  "apod/image/2508/"
                  "Crab_HubbleChandraSpitzer_3600.jpg",
            caption=caption,
            reply_markup=get_menu(lang)
        )

    elif text == "3":

        if lang == "ru":
            text = ("🪐 Это справка о планетах\n"
                    "https://astrovert.ru/journal/solar_system/"
                    "planety-solnechnoy-sistemy-opisanie-klassifikatsiya-i-pravila-nablyudeniya/"
            )
        else:
            text = ("🪐 This is info about planets\n"
                    "https://astrovert.ru/journal/solar_system/"
                    "planety-solnechnoy-sistemy-opisanie-klassifikatsiya-i-pravila-nablyudeniya/"
            )
        await message.answer(text, reply_markup=get_menu(lang))

    elif text == "4":
        if lang == "ru":
            text = ("📰 Это новости космоса\n"
                    "https://lenta.ru/rubrics/"
                    "science/cosmos/"
            )
        else:
            text = ("📰 This is space news\n"
                    "https://lenta.ru/rubrics/"
                    "science/cosmos/"
            )
        await message.answer(text, reply_markup=get_menu(lang))

    else:
        if lang == "ru":
            unknown = "Команда не найдена"
        else:
            unknown = "Command not found"
        await message.answer(
            unknown, reply_markup=get_menu(lang)
        )


# Запуск бота
async def main():
    await set_commands(bot)
    await dp.start_polling(bot)


# Запуск программы
if __name__ == "__main__":
    asyncio.run(main())
