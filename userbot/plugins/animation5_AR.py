# https://github.com/Jisan09/catuserbot credits to @Jisan7509

import asyncio


@bot.on(admin_cmd(pattern=f"loading$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"loading$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.3
    animation_ttl = range(20)
    event = await edit_or_reply(event, "▯")
    animation_chars = ["▮", "▯", "▬", "▭", "‎"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 4])


@bot.on(admin_cmd(pattern=f"square$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"square$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.3
    animation_ttl = range(20)
    event = await edit_or_reply(event, "◨")
    animation_chars = ["◧", "◨", "◧", "◨", "‎"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 4])


@bot.on(admin_cmd(pattern=f"up$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"up$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.3
    animation_ttl = range(20)
    event = await edit_or_reply(event, "╻")
    animation_chars = ["╹", "╻", "╹", "╻", "‎"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 4])


@bot.on(admin_cmd(pattern=f"round$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"round$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.3
    animation_ttl = range(20)
    event = await edit_or_reply(event, "Round...")
    animation_chars = ["⚫", "⬤", "●", "∘", "‎"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 4])


@bot.on(admin_cmd(pattern=f"hart$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"hart$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.5
    animation_ttl = range(20)
    event = await edit_or_reply(event, "❤️")
    animation_chars = ["🖤", "❤️", "🖤", "❤️", "‎"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 4])


@bot.on(admin_cmd(pattern=f"anim$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"anim$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(20)
    event = await edit_or_reply(event, "😢")
    animation_chars = [
        "😁",
        "😧",
        "😡",
        "😢",
        "😁",
        "😧",
        "😡",
        "😢",
        ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 10])


@bot.on(admin_cmd(pattern=f"fnl$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"fnl$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 2
    animation_ttl = range(6)
    event = await edit_or_reply(event, "Hey There....")
    animation_chars = ["😁🏿", "😁🏾", "😁🏽", "😁🏼", "‎😁", "**بخير لرؤيتك صديقي....**"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 6])


@bot.on(admin_cmd(pattern=f"monkey$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"monkey$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 2
    animation_ttl = range(12)
    event = await edit_or_reply(event, "Hey There....")
    animation_chars = ["🐵", "🙉", "🙈", "🙊", "🖕‎🐵🖕", "**Good to see you friend....**"]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 6])



@bot.on(admin_cmd(pattern=f"hand$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"hand$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(13)
    event = await edit_or_reply(event, "🖐️")
    animation_chars = [
        "👈",
        "👉",
        "☝️",
        "👆",
        "🖕",
        "👇",
        "✌️",
        "🤞",
        "🖖",
        "🤘",
        "🤙",
        "🖐️",
        "👌",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 13])


@bot.on(admin_cmd(pattern=f"gsg$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"gsg$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(12)
    event = await edit_or_reply(event, "ContDown....")
    animation_chars = [
        "🔟",
        "9️⃣",
        "8️⃣",
        "7️⃣",
        "6️⃣",
        "5️⃣",
        "4️⃣",
        "3️⃣",
        "2️⃣",
        "1️⃣",
        "0️⃣",
        "🆘",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 12])


@bot.on(admin_cmd(pattern=r"theart$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"theart$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.3
    animation_ttl = range(54)
    event = await edit_or_reply(event, "🖤")
    animation_chars = [
        "❤️",
        "🧡",
        "💛",
        "💚",
        "💙",
        "💜",
        "🖤",
        "💘",
        "💝",
        "❤️",
        "🧡",
        "💛",
        "💚",
        "💙",
        "💜",
        "🖤",
        "💘",
        "💝",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 18])


CMD_HELP.update(
    {
        "متحركات الخامسة": """**Plugin : **`متحركات الخامسة`
        
**Commands in animation5 are **
  •  `.loading`
  •  `.square`
  •  `.up`
  •  `.round`
  •  `.hart`
  •  `.anim`
  •  `.fnl`
  •  `.monkey`
  •  `.herber`
  •  `.hand`
  •  `.gsg`
  •  `.theart`
  
**Function : **__Different kinds of animation commands check yourself for their animation .__"""
    }
)
