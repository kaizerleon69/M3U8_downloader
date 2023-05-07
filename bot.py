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
        url,
    ]

    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()

    if not e_response:
        video_info = json.loads(t_response)
        video_url = video_info.get("url")
        file_name = video_info.get("title")
        return video_url, file_name
    else:
        return None, None

    
@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("Welcome to the m3u8 downloader bot! Send me a URL ")

@app.on_message(filters.text)
async def download_and_upload(client, message):
    url = message.text
    if "m3u8" in url:
        video_url, file_name = await download_m3u8(url)
        if video_url and file_name:
            await message.reply(f"Downloading {file_name}...")
            os.system(f'wget -O "{file_name}.mp4" "{video_url}"')
            await message.reply(f"Uploading {file_name}...")
            await client.send_video(message.chat.id, f"{file_name}.mp4")
            os.remove(f"{file_name}.mp4")
            await message.reply("Upload completed.")
        else:
            await message.reply("Error downloading the video.")



print('Bot starting!!')
app.run()
