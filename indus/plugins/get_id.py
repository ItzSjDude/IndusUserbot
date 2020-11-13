"""Get ID of any Telegram media, or any user
Syntax: .get_id"""
from telethon import events
from telethon.utils import pack_bot_file_id
from indus.utils import admin_cmd, sudo_cmd, eor


@indus.on(admin_cmd("id"))
@indus.on(sudo_cmd("id", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        chat = await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await eor(event,"Current Chat ID: `{}`\nFrom User ID: `{}`\nBot API File ID: `{}`".format(str(event.chat_id), str(r_msg.sender_id), bot_api_file_id))
        else:
            await eor(event,"Current Chat ID: `{}`\nFrom User ID: `{}`".format(str(event.chat_id), str(r_msg.sender_id)))
    else:
        await eor(event,"Current Chat ID: `{}`".format(str(event.chat_id)))
