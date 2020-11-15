## Mandatory Imports
```python3
from indus.utils import admin_cmd, sudo_cmd, eor
```
There is None Mandatory Imports. Because Var, bot and command are already automatically imported.

## Explanation
The Mandatory Imports are now automatically imported.

### Formation
Now I will show a short script to show the formation of the desired script.
```python3
@indus.on(admin_cmd(pattern="alive", outgoing=True))
@indus.on(sudo_cmd(pattern="alive", allow_sudo=True))
async def hello_world(event):
    if event.fwd_from:
        return
    await eor(event,"**HELLO WORLD**\n\nThe following is controlling me too!\n" + Var.SUDO_USERS)
```
