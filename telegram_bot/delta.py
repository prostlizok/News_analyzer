import logging
import json
import pandas as pd
import os
import psycopg2

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackContext
)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
LOCATIONS_FILE = "ua.csv"
DATA_DIR = "./user_data"

# DB_PARAMS = {
#     "dbname": "tg_data_base",
#     "user": "postgres",
#     "password": "123",
#     "host": "localhost",
#     "port": "5432"
# }

locations_df = pd.read_csv(LOCATIONS_FILE)
settlements = list(locations_df.iloc[:, 0])
settlements_upd = []
for i in list(locations_df.iloc[:, 0]):
    settlements_upd.append([i])


# def add_user_request(category, city, lan, lng, contact):
#     try:
#         conn = psycopg2.connect(**DB_PARAMS)
#         print("Connected to the database successfully!")

#         cur = conn.cursor()

#         cur.execute("INSERT INTO user_requests (category, city, latitude, longitude, contact) "
#                     "VALUES (%s, %s, %s, %s, %s)", (category, city, float(lan), float(lng), contact))
#         conn.commit()

#         cur.close()

#     except Exception as e:
#         print(f"Error: {e}")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

REQUEST, CITY, CONTACT, GET_NAME_AND_CONTACT = range(4)

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their needs."""
    reply_keyboard = [['Відбудова житлових будинків🏡'],
                       ['Відбудова критичної інфраструктури🏥'],
                       ['Їжа та продовольчі товари🍎'],
                       ['Одяг👕'],
                       ['Медикаменти та засоби особистої гігієни💊']]

    await update.message.reply_text(
        "Привіт👋\n"
        "На зв'язку бот Гуманітарного фонду! Обери категорію, в якій бажаєш отримати допомогу.\n",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder="Вкажи свій запит"
        ),
    )

    return REQUEST


async def request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the request and asks for a location."""
    user = update.message.from_user
    logger.info("User %s needs: %s", user.first_name, update.message.text)

    # reply_keyboard = settlements_upd
    # context.user_data['id'] = user.id
    context.user_data['request'] = context.user_data.get('request', update.message.text)

    await update.message.reply_text(
        "Дякуємо!\n"
        "Ваш запит вже прийнято в обробку🤝\n"
        "Зараз поділися, будь ласка, свої місцезнаходженням (з точністю до району населеного пункту), "
        "щоб ми могли надати допомогу",
        reply_markup=ReplyKeyboardMarkup(
            settlements_upd,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder="Обери свій населений пункт"
        ),
    )

    return CITY


async def city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for the user contacts."""
    user = update.message.from_user
    index = locations_df[locations_df['city'] == update.message.text].index[0]
    lat = locations_df.loc[index, 'lat']
    lon = locations_df.loc[index, 'lng']

    logger.info(
        "User %s location: %s, %s", user.first_name, lat, lon
    )

    context.user_data['city'] = update.message.text
    context.user_data['lat'] = lat
    context.user_data['lng'] = lon

    reply_keyboard = [
        ['Так, використати мій username'], ['Ні, я хочу ввести ім\'я вручну']
    ]

    await update.message.reply_text(
        "Чудово! Дякую👐\n\n"
        "Чи можу я використовувати твій поточний Telegram username для контакту з тобою?\n"
        "Якщо так, натисни кнопку \"Так, використати мій username\". Якщо ні, натисни \"Ні, я хочу ввести ім'я вручну\".",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                         one_time_keyboard=True,
                                         resize_keyboard=True,
                                         input_field_placeholder="Обери опцію")
    )

    return CONTACT


async def automated_name(update: Update, context: ContextTypes.DEFAULT_TYPE, user_data) -> int:
    """Add the user telegram nickname automatically."""
    user = update.message.from_user
    user_data['contact'] = user.username
    await update.message.reply_text(
        f"Супер, тепер ми будемо використовувати твій Telegram акаунт @{user.username} для зв'язку з тобою.\n"
        f"Очікуй на повідомлення найближчим часом❤️"
    )
    logger.info(f"User name: {user_data['contact']}")

    user_id = user.id
    file_path = os.path.join(DATA_DIR, f'user_{user_id}.json')

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(user_data, f, ensure_ascii=False, indent=4)

    api_url = "http://localhost:8000/v1/request_collection"  
    
    payload = {
        "city": user_data['city'],
        "explosion": False,  
        "num_of_explosions": 0,
        "damage": False,
        "victims": False,
        "num_of_victims": 0,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json=payload) as response:
            if response.status == 200:
                logger.info("Data inserted successfully via API")
            else:
                logger.error(f"Failed to insert data via API. Status: {response.status}")
    
    # add_user_request(user_data['request'], user_data['city'], user_data['lat'], user_data['lng'], user_data['contact'])

    return ConversationHandler.END


async def user_info_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Choose the way to add user contacts."""
    user_data = context.user_data
    if update.message.text == 'Так, використати мій username':
        await automated_name(update, context, user_data=user_data)
    elif update.message.text == 'Ні, я хочу ввести ім\'я вручну':
        await update.message.reply_text(
            "Будь ласка, введи своє ім'я та номер для контакту"
        )
        return GET_NAME_AND_CONTACT


async def handle_user_input(update: Update, context: CallbackContext):
    """Enter the user contacts manually."""
    user_data = context.user_data
    user_data['contact'] = update.message.text

    logger.info(f"User name: {user_data['contact']}")
    user = update.message.from_user
    user_id = user.id
    file_path = os.path.join(DATA_DIR, f'user_{user_id}.json')

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(context.user_data, f, ensure_ascii=False, indent=4)

    await update.message.reply_text(
        "Дякую! Твої дані були збережені.\n"
        "Наш менеджер зв'яжеться з тобою найближчим часом❤️"
    )
    add_user_request(user_data['request'], user_data['city'], user_data['lat'], user_data['lng'], user_data['contact'])

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Щасти!", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            REQUEST: [MessageHandler(filters.TEXT, request)],
            CITY: [MessageHandler(filters.TEXT, city)],
            CONTACT: [MessageHandler(filters.TEXT, user_info_decision)],
            GET_NAME_AND_CONTACT: [MessageHandler(filters.TEXT, handle_user_input)]
        },
        fallbacks=[
            CommandHandler("cancel", cancel)
        ],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
