from telethon.tl.types import ChannelParticipantsAdmins


@bot.on(admin_cmd(pattern="tagall$"))
@bot.on(sudo_cmd(pattern="tagall$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    mentions = "تـم عمـل تـاك لـ 200 شـخص"
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(chat, 200):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await reply_to_id.reply(mentions)
    await event.delete()


@bot.on(admin_cmd(pattern="all( (.*)|$)"))
@bot.on(sudo_cmd(pattern="all( (.*)|$)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    mentions = input_str or "تـم عمـل تـاك لـ 200 شـخص"
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(chat, 200):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await event.client.send_message(event.chat_id, mentions, reply_to=reply_to_id)
    await event.delete()


@bot.on(admin_cmd(pattern="report$"))
@bot.on(sudo_cmd(pattern="report$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = "@admin: **تـم عـمل ابـلاغ للأدمنـية**"
    chat = await event.get_input_chat()
    reply_to_id = await reply_id(event)
    async for x in event.client.iter_participants(
        chat, filter=ChannelParticipantsAdmins
    ):
        if not x.bot:
            mentions += f"[\u2063](tg://user?id={x.id})"
    await event.client.send_message(event.chat_id, mentions, reply_to=reply_to_id)
    await event.delete()



CMD_HELP.update(
    {
        "mention": """**Plugin : **`mention`

  •  **Syntax : **`.all`
  •  **Function : **__tags recent 100 persons in the group may not work for all__  

  •  **Syntax : **`.tagall`
  •  **Function : **__tags recent 100 persons in the group may not work for all__ 

  •  **Syntax : **`.report`
  •  **Function : **__tags admins in group__  

  •  **Syntax : **`.men username/userid text`
  •  **Function : **__tags that person with the given custom text other way for this is __
  •  **syntax : **`Hi username[custom text]`
"""
    }
)
