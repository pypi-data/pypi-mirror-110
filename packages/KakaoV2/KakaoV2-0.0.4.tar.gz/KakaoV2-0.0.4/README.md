KakaoV2
=======
KakaoV2 is Kakaotalk LOCO/HTTP API protocol wrapper for python.

Introduction
------------
Loco protocol compatible python library
This is discord.py style.

Quick Start
-------
```python
import KakaoV2

client = KakaoV2.Client(device_uuid="DeviceUUID")

@client.event
async def on_ready():
    print("Ready!")

@client.event
async def on_message(msg):
    print(msg.content, msg.author)
    await msg.reply("TEXT")
    await msg.send("TEXT")

client.run("ID", "PW")
```

License
-------
MIT Licence
