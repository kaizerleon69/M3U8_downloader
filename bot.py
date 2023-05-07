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

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("Send me an M3U8 URL.")
    


async def download_video_info(url):
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
        video_info = json.loads(t_response)
        return video_info, None

@app.on_message(filters.command("info"))
async def info_command(client, message):
    url = message.text.split(" ", 1)[1]
    video_info, error = await download_video_info(url)
    if error:
        await message.reply(f"Error: {error}")
    else:
        await message.reply(f"Title: {video_info['title']}\n"
                            f"Duration: {video_info['duration']} seconds")


print('Bot starting!!')
app.run()
