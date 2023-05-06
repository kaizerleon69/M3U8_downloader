import asyncio
import logging
import json
from pyrogram import filters, Client
from pyrogram.types import Message
import os

from config import Config
 
bot_token=Config.TG_BOT_TOKEN
api_id=Config.APP_ID
api_hash=Config.API_HASH

app = Client("Malith:memory:", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

  # sending files
async def sender(msg, download_location, fileName):
    await msg.reply_document(download_location, caption=f"{fileName}",quote=True)
    os.remove(download_location)
 
# downloading link
async def download(msg, download_location, url, formatt):
    try:
        command_to_exec = [
            "youtube-dl",
            "-f",
            formatt,
            "-o",
            download_location,
            url
        ]
        await msg.reply_text("Downloading!!", quote=True)
        # logger.info(command_to_exec)
        process = await asyncio.create_subprocess_exec(
            *command_to_exec,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
        await process.communicate()
    except:
        await msg.reply_text("An err occured!!", quote=True)
 
 
# getting forrmat details
async def getting_filename(url, msg):
    command_to_exec = [
            "youtube-dl",
            "--no-warnings",
            "--youtube-skip-dash-manifest",
            "-j",
            url
        ]
        # logger.info(command_to_exec)
    process = await asyncio.create_subprocess_exec(
            *command_to_exec,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    # logger.info(e_response)
    t_response = stdout.decode().strip()
    if t_response:
        # logger.info(t_response)
        x_reponse = t_response
 
        if "\n" in x_reponse:
            x_reponse = x_reponse.split("\n")
 
        response_json = json.loads(x_reponse)
        save_ytdl_json_path = str(msg.from_user.id) + ".json"
 
        with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
            json.dump(response_json, outfile, ensure_ascii=False)
 
        fileName = response_json["_filename"]
 
 
    os.remove(save_ytdl_json_path)
    return fileName
 
# getting forrmat details
async def getting_format(url, msg):
    command_to_exec = [
            "youtube-dl",
            "--no-warnings",
            "--youtube-skip-dash-manifest",
            "-j",
            url
        ]
        # logger.info(command_to_exec)
    process = await asyncio.create_subprocess_exec(
            *command_to_exec,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    # logger.info(e_response)
    t_response = stdout.decode().strip()
    if t_response:
        # logger.info(t_response)
        x_reponse = t_response
 
        if "\n" in x_reponse:
            x_reponse = x_reponse.split("\n")
 
        response_json = json.loads(x_reponse)
        save_ytdl_json_path = str(msg.from_user.id) + ".json"
 
        with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
            json.dump(response_json, outfile, ensure_ascii=False)
 
        # 
        if "formats" in response_json:
            dic = []
            await msg.reply_text("**Available formats::**", quote=True)
            for formats in response_json["formats"]:
                format_id = formats.get("format_id")
                await msg.reply_text(format_id)
 
    os.remove(save_ytdl_json_path)
 
 
 
 
@app.on_message(filters.private & filters.command('formats'))
async def getFormat(bot:Client, msg:Message):
    if (" " in msg.text):
        cmd, url = msg.text.split(" ", 1)
    await getting_format(url=url, msg=msg)
 

@app.on_message(filters.private & filters.command('start'))
async def getFormat(bot:Client, msg:Message):
    await msg.reply_text(f'**Welcome {msg.from_user.mention}**')
 
@app.on_message(filters.incoming | filters.private & filters.text)
async def downloader(bot:Client, msg:Message):
    url = msg.text
    formatt = None
    if "*" in url:
        url_parts = url.split("*")
        if len(url_parts) == 2:
            url = url_parts[0]
            formatt = url_parts[1]
        else:
            await msg.reply_text("File name error!!", quote=True)
        if url is not None:
            url = url.strip()
        if formatt is not None:
            formatt = formatt.strip()
    download_location = await getting_filename(url=url, msg=msg)
    await download(msg=msg, download_location=download_location, url=url, formatt=formatt)
    await sender(msg=msg, download_location=download_location, fileName=download_location)
 
print('Bot starting!!')
app.run()
