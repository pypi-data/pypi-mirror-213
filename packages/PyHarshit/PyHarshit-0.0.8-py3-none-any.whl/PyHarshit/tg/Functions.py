from pyrogram.errors import FloodWait
import re
import aiohttp
from pyrogram import Client
from pyrogram.types import *
from pyrogram import filters
from pyrogram.raw import functions
from pyrogram import enums


async def copy_msg(sender, msg_link, client, message, link):
    chat =  msg_link.split("/")[-2]
    print('copy_msg function is ready to call.')

    msg_id = 0
    try:
        msg_id = int(link.split("/")[-1])
    except ValueError:
        if '?single' in link:
            link_ = link.split("?single")[0]
            msg_id = int(link_.split("/")[-1])
        else:
            return False, "**Invalid Link!**"
    try:
        msg  = await client.get_messages(chat, msg_id)
    except Exception as e:
        await message.reply(f'{str(e)}')
    if 't.me/c/' in msg_link:
        await message.reply(f'Sorry, but i can only give you message of public channel.', quote=True)
    else:
        chat =  msg_link.split("/")[-2]
    if '?single' in link:
        try:
            await client.copy_media_group(int(sender), msg.chat.id, msg.id)
        except FloodWait as f:
            await message.reply(f'Bot is limited by telegram for {f.value + 2} seconds.\nPlease try again after {f.value + 2} seconds.', quote=True)
            await asyncio.sleep(f.value)
        except Exception as e: 
            return await message.reply(f'Error: {str(e)}', quote=True)
    else:
        try:
            await client.copy_message(int(sender), msg.chat.id, msg.id)
        except FloodWait as f:
            await message.reply(f'Bot is limited by telegram for {f.value + 2} seconds.\nPlease try again after {f.value + 2} seconds.', quote=True)
            await asyncio.sleep(f.value)
        except Exception as e: 
            return await message.reply(f'Error: {str(e)}', quote=True)
