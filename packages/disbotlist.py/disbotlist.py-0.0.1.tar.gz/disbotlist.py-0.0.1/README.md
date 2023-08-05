# disbotlist 

Useful library for [DisBotList.xyz](https://disbotlist.xyz)


## Installation
```
pip install disbotlist
```
## Example 
Server Count Post :
```python
from disbotlist import *
from discord.ext import commands

client = commands.Bot(command_prefix="!") 
dbl = disbotlist(client,"token of disbots")

@client.event
async def on_ready():
  x = await dbl.serverCountPost()
  print(x)

client.run("token")
```
