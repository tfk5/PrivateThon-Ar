
from telethon.tl.functions.messages import SaveDraftRequest


@bot.on(admin_cmd(pattern="chain$"))
@bot.on(sudo_cmd(pattern="chain$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("جـاري كشـف معلومـات الـرسالة ...")
    count = -1
    message = event.message
    while message:
        reply = await message.get_reply_message()
        if reply is None:
            await event.client(
                SaveDraftRequest(
                    await event.get_input_chat(), "", reply_to_msg_id=message.id
                )
            )
        message = reply
        count += 1
    await event.edit(f" مـعلومـات هـية: {count} ")


CMD_HELP.update(
    {
        " كـشف رسالة": """**Plugin :**`كـشف رسالة`
        
  • **Syntax : **`.chain reply to message`
  • **Function : **__Reply this command to any converstion(or message) so that it finds chain length of that message__"""
    }
)
