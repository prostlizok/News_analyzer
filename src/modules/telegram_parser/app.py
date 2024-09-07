from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timezone, timedelta
from telethon import TelegramClient
from llm import collect_info
import mysql.connector
from mysql.connector import Error

app = FastAPI()
api_id = '23820475'
api_hash = 'a824100fa06212137cf544aa07a257c8'

client = TelegramClient('session_2', api_id, api_hash)



db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2006Uliana',
    'database': 'map_db'
}



def insert_data_to_db(data):
        try:
            connection = mysql.connector.connect(**db_config)
            if connection.is_connected():
                cursor = connection.cursor()
                for item in data:
                    for emergency in item.get('emergency_info', []):
                        cursor.execute("""
                            INSERT INTO demage_data (city, explosion, num_of_explosions, damage, victims, num_of_victims, event_date)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (
                            emergency['city'],
                            emergency['explosion'],
                            emergency.get('num_of_explosions'),
                            emergency['damage'],
                            emergency['victims'],
                            emergency.get('num_of_victims'),
                            item['date'][:10] 
                        ))
                connection.commit()
                print("Дані успішно вставлено у базу даних.")
        except Error as e:
            print(f"Помилка при підключенні до MySQL: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()






async def startup():
    await client.start()


async def shutdown():
    await client.disconnect()

# Функція, яка збирає новини кожну хвилину
async def fetch_news():
    data_json = []
    channel = 'uliana_channel'  

    channel_entity = await client.get_entity(channel)
    async for message in client.iter_messages(channel_entity):
        if (datetime.now(tz=timezone.utc) - message.date) <= timedelta(minutes=1) and message.text:

   
                    message_data = {
                        "text": message.text,
                        "date": message.date.isoformat(), 
                        "channel": "monitorwarr",
                        "link": "https://t.me/monitorwarr/23894" 
                    }
                    data_json.append(message_data)
    output_json = collect_info(input_json=data_json)

    insert_data_to_db(output_json)
    print(f"Знайдено {output_json} нових повідомлень з каналу monitorwarr")

# Функція, яка збирає новини кожні 30 хвилин
async def fetch_news_from_other_channel():
    channel = 'monitorwarr'  
    other_news = []

    channel_entity = await client.get_entity(channel)
    async for message in client.iter_messages(channel_entity):
        if (datetime.now(tz=timezone.utc) - message.date) <= timedelta(minutes=30) and message.text:
            other_news.append(message)

    print(f"Знайдено {len(other_news)} нових повідомлень з іншого каналу monitorwarr")


scheduler = AsyncIOScheduler()
scheduler.add_job(fetch_news, 'interval', minutes=1, max_instances=5)
scheduler.add_job(fetch_news_from_other_channel, 'interval', minutes=30)  
scheduler.start()


@app.on_event("startup")
async def on_startup():
    await startup()


@app.on_event("shutdown")
async def on_shutdown():
    await shutdown()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
