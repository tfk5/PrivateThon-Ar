import asyncio

from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import parse_pre, sanga_seperator


@bot.on(admin_cmd(pattern="sc (.*)"))
@bot.on(sudo_cmd(pattern="sc (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        await edit_delete(
            event,
            "- Error, Reply or send ID/user",
        )
    if input_str:
        try:
            uid = int(input_str)
        except ValueError:
            try:
                u = await event.client.get_entity(input_str)
            except ValueError:
                await edit_delete(
                    event, "send ID/user"
                )
            uid = u.id
    else:
        uid = reply_message.sender_id
    chat = "@tgscanrobot"
    catevent = await edit_or_reply(event, "- Wait ...")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message(f"{uid}")
        except YouBlockedUserError:
            await edit_delete(catevent, "- Error, unblock @tgscanrobot")
        responses = []
        while True:
            try:
                response = await conv.get_response(timeout=2)
            except asyncio.TimeoutError:
                break
            responses.append(response.text)
        await event.client.send_read_acknowledge(conv.chat_id)
    if not responses:
        await edit_delete(catevent, "- Error, can't get result")
    if """This human is not in my database. Maybe I have not scanned the chat yet which this human is member of.
You can add new chat with command /add @groupname
For example, /add @grablab_osint""" in responses:
        await edit_delete(catevent, "No result Found")
    names, usernames = await sanga_seperator(responses)
    cmd = event.pattern_match.group(1)
    if cmd == "sc":
        sandy = None
        for i in names:
            if sandy:
                await event.reply(i, parse_mode=parse_pre)
            else:
                sandy = True
                await catevent.edit(i, parse_mode=parse_pre)


CMD_HELP.update(
    {
        "Scanner": ".ss"
    }
)
