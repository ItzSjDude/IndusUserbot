from telethon import events
from datetime import datetime
from indus.utils import admin_cmd, sudo_cmd, eor

@indus.on(admin_cmd(pattern="ping", outgoing=True))
@indus.on(sudo_cmd(pattern="ping", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await eor(event, f"Pong! 🏓 {ms} ..")

