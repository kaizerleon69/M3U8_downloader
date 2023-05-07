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
    await message.reply_text("Send me an M3U8 URL.")
    
@app.on_message(filters.command("download"))
async def download_m3u8_video(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide the m3u8 URL.")
        return

    url = message.command[1]
    output_file = "output1.mp4"

    try:
        await message.reply("Downloading and processing the video...")

        # Download and process the video using ffmpeg-python
        input_stream = ffmpeg.input(url, err_detect="ignore_err")
        output_stream = ffmpeg.output(input_stream, output_file, c="copy", bsf_a="aac_adtstoasc")
        ffmpeg.run(output_stream)

        await message.reply("Uploading the video...")
        await app.send_video(message.chat.id, output_file)
        os.remove(output_file)
    except Exception as e:
        await message.reply(f"Error: {e}")



print('Bot starting!!')
app.run()
