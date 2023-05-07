from pyrogram import Client, filters
from pyrogram.types import Message
import requests
import ffmpeg

from config import Config

bot_token = Config.TG_BOT_TOKEN
api_id = Config.APP_ID
api_hash = Config.API_HASH

app = Client("Malith:memory:",
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token)


def download_m3u8(url):
    r = requests.get(url)
    with open('video.m3u8', 'wb') as f:
        f.write(r.content)

def convert_m3u8_to_mp4():
    (
        ffmpeg
        .input('video.m3u8')
        .output('video.mp4', format='mp4')
        .run()
    )

def upload_mp4():
    with open('video.mp4', 'rb') as f:
        client.send_video(chat_id=<chat_id>, video=f, caption=<caption>)


    
@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("Welcome")
    
@app.on_message(filters.command("convert"))
async def convert_video(client: Client, message: Message):
    url = message.text.split(' ')[1]
    download_m3u8(url)
    convert_m3u8_to_mp4()
    upload_mp4()

    await message.reply_text("Video converted and uploaded!")


print('Bot starting!!')
app.run()
