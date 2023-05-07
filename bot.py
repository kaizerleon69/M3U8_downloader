import asyncio
import json
from pyrogram import Client, filters
from config import Config

bot_token = Config.TG_BOT_TOKEN
api_id = Config.APP_ID
api_hash = Config.API_HASH

app = Client("Malith:memory:",
             api_id=api_id,
             api_hash=api_hash,
             bot_token=bot_token)

async def download_m3u8(url):
    command_to_exec = [
        "youtube-dl",
        "--no-warnings",
        "--youtube-skip-dash-manifest",
        "-j",
        url
    ]

    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()

    if e_response:
        return None, e_response
    else:
        video_data = json.loads(t_response)
        return video_data['url'], None

    
@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("Welcome to the m3u8 downloader bot! Send me a URL and I'll download the m3u8 file for you.")

@app.on_message(filters.text)
async def download(_, message):
    url = message.text
    m3u8_url, error = await download_m3u8(url)

    if error:
        await message.reply_text(f"Error downloading m3u8 file: {error}")
    else:
        await message.reply_text(f"Downloaded m3u8 file: {m3u8_url}")


print('Bot starting!!')
app.run()
