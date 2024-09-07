from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timezone, timedelta
from telethon import TelegramClient
from llm import collect_info, get_updated_data


app = FastAPI()
api_id = '23820475'
api_hash = 'a824100fa06212137cf544aa07a257c8'

client = TelegramClient('session_2', api_id, api_hash)

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
    print("Inserting data to db")
    #insert_data_to_db(output_json)
    print(f"Знайдено {len(output_json)} нових повідомлень з каналу monitorwarr")

# Функція, яка збирає новини кожні 30 хвилин
async def fetch_news_from_other_channel():
    dsns_update = []
    channel = 'custom_dsns'  

    channel_entity = await client.get_entity(channel)
    async for message in client.iter_messages(channel_entity):
        if (datetime.now(tz=timezone.utc) - message.date) <= timedelta(minutes=30) and message.text:
            update_json = get_updated_data(message.text)
            print(update_json)
            dsns_update.append(update_json)
    update_with_dsns_data(dsns_update)
   # в update_json наступні дані {'city': 'Херсон', 'victims': False, 'damage': True, 'num_of_victims': 0}
    print(f"дані оновлено з дснс")


scheduler = AsyncIOScheduler()
scheduler.add_job(fetch_news, 'interval', minutes=0.1, max_instances=1)
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
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
