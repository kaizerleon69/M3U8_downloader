import os
from pyrogram import Client, filters
from m3u8_dl import M3U8_DL


from config import Config

bot_token = Config.TG_BOT_TOKEN
api_id = Config.APP_ID
api_hash = Config.API_HASH

app = Client("Malith:memory:",
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token)


def download_m3u8_video(url, output_path):
    dl = M3U8_DL(url)
    dl.download()
    dl.to_mp4(output_path)


    
@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("Welcome dsfds")

@app.on_message(filters.command("download") & filters.private)
def download_video(client, message):
    url = message.text.split(" ")[1]
    output_path = "downloaded_video.mp4"

    message.reply_text("Downloading and converting the video...")
    try:
        download_m3u8_video(url, output_path)
        message.reply_text("Video downloaded and converted successfully.")
    except Exception as e:
        message.reply_text(f"Error: {e}")

print('Bot starting!!')
app.run()
