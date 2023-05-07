from pyrogram import Client, filters
import ffmpeg
import os

from config import Config

bot_token = Config.TG_BOT_TOKEN
api_id = Config.APP_ID
api_hash = Config.API_HASH

app = Client("Malith:memory:",
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token)

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("Send me an M3U8 URL to download and convert to MP4.")

@app.on_message(filters.text)
async def download(_, message):
    url = message.text
    output = "output.mp4"

    try:
        stream = ffmpeg.input(url)
        stream = ffmpeg.output(stream, output, format="mp4")
        ffmpeg.run(stream)
        await message.reply_video(output)
    except Exception as e:
        await message.reply_text(f"Error: {e}")


print('Bot starting!!')
app.run()
