from telethon import events
from datetime import datetime
from indus.utils import admin_cmd, sudo_cmd, eor

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


@indus.on(admin_cmd(pattern="ping", outgoing=True))
@indus.on(sudo_cmd(pattern="ping", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await eor(event, f"Pong! 🏓 {ms} ..")


@indus.on(admin_cmd(pattern="pong", outgoing=True))
@indus.on(sudo_cmd(pattern="pong", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    end = datetime.now()
    ms = (end - start).microseconds * 0.00001
    await eor(event, f"Ping! 🎾 {ms} ..")
