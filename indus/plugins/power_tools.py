"""Restart or Terminate the bot from any chat
Available Commands:
.restart
.shutdown"""
# This Source Code Form is subject to the terms of the GNU
# General Public License, v.3.0. If a copy of the GPL was not distributed with this
# file, You can obtain one at https://www.gnu.org/licenses/gpl-3.0.en.html
from telethon import events
import asyncio
import os
import sys
from indus.utils import admin_cmd, sudo_cmd, eor
from indus import CMD_HNDLR, SUDO_HNDLR

@indus.on(admin_cmd("restart", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit(f"Restarted. `{CMD_HNDLR}ping` or `{CMD_HNDLR}help` to check if I am online")
    await borg.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()

@indus.on(sudo_cmd("restart", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    await eor(event,f"Restarted. `{SUDO_HNDLR}ping` or `{SUDO_HNDLR}help` to check if I am online")
    await borg.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()


@indus.on(admin_cmd("shutdown", outgoing=True))
@indus.on(sudo_cmd("shutdown", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Turning off ...Manually turn me on later")
    await borg.disconnect()
