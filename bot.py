import asyncio
import json
import os
from pyrogram import Client, filters
from config import Config

bot_token = Config.TG_BOT_TOKEN
api_id = Config.APP_ID
api_hash = Config.API_HASH

app = Client("Malith:memory:",
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token)

def download_m3u8(url, download_directory, minus_f_format="best"):
    command_to_exec = {
        "format": minus_f_format,
        "continue_dl": True,
        "hls_prefer_ffmpeg": True,
        "embed_subs": True,
        "outtmpl": download_directory
    }
    with youtube_dl.YoutubeDL(command_to_exec) as ydl:
        ydl.download([url])

    
@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("Welcome ")

@app.on_message(filters.command(["download"]))
async def download_handler(client: Client, message: Message):
    url = message.text.split()[-1]
    download_directory = "downloads/%(title)s.%(ext)s"
    minus_f_format = "best"

    await message.reply("Downloading...")
    download_m3u8(url, download_directory, minus_f_format)
    await message.reply("Download completed. Uploading...")

    with open(download_directory, 'rb') as f:
        await client.send_document(chat_id=message.chat.id, document=f)

    await message.reply("Upload completed.")



print('Bot starting!!')
app.run()
